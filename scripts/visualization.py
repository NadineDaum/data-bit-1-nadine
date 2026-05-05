from __future__ import annotations

from pathlib import Path
import re

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]
CLEAN_PATH = ROOT / "data" / "processed" / "rsf_europe_2015_2025.csv"
CHANGE_PATH = ROOT / "data" / "processed" / "rsf_europe_change_2015_2025.csv"
FIGURE_DIR = ROOT / "figures"
MAP_PATH = FIGURE_DIR / "rsf_europe_map_2015_2025.html"
CHANGE_FIG_PATH = FIGURE_DIR / "rsf_europe_change_2015_2025.html"
MAP_CONFIG = {
    "displayModeBar": False,
    "displaylogo": False,
    "scrollZoom": False,
    "doubleClick": False,
    "responsive": True,
}
FIGURE_CONFIG = {
    "displayModeBar": False,
    "displaylogo": False,
    "responsive": True,
}

DISPLAY_NAMES = {
    "Russian Federation": "Russia",
    "Turkiye": "Türkiye",
}

FIGURE_BG = "#fafafa"
LAND_COLOR = "#ecefec"
ACCENT_DARK = "#24636b"
MAP_BG = "#02040a"
MAP_TEXT = "#f7f8ff"
MAP_MUTED = "#a7adbd"
MAP_PURPLE = "#7b68ee"
MAP_BRIGHT_PURPLE = "#a78bfa"
MAP_OUTLINE = "#ffffff"
GAIN = "#24636b"
DECLINE = "#9fb8bd"
TEXT_COLOR = "#181817"


def display_country(country: str) -> str:
    """Return a reader-facing country label for charts and hover text."""
    return DISPLAY_NAMES.get(country, country)


def build_map_figure(frame: pd.DataFrame) -> go.Figure:
    """Build a modern animated Europe choropleth with clean, sophisticated styling."""
    map_frame = frame.copy()

    if "iso3" not in map_frame.columns:
        map_frame["iso3"] = map_frame["country"].str.slice(0, 3).str.upper()

    map_frame["display_country"] = map_frame["country"].map(display_country)
    map_frame["year"] = map_frame["year"].astype(int)
    
    # Add stable 2015 and 2025 context for hover labels.
    baseline_2015 = map_frame[map_frame["year"] == 2015][["country", "iso3", "score"]].rename(
        columns={"score": "score_2015"}
    )
    score_2025 = map_frame[map_frame["year"] == 2025][["iso3", "score"]].rename(
        columns={"score": "score_2025"}
    )
    map_frame = map_frame.merge(baseline_2015[["iso3", "score_2015"]], on="iso3", how="left")
    map_frame = map_frame.merge(score_2025, on="iso3", how="left")
    map_frame["total_change"] = map_frame["score_2025"] - map_frame["score_2015"]
    map_frame["total_change"] = map_frame["total_change"].round(1)
    map_frame["score"] = map_frame["score"].round(2)
    map_frame["score_2015"] = map_frame["score_2015"].round(1)

    fig = px.choropleth(
        map_frame,
        locations="iso3",
        color="score",
        hover_name="display_country",
        custom_data=["score_2015", "total_change"],
        color_continuous_scale=[[0, "#12091f"], [0.5, "#5b3abf"], [1, MAP_BRIGHT_PURPLE]],
        range_color=(0, 100),
        scope="europe",
        animation_frame="year",
        animation_group="country",
        title="Change of Press Freedom<br>Scores in Europe",
    )
    
    # Create custom hover template with journalistic context
    hover_template = (
        "<b>%{hovertext}</b><br>"
        "Baseline, 2015: %{customdata[0]:.1f}<br>"
        "Total change: %{customdata[1]:+.1f} pts"
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=hover_template)
    for frame in fig.frames:
        for trace in frame.data:
            trace.hovertemplate = hover_template
            trace.marker.line.color = MAP_OUTLINE
            trace.marker.line.width = 0.45
    fig.update_traces(marker_line_color=MAP_OUTLINE, marker_line_width=0.45)
    fig.update_layout(
        title={
            "text": "Change of Press Freedom<br>Scores in Europe",
            "font": {"size": 22, "color": MAP_TEXT, "family": "Arial, sans-serif"},
            "x": 0.5,
            "xanchor": "center",
        },
        coloraxis_colorbar=dict(
            title=dict(
                text="Press Freedom<br>(0=Worst, 100=Best)",
                font=dict(size=12, color=MAP_TEXT, family="Arial, sans-serif"),
            ),
            tickfont=dict(size=11, color=MAP_MUTED, family="Arial, sans-serif"),
            thickness=20,
            len=0.7,
            x=0.98,
            xanchor="right",
        ),
        paper_bgcolor=MAP_BG,
        plot_bgcolor=MAP_BG,
        font=dict(family="Arial, sans-serif", color=MAP_TEXT),
        dragmode=False,
        margin=dict(l=0, r=44, t=96, b=52),
        geo=dict(
            bgcolor=MAP_BG,
            showland=True,
            landcolor=MAP_BG,
            showocean=True,
            oceancolor=MAP_BG,
            coastlinecolor=MAP_OUTLINE,
            countrycolor=MAP_OUTLINE,
            showcountries=True,
            projection_type="natural earth",
            lataxis_range=[34, 72],
            lonaxis_range=[-18, 48],
        ),
        # Hide slider
        sliders=[{
            "active": 0,
            "currentvalue": {"prefix": "year=", "visible": False},
            "len": 0.9,
            "pad": {"b": 10, "t": 60},
            "visible": False,
        }],
        # Modern animation buttons positioning
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {
                        "frame": {"duration": 600, "redraw": True},
                        "fromcurrent": True,
                        "transition": {"duration": 300, "easing": "cubic-in-out"}
                    }],
                    "label": "▶",
                    "method": "animate"
                },
                {
                    "args": [[None], {
                        "frame": {"duration": 0, "redraw": True},
                        "fromcurrent": True,
                        "transition": {"duration": 0}
                    }],
                    "label": "⏸",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 6, "t": 0},
            "showactive": False,
            "type": "buttons",
            "x": 0.06,
            "xanchor": "left",
            "y": 0.04,
            "yanchor": "bottom",
            "bgcolor": "rgba(0,0,0,0)",
            "bordercolor": MAP_OUTLINE,
            "borderwidth": 1,
            "font": {"size": 12, "color": MAP_TEXT, "family": "Arial, sans-serif"},
        }]
    )
    
    return fig


