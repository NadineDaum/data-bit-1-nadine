from __future__ import annotations

from pathlib import Path
import shutil

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
SOURCE_URL = "ADD_DATA360_DOWNLOAD_URL_HERE"
RAW_FILENAME = "RWB_PFI.csv"


def download_raw_file(url: str, destination_path: Path) -> None:
    """Download the raw CSV directly when a stable source URL is available."""
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    destination_path.write_bytes(response.content)


def import_raw_file(source_path: Path, destination_path: Path) -> None:
    """Copy a manually downloaded raw file into the project raw-data folder."""
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, destination_path)


def sanity_check_raw_file(raw_path: Path) -> pd.DataFrame:
    """Load the raw CSV without modifying it, so we can inspect its structure."""
    return pd.read_csv(raw_path)


def main() -> None:
    raw_path = RAW_DIR / RAW_FILENAME
    print("Acquisition step")
    print(f"Expected raw file: {raw_path}")
    if raw_path.exists():
        frame = sanity_check_raw_file(raw_path)
        print(f"Loaded {len(frame):,} rows and {len(frame.columns):,} columns from raw data.")
    elif SOURCE_URL and SOURCE_URL != "ADD_DATA360_DOWNLOAD_URL_HERE":
        download_raw_file(SOURCE_URL, raw_path)
        frame = sanity_check_raw_file(raw_path)
        print(f"Downloaded and loaded {len(frame):,} rows and {len(frame.columns):,} columns from raw data.")
    else:
        print("Raw file not found yet. Download or copy it into data/raw/ before running the next steps.")


if __name__ == "__main__":
    main()
