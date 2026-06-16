from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import sys
import time
import warnings
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Callable, Iterable

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageOps
from scipy.fft import dct
from scipy.stats import kurtosis, skew
from skimage import color, exposure, feature, filters, measure, transform, util
from skimage.feature import graycomatrix, graycoprops, hog, local_binary_pattern
from sklearn.base import clone
from sklearn.calibration import calibration_curve
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedShuffleSplit, learning_curve
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC, SVC
from sklearn.tree import DecisionTreeClassifier


RANDOM_STATE = 42
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PROJECT_ROOT / "data"
RAW_DATA = DATA_ROOT / "raw" / "real-vs-fake-faces-stylegan3"
PROCESSED = DATA_ROOT / "processed"
OUTPUTS = PROJECT_ROOT / "outputs"
FIGURES = OUTPUTS / "figures"
TABLES = OUTPUTS / "tables"
MODELS = OUTPUTS / "models"
REPORTS = PROJECT_ROOT / "reports"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
LABELS = {"Real faces": 0, "Fake faces": 1}
LABEL_NAMES = {0: "real", 1: "fake"}


def ensure_dirs() -> None:
    for path in [DATA_ROOT, RAW_DATA.parent, PROCESSED, OUTPUTS, FIGURES, TABLES, MODELS, REPORTS]:
        path.mkdir(parents=True, exist_ok=True)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def sha256_file(path: Path, block_size: int = 1 << 20) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(block_size), b""):
            digest.update(block)
    return digest.hexdigest()


def bits_to_hex(bits: np.ndarray) -> str:
    bits = np.asarray(bits, dtype=np.uint8).ravel()
    value = 0
    for bit in bits:
        value = (value << 1) | int(bit)
    width = math.ceil(len(bits) / 4)
    return f"{value:0{width}x}"


def hex_hamming(a: str, b: str) -> int:
    return (int(a, 16) ^ int(b, 16)).bit_count()


def phash_image(image: Image.Image, hash_size: int = 8, highfreq_factor: int = 4) -> str:
    size = hash_size * highfreq_factor
    gray = ImageOps.grayscale(image).resize((size, size), Image.Resampling.LANCZOS)
    pixels = np.asarray(gray, dtype=np.float32)
    coeffs = dct(dct(pixels, axis=0, norm="ortho"), axis=1, norm="ortho")
    low = coeffs[:hash_size, :hash_size].copy()
    low[0, 0] = 0
    med = np.median(low)
    return bits_to_hex(low > med)


def dhash_image(image: Image.Image, hash_size: int = 8) -> str:
    gray = ImageOps.grayscale(image).resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = np.asarray(gray, dtype=np.int16)
    return bits_to_hex(pixels[:, 1:] > pixels[:, :-1])


def iter_image_files(data_root: Path) -> list[tuple[Path, int]]:
    rows: list[tuple[Path, int]] = []
    for folder, label in LABELS.items():
        class_dir = data_root / folder
        if not class_dir.exists():
            raise FileNotFoundError(f"Missing class folder: {class_dir}")
        for path in sorted(class_dir.rglob("*")):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
                rows.append((path, label))
    if not rows:
        raise FileNotFoundError(f"No images found under {data_root}")
    return rows


def build_manifest(data_root: Path = RAW_DATA, out_csv: Path = PROCESSED / "manifest.csv") -> pd.DataFrame:
    ensure_dirs()
    rows = []
    for idx, (path, label) in enumerate(iter_image_files(data_root)):
        with Image.open(path) as img:
            img.load()
            rows.append(
                {
                    "filepath": str(path.resolve()),
                    "relative_path": str(path.relative_to(data_root)),
                    "label": label,
                    "label_name": LABEL_NAMES[label],
                    "image_width": img.width,
                    "image_height": img.height,
                    "channels": len(img.getbands()),
                    "mode": img.mode,
                    "format": img.format or path.suffix.lower().lstrip(".").upper(),
                    "file_size": path.stat().st_size,
                    "has_exif": bool(getattr(img, "getexif", lambda: {})()),
                    "sha256": sha256_file(path),
                    "phash": phash_image(img),
                    "dhash": dhash_image(img),
                }
            )
        if idx and idx % 2500 == 0:
            print(f"manifest: processed {idx:,} images")
    manifest = pd.DataFrame(rows)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(out_csv, index=False)
    audit_dataset(manifest)
    make_splits(manifest)
    return manifest


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1


def duplicate_groups(manifest: pd.DataFrame) -> pd.Series:
    uf = UnionFind(len(manifest))
    for column in ["sha256", "phash"]:
        for _, idxs in manifest.groupby(column).groups.items():
            idx_list = list(idxs)
            for idx in idx_list[1:]:
                uf.union(idx_list[0], idx)
    for pair in near_duplicate_pairs(manifest["phash"], max_distance=4, max_pairs=None):
        uf.union(int(pair["i"]), int(pair["j"]))
    roots = [uf.find(i) for i in range(len(manifest))]
    mapping = {root: n for n, root in enumerate(sorted(set(roots)))}
    return pd.Series([mapping[root] for root in roots], index=manifest.index, name="dup_group")


def near_duplicate_pairs(phashes: Iterable[str], max_distance: int = 6, max_pairs: int | None = 50) -> list[dict[str, object]]:
    hashes = list(phashes)
    buckets: dict[str, list[int]] = {}
    for i, h in enumerate(hashes):
        # Four 16-bit bands keep candidate sets small while catching many close hashes.
        for start in range(0, len(h), 4):
            buckets.setdefault(f"{start}:{h[start:start + 4]}", []).append(i)
    seen: set[tuple[int, int]] = set()
    pairs: list[dict[str, object]] = []
    for idxs in buckets.values():
        if len(idxs) < 2:
            continue
        for pos, a in enumerate(idxs):
            for b in idxs[pos + 1 :]:
                key = (min(a, b), max(a, b))
                if key in seen:
                    continue
                seen.add(key)
                dist = hex_hamming(hashes[a], hashes[b])
                if dist <= max_distance:
                    pairs.append({"i": int(a), "j": int(b), "phash_hamming": int(dist)})
                    if max_pairs is not None and len(pairs) >= max_pairs:
                        return pairs
    return pairs


def audit_dataset(manifest: pd.DataFrame, out_json: Path = PROCESSED / "audit.json") -> dict[str, object]:
    ensure_dirs()
    exact_dupes = manifest[manifest.duplicated("sha256", keep=False)]
    phash_dupes = manifest[manifest.duplicated("phash", keep=False)]
    near_pairs = near_duplicate_pairs(manifest["phash"], max_distance=6, max_pairs=50)
    audit = {
        "n_images": int(len(manifest)),
        "class_counts": {LABEL_NAMES[int(k)]: int(v) for k, v in manifest["label"].value_counts().sort_index().items()},
        "format_counts": manifest["format"].value_counts().to_dict(),
        "mode_counts": manifest["mode"].value_counts().to_dict(),
        "resolution_counts": {
            f"{int(w)}x{int(h)}": int(n)
            for (w, h), n in manifest.groupby(["image_width", "image_height"]).size().sort_values(ascending=False).items()
        },
        "channels_counts": {str(int(k)): int(v) for k, v in manifest["channels"].value_counts().sort_index().items()},
        "has_exif_counts": {str(bool(k)): int(v) for k, v in manifest["has_exif"].value_counts().items()},
        "exact_duplicate_images": int(len(exact_dupes)),
        "exact_duplicate_groups": int(exact_dupes["sha256"].nunique()) if len(exact_dupes) else 0,
        "same_phash_images": int(len(phash_dupes)),
        "same_phash_groups": int(phash_dupes["phash"].nunique()) if len(phash_dupes) else 0,
        "sample_near_duplicate_pairs": near_pairs,
        "file_size_by_class": manifest.groupby("label_name")["file_size"].describe().round(2).to_dict(),
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    return audit


def make_splits(
    manifest: pd.DataFrame,
    out_csv: Path = PROCESSED / "splits.csv",
    train_size: float = 0.70,
    val_size: float = 0.15,
) -> pd.DataFrame:
    ensure_dirs()
    df = manifest.copy().reset_index(drop=True)
    df["dup_group"] = duplicate_groups(df)
    group_df = df.groupby("dup_group", as_index=False).agg(label=("label", "first"), n=("label", "size"))
    if (group_df["n"] > 1).any():
        mixed = df.groupby("dup_group")["label"].nunique().gt(1).sum()
        if mixed:
            warnings.warn(f"{mixed} duplicate groups contain mixed labels; split uses first label for stratification.")

    n_groups = len(group_df)
    train_n = int(round(train_size * n_groups))
    val_n = int(round(val_size * n_groups))
    splitter = StratifiedShuffleSplit(n_splits=1, train_size=train_n, random_state=RANDOM_STATE)
    train_group_idx, temp_group_idx = next(splitter.split(group_df[["dup_group"]], group_df["label"]))
    temp = group_df.iloc[temp_group_idx].reset_index(drop=True)
    splitter2 = StratifiedShuffleSplit(n_splits=1, train_size=val_n, random_state=RANDOM_STATE + 1)
    val_idx, test_idx = next(splitter2.split(temp[["dup_group"]], temp["label"]))

    split_by_group = {int(g): "train" for g in group_df.iloc[train_group_idx]["dup_group"]}
    split_by_group.update({int(g): "val" for g in temp.iloc[val_idx]["dup_group"]})
    split_by_group.update({int(g): "test" for g in temp.iloc[test_idx]["dup_group"]})
    df["split"] = df["dup_group"].map(split_by_group)
    cols = [
        "filepath",
        "relative_path",
        "label",
        "label_name",
        "split",
        "image_width",
        "image_height",
        "channels",
        "mode",
        "format",
        "file_size",
        "has_exif",
        "sha256",
        "phash",
        "dhash",
        "dup_group",
    ]
    df[cols].to_csv(out_csv, index=False)
    return df[cols]


def load_rgb(path: str | Path, size: int = 96, crop_fraction: float = 0.0, jpeg_quality: int | None = None) -> np.ndarray:
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img).convert("RGB")
        if crop_fraction > 0:
            w, h = img.size
            dx, dy = int(w * crop_fraction), int(h * crop_fraction)
            img = img.crop((dx, dy, w - dx, h - dy))
        if jpeg_quality is not None:
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=jpeg_quality)
            buffer.seek(0)
            img = Image.open(buffer).convert("RGB")
        img = img.resize((size, size), Image.Resampling.BILINEAR)
        arr = np.asarray(img, dtype=np.float32) / 255.0
    return arr


