#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageOps
from skimage.feature import graycomatrix
from sklearn.decomposition import PCA
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.utils import check_random_state


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data/processed"
OUTPUTS = ROOT / "outputs"
TABLES = OUTPUTS / "tables"
FIGURES = OUTPUTS / "figures"
MODELS = OUTPUTS / "models"
RANDOM_STATE = 42


@dataclass(frozen=True)
class ForensicConfig:
    feature_path: str = "data/processed/residual_cooc128.npy"
    split_path: str = "data/processed/splits.csv"
    model_id: str = "forensic_residual_pca_rbfsvc"
    image_size: int = 128
    train_limit: int = 6000
    pca_components: int = 128
    svm_c: float = 3.0
    svm_gamma: str = "scale"
    seed_min: int = 0
    seed_max: int = 30


def ensure_dirs() -> None:
    for path in [PROCESSED, TABLES, FIGURES, MODELS]:
        path.mkdir(parents=True, exist_ok=True)


def load_gray(path: str | Path, size: int) -> np.ndarray:
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img).convert("L")
        img = img.resize((size, size), Image.Resampling.BILINEAR)
        return np.asarray(img, dtype=np.float32)


def _same_shape(values: np.ndarray, target_shape: tuple[int, int]) -> np.ndarray:
    out = np.zeros(target_shape, dtype=np.float32)
    h = min(values.shape[0], target_shape[0])
    w = min(values.shape[1], target_shape[1])
    out[:h, :w] = values[:h, :w]
    if h < target_shape[0]:
        out[h:, :w] = out[h - 1 : h, :w]
    if w < target_shape[1]:
        out[:, w:] = out[:, w - 1 : w]
    return out


def residual_maps(gray: np.ndarray) -> list[np.ndarray]:
    h, w = gray.shape
    maps = [
        _same_shape(np.abs(gray[:, 1:] - gray[:, :-1]), (h, w)),
        _same_shape(np.abs(gray[1:, :] - gray[:-1, :]), (h, w)),
        _same_shape(np.abs(gray[1:, 1:] - gray[:-1, :-1]), (h, w)),
        _same_shape(np.abs(gray[1:, :-1] - gray[:-1, 1:]), (h, w)),
        _same_shape(np.abs(gray[:, 2:] - 2 * gray[:, 1:-1] + gray[:, :-2]), (h, w)),
        _same_shape(np.abs(gray[2:, :] - 2 * gray[1:-1, :] + gray[:-2, :]), (h, w)),
    ]
    lap = np.zeros_like(gray, dtype=np.float32)
    lap[1:-1, 1:-1] = np.abs(4 * gray[1:-1, 1:-1] - gray[:-2, 1:-1] - gray[2:, 1:-1] - gray[1:-1, :-2] - gray[1:-1, 2:])
    maps.append(lap)
    return maps


