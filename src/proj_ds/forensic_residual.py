from __future__ import annotations

from dataclasses import dataclass
import time
from pathlib import Path
from typing import Literal

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageOps
from pydantic import BaseModel, ConfigDict
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

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PROCESSED = PROJECT_ROOT / "data/processed"
OUTPUTS = PROJECT_ROOT / "outputs"
FIGURES = OUTPUTS / "figures"
MODELS = OUTPUTS / "models"

SPLITS_CSV = DATA_PROCESSED / "splits.csv"
RESIDUAL_FEATURES = DATA_PROCESSED / "residual_cooc128.npy"
MODEL_PATH = MODELS / "forensic_residual_pca_rbfsvc.joblib"
REPORT_FIGURE = FIGURES / "final_residual_evaluation.png"

MODEL_ID = "forensic_residual_pca_rbfsvc"
IMAGE_SIZE = 128
GRID_CELLS = 4
RESIDUAL_LEVELS = 9
RESIDUAL_MAP_COUNT = 7
FEATURE_DIM = (
    RESIDUAL_MAP_COUNT * GRID_CELLS * GRID_CELLS * RESIDUAL_LEVELS * RESIDUAL_LEVELS
)
RANDOM_STATE = 42
PCA_COMPONENTS = 128
SVM_C = 3.0


class SplitRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    filepath: str
    relative_path: str
    label: Literal[0, 1]
    label_name: Literal["real", "fake"]
    split: Literal["train", "val", "test"]
    image_width: int
    image_height: int
    channels: int
    mode: str
    format: str
    file_size: int
    has_exif: bool
    sha256: str
    dup_group: int


@dataclass(frozen=True)
class SplitData:
    frame: pd.DataFrame
    y: np.ndarray
    split: np.ndarray


@dataclass(frozen=True)
class MetricValues:
    accuracy: float
    balanced_accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
    pr_auc: float
    kappa: float
    confusion_matrix: list[list[int]]


@dataclass(frozen=True)
class SavedModel:
    model_id: str
    threshold: float
    model: Pipeline


def load_splits() -> SplitData:
    frame = pd.read_csv(SPLITS_CSV)
    rows = frame.to_dict(orient="index")
    for row in rows.values():
        SplitRow.model_validate(row)
    return SplitData(
        frame=frame,
        y=frame["label"].to_numpy(dtype=np.int64),
        split=frame["split"].to_numpy(dtype=str),
    )


def build_residual_features() -> Path:
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    splits = load_splits()
    features = np.lib.format.open_memmap(
        RESIDUAL_FEATURES,
        mode="w+",
        dtype=np.float32,
        shape=(len(splits.frame), FEATURE_DIM),
    )
    for row_index, filepath in enumerate(splits.frame["filepath"]):
        features[row_index] = residual_cooccurrence_features(Path(filepath))
    features.flush()
    return RESIDUAL_FEATURES


def residual_cooccurrence_features(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        gray_image = ImageOps.exif_transpose(image).convert("L")
        resized = gray_image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.BILINEAR)
        gray = np.asarray(resized, dtype=np.float32)

    features: list[np.ndarray] = []
    for residual in residual_maps(gray):
        quantized = np.clip(np.rint(residual / 2.0), 0, RESIDUAL_LEVELS - 1).astype(
            np.uint8
        )
        height, width = quantized.shape
        for grid_y in range(GRID_CELLS):
            for grid_x in range(GRID_CELLS):
                cell = quantized[
                    grid_y * height // GRID_CELLS : (grid_y + 1) * height // GRID_CELLS,
                    grid_x * width // GRID_CELLS : (grid_x + 1) * width // GRID_CELLS,
                ]
                cooccurrence = graycomatrix(
                    cell,
                    distances=[1],
                    angles=[0],
                    levels=RESIDUAL_LEVELS,
                    symmetric=True,
                    normed=True,
                )
                features.append(cooccurrence[:, :, 0, 0].ravel().astype(np.float32))
    return np.concatenate(features).astype(np.float32)


def residual_maps(gray: np.ndarray) -> tuple[np.ndarray, ...]:
    horizontal = np.pad(
        np.abs(gray[:, 1:] - gray[:, :-1]), ((0, 0), (0, 1)), mode="edge"
    )
    vertical = np.pad(np.abs(gray[1:, :] - gray[:-1, :]), ((0, 1), (0, 0)), mode="edge")
    diagonal = np.pad(
        np.abs(gray[1:, 1:] - gray[:-1, :-1]), ((0, 1), (0, 1)), mode="edge"
    )
    anti_diagonal = np.pad(
        np.abs(gray[1:, :-1] - gray[:-1, 1:]), ((0, 1), (1, 0)), mode="edge"
    )
    horizontal_second = np.pad(
        np.abs(gray[:, 2:] - 2 * gray[:, 1:-1] + gray[:, :-2]),
        ((0, 0), (1, 1)),
        mode="edge",
    )
    vertical_second = np.pad(
        np.abs(gray[2:, :] - 2 * gray[1:-1, :] + gray[:-2, :]),
        ((1, 1), (0, 0)),
        mode="edge",
    )
    laplacian = np.zeros_like(gray, dtype=np.float32)
    laplacian[1:-1, 1:-1] = np.abs(
        4 * gray[1:-1, 1:-1]
        - gray[:-2, 1:-1]
        - gray[2:, 1:-1]
        - gray[1:-1, :-2]
        - gray[1:-1, 2:]
    )
    return (
        horizontal,
        vertical,
        diagonal,
        anti_diagonal,
        horizontal_second,
        vertical_second,
        laplacian,
    )