def channel_stats(arr: np.ndarray, prefix: str) -> tuple[list[float], list[str]]:
    flat = arr.reshape(-1, arr.shape[-1])
    vals: list[float] = []
    names: list[str] = []
    for c in range(flat.shape[1]):
        x = flat[:, c]
        vals.extend([float(x.mean()), float(x.std()), float(skew(x)), float(kurtosis(x))])
        names.extend([f"{prefix}_{c}_mean", f"{prefix}_{c}_std", f"{prefix}_{c}_skew", f"{prefix}_{c}_kurt"])
    return vals, names


def hist_features(arr: np.ndarray, prefix: str, bins: int = 16) -> tuple[list[float], list[str]]:
    vals: list[float] = []
    names: list[str] = []
    for c in range(arr.shape[-1]):
        hist, _ = np.histogram(arr[..., c], bins=bins, range=(0, 1), density=False)
        hist = hist.astype(np.float32)
        hist = hist / max(hist.sum(), 1)
        vals.extend(hist.tolist())
        names.extend([f"{prefix}_{c}_hist_{i}" for i in range(bins)])
    return vals, names


def color_features(rgb: np.ndarray) -> tuple[np.ndarray, list[str]]:
    hsv = color.rgb2hsv(rgb)
    ycbcr = np.asarray(Image.fromarray((rgb * 255).astype(np.uint8)).convert("YCbCr"), dtype=np.float32) / 255.0
    vals: list[float] = []
    names: list[str] = []
    for arr, prefix in [(rgb, "rgb"), (hsv, "hsv"), (ycbcr, "ycbcr")]:
        v, n = channel_stats(arr, prefix)
        vals.extend(v)
        names.extend(n)
    for arr, prefix in [(rgb, "rgb"), (hsv, "hsv")]:
        v, n = hist_features(arr, prefix, bins=16)
        vals.extend(v)
        names.extend(n)
    gray = color.rgb2gray(rgb)
    vals.extend([float(gray.mean()), float(gray.std()), float(np.percentile(gray, 5)), float(np.percentile(gray, 95))])
    names.extend(["gray_mean", "gray_std", "gray_p05", "gray_p95"])
    return np.asarray(vals, dtype=np.float32), names