def residual_cooc_one(path: str | Path, image_size: int = 128) -> np.ndarray:
    gray = load_gray(path, image_size)
    feats: list[np.ndarray] = []
    for residual in residual_maps(gray):
        quantized = np.clip(np.rint(residual / 2.0), 0, 8).astype(np.uint8)
        h, w = quantized.shape
        for gy in range(4):
            for gx in range(4):
                cell = quantized[gy * h // 4 : (gy + 1) * h // 4, gx * w // 4 : (gx + 1) * w // 4]
                glcm = graycomatrix(cell, distances=[1], angles=[0], levels=9, symmetric=True, normed=True)
                feats.append(glcm[:, :, 0, 0].ravel().astype(np.float32))
    return np.concatenate(feats).astype(np.float32)


def build_residual_cooc_cache(splits: pd.DataFrame, out_path: Path, image_size: int) -> None:
    rows = np.vstack([residual_cooc_one(path, image_size=image_size) for path in splits["filepath"]]).astype(np.float32)
    np.save(out_path, rows)


def stratified_subset(indices: np.ndarray, y: np.ndarray, n: int, seed: int) -> np.ndarray:
    rng = check_random_state(seed)
    out: list[int] = []
    per_class = n // 2
    for klass in [0, 1]:
        class_indices = indices[y[indices] == klass]
        out.extend(rng.choice(class_indices, size=per_class, replace=False).tolist())
    return np.asarray(sorted(out), dtype=int)


def make_pipeline(config: ForensicConfig) -> Pipeline:
    return Pipeline(
        [
            ("scale", StandardScaler()),
            ("pca", PCA(n_components=config.pca_components, whiten=True, svd_solver="randomized", random_state=RANDOM_STATE)),
            ("model", SVC(C=config.svm_c, gamma=config.svm_gamma, cache_size=2048, random_state=RANDOM_STATE)),
        ]
    )


def best_accuracy_threshold(y_true: np.ndarray, score: np.ndarray) -> tuple[float, float]:
    thresholds = np.unique(np.quantile(score, np.linspace(0.01, 0.99, 199)))
    best_threshold = 0.0
    best_accuracy = -1.0
    for threshold in thresholds:
        accuracy = accuracy_score(y_true, score >= threshold)
        if accuracy > best_accuracy:
            best_threshold = float(threshold)
            best_accuracy = float(accuracy)
    return best_threshold, best_accuracy


def metric_dict(y_true: np.ndarray, score: np.ndarray, threshold: float) -> dict[str, object]:
    pred = (score >= threshold).astype(int)
    return {
        "accuracy": float(accuracy_score(y_true, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, pred)),
        "precision": float(precision_score(y_true, pred, zero_division=0)),
        "recall": float(recall_score(y_true, pred, zero_division=0)),
        "f1": float(f1_score(y_true, pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, score)),
        "pr_auc": float(average_precision_score(y_true, score)),
        "kappa": float(cohen_kappa_score(y_true, pred)),
        "confusion_matrix": confusion_matrix(y_true, pred).astype(int).tolist(),
    }


def plot_seed_search(validation: pd.DataFrame) -> None:
    plot_data = validation.sort_values("subset_seed")
    fig, ax1 = plt.subplots(figsize=(8, 4.6))
    ax1.plot(plot_data["subset_seed"], plot_data["validation_roc_auc"], marker="o", label="val ROC-AUC", color="#1f77b4")
    ax1.plot(plot_data["subset_seed"], plot_data["validation_accuracy_tuned"], marker="o", label="val accuracy", color="#2ca02c")
    ax1.set_xlabel("stratified subset seed")
    ax1.set_ylabel("validation score")
    ax1.set_ylim(0.78, 0.92)
    selected = validation.sort_values(["validation_roc_auc", "validation_accuracy_tuned"], ascending=False).iloc[0]
    ax1.axvline(selected["subset_seed"], color="#d62728", linestyle="--", linewidth=1, label="selected")
    ax1.legend(fontsize=8, loc="lower right")
    ax1.set_title("Residual PCA-RBF SVM validation sweep")
    fig.tight_layout()
    fig.savefig(FIGURES / "forensic_seed_validation.png", dpi=180)
    plt.close(fig)


def plot_confusion(test_metrics: dict[str, object]) -> None:
    cm = np.asarray(test_metrics["confusion_matrix"], dtype=int)
    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    ax.imshow(cm, cmap="Blues")
    ax.set_xticks([0, 1], ["real", "fake"])
    ax.set_yticks([0, 1], ["real", "fake"])
    ax.set_xlabel("predicted")
    ax.set_ylabel("true")
    ax.set_title("Residual PCA-RBF SVM confusion matrix")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, int(cm[i, j]), ha="center", va="center", color="black", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIGURES / "forensic_confusion_matrix.png", dpi=180)
    plt.close(fig)


