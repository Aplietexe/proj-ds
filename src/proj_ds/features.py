from __future__ import annotations

from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageOps
from scipy.fft import dct
from scipy.stats import kurtosis, skew
from skimage import color, feature, filters, measure, transform, util
from skimage.feature import graycomatrix, graycoprops, hog, local_binary_pattern

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED = PROJECT_ROOT / "data/processed"
SPLITS_CSV = PROCESSED / "splits.csv"
FEATURES_NPZ = PROCESSED / "features.npz"
FEATURE_KEYS = ("color", "texture", "hog", "frequency", "raw_gray32", "raw_rgb32")
type FeatureRow = dict[str, np.ndarray]


def build_features() -> Path:
    splits = pd.read_csv(SPLITS_CSV)
    paths = splits["filepath"].to_list()
    rows = [image_features(path) for path in paths]

    arrays: dict[str, np.ndarray] = {}
    for key in FEATURE_KEYS:
        arrays[key] = np.vstack([row[key] for row in rows]).astype(np.float32)
    arrays["y"] = splits["label"].to_numpy(dtype=np.int8)
    arrays["split"] = splits["split"].to_numpy(dtype="U5")
    arrays["filepath"] = splits["filepath"].to_numpy(dtype=object)
    arrays["relative_path"] = splits["relative_path"].to_numpy(dtype=object)
    np.savez_compressed(
        FEATURES_NPZ,
        color=arrays["color"],
        texture=arrays["texture"],
        hog=arrays["hog"],
        frequency=arrays["frequency"],
        raw_gray32=arrays["raw_gray32"],
        raw_rgb32=arrays["raw_rgb32"],
        y=arrays["y"],
        split=arrays["split"],
        filepath=arrays["filepath"],
        relative_path=arrays["relative_path"],
    )
    return FEATURES_NPZ


def load_features(path: Path = FEATURES_NPZ) -> dict[str, np.ndarray]:
    loaded = np.load(path, allow_pickle=True)
    return {key: loaded[key] for key in loaded.files}


def feature_matrix(data: dict[str, np.ndarray], name: str) -> np.ndarray:
    if name == "all":
        return np.hstack(
            [data["hog"], data["texture"], data["color"], data["frequency"]]
        ).astype(np.float32)
    if name == "stats":
        return np.hstack([data["texture"], data["color"], data["frequency"]]).astype(
            np.float32
        )
    if name == "hog_texture":
        return np.hstack([data["hog"], data["texture"]]).astype(np.float32)
    return data[name].astype(np.float32)


def image_features(path: str) -> FeatureRow:
    rgb = load_rgb(path)
    return {
        "color": color_features(rgb),
        "texture": texture_features(rgb),
        "hog": hog_features(rgb),
        "frequency": frequency_features(rgb),
        "raw_gray32": raw_pixels(rgb, "gray"),
        "raw_rgb32": raw_pixels(rgb, "rgb"),
    }


def load_rgb(path: str, image_size: int = 96) -> np.ndarray:
    with Image.open(path) as image:
        rgb_image = ImageOps.exif_transpose(image).convert("RGB")
        rgb_image = rgb_image.resize(
            (image_size, image_size), Image.Resampling.BILINEAR
        )
        return np.asarray(rgb_image, dtype=np.float32) / 255.0


def load_transformed_rgb(
    path: str, image_size: int, crop_fraction: float, jpeg_quality: int
) -> np.ndarray:
    with Image.open(path) as image:
        rgb_image = ImageOps.exif_transpose(image).convert("RGB")
        if crop_fraction > 0:
            width, height = rgb_image.size
            dx = int(width * crop_fraction)
            dy = int(height * crop_fraction)
            rgb_image = rgb_image.crop((dx, dy, width - dx, height - dy))
        if jpeg_quality > 0:
            buffer = BytesIO()
            rgb_image.save(buffer, format="JPEG", quality=jpeg_quality)
            buffer.seek(0)
            rgb_image = Image.open(buffer).convert("RGB")
        rgb_image = rgb_image.resize(
            (image_size, image_size), Image.Resampling.BILINEAR
        )
        return np.asarray(rgb_image, dtype=np.float32) / 255.0


def channel_stats(arr: np.ndarray) -> list[float]:
    flat = arr.reshape(-1, arr.shape[-1])
    values: list[float] = []
    for channel in range(flat.shape[1]):
        x = flat[:, channel]
        values.extend(
            [float(x.mean()), float(x.std()), float(skew(x)), float(kurtosis(x))]
        )
    return values


def hist_features(arr: np.ndarray) -> list[float]:
    values: list[float] = []
    for channel in range(arr.shape[-1]):
        hist, _ = np.histogram(arr[..., channel], bins=16, range=(0, 1))
        normalized = hist.astype(np.float32) / max(float(hist.sum()), 1.0)
        values.extend(normalized.tolist())
    return values


