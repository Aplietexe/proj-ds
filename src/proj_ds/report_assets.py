from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import time
from typing import Literal

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image, ImageOps
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    cohen_kappa_score,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.pipeline import Pipeline

matplotlib.use("Agg")

from matplotlib import pyplot as plt

from proj_ds.features import FEATURE_KEYS, feature_matrix, load_features
from proj_ds.planned_models import ScoreKind, candidate_by_id, candidate_grid
from proj_ds.residual_texture import (
    PROJECT_ROOT,
    RESIDUAL_FEATURES,
    SPLITS_CSV,
    best_accuracy_threshold,
    build_residual_features,
    load_splits,
    make_model,
    metric_values,
    residual_maps,
)

REPORTS = PROJECT_ROOT / "reports"
FIGURES = REPORTS / "figures"
TABLES = REPORTS / "tables"
RANDOM_STATE = 42
PLANNED_MODEL_ID = "pca_all_rbfsvc_k200"

MetricName = Literal[
    "accuracy",
    "balanced_accuracy",
    "precision",
    "recall",
    "f1",
    "roc_auc",
    "pr_auc",
    "kappa",
]


@dataclass(frozen=True)
class ModelResult:
    public_name: str
    y_true: np.ndarray
    scores: np.ndarray
    predictions: np.ndarray
    metrics: dict[MetricName, float]
    confusion_matrix: np.ndarray
    estimator: Pipeline
    projected_test: np.ndarray


@dataclass(frozen=True)
class ValidationResult:
    public_name: str
    representation: str
    preprocessing: str
    feature_dim: int
    train_n: int
    validation_n: int
    train_seconds: float
    prediction_ms_per_image: float
    metrics: dict[MetricName, float]
    note: str


def generate_report_assets() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", context="talk")

    splits = load_splits()
    data = load_features()
    validation_results = evaluate_planned_validation_models(data)
    planned_result = evaluate_planned_model(data)
    residual_result, residual_validation = evaluate_residual_model()
    all_validation_results = validation_results + [residual_validation]

    write_dataset_tables(splits.frame, data)
    write_model_metrics([planned_result, residual_result])
    write_validation_metrics(all_validation_results)
    plot_split_distribution(splits.frame)
    plot_image_examples(splits.frame)
    plot_feature_dimensions(data)
    plot_metric_comparison([planned_result, residual_result])
    plot_validation_roc_auc(all_validation_results)
    plot_validation_top_metrics(all_validation_results)
    plot_confusion_matrix(residual_result)
    plot_roc_pr_curves(residual_result)
    plot_score_distribution(residual_result)
    plot_pca_projection(residual_result)
    plot_local_differences_example(splits.frame)


def evaluate_planned_validation_models(
    data: dict[str, np.ndarray],
) -> list[ValidationResult]:
    split = data["split"].astype(str)
    train_mask = split == "train"
    validation_mask = split == "val"
    y = data["y"].astype(int)
    results: list[ValidationResult] = []
    for candidate in candidate_grid():
        x = feature_matrix(data, candidate.features)
        estimator = candidate.estimator
        started = time.perf_counter()
        estimator.fit(x[train_mask], y[train_mask])
        train_seconds = time.perf_counter() - started
        started = time.perf_counter()
        scores, predictions = candidate_scores_predictions(
            estimator, x[validation_mask], candidate.score_kind
        )
        predict_seconds = time.perf_counter() - started
        results.append(
            ValidationResult(
                public_name=public_model_name(candidate.model_id),
                representation=feature_label(candidate.features),
                preprocessing=preprocessing_label(candidate.model_id),
                feature_dim=int(x.shape[1]),
                train_n=int(train_mask.sum()),
                validation_n=int(validation_mask.sum()),
                train_seconds=train_seconds,
                prediction_ms_per_image=1000
                * predict_seconds
                / int(validation_mask.sum()),
                metrics=metric_dict(y[validation_mask], scores, predictions),
                note="Candidato evaluado en validacion",
            )
        )
    return results