def plot_roc_pr(predictions: pd.DataFrame) -> None:
    curves = [("forensic_residual_pca_rbfsvc", predictions)]
    model_metrics = TABLES / "model_metrics.csv"
    classical_predictions = TABLES / "test_predictions.csv"
    if model_metrics.exists() and classical_predictions.exists():
        best_id = str(pd.read_csv(model_metrics).iloc[0]["model_id"])
        all_pred = pd.read_csv(classical_predictions)
        best = all_pred[all_pred["model_id"] == best_id]
        if not best.empty:
            curves.append((best_id, best))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    for label, frame in curves:
        fpr, tpr, _ = roc_curve(frame["y_true"], frame["score"])
        roc_auc = roc_auc_score(frame["y_true"], frame["score"])
        axes[0].plot(fpr, tpr, label=f"{label} ({roc_auc:.3f})")
        precision, recall, _ = precision_recall_curve(frame["y_true"], frame["score"])
        pr_auc = average_precision_score(frame["y_true"], frame["score"])
        axes[1].plot(recall, precision, label=f"{label} ({pr_auc:.3f})")
    axes[0].plot([0, 1], [0, 1], linestyle="--", color="gray", linewidth=1)
    axes[0].set_xlabel("false positive rate")
    axes[0].set_ylabel("true positive rate")
    axes[0].set_title("ROC curve")
    axes[1].set_xlabel("recall")
    axes[1].set_ylabel("precision")
    axes[1].set_title("Precision-recall curve")
    for ax in axes:
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "forensic_roc_pr.png", dpi=180)
    plt.close(fig)


def write_comparison(test_metrics: dict[str, object]) -> None:
    rows = [
        {
            "model_id": "forensic_residual_pca_rbfsvc",
            "family": "classical_kernel_svm",
            "course_topic": "hand-engineered residual co-occurrence features; StandardScaler; PCA whitening; RBF SVM",
            "features": "residual_cooc128",
            **{k: test_metrics[k] for k in ["accuracy", "precision", "recall", "f1", "roc_auc", "pr_auc", "kappa"]},
        }
    ]
    model_metrics_path = TABLES / "model_metrics.csv"
    if model_metrics_path.exists():
        best_classical = pd.read_csv(model_metrics_path).iloc[0]
        rows.append(
            {
                "model_id": best_classical["model_id"],
                "family": "classical_ensemble",
                "course_topic": "hand-engineered color/texture/frequency statistics; gradient boosting",
                "features": best_classical["features"],
                "accuracy": best_classical["accuracy"],
                "precision": best_classical["precision"],
                "recall": best_classical["recall"],
                "f1": best_classical["f1"],
                "roc_auc": best_classical["roc_auc"],
                "pr_auc": best_classical["pr_auc"],
                "kappa": best_classical["kappa"],
            }
        )
    pd.DataFrame(rows).to_csv(TABLES / "forensic_comparison.csv", index=False)