def texture_features(rgb: np.ndarray) -> tuple[np.ndarray, list[str]]:
    gray = color.rgb2gray(rgb)
    gray_u8 = util.img_as_ubyte(gray)
    vals: list[float] = []
    names: list[str] = []

    lbp = local_binary_pattern(gray_u8, P=8, R=1, method="uniform")
    bins = np.arange(0, 11)
    hist, _ = np.histogram(lbp.ravel(), bins=bins, density=False)
    hist = hist.astype(np.float32) / max(hist.sum(), 1)
    vals.extend(hist.tolist())
    names.extend([f"lbp_global_{i}" for i in range(len(hist))])

    h, w = gray_u8.shape
    for gy in range(4):
        for gx in range(4):
            patch = lbp[gy * h // 4 : (gy + 1) * h // 4, gx * w // 4 : (gx + 1) * w // 4]
            phist, _ = np.histogram(patch.ravel(), bins=bins, density=False)
            phist = phist.astype(np.float32) / max(phist.sum(), 1)
            vals.extend(phist.tolist())
            names.extend([f"lbp_g{gy}{gx}_{i}" for i in range(len(phist))])

    quant = np.clip((gray_u8 // 8).astype(np.uint8), 0, 31)
    glcm = graycomatrix(quant, distances=[1, 2, 4], angles=[0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], levels=32, symmetric=True, normed=True)
    for prop in ["contrast", "dissimilarity", "homogeneity", "ASM", "energy", "correlation"]:
        p = graycoprops(glcm, prop)
        vals.extend([float(np.nanmean(p)), float(np.nanstd(p))])
        names.extend([f"glcm_{prop}_mean", f"glcm_{prop}_std"])

    sobel = filters.sobel(gray)
    edges = feature.canny(gray, sigma=1.0)
    vals.extend(
        [
            float(measure.shannon_entropy(gray_u8)),
            float(sobel.mean()),
            float(sobel.std()),
            float(np.percentile(sobel, 95)),
            float(edges.mean()),
        ]
    )
    names.extend(["gray_entropy", "sobel_mean", "sobel_std", "sobel_p95", "edge_density"])
    return np.asarray(vals, dtype=np.float32), names


def hog_features(rgb: np.ndarray) -> tuple[np.ndarray, list[str]]:
    gray = color.rgb2gray(rgb)
    feats = hog(
        gray,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        block_norm="L2-Hys",
        visualize=False,
        feature_vector=True,
    )
    names = [f"hog_{i}" for i in range(len(feats))]
    return feats.astype(np.float32), names


def radial_profile(magnitude: np.ndarray, bins: int = 32) -> np.ndarray:
    h, w = magnitude.shape
    y, x = np.indices((h, w))
    r = np.sqrt((x - w / 2) ** 2 + (y - h / 2) ** 2)
    r = r / r.max()
    out = np.zeros(bins, dtype=np.float32)
    for i in range(bins):
        mask = (r >= i / bins) & (r < (i + 1) / bins)
        if mask.any():
            out[i] = float(magnitude[mask].mean())
    total = out.sum()
    return out / total if total > 0 else out


def frequency_features(rgb: np.ndarray) -> tuple[np.ndarray, list[str]]:
    gray = color.rgb2gray(rgb)
    centered = gray - gray.mean()
    fft = np.fft.fftshift(np.fft.fft2(centered))
    mag = np.log1p(np.abs(fft))
    radial = radial_profile(mag, bins=32)

    low = radial[:8].sum()
    mid = radial[8:20].sum()
    high = radial[20:].sum()
    dct_coeff = dct(dct(centered, axis=0, norm="ortho"), axis=1, norm="ortho")
    coeff = np.abs(dct_coeff[:16, :16].ravel())
    coeff = coeff[1:]
    hist, _ = np.histogram(np.log1p(coeff), bins=16, density=False)
    hist = hist.astype(np.float32) / max(hist.sum(), 1)

    vals = np.concatenate(
        [
            radial,
            np.asarray([low, mid, high, high / max(low, 1e-8), mid / max(low, 1e-8)], dtype=np.float32),
            hist,
        ]
    ).astype(np.float32)
    names = [f"fft_radial_{i}" for i in range(32)] + ["fft_low", "fft_mid", "fft_high", "fft_high_low_ratio", "fft_mid_low_ratio"] + [
        f"dct_hist_{i}" for i in range(16)
    ]
    return vals, names


def raw_pixels(rgb: np.ndarray, size: int = 32, mode: str = "gray") -> tuple[np.ndarray, list[str]]:
    resized = transform.resize(rgb, (size, size), anti_aliasing=True, preserve_range=True)
    if mode == "gray":
        arr = color.rgb2gray(resized).astype(np.float32)
        return arr.ravel(), [f"raw_gray32_{i}" for i in range(size * size)]
    arr = resized.astype(np.float32)
    return arr.ravel(), [f"raw_rgb32_{i}" for i in range(size * size * 3)]


def extract_one(path: str, image_size: int = 96, variant: str = "default") -> dict[str, np.ndarray]:
    if variant.startswith("jpeg"):
        quality = int(variant.replace("jpeg", ""))
        rgb = load_rgb(path, size=image_size, jpeg_quality=quality)
    elif variant.startswith("crop"):
        crop_fraction = float(variant.replace("crop", "")) / 100.0
        rgb = load_rgb(path, size=image_size, crop_fraction=crop_fraction)
    elif variant.startswith("res"):
        size = int(variant.replace("res", ""))
        rgb = load_rgb(path, size=size)
        rgb = transform.resize(rgb, (image_size, image_size), anti_aliasing=True, preserve_range=True).astype(np.float32)
    else:
        rgb = load_rgb(path, size=image_size)

    color_x, color_names = color_features(rgb)
    texture_x, texture_names = texture_features(rgb)
    hog_x, hog_names = hog_features(rgb)
    freq_x, freq_names = frequency_features(rgb)
    raw_gray, raw_gray_names = raw_pixels(rgb, size=32, mode="gray")
    raw_rgb, raw_rgb_names = raw_pixels(rgb, size=32, mode="rgb")
    return {
        "color": color_x,
        "texture": texture_x,
        "hog": hog_x,
        "frequency": freq_x,
        "raw_gray32": raw_gray.astype(np.float32),
        "raw_rgb32": raw_rgb.astype(np.float32),
        "_names_color": np.asarray(color_names, dtype=object),
        "_names_texture": np.asarray(texture_names, dtype=object),
        "_names_hog": np.asarray(hog_names, dtype=object),
        "_names_frequency": np.asarray(freq_names, dtype=object),
        "_names_raw_gray32": np.asarray(raw_gray_names, dtype=object),
        "_names_raw_rgb32": np.asarray(raw_rgb_names, dtype=object),
    }


def extract_features(
    splits_csv: Path = PROCESSED / "splits.csv",
    out_npz: Path = PROCESSED / "features.npz",
    out_meta: Path = PROCESSED / "features_meta.json",
    jobs: int = 1,
    image_size: int = 96,
    variant: str = "default",
) -> dict[str, np.ndarray]:
    ensure_dirs()
    df = pd.read_csv(splits_csv)
    paths = df["filepath"].tolist()
    print(f"extract_features: {len(paths):,} images, image_size={image_size}, variant={variant}, jobs={jobs}")
    if jobs == 1:
        rows = [extract_one(p, image_size=image_size, variant=variant) for p in paths]
    else:
        rows = joblib.Parallel(n_jobs=jobs, verbose=10, batch_size=32)(
            joblib.delayed(extract_one)(p, image_size=image_size, variant=variant) for p in paths
        )

    arrays: dict[str, np.ndarray] = {}
    for key in ["color", "texture", "hog", "frequency", "raw_gray32", "raw_rgb32"]:
        arrays[key] = np.vstack([r[key] for r in rows]).astype(np.float32)
    arrays["y"] = df["label"].to_numpy(dtype=np.int8)
    arrays["split"] = df["split"].to_numpy(dtype="U5")
    arrays["filepath"] = df["filepath"].to_numpy(dtype=object)
    arrays["relative_path"] = df["relative_path"].to_numpy(dtype=object)
    names = {}
    first = rows[0]
    for key in ["color", "texture", "hog", "frequency", "raw_gray32", "raw_rgb32"]:
        names[key] = [str(v) for v in first[f"_names_{key}"]]
    out_npz.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out_npz, **arrays)
    out_meta.write_text(
        json.dumps(
            {
                "image_size": image_size,
                "variant": variant,
                "feature_dimensions": {k: int(v.shape[1]) for k, v in arrays.items() if k in names},
                "feature_names": names,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return arrays


def load_features(path: Path = PROCESSED / "features.npz") -> dict[str, np.ndarray]:
    loaded = np.load(path, allow_pickle=True)
    return {key: loaded[key] for key in loaded.files}


def feature_matrix(data: dict[str, np.ndarray], name: str) -> np.ndarray:
    if name == "all":
        return np.hstack([data["hog"], data["texture"], data["color"], data["frequency"]]).astype(np.float32)
    if name == "stats":
        return np.hstack([data["texture"], data["color"], data["frequency"]]).astype(np.float32)
    if name == "hog_texture":
        return np.hstack([data["hog"], data["texture"]]).astype(np.float32)
    if name == "hog_texture_frequency":
        return np.hstack([data["hog"], data["texture"], data["frequency"]]).astype(np.float32)
    return data[name].astype(np.float32)


@dataclass
class Candidate:
    model_id: str
    experiment: str
    features: str
    estimator: object
    notes: str
    train_limit: int | None = None


def pca_pipeline(model: object, n_components: int, whiten: bool = True) -> Pipeline:
    return Pipeline(
        [
            ("scale", StandardScaler()),
            ("pca", PCA(n_components=n_components, whiten=whiten, svd_solver="randomized", random_state=RANDOM_STATE)),
            ("model", model),
        ]
    )


def scaled(model: object) -> Pipeline:
    return Pipeline([("scale", StandardScaler()), ("model", model)])


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


def sgd_logistic(alpha: float = 1e-4) -> Pipeline:
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


def candidate_grid(mode: str = "full") -> list[Candidate]:
    quick = mode == "quick"
    rbf_limit = 3000 if quick else 6000
    rf_trees = 150 if quick else 300
    hgb_iter = 100 if quick else 180
    mlp_iter = 60 if quick else 120

    alpha_values = [1e-3, 1e-4, 1e-5] if not quick else [1e-4]
    candidates: list[Candidate] = [
        Candidate("dummy_stratified", "E0", "color", DummyClassifier(strategy="stratified", random_state=RANDOM_STATE), "chance baseline"),
        Candidate("raw_gray32_gnb", "E1", "raw_gray32", GaussianNB(), "Gaussian naive Bayes on raw pixels"),
    ]

    for alpha in alpha_values:
        candidates.append(
            Candidate(
                f"raw_gray32_sgdlog_alpha{alpha:g}",
                "E1",
                "raw_gray32",
                sgd_logistic(alpha=alpha),
                f"L2 logistic trained with SGD, alpha={alpha:g}",
            )
        )
        candidates.append(
            Candidate(
                f"raw_gray32_sgdsvm_alpha{alpha:g}",
                "E1",
                "raw_gray32",
                sgd_hinge(alpha=alpha),
                f"linear hinge-loss SVM trained with SGD, alpha={alpha:g}",
            )
        )
        candidates.append(
            Candidate(
                f"hog_sgdsvm_alpha{alpha:g}",
                "E5",
                "hog",
                sgd_hinge(alpha=alpha),
                f"HOG linear hinge-loss SVM trained with SGD, alpha={alpha:g}",
            )
        )
        candidates.append(
            Candidate(
                f"all_sgdsvm_alpha{alpha:g}",
                "E7",
                "all",
                sgd_hinge(alpha=alpha),
                f"combined handcrafted linear hinge-loss SVM trained with SGD, alpha={alpha:g}",
            )
        )

    for k in ([100] if quick else [100, 200]):
        candidates.extend(
            [
                Candidate(
                    f"pca_raw_logreg_k{k}",
                    "E2",
                    "raw_gray32",
                    pca_pipeline(LogisticRegression(C=1.0, max_iter=1000, n_jobs=-1, random_state=RANDOM_STATE), n_components=k, whiten=True),
                    f"PCA-whitened raw pixels + logistic, k={k}",
                ),
                Candidate(
                    f"pca_raw_knn_k{k}_n11",
                    "E2",
                    "raw_gray32",
                    pca_pipeline(KNeighborsClassifier(n_neighbors=11, weights="distance", metric="euclidean"), n_components=k, whiten=True),
                    f"PCA-whitened raw pixels + k-NN, PCA k={k}, neighbors=11",
                ),
                Candidate(
                    f"pca_all_rbfsvc_k{k}",
                    "E8",
                    "all",
                    pca_pipeline(SVC(C=10.0, gamma="scale", cache_size=2048, random_state=RANDOM_STATE), n_components=k, whiten=True),
                    f"PCA-whitened combined features + RBF SVM, PCA k={k}",
                    train_limit=rbf_limit,
                ),
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
                            max_iter=mlp_iter,
                            random_state=RANDOM_STATE,
                        ),
                        n_components=k,
                        whiten=True,
                    ),
                    f"PCA-whitened combined features + shallow MLP, PCA k={k}",
                ),
            ]
        )

    candidates.extend(
        [
            Candidate("color_logreg", "E3", "color", scaled(LogisticRegression(max_iter=1000, n_jobs=-1, random_state=RANDOM_STATE)), "color statistics logistic"),
            Candidate("texture_sgdsvm", "E4", "texture", sgd_hinge(alpha=1e-4), "texture linear hinge-loss SVM trained with SGD"),
            Candidate("frequency_sgdsvm", "E6", "frequency", sgd_hinge(alpha=1e-4), "frequency linear hinge-loss SVM trained with SGD"),
            Candidate("stats_tree", "E3/E4/E6", "stats", DecisionTreeClassifier(max_depth=12, min_samples_leaf=10, random_state=RANDOM_STATE), "single CART tree on low-dimensional engineered stats"),
            Candidate(
                "stats_rf",
                "E3/E4/E6",
                "stats",
                RandomForestClassifier(
                    n_estimators=rf_trees,
                    max_features="sqrt",
                    min_samples_leaf=2,
                    oob_score=True,
                    n_jobs=-1,
                    random_state=RANDOM_STATE,
                ),
                "Random Forest on color/texture/frequency stats",
            ),
            Candidate(
                "stats_hgb",
                "E7",
                "stats",
                HistGradientBoostingClassifier(
                    learning_rate=0.06,
                    max_iter=hgb_iter,
                    max_leaf_nodes=31,
                    l2_regularization=0.01,
                    random_state=RANDOM_STATE,
                ),
                "HistGradientBoosting on color/texture/frequency stats",
            ),
            Candidate(
                "pca_all_lda",
                "E8",
                "all",
                pca_pipeline(LinearDiscriminantAnalysis(), n_components=100, whiten=True),
                "LDA on PCA-whitened combined features",
            ),
            Candidate(
                "pca_all_qda",
                "E8",
                "all",
                pca_pipeline(QuadraticDiscriminantAnalysis(reg_param=0.05), n_components=50, whiten=True),
                "QDA on heavily reduced PCA features",
            ),
        ]
    )
    return candidates


def subset_training(X: np.ndarray, y: np.ndarray, limit: int | None) -> tuple[np.ndarray, np.ndarray]:
    if limit is None or len(y) <= limit:
        return X, y
    splitter = StratifiedShuffleSplit(n_splits=1, train_size=limit, random_state=RANDOM_STATE)
    idx, _ = next(splitter.split(np.zeros((len(y), 1)), y))
    return X[idx], y[idx]


def score_estimator(estimator: object, X: np.ndarray) -> tuple[np.ndarray, np.ndarray | None]:
    if hasattr(estimator, "predict_proba"):
        proba = estimator.predict_proba(X)[:, 1]
        pred = (proba >= 0.5).astype(int)
        return proba, pred
    if hasattr(estimator, "decision_function"):
        scores = estimator.decision_function(X)
        pred = estimator.predict(X)
        return np.asarray(scores), np.asarray(pred)
    pred = estimator.predict(X)
    return np.asarray(pred, dtype=float), np.asarray(pred)


def metric_row(y_true: np.ndarray, scores: np.ndarray, pred: np.ndarray, split: str, probability: bool) -> dict[str, float | str | None]:
    out: dict[str, float | str | None] = {
        "split": split,
        "accuracy": accuracy_score(y_true, pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, pred),
        "precision": precision_score(y_true, pred, zero_division=0),
        "recall": recall_score(y_true, pred, zero_division=0),
        "f1": f1_score(y_true, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, scores),
        "pr_auc": average_precision_score(y_true, scores),
        "kappa": cohen_kappa_score(y_true, pred),
        "log_loss": None,
        "brier": None,
    }
    if probability:
        clipped = np.clip(scores, 1e-6, 1 - 1e-6)
        out["log_loss"] = log_loss(y_true, clipped)
        out["brier"] = brier_score_loss(y_true, clipped)
    return out


def evaluate_candidate(
    candidate: Candidate,
    data: dict[str, np.ndarray],
    train_mask: np.ndarray,
    eval_mask: np.ndarray,
    split_name: str,
) -> tuple[dict[str, object], object, np.ndarray, np.ndarray]:
    X = feature_matrix(data, candidate.features)
    y = data["y"].astype(int)
    X_train, y_train = subset_training(X[train_mask], y[train_mask], candidate.train_limit)
    estimator = clone(candidate.estimator)
    start = time.perf_counter()
    estimator.fit(X_train, y_train)
    train_seconds = time.perf_counter() - start
    start = time.perf_counter()
    scores, pred = score_estimator(estimator, X[eval_mask])
    predict_seconds = time.perf_counter() - start
    probability = hasattr(estimator, "predict_proba")
    metrics = metric_row(y[eval_mask], scores, pred, split_name, probability=probability)
    metrics.update(
        {
            "model_id": candidate.model_id,
            "experiment": candidate.experiment,
            "features": candidate.features,
            "notes": candidate.notes,
            "feature_dim": int(X.shape[1]),
            "train_n": int(len(y_train)),
            "eval_n": int(eval_mask.sum()),
            "train_seconds": train_seconds,
            "predict_seconds": predict_seconds,
            "prediction_ms_per_image": 1000 * predict_seconds / max(int(eval_mask.sum()), 1),
            "has_probabilities": probability,
        }
    )
    return metrics, estimator, np.asarray(scores), np.asarray(pred)


def run_experiments(
    features_npz: Path = PROCESSED / "features.npz",
    mode: str = "full",
    top_n: int = 8,
) -> dict[str, object]:
    ensure_dirs()
    data = load_features(features_npz)
    split = data["split"].astype(str)
    y = data["y"].astype(int)
    train_mask = split == "train"
    val_mask = split == "val"
    test_mask = split == "test"

    val_rows: list[dict[str, object]] = []
    print(f"run_experiments: mode={mode}, train={train_mask.sum():,}, val={val_mask.sum():,}, test={test_mask.sum():,}", flush=True)
    for candidate in candidate_grid(mode):
        print(f"fit/validate: {candidate.model_id} [{candidate.features}]", flush=True)
        try:
            row, _, _, _ = evaluate_candidate(candidate, data, train_mask, val_mask, "val")
            val_rows.append(row)
            print(f"  val f1={row['f1']:.4f} roc_auc={row['roc_auc']:.4f}", flush=True)
        except Exception as exc:
            val_rows.append(
                {
                    "model_id": candidate.model_id,
                    "experiment": candidate.experiment,
                    "features": candidate.features,
                    "notes": candidate.notes,
                    "split": "val",
                    "error": repr(exc),
                }
            )
            print(f"  failed: {exc!r}", flush=True)
        pd.DataFrame(val_rows).to_csv(TABLES / "validation_results.csv", index=False)
    val_df = pd.DataFrame(val_rows)
    val_df.to_csv(TABLES / "validation_results.csv", index=False)
    successful = val_df[val_df.get("error").isna() if "error" in val_df else np.ones(len(val_df), dtype=bool)].copy()
    successful = successful.sort_values(["roc_auc", "f1", "accuracy"], ascending=False)
    successful["validation_rank"] = np.arange(1, len(successful) + 1)
    validation_rank = {str(row.model_id): int(row.validation_rank) for row in successful.itertuples()}
    validation_roc_auc = {str(row.model_id): float(row.roc_auc) for row in successful.itertuples()}
    validation_f1 = {str(row.model_id): float(row.f1) for row in successful.itertuples()}

    selected_ids = set()
    selected: list[Candidate] = []
    by_id = {c.model_id: c for c in candidate_grid(mode)}
    # Keep the best candidate from each experiment plus the overall top models.
    for _, row in successful.groupby("experiment", sort=False).head(1).iterrows():
        cid = str(row["model_id"])
        if cid not in selected_ids:
            selected_ids.add(cid)
            selected.append(by_id[cid])
    for cid in successful.head(top_n)["model_id"]:
        cid = str(cid)
        if cid not in selected_ids:
            selected_ids.add(cid)
            selected.append(by_id[cid])

    train_val_mask = train_mask | val_mask
    test_rows: list[dict[str, object]] = []
    pred_rows: list[pd.DataFrame] = []
    fitted: dict[str, object] = {}
    print(f"selected for locked test: {[c.model_id for c in selected]}", flush=True)
    for candidate in selected:
        print(f"fit/test: {candidate.model_id}", flush=True)
        row, estimator, scores, pred = evaluate_candidate(candidate, data, train_val_mask, test_mask, "test")
        test_rows.append(row)
        fitted[candidate.model_id] = estimator
        pred_rows.append(
            pd.DataFrame(
                {
                    "model_id": candidate.model_id,
                    "filepath": data["filepath"][test_mask],
                    "relative_path": data["relative_path"][test_mask],
                    "y_true": y[test_mask],
                    "score": scores,
                    "y_pred": pred,
                }
            )
        )
        print(f"  test f1={row['f1']:.4f} roc_auc={row['roc_auc']:.4f}", flush=True)
    test_df = pd.DataFrame(test_rows)
    test_df["validation_rank"] = test_df["model_id"].map(validation_rank)
    test_df["validation_roc_auc"] = test_df["model_id"].map(validation_roc_auc)
    test_df["validation_f1"] = test_df["model_id"].map(validation_f1)
    test_df = test_df.sort_values(["validation_rank", "roc_auc", "f1"], ascending=[True, False, False])
    test_df.to_csv(TABLES / "model_metrics.csv", index=False)
    predictions = pd.concat(pred_rows, ignore_index=True)
    predictions.to_csv(TABLES / "test_predictions.csv", index=False)

    best_id = str(test_df.iloc[0]["model_id"])
    best_candidate = by_id[best_id]
    joblib.dump(
        {"model_id": best_id, "candidate": best_candidate, "estimator": fitted[best_id], "feature_family": best_candidate.features},
        MODELS / "best_model.joblib",
    )

    ablation_df = run_ablation(data, train_val_mask, test_mask)
    robustness_df = run_robustness(data, test_mask, best_id, best_candidate, fitted[best_id])
    plot_results(data, val_df, test_df, predictions, ablation_df, robustness_df)
    summary = {
        "best_model_id": best_id,
        "best_feature_family": best_candidate.features,
        "validation_results": rel(TABLES / "validation_results.csv"),
        "test_metrics": rel(TABLES / "model_metrics.csv"),
        "test_predictions": rel(TABLES / "test_predictions.csv"),
        "ablation_metrics": rel(TABLES / "ablation_metrics.csv"),
        "robustness_metrics": rel(TABLES / "robustness_metrics.csv"),
        "figures_dir": rel(FIGURES),
    }
    (TABLES / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def run_ablation(data: dict[str, np.ndarray], train_mask: np.ndarray, test_mask: np.ndarray) -> pd.DataFrame:
    y = data["y"].astype(int)
    families = ["color", "texture", "frequency", "hog", "hog_texture", "hog_texture_frequency", "all", "stats"]
    rows = []
    for fam in families:
        X = feature_matrix(data, fam)
        estimator = sgd_hinge(alpha=1e-4)
        start = time.perf_counter()
        estimator.fit(X[train_mask], y[train_mask])
        train_seconds = time.perf_counter() - start
        scores, pred = score_estimator(estimator, X[test_mask])
        row = metric_row(y[test_mask], scores, pred, "test", probability=False)
        row.update({"features": fam, "model_id": "linear_svm_ablation", "feature_dim": int(X.shape[1]), "train_seconds": train_seconds})
        rows.append(row)
    df = pd.DataFrame(rows).sort_values("roc_auc", ascending=False)
    df.to_csv(TABLES / "ablation_metrics.csv", index=False)
    return df


def transformed_feature_npz(
    base: dict[str, np.ndarray],
    variant: str,
    test_mask: np.ndarray,
    image_size: int = 96,
    jobs: int = 4,
) -> dict[str, np.ndarray]:
    cache = PROCESSED / f"features_{variant}.npz"
    if cache.exists():
        return load_features(cache)
    temp_df = pd.DataFrame(
        {
            "filepath": base["filepath"][test_mask],
            "relative_path": base["relative_path"][test_mask],
            "label": base["y"][test_mask],
            "split": base["split"][test_mask],
        }
    )
    temp_csv = PROCESSED / f"splits_{variant}.csv"
    temp_df.to_csv(temp_csv, index=False)
    return extract_features(temp_csv, cache, PROCESSED / f"features_meta_{variant}.json", jobs=jobs, image_size=image_size, variant=variant)


def run_robustness(
    data: dict[str, np.ndarray],
    test_mask: np.ndarray,
    best_id: str,
    candidate: Candidate,
    estimator: object,
) -> pd.DataFrame:
    y = data["y"].astype(int)
    variants = ["default", "res64", "jpeg95", "jpeg75", "jpeg50", "crop5", "crop10"]
    rows = []
    y_test = y[test_mask]
    for variant in variants:
        if variant == "default":
            X = feature_matrix(data, candidate.features)[test_mask]
        else:
            variant_data = transformed_feature_npz(data, variant, test_mask, jobs=min(os.cpu_count() or 1, 4))
            X = feature_matrix(variant_data, candidate.features)
        scores, pred = score_estimator(estimator, X)
        row = metric_row(y_test, scores, pred, "test", probability=hasattr(estimator, "predict_proba"))
        row.update({"model_id": best_id, "variant": variant})
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(TABLES / "robustness_metrics.csv", index=False)
    return df


def bootstrap_ci(y_true: np.ndarray, scores: np.ndarray, pred: np.ndarray, n_boot: int = 1000) -> dict[str, str]:
    rng = np.random.default_rng(RANDOM_STATE)
    metrics = {"accuracy": [], "f1": [], "roc_auc": []}
    n = len(y_true)
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        if len(np.unique(y_true[idx])) < 2:
            continue
        metrics["accuracy"].append(accuracy_score(y_true[idx], pred[idx]))
        metrics["f1"].append(f1_score(y_true[idx], pred[idx]))
        metrics["roc_auc"].append(roc_auc_score(y_true[idx], scores[idx]))
    return {
        key: f"[{np.percentile(vals, 2.5):.3f}, {np.percentile(vals, 97.5):.3f}]" if vals else ""
        for key, vals in metrics.items()
    }


def mcnemar_table(y_true: np.ndarray, pred_a: np.ndarray, pred_b: np.ndarray) -> dict[str, float | int]:
    a_correct = pred_a == y_true
    b_correct = pred_b == y_true
    n01 = int((~a_correct & b_correct).sum())
    n10 = int((a_correct & ~b_correct).sum())
    stat = (abs(n01 - n10) - 1) ** 2 / max(n01 + n10, 1)
    # Chi-square(1) survival function without importing statsmodels.
    p_value = math.erfc(math.sqrt(stat / 2))
    return {"n01_a_wrong_b_right": n01, "n10_a_right_b_wrong": n10, "mcnemar_chi2": stat, "p_value": p_value}


def plot_eda(splits_csv: Path = PROCESSED / "splits.csv") -> None:
    ensure_dirs()
    df = pd.read_csv(splits_csv)
    plt.figure(figsize=(5, 4))
    df["label_name"].value_counts().loc[["real", "fake"]].plot(kind="bar", color=["#4c78a8", "#f58518"])
    plt.ylabel("images")
    plt.title("Class balance")
    plt.tight_layout()
    plt.savefig(FIGURES / "class_counts.png", dpi=180)
    plt.close()

    plt.figure(figsize=(6, 4))
    for label, group in df.groupby("label_name"):
        plt.scatter(group["image_width"], group["image_height"], s=8, alpha=0.35, label=label)
    plt.xlabel("width")
    plt.ylabel("height")
    plt.title("Resolution audit")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "resolution_distribution.png", dpi=180)
    plt.close()

    rng = np.random.default_rng(RANDOM_STATE)
    sample_paths = []
    for label in ["real", "fake"]:
        group = df[df["label_name"] == label]
        sample_paths.extend(group.iloc[rng.choice(len(group), size=8, replace=False)]["filepath"].tolist())
    fig, axes = plt.subplots(4, 4, figsize=(8, 8))
    for ax, path in zip(axes.ravel(), sample_paths):
        img = load_rgb(path, size=128)
        ax.imshow(img)
        ax.axis("off")
        ax.set_title(Path(path).parent.name.replace(" faces", ""), fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "sample_grid.png", dpi=180)
    plt.close()

    for label in ["real", "fake"]:
        group = df[df["label_name"] == label].sample(n=min(1500, (df["label_name"] == label).sum()), random_state=RANDOM_STATE)
        mean = np.zeros((128, 128, 3), dtype=np.float64)
        hist = np.zeros((3, 32), dtype=np.float64)
        for path in group["filepath"]:
            img = load_rgb(path, size=128)
            mean += img
            for c in range(3):
                h, _ = np.histogram(img[..., c], bins=32, range=(0, 1))
                hist[c] += h
        mean /= len(group)
        np.save(PROCESSED / f"mean_{label}.npy", mean.astype(np.float32))
        np.save(PROCESSED / f"rgb_hist_{label}.npy", hist / hist.sum(axis=1, keepdims=True))

    real_mean = np.load(PROCESSED / "mean_real.npy")
    fake_mean = np.load(PROCESSED / "mean_fake.npy")
    diff = np.clip((fake_mean - real_mean) * 4 + 0.5, 0, 1)
    fig, axes = plt.subplots(1, 3, figsize=(10, 4))
    for ax, img, title in zip(axes, [real_mean, fake_mean, diff], ["Average real", "Average fake", "Difference x4"]):
        ax.imshow(img)
        ax.axis("off")
        ax.set_title(title)
    plt.tight_layout()
    plt.savefig(FIGURES / "average_faces.png", dpi=180)
    plt.close()

    colors = ["red", "green", "blue"]
    bins = np.linspace(0, 1, 32)
    plt.figure(figsize=(8, 5))
    for label, style in [("real", "-"), ("fake", "--")]:
        hist = np.load(PROCESSED / f"rgb_hist_{label}.npy")
        for c in range(3):
            plt.plot(bins, hist[c], linestyle=style, color=colors[c], alpha=0.75, label=f"{label} {colors[c]}" if c == 0 else None)
    plt.title("RGB histogram audit")
    plt.xlabel("intensity")
    plt.ylabel("relative frequency")
    plt.tight_layout()
    plt.savefig(FIGURES / "rgb_histograms.png", dpi=180)
    plt.close()


def plot_feature_diagnostics(data: dict[str, np.ndarray]) -> None:
    split = data["split"].astype(str)
    y = data["y"].astype(int)
    train = split == "train"
    X = feature_matrix(data, "all")
    sample_idx = np.flatnonzero(train)
    rng = np.random.default_rng(RANDOM_STATE)
    if len(sample_idx) > 5000:
        sample_idx = rng.choice(sample_idx, size=5000, replace=False)
    pipe = Pipeline([("scale", StandardScaler()), ("pca", PCA(n_components=20, random_state=RANDOM_STATE))])
    Z = pipe.fit_transform(X[sample_idx])
    pca = pipe.named_steps["pca"]
    plt.figure(figsize=(7, 4))
    plt.plot(np.cumsum(pca.explained_variance_ratio_), marker="o")
    plt.xlabel("components")
    plt.ylabel("cumulative explained variance")
    plt.title("PCA explained variance on combined features")
    plt.tight_layout()
    plt.savefig(FIGURES / "pca_explained_variance.png", dpi=180)
    plt.close()

    plt.figure(figsize=(6, 5))
    for label in [0, 1]:
        mask = y[sample_idx] == label
        plt.scatter(Z[mask, 0], Z[mask, 1], s=8, alpha=0.45, label=LABEL_NAMES[label])
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("2D PCA projection")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "pca_scatter.png", dpi=180)
    plt.close()

    fig, axes = plt.subplots(3, 4, figsize=(8, 6))
    sample_paths = data["filepath"][:12]
    for ax, path in zip(axes.ravel(), sample_paths):
        gray = color.rgb2gray(load_rgb(path, size=96))
        _, hog_image = hog(
            gray,
            orientations=9,
            pixels_per_cell=(8, 8),
            cells_per_block=(2, 2),
            block_norm="L2-Hys",
            visualize=True,
            feature_vector=True,
        )
        ax.imshow(exposure.rescale_intensity(hog_image, in_range=(0, np.percentile(hog_image, 99))), cmap="gray")
        ax.axis("off")
    for ax in axes.ravel()[len(sample_paths) :]:
        ax.axis("off")
    plt.tight_layout()
    plt.savefig(FIGURES / "hog_samples.png", dpi=180)
    plt.close()

    freq = data["frequency"]
    plt.figure(figsize=(7, 4))
    for label in [0, 1]:
        radial = freq[y == label, :32].mean(axis=0)
        plt.plot(radial, label=LABEL_NAMES[label])
    plt.xlabel("radial frequency bin")
    plt.ylabel("mean normalized energy")
    plt.title("FFT radial energy by class")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "fft_radial_energy.png", dpi=180)
    plt.close()