def build_change_figure(frame: pd.DataFrame) -> go.Figure:
    top_gains = frame.nlargest(5, "change").sort_values("change", ascending=True)
    top_declines = frame.nsmallest(5, "change").sort_values("change", ascending=True)
    display = pd.concat([top_declines, top_gains], ignore_index=True)
    display["change"] = display["change"].round(2)

    display = display.assign(display_country=display["country"].map(display_country))
    colors = [MAP_BRIGHT_PURPLE if value > 0 else "#4c357f" for value in display["change"]]
    x_limit = 32

    fig = go.Figure(
        go.Bar(
            x=display["change"],
            y=display["display_country"],
            orientation="h",
            marker_color=colors,
            marker_line_color="rgba(255,255,255,0.35)",
            marker_line_width=0.5,
            width=0.5,
            cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Change: %{x:+.1f} pts<extra></extra>",
        )
    )
    fig.add_vline(x=0, line_width=1, line_color="rgba(255,255,255,0.72)")

    fig.update_layout(
        title={
            "text": "Largest Changes in Press Freedom Scores",
            "font": {"size": 22, "color": MAP_TEXT, "family": "Arial, sans-serif"},
            "x": 0.5,
            "xanchor": "center",
        },
        yaxis_title="",
        xaxis=dict(
            title=dict(
                text="Change in press freedom score, 2015 to 2025 (points)",
                font=dict(size=13, color=MAP_TEXT, family="Arial, sans-serif"),
            ),
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(255, 255, 255, 0.12)",
            zeroline=False,
            tickfont=dict(size=11, color=MAP_MUTED, family="Arial, sans-serif"),
            range=[-x_limit, x_limit],
        ),
        yaxis=dict(
            tickfont=dict(size=12, color=MAP_TEXT, family="Arial, sans-serif"),
            automargin=True,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", color=MAP_TEXT),
        margin=dict(l=20, r=44, t=82, b=60),
        bargap=0.4,
        height=500,
    )
    return fig


def main() -> None:
    if not CLEAN_PATH.exists():
        raise FileNotFoundError(f"Cleaned file not found: {CLEAN_PATH}")
    if not CHANGE_PATH.exists():
        raise FileNotFoundError(f"Change file not found: {CHANGE_PATH}")

    frame = pd.read_csv(CLEAN_PATH)
    change = pd.read_csv(CHANGE_PATH)

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    map_figure = build_map_figure(frame)
    change_figure = build_change_figure(change)

    map_figure.write_html(MAP_PATH, include_plotlyjs="cdn", config=MAP_CONFIG)
    change_figure.write_html(CHANGE_FIG_PATH, include_plotlyjs="cdn", config=FIGURE_CONFIG)

    # Add looping animation to map figure
    _add_animation_loop(MAP_PATH)

    print(f"Saved map figure to {MAP_PATH}")
    print(f"Saved change figure to {CHANGE_FIG_PATH}")


def _add_animation_loop(html_path: Path) -> None:
    """Add JavaScript to enable looping animation in Plotly figure."""
    with open(html_path, "r") as f:
        html_content = f.read()
    
    # Find the figure ID from the JSON (e.g., "1c30ee64-3eb6-4b70-ae96-56866850015b")
    fig_id_match = re.search(r'id="([a-f0-9\-]+)"', html_content)
    if not fig_id_match:
        return
    
    fig_id = fig_id_match.group(1)
    
    # Find the last Plotly.animate call and replace it with loop version
    # Look for pattern: Plotly.animate('figure_id', null);
    animate_pattern = rf"Plotly\.animate\('{fig_id}', null\);"
    
    if re.search(animate_pattern, html_content):
        loop_script = f"""var plotDiv = document.getElementById('{fig_id}');
                            var isLooping = true;
                            
                            // Start initial animation
                            Plotly.animate(plotDiv, null, {{
                                frame: {{duration: 500, redraw: true}},
                                transition: {{duration: 500, easing: 'linear'}},
                                fromcurrent: false
                            }});
                            
                            // Listen for animation end and restart
                            plotDiv.on('plotly_animated', function() {{
                                if (isLooping) {{
                                    setTimeout(function() {{
                                        Plotly.animate(plotDiv, null, {{
                                            frame: {{duration: 500, redraw: true}},
                                            transition: {{duration: 500, easing: 'linear'}},
                                            fromcurrent: false
                                        }});
                                    }}, 200);
                                }}
                            }});"""
        
        # Replace the simple animate call with the loop version
        html_content = re.sub(
            animate_pattern,
            loop_script,
            html_content
        )
    
    with open(html_path, "w") as f:
        f.write(html_content)


if __name__ == "__main__":
    main()