def run(config: ForensicConfig, rebuild_features: bool = False) -> Path:
    ensure_dirs()
    split_path = ROOT / config.split_path
    feature_path = ROOT / config.feature_path
    splits = pd.read_csv(split_path)
    if rebuild_features or not feature_path.exists():
        build_residual_cooc_cache(splits, feature_path, config.image_size)

    X = np.load(feature_path, mmap_mode="r")
    y = splits["label"].to_numpy(dtype=int)
    split = splits["split"].to_numpy()
    train_idx = np.flatnonzero(split == "train")
    val_idx = np.flatnonzero(split == "val")
    test_idx = np.flatnonzero(split == "test")

    validation_rows: list[dict[str, object]] = []
    fitted: dict[int, Pipeline] = {}
    for seed in range(config.seed_min, config.seed_max + 1):
        fit_idx = stratified_subset(train_idx, y, config.train_limit, seed)
        model = make_pipeline(config)
        started = time.perf_counter()
        model.fit(X[fit_idx], y[fit_idx])
        train_seconds = time.perf_counter() - started
        val_score = model.decision_function(X[val_idx])
        threshold, threshold_accuracy = best_accuracy_threshold(y[val_idx], val_score)
        metrics = metric_dict(y[val_idx], val_score, threshold)
        validation_rows.append(
            {
                "model_id": config.model_id,
                "subset_seed": seed,
                "threshold": threshold,
                "validation_accuracy_tuned": threshold_accuracy,
                "validation_roc_auc": metrics["roc_auc"],
                "validation_f1": metrics["f1"],
                "validation_precision": metrics["precision"],
                "validation_recall": metrics["recall"],
                "train_seconds": train_seconds,
            }
        )
        fitted[seed] = model
        print(
            f"seed={seed:02d} val_roc_auc={metrics['roc_auc']:.4f} "
            f"val_acc={threshold_accuracy:.4f} threshold={threshold:.4f}",
            flush=True,
        )

    validation = pd.DataFrame(validation_rows)
    validation = validation.sort_values(["validation_roc_auc", "validation_accuracy_tuned"], ascending=False).reset_index(drop=True)
    selected = validation.iloc[0]
    selected_seed = int(selected["subset_seed"])
    selected_model = fitted[selected_seed]
    threshold = float(selected["threshold"])

    val_score = selected_model.decision_function(X[val_idx])
    test_score = selected_model.decision_function(X[test_idx])
    val_metrics = metric_dict(y[val_idx], val_score, threshold)
    test_metrics = metric_dict(y[test_idx], test_score, threshold)
    pred = (test_score >= threshold).astype(int)
    predictions = pd.DataFrame(
        {
            "model_id": config.model_id,
            "filepath": splits.iloc[test_idx]["filepath"].to_numpy(),
            "relative_path": splits.iloc[test_idx]["relative_path"].to_numpy(),
            "y_true": y[test_idx],
            "score": test_score,
            "y_pred": pred,
        }
    )

    metrics = {
        "model_id": config.model_id,
        "method": "Residual co-occurrence features with StandardScaler, PCA whitening, and an RBF-kernel SVM.",
        "config": asdict(config),
        "selected_seed": selected_seed,
        "selected_by": "validation_roc_auc, then validation_accuracy_tuned",
        "threshold": threshold,
        "feature_shape": [int(X.shape[0]), int(X.shape[1])],
        "train_n": config.train_limit,
        "val_n": int(len(val_idx)),
        "test_n": int(len(test_idx)),
        "val_metrics": val_metrics,
        "test_metrics": test_metrics,
    }

    validation.to_csv(TABLES / "forensic_validation_results.csv", index=False)
    predictions.to_csv(TABLES / "forensic_test_predictions.csv", index=False)
    (TABLES / "forensic_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    write_comparison(test_metrics)
    plot_seed_search(validation)
    plot_confusion(test_metrics)
    plot_roc_pr(predictions)
    joblib.dump({"model": selected_model, "threshold": threshold, "config": asdict(config), "metrics": metrics}, MODELS / "forensic_residual_pca_rbfsvc.joblib")
    print(json.dumps({"selected_seed": selected_seed, "threshold": threshold, "test_metrics": test_metrics}, indent=2))
    return TABLES / "forensic_metrics.json"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the course-aligned residual co-occurrence PCA-RBF SVM.")
    parser.add_argument("--rebuild-features", action="store_true", help="Rebuild data/processed/residual_cooc128.npy before training.")
    parser.add_argument("--seed-min", type=int, default=0)
    parser.add_argument("--seed-max", type=int, default=30)
    parser.add_argument("--train-limit", type=int, default=6000)
    parser.add_argument("--pca-components", type=int, default=128)
    parser.add_argument("--svm-c", type=float, default=3.0)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = ForensicConfig(
        train_limit=args.train_limit,
        pca_components=args.pca_components,
        svm_c=args.svm_c,
        seed_min=args.seed_min,
        seed_max=args.seed_max,
    )
    run(config, rebuild_features=args.rebuild_features)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
