from __future__ import annotations

import hashlib
from pathlib import Path

import kagglehub
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.model_selection import StratifiedShuffleSplit

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA = PROJECT_ROOT / "data/raw/real-vs-fake-faces-stylegan3"
PROCESSED = PROJECT_ROOT / "data/processed"
RANDOM_STATE = 42
LABELS = {"Real faces": 0, "Fake faces": 1}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
DATASET = "troykueh/real-vs-fake-faces-stylegan3"
IMAGE_COLUMNS = pd.Index(
    [
        "filepath",
        "relative_path",
        "label",
        "label_name",
        "image_width",
        "image_height",
        "channels",
        "mode",
        "format",
        "file_size",
        "has_exif",
        "sha256",
    ]
)
type ImageRow = tuple[str, str, int, str, int, int, int, str, str, int, bool, str]


def prepare_dataset() -> Path:
    RAW_DATA.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    if not RAW_DATA.exists():
        if RAW_DATA.is_symlink():
            RAW_DATA.unlink()
        RAW_DATA.symlink_to(
            Path(kagglehub.dataset_download(DATASET)), target_is_directory=True
        )

    image_rows: list[ImageRow] = []
    for folder, label in LABELS.items():
        label_name = "real" if label == 0 else "fake"
        for path in sorted((RAW_DATA / folder).rglob("*")):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
                with Image.open(path) as image:
                    image.load()
                    image_format = image.format
                    assert image_format is not None
                    image_rows.append(
                        (
                            str(path.resolve()),
                            str(path.relative_to(RAW_DATA)),
                            label,
                            label_name,
                            image.width,
                            image.height,
                            len(image.getbands()),
                            image.mode,
                            image_format,
                            path.stat().st_size,
                            bool(image.getexif()),
                            sha256_file(path),
                        )
                    )

    frame = pd.DataFrame(image_rows, columns=IMAGE_COLUMNS)
    frame["dup_group"] = np.arange(len(frame))

    train_splitter = StratifiedShuffleSplit(
        n_splits=1, train_size=14000, random_state=RANDOM_STATE
    )
    train_idx, temp_idx = next(
        train_splitter.split(frame[["relative_path"]], frame["label"])
    )
    temp = frame.iloc[temp_idx].reset_index(drop=True)
    val_splitter = StratifiedShuffleSplit(
        n_splits=1, train_size=3000, random_state=RANDOM_STATE + 1
    )
    val_idx, test_idx = next(val_splitter.split(temp[["relative_path"]], temp["label"]))

    frame["split"] = "train"
    frame.loc[temp_idx, "split"] = "test"
    frame.loc[temp_idx[val_idx], "split"] = "val"
    frame.loc[temp_idx[test_idx], "split"] = "test"

    splits_path = PROCESSED / "splits.csv"
    frame.to_csv(splits_path, index=False)

    return splits_path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        block = handle.read(1 << 20)
        while block:
            digest.update(block)
            block = handle.read(1 << 20)
    return digest.hexdigest()


if __name__ == "__main__":
    prepare_dataset()
