from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Canonical analytical universe for this project.
# "Europe" means this RSF/Data360 processing subset, not EU membership.
EUROPE_ISO3 = (
    "ALB", "AND", "ARM", "AUT", "AZE", "BEL", "BGR", "BIH", "BLR", "CHE",
    "CYP", "CZE", "DEU", "DNK", "ESP", "EST", "FIN", "FRA", "GBR", "GEO",
    "GRC", "HRV", "HUN", "IRL", "ISL", "ITA", "LIE", "LTU", "LUX", "LVA",
    "MDA", "MKD", "MLT", "MNE", "NLD", "NOR", "POL", "PRT", "ROU", "RUS",
    "SRB", "SVK", "SVN", "SWE", "TUR", "UKR",
)

EUROPE_ISO3_SET = set(EUROPE_ISO3)

# Plotly's built-in ISO-3 choropleth geometry is the map geometry source.
MAP_GEOMETRY_ISO3 = EUROPE_ISO3_SET

DISPLAY_NAMES = {
    "Russian Federation": "Russia",
    "Turkiye": "Türkiye",
}

ISO_DISPLAY_NAMES = {
    "RUS": "Russia",
    "TUR": "Türkiye",
}


def display_country(country: str) -> str:
    """Return the reader-facing country label used across article outputs."""
    return DISPLAY_NAMES.get(country, country)
