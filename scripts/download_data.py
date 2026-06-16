#!/usr/bin/env python
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from proj_ds.pipeline import download_data


if __name__ == "__main__":
    download_data()
