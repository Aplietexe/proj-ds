from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import time
from typing import Literal

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import (
    LinearDiscriminantAnalysis,
    QuadraticDiscriminantAnalysis,
)
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    cohen_kappa_score,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from proj_ds.features import FEATURES_NPZ, feature_matrix, load_features

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = PROJECT_ROOT / "outputs"
MODELS = OUTPUTS / "models"
RANDOM_STATE = 42
type ScoreKind = Literal["proba", "decision", "predict"]


@dataclass
class Candidate:
    model_id: str
    experiment: str
    features: str
    estimator: Pipeline
    score_kind: ScoreKind
    notes: str


def run_planned_models() -> Path:
    MODELS.mkdir(parents=True, exist_ok=True)
    data = load_features(FEATURES_NPZ)
    split = data["split"].astype(str)
    train_mask = split == "train"
    val_mask = split == "val"
    test_mask = split == "test"

    candidates = candidate_grid()
    validation_rows: list[dict[str, object]] = []
    for candidate in candidates:
        row, _, _, _ = evaluate_candidate(candidate, data, train_mask, val_mask, "val")
        validation_rows.append(row)

    validation = pd.DataFrame(validation_rows)
    validation = validation.sort_values(["roc_auc", "f1", "accuracy"], ascending=False)
    validation["validation_rank"] = np.arange(1, len(validation) + 1)

    best_id = str(validation.iloc[0]["model_id"])
    best_candidate = candidate_by_id(candidates, best_id)
    train_val_mask = train_mask | val_mask
    test_row, estimator, _, _ = evaluate_candidate(
        best_candidate, data, train_val_mask, test_mask, "test"
    )
    test_row["validation_rank"] = 1
    test_row["validation_roc_auc"] = float(validation.iloc[0]["roc_auc"])
    test_row["validation_f1"] = float(validation.iloc[0]["f1"])
    test_metrics = pd.DataFrame([test_row])

    model_path = MODELS / f"{best_id}.joblib"
    joblib.dump(
        {
            "model_id": best_id,
            "candidate": best_candidate,
            "estimator": estimator,
            "feature_family": best_candidate.features,
        },
        model_path,
    )
    print("\nValidation ranking")
    print(
        validation[
            ["validation_rank", "model_id", "features", "accuracy", "f1", "roc_auc"]
        ].to_string(index=False)
    )
    print("\nLocked test metrics for selected planned model")
    print(
        test_metrics[
            [
                "validation_rank",
                "model_id",
                "features",
                "accuracy",
                "f1",
                "roc_auc",
                "pr_auc",
                "kappa",
            ]
        ].to_string(index=False)
    )
    print(f"\nSaved planned model: {model_path.relative_to(PROJECT_ROOT)}")
    return model_path


