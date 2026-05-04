"""Generate list-view data from the cleaned press freedom table."""
from pathlib import Path
import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN_PATH = ROOT / "data" / "processed" / "rsf_europe_2015_2025.csv"
DATA_DIR = ROOT / "data"
OUTPUT_PATH = ROOT / "data" / "countries_list.json"
JS_OUTPUT_PATH = ROOT / "assets" / "js" / "countries-data.js"

DISPLAY_NAMES = {
    "Russian Federation": "Russia",
    "Turkiye": "Türkiye",
}


def display_country(country: str) -> str:
    """Return a reader-facing country label for charts and tables."""
    return DISPLAY_NAMES.get(country, country)


def build_list_data() -> None:
    """Create a JSON file with 2015, 2025 scores and change for all countries."""
    if not CLEAN_PATH.exists():
        raise FileNotFoundError(f"Cleaned file not found: {CLEAN_PATH}")
    
    frame = pd.read_csv(CLEAN_PATH)
    
    # Get 2015 and 2025 scores
    data_2015 = frame[frame["year"] == 2015][["country", "iso3", "score"]].rename(
        columns={"score": "score_2015"}
    )
    data_2025 = frame[frame["year"] == 2025][["country", "iso3", "score"]].rename(
        columns={"score": "score_2025"}
    )
    
    # Merge on country
    merged = data_2015.merge(data_2025[["iso3", "score_2025"]], on="iso3", how="inner")
    
    # Calculate change
    merged["change"] = merged["score_2025"] - merged["score_2015"]
    
    # Sort by change descending (big movers first)
    merged = merged.sort_values("change", ascending=False)
    
    # Convert to list of dicts
    countries_list = []
    for idx, row in merged.iterrows():
        countries_list.append(
            {
                "rank": len(countries_list) + 1,
                "country": display_country(row["country"]),
                "iso3": row["iso3"],
                "score_2015": round(row["score_2015"], 2),
                "score_2025": round(row["score_2025"], 2),
                "change": round(row["change"], 2),
            }
        )
    
    # Write JSON
    with open(OUTPUT_PATH, "w") as f:
        json.dump(countries_list, f, indent=2)

    JS_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(JS_OUTPUT_PATH, "w") as f:
        f.write("const countriesDataInline = ")
        json.dump(countries_list, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    
    print(f"Saved list data to {OUTPUT_PATH}")
    print(f"Saved inline list data to {JS_OUTPUT_PATH}")
    print(f"Total countries: {len(countries_list)}")


if __name__ == "__main__":
    build_list_data()
