from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN_PATH = ROOT / "data" / "processed" / "rsf_europe_2015_2025.csv"
CHANGE_PATH = ROOT / "data" / "processed" / "rsf_europe_change_2015_2025.csv"
LATEST_PATH = ROOT / "data" / "processed" / "rsf_europe_latest_2025.csv"
STABILITY_PATH = ROOT / "data" / "processed" / "rsf_europe_stability_2015_2025.csv"


def build_change_table(frame: pd.DataFrame) -> pd.DataFrame:
    latest = frame.loc[frame["year"] == 2025, ["country", "score"]].rename(columns={"score": "score_2025"})
    first = frame.loc[frame["year"] == 2015, ["country", "score"]].rename(columns={"score": "score_2015"})

    change = first.merge(latest, on="country", how="inner")
    change["change"] = change["score_2025"] - change["score_2015"]
    change = change.sort_values("change", ascending=False)
    change["change_rank"] = range(1, len(change) + 1)
    return change


def build_stability_table(frame: pd.DataFrame) -> pd.DataFrame:
    grouped = frame.groupby("country")["score"].agg(min_score="min", max_score="max").reset_index()
    grouped["score_range"] = grouped["max_score"] - grouped["min_score"]
    return grouped.sort_values("score_range", ascending=False)


def main() -> None:
    if not CLEAN_PATH.exists():
        raise FileNotFoundError(f"Cleaned file not found: {CLEAN_PATH}")

    frame = pd.read_csv(CLEAN_PATH)
    latest = frame.loc[frame["year"] == 2025, ["country", "score"]].sort_values("score", ascending=False)
    latest = latest.rename(columns={"score": "score_2025"})

    change = build_change_table(frame)
    stability = build_stability_table(frame)

    CHANGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    latest.to_csv(LATEST_PATH, index=False)
    change.to_csv(CHANGE_PATH, index=False)
    stability.to_csv(STABILITY_PATH, index=False)

    print(f"Saved latest table to {LATEST_PATH}")
    print(f"Saved change table to {CHANGE_PATH}")
    print(f"Saved stability table to {STABILITY_PATH}")
    print("\nTop movements:")
    print(change.head(7).to_string(index=False))
    print("\nBottom movements:")
    print(change.tail(7).to_string(index=False))


if __name__ == "__main__":
    main()