def candidate_grid() -> list[Candidate]:
    candidates = [
        Candidate(
            "dummy_stratified",
            "E0",
            "color",
            Pipeline(
                [
                    (
                        "model",
                        DummyClassifier(
                            strategy="stratified", random_state=RANDOM_STATE
                        ),
                    )
                ]
            ),
            "proba",
            "chance baseline",
        ),
        Candidate(
            "raw_gray32_gnb",
            "E1",
            "raw_gray32",
            Pipeline([("model", GaussianNB())]),
            "proba",
            "Gaussian Naive Bayes on raw pixels",
        ),
        Candidate(
            "color_logreg",
            "E3",
            "color",
            scaled(LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
            "proba",
            "logistic regression on color statistics",
        ),
        Candidate(
            "texture_sgdsvm",
            "E4",
            "texture",
            sgd_hinge(),
            "decision",
            "linear SVM on texture features",
        ),
        Candidate(
            "frequency_sgdsvm",
            "E6",
            "frequency",
            sgd_hinge(),
            "decision",
            "linear SVM on frequency features",
        ),
        Candidate(
            "hog_sgdsvm_alpha0.0001",
            "E5",
            "hog",
            sgd_hinge(),
            "decision",
            "linear SVM on HOG features",
        ),
        Candidate(
            "all_sgdsvm_alpha0.0001",
            "E7",
            "all",
            sgd_hinge(),
            "decision",
            "linear SVM on combined handcrafted features",
        ),
        Candidate(
            "stats_tree",
            "E3/E4/E6",
            "stats",
            Pipeline(
                [
                    (
                        "model",
                        DecisionTreeClassifier(
                            max_depth=12,
                            min_samples_leaf=10,
                            random_state=RANDOM_STATE,
                        ),
                    )
                ]
            ),
            "proba",
            "CART tree on color/texture/frequency statistics",
        ),
        Candidate(
            "stats_rf",
            "E3/E4/E6",
            "stats",
            Pipeline(
                [
                    (
                        "model",
                        RandomForestClassifier(
                            n_estimators=300,
                            max_features="sqrt",
                            min_samples_leaf=2,
                            oob_score=True,
                            n_jobs=-1,
                            random_state=RANDOM_STATE,
                        ),
                    )
                ]
            ),
            "proba",
            "Random Forest on color/texture/frequency statistics",
        ),
        Candidate(
            "stats_hgb",
            "E7",
            "stats",
            Pipeline(
                [
                    (
                        "model",
                        HistGradientBoostingClassifier(
                            learning_rate=0.06,
                            max_iter=180,
                            max_leaf_nodes=31,
                            l2_regularization=0.01,
                            random_state=RANDOM_STATE,
                        ),
                    )
                ]
            ),
            "proba",
            "HistGradientBoosting on color/texture/frequency statistics",
        ),
        Candidate(
            "pca_raw_logreg_k100",
            "E2",
            "raw_gray32",
            pca_pipeline(
                LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
                100,
            ),
            "proba",
            "PCA-whitened raw pixels with logistic regression",
        ),
        Candidate(
            "pca_raw_knn_k100_n11",
            "E2",
            "raw_gray32",
            pca_pipeline(KNeighborsClassifier(n_neighbors=11, weights="distance"), 100),
            "proba",
            "PCA-whitened raw pixels with k-NN",
        ),
        Candidate(
            "pca_all_rbfsvc_k100",
            "E8",
            "all",
            pca_pipeline(SVC(C=10.0, gamma="scale", random_state=RANDOM_STATE), 100),
            "decision",
            "PCA-whitened combined handcrafted features with RBF SVM",
        ),
        Candidate(
            "pca_all_lda",
            "E8",
            "all",
            pca_pipeline(LinearDiscriminantAnalysis(), 100),
            "decision",
            "LDA on PCA-whitened combined handcrafted features",
        ),
        Candidate(
            "pca_all_qda",
            "E8",
            "all",
            pca_pipeline(QuadraticDiscriminantAnalysis(reg_param=0.05), 50),
            "proba",
            "QDA on heavily reduced PCA features",
        ),
    ]
    for alpha in (1e-3, 1e-4, 1e-5):
        candidates.append(
            Candidate(
                f"raw_gray32_sgdlog_alpha{alpha:g}",
                "E1",
                "raw_gray32",
                sgd_logistic(alpha),
                "decision",
                f"L2 logistic trained with SGD, alpha={alpha:g}",
            )
        )
        candidates.append(
            Candidate(
                f"raw_gray32_sgdsvm_alpha{alpha:g}",
                "E1",
                "raw_gray32",
                sgd_hinge(alpha),
                "decision",
                f"linear hinge-loss SVM trained with SGD, alpha={alpha:g}",
            )
        )
    for alpha in (1e-3, 1e-5):
        candidates.append(
            Candidate(
                f"hog_sgdsvm_alpha{alpha:g}",
                "E5",
                "hog",
                sgd_hinge(alpha),
                "decision",
                f"HOG linear hinge-loss SVM trained with SGD, alpha={alpha:g}",
            )
        )
        candidates.append(
            Candidate(
                f"all_sgdsvm_alpha{alpha:g}",
                "E7",
                "all",
                sgd_hinge(alpha),
                "decision",
                f"combined handcrafted linear hinge-loss SVM trained with SGD, alpha={alpha:g}",
            )
        )
    for k in (200,):
        candidates.append(
            Candidate(
                f"pca_raw_logreg_k{k}",
                "E2",
                "raw_gray32",
                pca_pipeline(
                    LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
                    k,
                ),
                "proba",
                f"PCA-whitened raw pixels with logistic regression, k={k}",
            )
        )
        candidates.append(
            Candidate(
                f"pca_raw_knn_k{k}_n11",
                "E2",
                "raw_gray32",
                pca_pipeline(
                    KNeighborsClassifier(n_neighbors=11, weights="distance"), k
                ),
                "proba",
                f"PCA-whitened raw pixels with k-NN, k={k}",
            )
        )
        candidates.append(
            Candidate(
                f"pca_all_rbfsvc_k{k}",
                "E8",
                "all",
                pca_pipeline(
                    SVC(C=10.0, gamma="scale", random_state=RANDOM_STATE),
                    k,
                ),
                "decision",
                f"PCA-whitened combined handcrafted features with RBF SVM, k={k}",
            )
        )
    for k in (100, 200):
        candidates.append(
            Candidate(
                f"pca_all_mlp_k{k}",
                "E8",
                "all",
                pca_pipeline(
                    MLPClassifier(
                        hidden_layer_sizes=(256, 128),
                        activation="relu",
                        alpha=1e-4,
                        early_stopping=True,
                        max_iter=120,
                        random_state=RANDOM_STATE,
                    ),
                    k,
                ),
                "proba",
                f"PCA-whitened combined handcrafted features with shallow MLP, k={k}",
            )
        )
    return candidates


def candidate_by_id(candidates: list[Candidate], model_id: str) -> Candidate:
    matches = [candidate for candidate in candidates if candidate.model_id == model_id]
    assert len(matches) == 1
    return matches[0]


def scaled(model: object) -> Pipeline:
    return Pipeline([("scale", StandardScaler()), ("model", model)])


def pca_pipeline(model: object, n_components: int) -> Pipeline:
    return Pipeline(
        [
            ("scale", StandardScaler()),
            (
                "pca",
                PCA(
                    n_components=n_components,
                    whiten=True,
                    svd_solver="randomized",
                    random_state=RANDOM_STATE,
                ),
            ),
            ("model", model),
        ]
    )


def sgd_hinge(alpha: float = 1e-4) -> Pipeline:
    return scaled(
        SGDClassifier(
            loss="hinge",
            penalty="l2",
            alpha=alpha,
            max_iter=1500,
            tol=1e-3,
            early_stopping=True,
            validation_fraction=0.1,
            n_jobs=-1,
            random_state=RANDOM_STATE,
        )
    )


def sgd_logistic(alpha: float) -> Pipeline:
    return scaled(
        SGDClassifier(
            loss="log_loss",
            penalty="l2",
            alpha=alpha,
            max_iter=1500,
            tol=1e-3,
            early_stopping=True,
            validation_fraction=0.1,
            n_jobs=-1,
            random_state=RANDOM_STATE,
        )
    )


def evaluate_candidate(
    candidate: Candidate,
    data: dict[str, np.ndarray],
    train_mask: np.ndarray,
    eval_mask: np.ndarray,
    split_name: str,
) -> tuple[dict[str, object], Pipeline, np.ndarray, np.ndarray]:
    x = feature_matrix(data, candidate.features)
    y = data["y"].astype(int)
    estimator = clone(candidate.estimator)
    assert isinstance(estimator, Pipeline)
    started = time.perf_counter()
    estimator.fit(x[train_mask], y[train_mask])
    train_seconds = time.perf_counter() - started
    started = time.perf_counter()
    scores, predictions = score_estimator(estimator, x[eval_mask], candidate.score_kind)
    predict_seconds = time.perf_counter() - started
    row = metric_row(
        y[eval_mask],
        scores,
        predictions,
        split_name,
        candidate.score_kind == "proba",
    )
    row.update(
        {
            "model_id": candidate.model_id,
            "experiment": candidate.experiment,
            "features": candidate.features,
            "notes": candidate.notes,
            "feature_dim": int(x.shape[1]),
            "train_n": int(train_mask.sum()),
            "eval_n": int(eval_mask.sum()),
            "train_seconds": train_seconds,
            "predict_seconds": predict_seconds,
            "prediction_ms_per_image": 1000 * predict_seconds / int(eval_mask.sum()),
            "has_probabilities": candidate.score_kind == "proba",
        }
    )
    return row, estimator, scores, predictions


def score_estimator(
    estimator: Pipeline, x: np.ndarray, score_kind: ScoreKind
) -> tuple[np.ndarray, np.ndarray]:
    if score_kind == "proba":
        scores = np.asarray(estimator.predict_proba(x)[:, 1], dtype=float)
        return scores, (scores >= 0.5).astype(int)
    if score_kind == "decision":
        scores = np.asarray(estimator.decision_function(x), dtype=float)
        return scores, np.asarray(estimator.predict(x), dtype=int)
    predictions = np.asarray(estimator.predict(x), dtype=int)
    return predictions.astype(float), predictions


def metric_row(
    y_true: np.ndarray,
    scores: np.ndarray,
    predictions: np.ndarray,
    split_name: str,
    has_probabilities: bool,
) -> dict[str, object]:
    row: dict[str, object] = {
        "split": split_name,
        "accuracy": float(accuracy_score(y_true, predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, predictions)),
        "precision": float(precision_score(y_true, predictions)),
        "recall": float(recall_score(y_true, predictions)),
        "f1": float(f1_score(y_true, predictions)),
        "roc_auc": float(roc_auc_score(y_true, scores)),
        "pr_auc": float(average_precision_score(y_true, scores)),
        "kappa": float(cohen_kappa_score(y_true, predictions)),
        "log_loss": "",
        "brier": "",
    }
    if has_probabilities:
        clipped = np.clip(scores, 1e-6, 1 - 1e-6)
        row["log_loss"] = float(log_loss(y_true, clipped))
        row["brier"] = float(brier_score_loss(y_true, clipped))
    return row


if __name__ == "__main__":
    run_planned_models()