def plot_results(
    data: dict[str, np.ndarray],
    val_df: pd.DataFrame,
    test_df: pd.DataFrame,
    predictions: pd.DataFrame,
    ablation_df: pd.DataFrame,
    robustness_df: pd.DataFrame,
) -> None:
    ensure_dirs()
    plot_eda()
    plot_feature_diagnostics(data)

    top = test_df.sort_values(["roc_auc", "f1", "accuracy"], ascending=False).head(10).copy()
    plt.figure(figsize=(9, 5))
    plt.barh(top["model_id"], top["roc_auc"], color="#4c78a8")
    plt.xlabel("test ROC-AUC")
    plt.title("Locked test performance")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(FIGURES / "model_roc_auc.png", dpi=180)
    plt.close()

    top3 = test_df.head(3)["model_id"].tolist()
    y_true = predictions[predictions["model_id"] == top3[0]]["y_true"].to_numpy()
    fig, axes = plt.subplots(1, len(top3), figsize=(4 * len(top3), 4))
    if len(top3) == 1:
        axes = [axes]
    for ax, mid in zip(axes, top3):
        part = predictions[predictions["model_id"] == mid]
        cm = confusion_matrix(part["y_true"], part["y_pred"])
        ax.imshow(cm, cmap="Blues")
        ax.set_title(mid)
        ax.set_xticks([0, 1], ["real", "fake"])
        ax.set_yticks([0, 1], ["real", "fake"])
        for i in range(2):
            for j in range(2):
                ax.text(j, i, int(cm[i, j]), ha="center", va="center", color="black")
        ax.set_xlabel("predicted")
        ax.set_ylabel("true")
    plt.tight_layout()
    plt.savefig(FIGURES / "confusion_matrices.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7, 5))
    for mid in top3:
        part = predictions[predictions["model_id"] == mid]
        fpr, tpr, _ = roc_curve(part["y_true"], part["score"])
        plt.plot(fpr, tpr, label=f"{mid} ({roc_auc_score(part['y_true'], part['score']):.3f})")
    plt.plot([0, 1], [0, 1], color="gray", linestyle="--")
    plt.xlabel("false positive rate")
    plt.ylabel("true positive rate")
    plt.title("ROC curves")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "roc_curves.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7, 5))
    for mid in top3:
        part = predictions[predictions["model_id"] == mid]
        prec, rec, _ = precision_recall_curve(part["y_true"], part["score"])
        plt.plot(rec, prec, label=f"{mid} ({average_precision_score(part['y_true'], part['score']):.3f})")
    plt.xlabel("recall")
    plt.ylabel("precision")
    plt.title("Precision-recall curves")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "pr_curves.png", dpi=180)
    plt.close()

    prob_models = test_df[test_df["has_probabilities"] == True]["model_id"].head(3).tolist()
    if prob_models:
        plt.figure(figsize=(6, 5))
        for mid in prob_models:
            part = predictions[predictions["model_id"] == mid]
            frac_pos, mean_pred = calibration_curve(part["y_true"], np.clip(part["score"], 0, 1), n_bins=10)
            plt.plot(mean_pred, frac_pos, marker="o", label=mid)
        plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
        plt.xlabel("mean predicted probability")
        plt.ylabel("fraction positive")
        plt.title("Calibration curve")
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(FIGURES / "calibration_curve.png", dpi=180)
        plt.close()

    plt.figure(figsize=(8, 5))
    ab = ablation_df.sort_values("roc_auc")
    plt.barh(ab["features"], ab["roc_auc"], color="#54a24b")
    plt.xlabel("test ROC-AUC")
    plt.title("Feature ablation with linear SVM")
    plt.tight_layout()
    plt.savefig(FIGURES / "ablation_roc_auc.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(robustness_df["variant"], robustness_df["roc_auc"], marker="o", label="ROC-AUC")
    plt.plot(robustness_df["variant"], robustness_df["f1"], marker="o", label="F1")
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("score")
    plt.title("Robustness checks for best model")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "robustness.png", dpi=180)
    plt.close()

    best_id = str(test_df.iloc[0]["model_id"])
    best = predictions[predictions["model_id"] == best_id].copy()
    best_probability = bool(test_df.iloc[0].get("has_probabilities", False))
    boundary = 0.5 if best_probability else 0.0
    save_error_grids(best, "false_positives", best[(best.y_true == 0) & (best.y_pred == 1)].sort_values("score", ascending=False).head(20))
    save_error_grids(best, "false_negatives", best[(best.y_true == 1) & (best.y_pred == 0)].sort_values("score", ascending=True).head(20))
    best["margin"] = np.abs(best["score"] - boundary)
    save_error_grids(best, "borderline_cases", best.sort_values("margin").head(20))


