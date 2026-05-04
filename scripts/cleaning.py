from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "RWB_PFI.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "rsf_europe_2015_2025.csv"

# Broad Europe whitelist for the Data Bit. It includes transcontinental and
# microstate economies commonly mapped with Europe in journalism visuals.
EUROPE_ISO3 = {
    "ALB", "AND", "ARM", "AUT", "AZE", "BEL", "BGR", "BIH", "BLR", "CHE",
    "CYP", "CZE", "DEU", "DNK", "ESP", "EST", "FIN", "FRA", "GBR", "GEO",
    "GRC", "HRV", "HUN", "IRL", "ISL", "ITA", "KOS", "LIE", "LTU", "LUX",
    "LVA", "MCO", "MDA", "MKD", "MLT", "MNE", "NLD", "NOR", "POL", "PRT",
    "ROU", "RUS", "SMR", "SRB", "SVK", "SVN", "SWE", "TUR", "UKR", "VAT",
}

RAW_COLUMNS = {
    "country": "REF_AREA_LABEL",
    "iso3": "REF_AREA",
    "year": "TIME_PERIOD",
    "score": "OBS_VALUE",
    "indicator": "INDICATOR",
    "status": "OBS_STATUS",
    "confidence": "OBS_CONF",
}


def clean_press_freedom_data(raw_path: Path) -> pd.DataFrame:
    frame = pd.read_csv(raw_path)

    missing_columns = [column for column in RAW_COLUMNS.values() if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"Missing expected raw columns: {', '.join(missing_columns)}")

    cleaned = frame.loc[frame["INDICATOR"] == "RWB_PFI_SCORE", [
        RAW_COLUMNS["country"],
        RAW_COLUMNS["iso3"],
        RAW_COLUMNS["year"],
        RAW_COLUMNS["score"],
        RAW_COLUMNS["status"],
        RAW_COLUMNS["confidence"],
    ]].copy()

    cleaned = cleaned.rename(
        columns={
            RAW_COLUMNS["country"]: "country",
            RAW_COLUMNS["iso3"]: "iso3",
            RAW_COLUMNS["year"]: "year",
            RAW_COLUMNS["score"]: "score",
            RAW_COLUMNS["status"]: "status",
            RAW_COLUMNS["confidence"]: "confidence",
        }
    )

    cleaned["year"] = pd.to_numeric(cleaned["year"], errors="coerce").astype("Int64")
    cleaned["score"] = pd.to_numeric(cleaned["score"], errors="coerce")
    cleaned["iso3"] = cleaned["iso3"].astype(str).str.upper()

    cleaned = cleaned.loc[cleaned["iso3"].isin(EUROPE_ISO3)].copy()
    cleaned = cleaned.loc[cleaned["year"].between(2015, 2025, inclusive="both")].copy()
    cleaned = cleaned.dropna(subset=["country", "year", "score", "iso3"])
    cleaned = cleaned.drop_duplicates(subset=["iso3", "year"])

    cleaned = cleaned[["country", "iso3", "year", "score", "status", "confidence"]].sort_values(["country", "year"])
    return cleaned


def main() -> None:
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Raw file not found: {RAW_PATH}")

    processed = clean_press_freedom_data(RAW_PATH)
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    processed.to_csv(PROCESSED_PATH, index=False)
    print(f"Saved cleaned data to {PROCESSED_PATH}")
    print(processed.head().to_string(index=False))


if __name__ == "__main__":
    main()
