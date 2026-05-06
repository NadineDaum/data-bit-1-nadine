from __future__ import annotations

from pathlib import Path

import pandas as pd

from config import EUROPE_ISO3_SET, MAP_GEOMETRY_ISO3, ROOT, display_country

RAW_PATH = ROOT / "data" / "raw" / "RWB_PFI.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "rsf_europe_2015_2025.csv"
CONSISTENCY_PATH = ROOT / "data" / "processed" / "country_consistency_check.csv"

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

    cleaned = cleaned.loc[cleaned["iso3"].isin(EUROPE_ISO3_SET)].copy()
    cleaned = cleaned.loc[cleaned["year"].between(2015, 2025, inclusive="both")].copy()
    cleaned = cleaned.dropna(subset=["country", "year", "score", "iso3"])
    cleaned = cleaned.drop_duplicates(subset=["iso3", "year"])

    cleaned = cleaned[["country", "iso3", "year", "score", "status", "confidence"]].sort_values(["country", "year"])
    return cleaned


def build_consistency_check(raw_frame: pd.DataFrame, processed: pd.DataFrame) -> pd.DataFrame:
    """Summarize whether each canonical country is available across outputs."""
    raw_scores = raw_frame.loc[raw_frame["INDICATOR"] == "RWB_PFI_SCORE"].copy()
    raw_scores["REF_AREA"] = raw_scores["REF_AREA"].astype(str).str.upper()

    rows = []
    for iso3 in sorted(EUROPE_ISO3_SET):
        processed_country = processed.loc[processed["iso3"] == iso3, "country"]
        raw_country = raw_scores.loc[raw_scores["REF_AREA"] == iso3, "REF_AREA_LABEL"]
        country = ""
        if not processed_country.empty:
            country = processed_country.iloc[0]
        elif not raw_country.empty:
            country = raw_country.iloc[0]

        years = set(processed.loc[processed["iso3"] == iso3, "year"].astype(int))
        has_complete_years = {2015, 2025}.issubset(years)
        in_map_geometry = iso3 in MAP_GEOMETRY_ISO3

        rows.append(
            {
                "country": display_country(country) if country else "",
                "iso3": iso3,
                "in_rsf_data": iso3 in set(raw_scores["REF_AREA"]),
                "in_map_geometry": in_map_geometry,
                "has_2015": 2015 in years,
                "has_2025": 2025 in years,
                "in_final_outputs": has_complete_years and in_map_geometry,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Raw file not found: {RAW_PATH}")

    raw = pd.read_csv(RAW_PATH)
    processed = clean_press_freedom_data(RAW_PATH)
    consistency = build_consistency_check(raw, processed)
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    processed.to_csv(PROCESSED_PATH, index=False)
    consistency.to_csv(CONSISTENCY_PATH, index=False)

    countries_in_processed = processed["iso3"].nunique()
    countries_with_complete_years = consistency.loc[
        consistency["has_2015"] & consistency["has_2025"], "iso3"
    ].nunique()
    countries_in_map = consistency.loc[consistency["in_final_outputs"], "iso3"].nunique()
    missing_geometry = consistency.loc[
        consistency["in_rsf_data"] & ~consistency["in_map_geometry"], "iso3"
    ].tolist()
    missing_2015_or_2025 = consistency.loc[
        consistency["in_rsf_data"] & ~(consistency["has_2015"] & consistency["has_2025"]), "iso3"
    ].tolist()

    print(f"Saved cleaned data to {PROCESSED_PATH}")
    print(f"Saved consistency check to {CONSISTENCY_PATH}")
    print(f"Countries in processed data: {countries_in_processed}")
    print(f"Countries with 2015 and 2025 values: {countries_with_complete_years}")
    print(f"Countries in map: {countries_in_map}")
    print(f"Countries missing geometry: {missing_geometry}")
    print(f"Countries missing 2015 or 2025: {missing_2015_or_2025}")
    print(processed.head().to_string(index=False))


if __name__ == "__main__":
    main()