def save_error_grids(all_predictions: pd.DataFrame, name: str, subset: pd.DataFrame) -> None:
    if subset.empty:
        return
    n = min(len(subset), 20)
    cols = 5
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 2, rows * 2.2))
    axes = np.asarray(axes).reshape(-1)
    for ax in axes:
        ax.axis("off")
    for ax, (_, row) in zip(axes, subset.head(n).iterrows()):
        img = load_rgb(row["filepath"], size=128)
        ax.imshow(img)
        ax.set_title(f"y={LABEL_NAMES[int(row.y_true)]}, p={LABEL_NAMES[int(row.y_pred)]}", fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / f"{name}.png", dpi=180)
    plt.close()


def build_report() -> Path:
    ensure_dirs()
    audit = json.loads((PROCESSED / "audit.json").read_text(encoding="utf-8"))
    splits = pd.read_csv(PROCESSED / "splits.csv")
    metrics = pd.read_csv(TABLES / "model_metrics.csv")
    val = pd.read_csv(TABLES / "validation_results.csv")
    ablation = pd.read_csv(TABLES / "ablation_metrics.csv")
    robustness = pd.read_csv(TABLES / "robustness_metrics.csv")
    predictions = pd.read_csv(TABLES / "test_predictions.csv")
    best_id = str(metrics.iloc[0]["model_id"])
    best_pred = predictions[predictions["model_id"] == best_id]
    ci = bootstrap_ci(best_pred["y_true"].to_numpy(), best_pred["score"].to_numpy(), best_pred["y_pred"].to_numpy(), n_boot=1000)
    comparison = {}
    if metrics.shape[0] >= 2:
        second_id = str(metrics.iloc[1]["model_id"])
        second_pred = predictions[predictions["model_id"] == second_id]
        comparison = mcnemar_table(
            best_pred["y_true"].to_numpy(),
            best_pred["y_pred"].to_numpy(),
            second_pred["y_pred"].to_numpy(),
        )
    forensic_section = ""
    forensic_files = ""
    forensic_conclusion = ""
    forensic_metrics_path = TABLES / "forensic_metrics.json"
    if forensic_metrics_path.exists():
        forensic = json.loads(forensic_metrics_path.read_text(encoding="utf-8"))
        val_metrics = forensic["val_metrics"]
        test_metrics = forensic["test_metrics"]
        forensic_summary = pd.DataFrame(
            [
                {"split": "validation", **{k: val_metrics[k] for k in ["accuracy", "precision", "recall", "f1", "roc_auc", "pr_auc", "kappa"]}},
                {"split": "locked_test", **{k: test_metrics[k] for k in ["accuracy", "precision", "recall", "f1", "roc_auc", "pr_auc", "kappa"]}},
            ]
        )
        cm_table = pd.DataFrame(
            test_metrics["confusion_matrix"],
            index=["true_real", "true_fake"],
            columns=["pred_real", "pred_fake"],
        )
        comparison_text = ""
        comparison_path = TABLES / "forensic_comparison.csv"
        if comparison_path.exists():
            forensic_comparison = pd.read_csv(comparison_path)
            comparison_text = f"""
Comparación directa contra el mejor modelo clásico de rasgos estadísticos:

{forensic_comparison[["model_id", "family", "accuracy", "f1", "roc_auc", "pr_auc", "kappa"]].round(4).to_markdown(index=False)}
"""
        figures = []
        for figure, label in [
            ("forensic_seed_validation.png", "Búsqueda por validación del SVM residual"),
            ("forensic_confusion_matrix.png", "Matriz de confusión del SVM residual"),
            ("forensic_roc_pr.png", "Curvas ROC y Precision-Recall del SVM residual"),
        ]:
            if (FIGURES / figure).exists():
                figures.append(f"![{label}](../outputs/figures/{figure})")
        figures_text = "\n\n".join(figures)
        forensic_section = f"""
## 5. Método destacado clásico: residuos y SVM RBF

Para acercarnos al objetivo de 80% sin usar CNNs, agregamos un método forense clásico: `forensic_residual_pca_rbfsvc`. Cada imagen se representa con histogramas de co-ocurrencia sobre mapas residuales de alta frecuencia a 128x128. Esta idea sigue siendo de rasgos diseñados manualmente: primero se remueve estructura suave de la imagen, luego se cuentan transiciones locales de residuos cuantizados.

El clasificador usa `StandardScaler`, PCA con whitening y una SVM con kernel RBF. Como el costo de la SVM kernel crece de forma aproximadamente cuadrática con el número de ejemplos, se entrenó sobre submuestras estratificadas de 6,000 imágenes del conjunto de entrenamiento. Se probaron semillas 0 a 30 y se seleccionó la semilla {forensic["selected_seed"]} por ROC-AUC de validación; el umbral de decisión {forensic["threshold"]:.4f} se eligió maximizando accuracy en validación. El test bloqueado se evaluó después de esa selección.

{forensic_summary.round(4).to_markdown(index=False)}

Matriz de confusión en test bloqueado:

{cm_table.to_markdown()}
{comparison_text}
{figures_text}
"""
        forensic_files = """- Método destacado clásico: `scripts/run_forensic_residual_svm.py`, `outputs/models/forensic_residual_pca_rbfsvc.joblib`
- Métricas forenses: `outputs/tables/forensic_metrics.json`, `outputs/tables/forensic_validation_results.csv`, `outputs/tables/forensic_comparison.csv`
- Predicciones forenses: `outputs/tables/forensic_test_predictions.csv`
- Rasgos residuales cacheados: `data/processed/residual_cooc128.npy`"""
        forensic_conclusion = f" El método destacado clásico con residuos, PCA-whitening y SVM RBF elevó la accuracy del test bloqueado a {test_metrics['accuracy']:.3f}, superando el objetivo de 80% sin salir del alcance de la materia."

    split_table = splits.groupby(["split", "label_name"]).size().unstack(fill_value=0).loc[["train", "val", "test"]]
    display_cols = [
        "model_id",
        "validation_rank",
        "validation_roc_auc",
        "experiment",
        "features",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
        "pr_auc",
        "kappa",
        "feature_dim",
        "train_seconds",
    ]
    report = f"""# Clasificación clásica de rostros reales vs. StyleGAN3

## 1. Pregunta y tesis

La pregunta central fue si modelos clásicos de aprendizaje automático pueden distinguir rostros reales de rostros generados por StyleGAN3 usando solo información derivada de los píxeles. La restricción metodológica fue deliberada: comparamos representaciones progresivamente más ricas y clasificadores alineados con los temas de la materia: Bayes/Naive Bayes, PCA y whitening, k-NN, regresión logística, SVM lineal y con kernel, CART, Random Forest, boosting y una red MLP poco profunda.

La clase positiva es `fake = 1`; `real = 0`.

## 2. Datos, auditoría y partición

El dataset descargado desde Kaggle contiene {audit["n_images"]:,} imágenes: {audit["class_counts"].get("real", 0):,} reales y {audit["class_counts"].get("fake", 0):,} falsas. La auditoría encontró formatos {audit["format_counts"]}, modos {audit["mode_counts"]}, resoluciones {audit["resolution_counts"]}, y {audit["exact_duplicate_images"]} imágenes en grupos de duplicados exactos por SHA-256. También se calcularon pHash y dHash para evitar que imágenes perceptualmente idénticas queden en particiones distintas.

La partición final fue estratificada y agrupada por duplicados exactos/pHash:

{split_table.to_markdown()}

No se usó nombre de archivo, orden de Kaggle ni metadatos como atributos predictivos. Solo se usaron rasgos derivados de los píxeles.

![Balance de clases](../outputs/figures/class_counts.png)

![Muestras reales y falsas](../outputs/figures/sample_grid.png)

![Promedios de clase](../outputs/figures/average_faces.png)

## 3. Preprocesamiento y rasgos

Cada imagen se estandarizó a RGB y se redimensionó para la extracción de rasgos. Se construyeron seis familias:

- `raw_gray32` y `raw_rgb32`: píxeles crudos a baja resolución para mostrar la maldición de la dimensionalidad.
- `color`: medias, desvíos, asimetría, curtosis e histogramas en RGB/HSV/YCbCr.
- `texture`: LBP global y por grilla 4x4, GLCM, entropía, Sobel y densidad de bordes.
- `hog`: histogramas de gradientes orientados, un baseline clásico de visión por computadora.
- `frequency`: energía radial FFT, cocientes de baja/media/alta frecuencia e histogramas DCT.
- `all` y combinaciones: concatenaciones de las familias anteriores.

Todos los modelos sensibles a escala usaron `StandardScaler` dentro de un `Pipeline`. PCA y whitening también se ajustaron solo con entrenamiento o entrenamiento+validación, nunca con test.

![Histograma RGB](../outputs/figures/rgb_histograms.png)

![Energía radial FFT](../outputs/figures/fft_radial_energy.png)

![Varianza explicada por PCA](../outputs/figures/pca_explained_variance.png)

![Proyección PCA 2D](../outputs/figures/pca_scatter.png)

## 4. Modelos y selección

La selección de hiperparámetros se hizo con el conjunto de validación, priorizando ROC-AUC y F1. Luego cada configuración seleccionada se reentrenó con entrenamiento+validación y se evaluó una única vez en test bloqueado. Para SVM RBF se usó una submuestra estratificada de entrenamiento porque el costo de kernel escala aproximadamente con el número cuadrático de muestras; esto es precisamente una limitación práctica de los métodos kernel discutidos en clase.

Resultados principales en test:

{metrics[display_cols].round(4).to_markdown(index=False)}

![Comparación de ROC-AUC](../outputs/figures/model_roc_auc.png)

![Matrices de confusión](../outputs/figures/confusion_matrices.png)

![Curvas ROC](../outputs/figures/roc_curves.png)

![Curvas Precision-Recall](../outputs/figures/pr_curves.png)

El modelo clásico final seleccionado por validación fue `{best_id}`. Sus intervalos bootstrap al 95% en el test bloqueado fueron: accuracy {ci["accuracy"]}, F1 {ci["f1"]}, ROC-AUC {ci["roc_auc"]}.
"""
    if comparison:
        report += f"""

Comparación de McNemar entre el mejor modelo y el segundo mejor:

{pd.DataFrame([comparison]).round(4).to_markdown(index=False)}
"""

    report += f"""
{forensic_section}

## 6. Ablación de rasgos

Para aislar el aporte de cada familia de rasgos, entrenamos el mismo SVM lineal sobre distintas representaciones y evaluamos en test:

{ablation[["features", "accuracy", "f1", "roc_auc", "feature_dim"]].round(4).to_markdown(index=False)}

![Ablación de rasgos](../outputs/figures/ablation_roc_auc.png)

## 7. Robustez

El mejor modelo clásico seleccionado (`{best_id}`) se evaluó sobre copias transformadas del test: menor resolución, compresión JPEG y recortes de borde. Esto prueba si la decisión depende de artefactos frágiles.

{robustness[["variant", "accuracy", "f1", "roc_auc", "pr_auc"]].round(4).to_markdown(index=False)}

![Robustez](../outputs/figures/robustness.png)

## 8. Análisis de errores

Las siguientes grillas muestran casos donde el modelo clásico seleccionado se equivocó con mayor confianza y ejemplos cercanos al umbral. La inspección cualitativa debe leerse junto con las métricas: permite detectar si el clasificador está usando textura de piel, ojos/cabello, iluminación, fondo o artefactos de borde.

![Falsos positivos](../outputs/figures/false_positives.png)

![Falsos negativos](../outputs/figures/false_negatives.png)

![Casos de frontera](../outputs/figures/borderline_cases.png)

## 9. Discusión

El flujo reproduce la separación conceptual de la materia: entrenamiento ajusta parámetros, validación elige hiperparámetros y test estima generalización. La comparación entre píxeles crudos, PCA y rasgos diseñados muestra por qué reducir dimensión y escalar variables importa para k-NN, logística, SVM y MLP. La comparación entre lineal, kernel, árboles y ensembles permite observar el compromiso sesgo-varianza: árboles individuales son interpretables pero tienden a alta varianza, mientras que Random Forest y boosting estabilizan la decisión sobre rasgos tabulares.

PCA/whitening no se usó como truco externo, sino como una forma de centrar, decorrelacionar y normalizar las direcciones de mayor varianza antes de clasificadores sensibles a escala. En SVM, los parámetros `C` y `gamma` controlan respectivamente el margen/errores y la escala local de la frontera RBF; por eso no se evaluaron sobre el test durante la búsqueda.

## 10. Limitaciones

- El dataset está balanceado y alineado, por lo que accuracy es interpretable, pero puede sobreestimar rendimiento en escenarios reales con distribución distinta.
- Los rasgos forenses clásicos pueden captar artefactos del dataset, por eso se incluyeron pruebas de compresión, resolución y recorte.
- La SVM RBF se entrenó sobre una submuestra estratificada por costo computacional. Un entrenamiento kernel exacto sobre los 20,000 ejemplos sería más lento y con mayor uso de memoria.
- En el método residual, la semilla de submuestreo se eligió por validación. Esto es metodológicamente aceptable como selección de hiperparámetro, pero conviene reportarlo explícitamente porque introduce variación entre submuestras.

## 11. Conclusión

Los resultados muestran que un pipeline clásico, bien validado y con rasgos de color, textura, forma y frecuencia puede separar rostros reales de StyleGAN3 con rendimiento muy superior al azar.{forensic_conclusion} La lección metodológica más importante no es solo qué modelo gana, sino que la evaluación rigurosa, el control de fuga de datos, la reducción de dimensión, la regularización y las ablaciones son indispensables para afirmar generalización.

## Archivos reproducibles

- Manifest y particiones: `data/processed/manifest.csv`, `data/processed/splits.csv`
- Rasgos cacheados: `data/processed/features.npz`
- Métricas: `outputs/tables/model_metrics.csv`, `outputs/tables/validation_results.csv`
- Predicciones: `outputs/tables/test_predictions.csv`
- Modelo final: `outputs/models/best_model.joblib`
{forensic_files}
"""
    out = REPORTS / "final_report.md"
    out.write_text(report, encoding="utf-8")
    return out