def train_forensic_residual_svm() -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    MODELS.mkdir(parents=True, exist_ok=True)
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
    test_y = splits.y[test_indices]

    model = make_model()
    started = time.perf_counter()
    model.fit(features[train_indices], splits.y[train_indices])
    train_seconds = time.perf_counter() - started

    validation_scores = model.decision_function(features[validation_indices])
    threshold, _ = best_accuracy_threshold(
        splits.y[validation_indices], validation_scores
    )
    test_scores = model.decision_function(features[test_indices])
    val_metrics = metric_values(
        splits.y[validation_indices], validation_scores, threshold
    )
    test_metrics = metric_values(test_y, test_scores, threshold)

    matrix = np.asarray(test_metrics.confusion_matrix, dtype=int)
    fpr, tpr, _ = roc_curve(test_y, test_scores)
    precision, recall, _ = precision_recall_curve(test_y, test_scores)
    figure, axes = plt.subplots(1, 3, figsize=(12, 3.6))
    axes[0].imshow(matrix, cmap="Blues")
    axes[0].set_xticks([0, 1], ["real", "fake"])
    axes[0].set_yticks([0, 1], ["real", "fake"])
    axes[0].set_xlabel("predicted")
    axes[0].set_ylabel("true")
    axes[0].set_title("Confusion matrix")
    for row in range(2):
        for column in range(2):
            axes[0].text(
                column,
                row,
                str(int(matrix[row, column])),
                ha="center",
                va="center",
                fontsize=10,
            )
    axes[1].plot(fpr, tpr, label=f"AUC {test_metrics.roc_auc:.3f}")
    axes[1].plot([0, 1], [0, 1], linestyle="--", color="gray", linewidth=1)
    axes[1].set_xlabel("false positive rate")
    axes[1].set_ylabel("true positive rate")
    axes[1].set_title("ROC")
    axes[1].legend(fontsize=8)
    axes[2].plot(recall, precision, label=f"AP {test_metrics.pr_auc:.3f}")
    axes[2].set_xlabel("recall")
    axes[2].set_ylabel("precision")
    axes[2].set_title("Precision-recall")
    axes[2].legend(fontsize=8)
    figure.tight_layout()
    figure.savefig(REPORT_FIGURE, dpi=180)
    plt.close(figure)

    joblib.dump(
        SavedModel(model_id=MODEL_ID, threshold=threshold, model=model),
        MODEL_PATH,
    )
    print(
        f"model={MODEL_ID} train_n={len(train_indices)} val_n={len(validation_indices)} test_n={len(test_indices)} train_seconds={train_seconds:.2f}",
        flush=True,
    )
    print(f"threshold={threshold:.6f}", flush=True)
    print(
        f"validation accuracy={val_metrics.accuracy:.4f} f1={val_metrics.f1:.4f} roc_auc={val_metrics.roc_auc:.4f} pr_auc={val_metrics.pr_auc:.4f}",
        flush=True,
    )
    print(
        f"test accuracy={test_metrics.accuracy:.4f} f1={test_metrics.f1:.4f} roc_auc={test_metrics.roc_auc:.4f} pr_auc={test_metrics.pr_auc:.4f} kappa={test_metrics.kappa:.4f}",
        flush=True,
    )
    print(
        f"test_confusion_matrix={test_metrics.confusion_matrix}",
        flush=True,
    )
    print(
        f"saved_model={MODEL_PATH.relative_to(PROJECT_ROOT)}",
        flush=True,
    )
    print(
        f"saved_figure={REPORT_FIGURE.relative_to(PROJECT_ROOT)}",
        flush=True,
    )
    return MODEL_PATH


def make_model() -> Pipeline:
    return Pipeline(
        [
            ("scale", StandardScaler()),
            (
                "pca",
                PCA(
                    n_components=PCA_COMPONENTS,
                    whiten=True,
                    svd_solver="randomized",
                    random_state=RANDOM_STATE,
                ),
            ),
            (
                "model",
                SVC(C=SVM_C, gamma="scale", random_state=RANDOM_STATE),
            ),
        ]
    )


def best_accuracy_threshold(
    y_true: np.ndarray, scores: np.ndarray
) -> tuple[float, float]:
    thresholds = np.unique(np.quantile(scores, np.linspace(0.01, 0.99, 199)))
    best_threshold = 0.0
    best_accuracy = -1.0
    for threshold in thresholds:
        accuracy = accuracy_score(y_true, scores >= threshold)
        if accuracy > best_accuracy:
            best_threshold = float(threshold)
            best_accuracy = float(accuracy)
    return best_threshold, best_accuracy


def metric_values(
    y_true: np.ndarray, scores: np.ndarray, threshold: float
) -> MetricValues:
    predictions = scores >= threshold
    return MetricValues(
        accuracy=float(accuracy_score(y_true, predictions)),
        balanced_accuracy=float(balanced_accuracy_score(y_true, predictions)),
        precision=float(precision_score(y_true, predictions)),
        recall=float(recall_score(y_true, predictions)),
        f1=float(f1_score(y_true, predictions)),
        roc_auc=float(roc_auc_score(y_true, scores)),
        pr_auc=float(average_precision_score(y_true, scores)),
        kappa=float(cohen_kappa_score(y_true, predictions)),
        confusion_matrix=confusion_matrix(y_true, predictions).astype(int).tolist(),
    )


if __name__ == "__main__":
    train_forensic_residual_svm()