def evaluate_planned_model(data: dict[str, np.ndarray]) -> ModelResult:
    split = data["split"].astype(str)
    train_val_mask = (split == "train") | (split == "val")
    test_mask = split == "test"
    candidate = candidate_by_id(candidate_grid(), PLANNED_MODEL_ID)
    x = feature_matrix(data, candidate.features)
    y = data["y"].astype(int)
    estimator = candidate.estimator
    estimator.fit(x[train_val_mask], y[train_val_mask])
    scores = np.asarray(estimator.decision_function(x[test_mask]), dtype=float)
    predictions = (scores >= 0).astype(int)
    values = metric_values(y[test_mask], scores, 0.0)
    projected = np.zeros((int(test_mask.sum()), 2), dtype=np.float32)
    return ModelResult(
        public_name="SVM con PCA sobre variables construidas",
        y_true=y[test_mask],
        scores=scores,
        predictions=predictions,
        metrics={
            "accuracy": values.accuracy,
            "balanced_accuracy": values.balanced_accuracy,
            "precision": values.precision,
            "recall": values.recall,
            "f1": values.f1,
            "roc_auc": values.roc_auc,
            "pr_auc": values.pr_auc,
            "kappa": values.kappa,
        },
        confusion_matrix=np.asarray(values.confusion_matrix, dtype=int),
        estimator=estimator,
        projected_test=projected,
    )


def evaluate_residual_model() -> tuple[ModelResult, ValidationResult]:
    splits = load_splits()
    if (
        not RESIDUAL_FEATURES.exists()
        or RESIDUAL_FEATURES.stat().st_mtime < SPLITS_CSV.stat().st_mtime
    ):
        build_residual_features()

    features = np.load(RESIDUAL_FEATURES, mmap_mode="r")
    train_indices = np.flatnonzero(splits.split == "train")
    validation_indices = np.flatnonzero(splits.split == "val")
    test_indices = np.flatnonzero(splits.split == "test")

    model = make_model()
    started = time.perf_counter()
    model.fit(features[train_indices], splits.y[train_indices])
    train_seconds = time.perf_counter() - started
    started = time.perf_counter()
    validation_scores = model.decision_function(features[validation_indices])
    threshold, _ = best_accuracy_threshold(
        splits.y[validation_indices], validation_scores
    )
    validation_predict_seconds = time.perf_counter() - started
    test_scores = model.decision_function(features[test_indices])
    predictions = (test_scores >= threshold).astype(int)
    validation_predictions = (validation_scores >= threshold).astype(int)
    validation_metrics = metric_dict(
        splits.y[validation_indices], validation_scores, validation_predictions
    )
    values = metric_values(splits.y[test_indices], test_scores, threshold)
    projected = np.asarray(model[:-1].transform(features[test_indices]), dtype=float)[
        :, :2
    ]
    public_name = "SVM con PCA sobre diferencias locales de pixeles"
    return (
        ModelResult(
            public_name=public_name,
            y_true=splits.y[test_indices],
            scores=np.asarray(test_scores, dtype=float),
            predictions=predictions,
            metrics={
                "accuracy": values.accuracy,
                "balanced_accuracy": values.balanced_accuracy,
                "precision": values.precision,
                "recall": values.recall,
                "f1": values.f1,
                "roc_auc": values.roc_auc,
                "pr_auc": values.pr_auc,
                "kappa": values.kappa,
            },
            confusion_matrix=np.asarray(values.confusion_matrix, dtype=int),
            estimator=model,
            projected_test=projected,
        ),
        ValidationResult(
            public_name=public_name,
            representation="Diferencias locales de pixeles",
            preprocessing="Estandarizacion + PCA con whitening",
            feature_dim=int(features.shape[1]),
            train_n=len(train_indices),
            validation_n=len(validation_indices),
            train_seconds=train_seconds,
            prediction_ms_per_image=1000
            * validation_predict_seconds
            / len(validation_indices),
            metrics=validation_metrics,
            note="Modelo adicional; el umbral se eligio sobre validacion",
        ),
    )