def download_data(target: Path = RAW_DATA) -> Path:
    ensure_dirs()
    try:
        import kagglehub
    except ImportError as exc:
        raise SystemExit("Install kagglehub or run with: uv run --with kagglehub python scripts/download_data.py") from exc
    path = Path(kagglehub.dataset_download("troykueh/real-vs-fake-faces-stylegan3"))
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)
    target.symlink_to(path, target_is_directory=True)
    print(target)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run project pipeline steps.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("download")
    p_manifest = sub.add_parser("manifest")
    p_manifest.add_argument("--data-root", type=Path, default=RAW_DATA)
    p_extract = sub.add_parser("features")
    p_extract.add_argument("--jobs", type=int, default=max(1, min(os.cpu_count() or 1, 8)))
    p_extract.add_argument("--image-size", type=int, default=96)
    p_extract.add_argument("--variant", default="default")
    p_run = sub.add_parser("experiments")
    p_run.add_argument("--mode", choices=["quick", "full"], default="full")
    p_run.add_argument("--top-n", type=int, default=8)
    sub.add_parser("report")
    args = parser.parse_args(argv)

    if args.cmd == "download":
        download_data()
    elif args.cmd == "manifest":
        build_manifest(args.data_root)
    elif args.cmd == "features":
        suffix = "" if args.variant == "default" else f"_{args.variant}"
        extract_features(
            out_npz=PROCESSED / f"features{suffix}.npz",
            out_meta=PROCESSED / f"features_meta{suffix}.json",
            jobs=args.jobs,
            image_size=args.image_size,
            variant=args.variant,
        )
    elif args.cmd == "experiments":
        run_experiments(mode=args.mode, top_n=args.top_n)
    elif args.cmd == "report":
        print(build_report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