def color_features(rgb: np.ndarray) -> np.ndarray:
    hsv = color.rgb2hsv(rgb)
    ycbcr = (
        np.asarray(Image.fromarray((rgb * 255).astype(np.uint8)).convert("YCbCr"))
        / 255.0
    )
    values: list[float] = []
    for arr in (rgb, hsv, ycbcr):
        values.extend(channel_stats(arr))
    for arr in (rgb, hsv):
        values.extend(hist_features(arr))
    gray = color.rgb2gray(rgb)
    values.extend(
        [
            float(gray.mean()),
            float(gray.std()),
            float(np.percentile(gray, 5)),
            float(np.percentile(gray, 95)),
        ]
    )
    return np.asarray(values, dtype=np.float32)


def texture_features(rgb: np.ndarray) -> np.ndarray:
    gray = color.rgb2gray(rgb)
    gray_u8 = util.img_as_ubyte(gray)
    assert gray_u8.ndim == 2
    values: list[float] = []

    lbp = local_binary_pattern(gray_u8, P=8, R=1, method="uniform")
    bins = np.arange(0, 11)
    hist, _ = np.histogram(lbp.ravel(), bins=bins)
    normalized = hist.astype(np.float32) / max(float(hist.sum()), 1.0)
    values.extend(normalized.tolist())

    height = len(gray_u8)
    width = int(gray_u8.size // height)
    for grid_y in range(4):
        for grid_x in range(4):
            patch = lbp[
                grid_y * height // 4 : (grid_y + 1) * height // 4,
                grid_x * width // 4 : (grid_x + 1) * width // 4,
            ]
            patch_hist, _ = np.histogram(patch.ravel(), bins=bins)
            patch_normalized = patch_hist.astype(np.float32) / max(
                float(patch_hist.sum()), 1.0
            )
            values.extend(patch_normalized.tolist())

    quantized = np.clip((gray_u8 // 8).astype(np.uint8), 0, 31)
    glcm = graycomatrix(
        quantized,
        distances=[1, 2, 4],
        angles=[0, np.pi / 4, np.pi / 2, 3 * np.pi / 4],
        levels=32,
        symmetric=True,
        normed=True,
    )
    for prop in (
        "contrast",
        "dissimilarity",
        "homogeneity",
        "ASM",
        "energy",
        "correlation",
    ):
        prop_values = graycoprops(glcm, prop)
        values.extend([float(np.nanmean(prop_values)), float(np.nanstd(prop_values))])

    sobel = filters.sobel(gray)
    edges = feature.canny(gray, sigma=1.0)
    values.extend(
        [
            float(measure.shannon_entropy(gray_u8)),
            float(sobel.mean()),
            float(sobel.std()),
            float(np.percentile(sobel, 95)),
            float(edges.mean()),
        ]
    )
    return np.asarray(values, dtype=np.float32)


def hog_features(rgb: np.ndarray) -> np.ndarray:
    gray = color.rgb2gray(rgb)
    features = hog(
        gray,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        block_norm="L2-Hys",
        visualize=False,
        feature_vector=True,
    )
    return features.astype(np.float32)


def radial_profile(magnitude: np.ndarray) -> np.ndarray:
    height, width = magnitude.shape
    y, x = np.indices((height, width))
    radius = np.sqrt((x - width / 2) ** 2 + (y - height / 2) ** 2)
    radius = radius / radius.max()
    values = np.zeros(32, dtype=np.float32)
    for index in range(32):
        mask = (radius >= index / 32) & (radius < (index + 1) / 32)
        if mask.any():
            values[index] = float(magnitude[mask].mean())
    total = float(values.sum())
    if total > 0:
        values = values / total
    return values


def frequency_features(rgb: np.ndarray) -> np.ndarray:
    gray = color.rgb2gray(rgb)
    centered = gray - gray.mean()
    fft = np.fft.fftshift(np.fft.fft2(centered))
    magnitude = np.log1p(np.abs(fft))
    radial = radial_profile(magnitude)

    low = radial[:8].sum()
    mid = radial[8:20].sum()
    high = radial[20:].sum()
    coeffs = np.asarray(
        dct(dct(centered, axis=0, norm="ortho"), axis=1, norm="ortho"),
        dtype=np.float32,
    )
    coeffs = np.abs(coeffs[:16, :16].ravel()[1:])
    hist, _ = np.histogram(np.log1p(coeffs), bins=16)
    normalized = hist.astype(np.float32) / max(float(hist.sum()), 1.0)
    values = np.concatenate(
        [
            radial,
            np.asarray(
                [low, mid, high, high / max(low, 1e-8), mid / max(low, 1e-8)],
                dtype=np.float32,
            ),
            normalized,
        ]
    )
    return values.astype(np.float32)


def raw_pixels(rgb: np.ndarray, mode: str) -> np.ndarray:
    resized = np.asarray(
        transform.resize(rgb, (32, 32), anti_aliasing=True, preserve_range=True),
        dtype=np.float32,
    )
    if mode == "gray":
        gray = color.rgb2gray(resized).astype(np.float32)
        return gray.ravel()
    return resized.astype(np.float32).ravel()


if __name__ == "__main__":
    build_features()