def candidate_scores_predictions(
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


def metric_dict(
    y_true: np.ndarray, scores: np.ndarray, predictions: np.ndarray
) -> dict[MetricName, float]:
    return {
        "accuracy": float(accuracy_score(y_true, predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, predictions)),
        "precision": float(precision_score(y_true, predictions)),
        "recall": float(recall_score(y_true, predictions)),
        "f1": float(f1_score(y_true, predictions)),
        "roc_auc": float(roc_auc_score(y_true, scores)),
        "pr_auc": float(average_precision_score(y_true, scores)),
        "kappa": float(cohen_kappa_score(y_true, predictions)),
    }


def write_dataset_tables(frame: pd.DataFrame, data: dict[str, np.ndarray]) -> None:
    split_summary = (
        frame.groupby(["split", "label_name"]).size().to_frame("cantidad").reset_index()
    )
    split_summary["particion"] = split_summary["split"].map(split_label)
    split_summary["clase"] = split_summary["label_name"].map(class_label)
    split_summary[["particion", "clase", "cantidad"]].to_csv(
        TABLES / "dataset_particiones.csv", index=False
    )

    feature_names: list[str] = []
    feature_dimensions: list[int] = []
    for key in FEATURE_KEYS:
        feature_names.append(feature_label(key))
        feature_dimensions.append(int(data[key].shape[1]))
    feature_names.append("Diferencias locales de pixeles")
    feature_dimensions.append(int(np.load(RESIDUAL_FEATURES, mmap_mode="r").shape[1]))
    pd.DataFrame(
        {"familia_de_variables": feature_names, "dimension": feature_dimensions}
    ).to_csv(TABLES / "dimensiones_variables.csv", index=False)


def write_model_metrics(results: list[ModelResult]) -> None:
    frame = pd.DataFrame(
        {
            "modelo": [result.public_name for result in results],
            "accuracy": [result.metrics["accuracy"] for result in results],
            "balanced_accuracy": [
                result.metrics["balanced_accuracy"] for result in results
            ],
            "precision": [result.metrics["precision"] for result in results],
            "recall": [result.metrics["recall"] for result in results],
            "f1": [result.metrics["f1"] for result in results],
            "roc_auc": [result.metrics["roc_auc"] for result in results],
            "pr_auc": [result.metrics["pr_auc"] for result in results],
            "kappa": [result.metrics["kappa"] for result in results],
        }
    )
    frame.to_csv(TABLES / "metricas_test.csv", index=False)


def write_validation_metrics(results: list[ValidationResult]) -> None:
    ordered = sorted(
        results, key=lambda result: result.metrics["roc_auc"], reverse=True
    )
    frame = pd.DataFrame(
        {
            "ranking_validacion": list(range(1, len(ordered) + 1)),
            "modelo": [result.public_name for result in ordered],
            "variables": [result.representation for result in ordered],
            "preprocesamiento": [result.preprocessing for result in ordered],
            "dimension": [result.feature_dim for result in ordered],
            "train_n": [result.train_n for result in ordered],
            "validacion_n": [result.validation_n for result in ordered],
            "accuracy": [result.metrics["accuracy"] for result in ordered],
            "balanced_accuracy": [
                result.metrics["balanced_accuracy"] for result in ordered
            ],
            "precision": [result.metrics["precision"] for result in ordered],
            "recall": [result.metrics["recall"] for result in ordered],
            "f1": [result.metrics["f1"] for result in ordered],
            "roc_auc": [result.metrics["roc_auc"] for result in ordered],
            "pr_auc": [result.metrics["pr_auc"] for result in ordered],
            "kappa": [result.metrics["kappa"] for result in ordered],
            "train_seconds": [result.train_seconds for result in ordered],
            "prediction_ms_per_image": [
                result.prediction_ms_per_image for result in ordered
            ],
            "nota": [result.note for result in ordered],
        }
    )
    frame.to_csv(TABLES / "validacion_modelos.csv", index=False)


def plot_split_distribution(frame: pd.DataFrame) -> None:
    counts = (
        frame.groupby(["split", "label_name"]).size().to_frame("cantidad").reset_index()
    )
    counts["particion"] = counts["split"].map(split_label)
    counts["clase"] = counts["label_name"].map(class_label)
    plt.figure(figsize=(9, 5))
    axis = sns.barplot(data=counts, x="particion", y="cantidad", hue="clase")
    axis.set_xlabel("")
    axis.set_ylabel("Cantidad de imagenes")
    axis.set_title("Distribucion de clases por particion")
    axis.legend(title="Clase")
    save_current_figure("01_distribucion_clases.png")


def plot_image_examples(frame: pd.DataFrame) -> None:
    sample = (
        frame[frame["split"] == "train"]
        .groupby("label_name", group_keys=False)
        .sample(n=5, random_state=RANDOM_STATE)
    )
    fig, axes = plt.subplots(2, 5, figsize=(11, 5))
    for axis, (_, row) in zip(axes.ravel(), sample.iterrows(), strict=True):
        with Image.open(Path(str(row["filepath"]))) as image:
            rgb = ImageOps.exif_transpose(image).convert("RGB")
            axis.imshow(rgb)
        axis.set_title(class_label(str(row["label_name"])))
        axis.axis("off")
    fig.suptitle("Ejemplos de imagenes del conjunto de entrenamiento")
    save_current_figure("02_ejemplos_imagenes.png")


def plot_feature_dimensions(data: dict[str, np.ndarray]) -> None:
    feature_names = [feature_label(key) for key in FEATURE_KEYS]
    feature_dimensions = [int(data[key].shape[1]) for key in FEATURE_KEYS]
    feature_names.append("Diferencias locales de pixeles")
    feature_dimensions.append(int(np.load(RESIDUAL_FEATURES, mmap_mode="r").shape[1]))
    frame = pd.DataFrame({"familia": feature_names, "dimension": feature_dimensions})
    plt.figure(figsize=(11, 5))
    axis = sns.barplot(data=frame, x="dimension", y="familia", color="#4C78A8")
    axis.set_xlabel("Cantidad de variables")
    axis.set_ylabel("")
    axis.set_title("Dimension de cada representacion")
    save_current_figure("03_dimension_variables.png")


def plot_metric_comparison(results: list[ModelResult]) -> None:
    rows = []
    selected_metrics: tuple[MetricName, ...] = (
        "accuracy",
        "f1",
        "roc_auc",
        "pr_auc",
        "kappa",
    )
    for result in results:
        for metric in selected_metrics:
            rows.append(
                (result.public_name, metric_label(metric), result.metrics[metric])
            )
    frame = pd.DataFrame(rows, columns=["modelo", "metrica", "valor"])
    plt.figure(figsize=(12, 6))
    axis = sns.barplot(data=frame, x="metrica", y="valor", hue="modelo")
    axis.set_ylim(0, 1)
    axis.set_xlabel("")
    axis.set_ylabel("Valor en test")
    axis.set_title("Comparacion de metricas en el conjunto de test")
    axis.legend(title="")
    save_current_figure("04_metricas_test.png")


def plot_validation_roc_auc(results: list[ValidationResult]) -> None:
    ordered = sorted(results, key=lambda result: result.metrics["roc_auc"])
    frame = pd.DataFrame(
        {
            "modelo": [result.public_name for result in ordered],
            "roc_auc": [result.metrics["roc_auc"] for result in ordered],
        }
    )
    plt.figure(figsize=(12, 14))
    axis = sns.barplot(data=frame, x="roc_auc", y="modelo", color="#4C78A8")
    axis.set_xlim(0, 1)
    axis.set_xlabel("ROC-AUC en validacion")
    axis.set_ylabel("")
    axis.set_title("Comparacion completa de modelos en validacion")
    save_current_figure("10_validacion_roc_auc_modelos.png")


def plot_validation_top_metrics(results: list[ValidationResult]) -> None:
    ordered = sorted(
        results, key=lambda result: result.metrics["roc_auc"], reverse=True
    )[:12]
    selected_metrics: tuple[MetricName, ...] = (
        "accuracy",
        "f1",
        "roc_auc",
        "pr_auc",
        "kappa",
    )
    model_names: list[str] = []
    metric_names: list[str] = []
    metric_values: list[float] = []
    for result in ordered:
        for metric in selected_metrics:
            model_names.append(result.public_name)
            metric_names.append(metric_label(metric))
            metric_values.append(result.metrics[metric])
    frame = pd.DataFrame(
        {"modelo": model_names, "metrica": metric_names, "valor": metric_values}
    )
    plt.figure(figsize=(13, 8))
    axis = sns.barplot(data=frame, x="valor", y="modelo", hue="metrica")
    axis.set_xlim(0, 1)
    axis.set_xlabel("Valor en validacion")
    axis.set_ylabel("")
    axis.set_title("Metricas de validacion para los modelos mejor ordenados")
    axis.legend(title="")
    save_current_figure("11_validacion_metricas_top12.png")


def plot_confusion_matrix(result: ModelResult) -> None:
    plt.figure(figsize=(6, 5))
    axis = sns.heatmap(
        result.confusion_matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        xticklabels=["Real", "Generada"],
        yticklabels=["Real", "Generada"],
    )
    axis.set_xlabel("Clase predicha")
    axis.set_ylabel("Clase real")
    axis.set_title("Matriz de confusion en test")
    save_current_figure("05_matriz_confusion.png")


def plot_roc_pr_curves(result: ModelResult) -> None:
    false_positive_rate, true_positive_rate, _ = roc_curve(result.y_true, result.scores)
    precision, recall, _ = precision_recall_curve(result.y_true, result.scores)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(false_positive_rate, true_positive_rate, linewidth=2)
    axes[0].plot([0, 1], [0, 1], linestyle="--", color="gray")
    axes[0].set_xlabel("FPR")
    axes[0].set_ylabel("TPR / Recall")
    axes[0].set_title(f"ROC-AUC = {result.metrics['roc_auc']:.3f}")
    axes[1].plot(recall, precision, linewidth=2)
    axes[1].set_xlabel("Recall")
    axes[1].set_ylabel("Precision")
    axes[1].set_title(f"PR-AUC = {result.metrics['pr_auc']:.3f}")
    fig.suptitle("Curvas de umbral para el modelo final")
    save_current_figure("06_curvas_roc_pr.png")


def plot_score_distribution(result: ModelResult) -> None:
    frame = pd.DataFrame(
        {
            "score": result.scores,
            "clase": [class_label_from_int(value) for value in result.y_true],
        }
    )
    plt.figure(figsize=(10, 5))
    axis = plt.gca()
    palette = {"Real": "#4C78A8", "Generada": "#E45756"}
    for label in ("Real", "Generada"):
        scores = frame.loc[frame["clase"] == label, "score"].to_numpy(dtype=float)
        sns.kdeplot(
            x=scores,
            fill=True,
            common_norm=False,
            label=label,
            color=palette[label],
            ax=axis,
        )
    axis.set_xlabel("Score del clasificador")
    axis.set_ylabel("Densidad")
    axis.set_title("Distribucion de scores por clase real")
    axis.legend(title="Clase")
    save_current_figure("07_scores_por_clase.png")


def plot_pca_projection(result: ModelResult) -> None:
    correct = result.y_true == result.predictions
    frame = pd.DataFrame(
        {
            "pc1": result.projected_test[:, 0],
            "pc2": result.projected_test[:, 1],
            "clase": [class_label_from_int(value) for value in result.y_true],
            "resultado": [
                "Correcta" if is_correct else "Error" for is_correct in correct
            ],
        }
    )
    plt.figure(figsize=(9, 7))
    axis = sns.scatterplot(
        data=frame,
        x="pc1",
        y="pc2",
        hue="clase",
        style="resultado",
        alpha=0.65,
        s=45,
    )
    axis.set_xlabel("Componente 1")
    axis.set_ylabel("Componente 2")
    axis.set_title("Proyeccion PCA del conjunto de test")
    axis.legend(title="")
    save_current_figure("08_proyeccion_pca_test.png")


def plot_local_differences_example(frame: pd.DataFrame) -> None:
    row = (
        frame[(frame["split"] == "train") & (frame["label_name"] == "fake")]
        .sample(n=1, random_state=RANDOM_STATE)
        .iloc[0]
    )
    with Image.open(Path(str(row["filepath"]))) as image:
        gray_image = ImageOps.exif_transpose(image).convert("L")
        resized = gray_image.resize((128, 128), Image.Resampling.BILINEAR)
        gray = np.asarray(resized, dtype=np.float32)
    maps = residual_maps(gray)
    titles = [
        "Imagen",
        "Diferencia horizontal",
        "Diferencia vertical",
        "Diferencia diagonal",
        "Laplaciano",
    ]
    images = [gray, maps[0], maps[1], maps[2], maps[6]]
    fig, axes = plt.subplots(1, 5, figsize=(13, 3))
    for axis, title, image_array in zip(axes, titles, images, strict=True):
        axis.imshow(image_array, cmap="gray")
        axis.set_title(title, fontsize=12)
        axis.axis("off")
    fig.suptitle("Variables basadas en diferencias locales de pixeles")
    save_current_figure("09_diferencias_locales.png")


def split_label(value: str) -> str:
    if value == "train":
        return "Entrenamiento"
    if value == "val":
        return "Validacion"
    return "Test"


def class_label(value: str) -> str:
    if value == "real":
        return "Real"
    return "Generada"


def class_label_from_int(value: int) -> str:
    if value == 0:
        return "Real"
    return "Generada"


def public_model_name(model_id: str) -> str:
    labels = {
        "dummy_stratified": "Baseline aleatorio estratificado",
        "raw_gray32_gnb": "Naive Bayes Gaussiano sobre pixeles grises",
        "color_logreg": "Regresion logistica sobre color",
        "texture_sgdsvm": "SVM lineal sobre textura",
        "frequency_sgdsvm": "SVM lineal sobre frecuencia",
        "hog_sgdsvm_alpha0.0001": "SVM lineal sobre HOG (alpha=1e-4)",
        "all_sgdsvm_alpha0.0001": "SVM lineal sobre variables construidas (alpha=1e-4)",
        "stats_tree": "Arbol de decision sobre estadisticos",
        "stats_rf": "Random Forest sobre estadisticos",
        "stats_hgb": "Gradient Boosting sobre estadisticos",
        "pca_raw_logreg_k100": "Regresion logistica con PCA sobre pixeles grises (100 comp.)",
        "pca_raw_knn_k100_n11": "k-NN con PCA sobre pixeles grises (100 comp., k=11)",
        "pca_all_rbfsvc_k100": "SVM RBF con PCA sobre variables construidas (100 comp.)",
        "pca_all_lda": "LDA con PCA sobre variables construidas",
        "pca_all_qda": "QDA con PCA sobre variables construidas",
        "raw_gray32_sgdlog_alpha0.001": "Regresion logistica SGD sobre pixeles grises (alpha=1e-3)",
        "raw_gray32_sgdsvm_alpha0.001": "SVM lineal sobre pixeles grises (alpha=1e-3)",
        "raw_gray32_sgdlog_alpha0.0001": "Regresion logistica SGD sobre pixeles grises (alpha=1e-4)",
        "raw_gray32_sgdsvm_alpha0.0001": "SVM lineal sobre pixeles grises (alpha=1e-4)",
        "raw_gray32_sgdlog_alpha1e-05": "Regresion logistica SGD sobre pixeles grises (alpha=1e-5)",
        "raw_gray32_sgdsvm_alpha1e-05": "SVM lineal sobre pixeles grises (alpha=1e-5)",
        "hog_sgdsvm_alpha0.001": "SVM lineal sobre HOG (alpha=1e-3)",
        "all_sgdsvm_alpha0.001": "SVM lineal sobre variables construidas (alpha=1e-3)",
        "hog_sgdsvm_alpha1e-05": "SVM lineal sobre HOG (alpha=1e-5)",
        "all_sgdsvm_alpha1e-05": "SVM lineal sobre variables construidas (alpha=1e-5)",
        "pca_raw_logreg_k200": "Regresion logistica con PCA sobre pixeles grises (200 comp.)",
        "pca_raw_knn_k200_n11": "k-NN con PCA sobre pixeles grises (200 comp., k=11)",
        "pca_all_rbfsvc_k200": "SVM RBF con PCA sobre variables construidas (200 comp.)",
        "pca_all_mlp_k100": "Red neuronal con PCA sobre variables construidas (100 comp.)",
        "pca_all_mlp_k200": "Red neuronal con PCA sobre variables construidas (200 comp.)",
    }
    return labels[model_id]


def preprocessing_label(model_id: str) -> str:
    if model_id in {
        "dummy_stratified",
        "raw_gray32_gnb",
        "stats_tree",
        "stats_rf",
        "stats_hgb",
    }:
        return "Sin estandarizacion"
    if model_id.startswith("pca_"):
        return "Estandarizacion + PCA con whitening"
    return "Estandarizacion"


def feature_label(value: str) -> str:
    labels = {
        "color": "Color",
        "texture": "Textura",
        "hog": "Gradientes HOG",
        "frequency": "Frecuencia",
        "raw_gray32": "Pixeles gris 32x32",
        "raw_rgb32": "Pixeles RGB 32x32",
        "stats": "Color + textura + frecuencia",
        "hog_texture": "HOG + textura",
        "all": "Color + textura + HOG + frecuencia",
    }
    return labels[value]


def metric_label(value: MetricName) -> str:
    labels: dict[MetricName, str] = {
        "accuracy": "Accuracy",
        "balanced_accuracy": "Balanced accuracy",
        "precision": "Precision",
        "recall": "Recall",
        "f1": "F1",
        "roc_auc": "ROC-AUC",
        "pr_auc": "PR-AUC",
        "kappa": "Kappa",
    }
    return labels[value]


def save_current_figure(filename: str) -> None:
    plt.tight_layout()
    plt.savefig(FIGURES / filename, dpi=180, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    generate_report_assets()
