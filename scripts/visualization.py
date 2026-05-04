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

DISPLAY_NAMES = {
    "Russian Federation": "Russia",
    "Turkiye": "Türkiye",
}

FIGURE_BG = "#fafafa"
LAND_COLOR = "#ecefec"
ACCENT_DARK = "#24636b"
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
    
    # Get 2015 baseline scores for hover context
    baseline_2015 = map_frame[map_frame["year"] == 2015][["country", "iso3", "score"]].rename(
        columns={"score": "score_2015"}
    )
    map_frame = map_frame.merge(baseline_2015[["iso3", "score_2015"]], on="iso3", how="left")
    map_frame["change_since_2015"] = map_frame["score"] - map_frame["score_2015"]
    map_frame["change_since_2015"] = map_frame["change_since_2015"].round(2)
    map_frame["score"] = map_frame["score"].round(2)
    map_frame["score_2015"] = map_frame["score_2015"].round(2)

    fig = px.choropleth(
        map_frame,
        locations="iso3",
        color="score",
        hover_name="display_country",
        custom_data=["score_2015", "change_since_2015"],
        color_continuous_scale=[[0, "#edf3f1"], [1, ACCENT_DARK]],
        range_color=(0, 100),
        scope="europe",
        animation_frame="year",
        animation_group="country",
        title="Press freedom scores in Europe, 2015 to 2025",
    )
    
    # Create custom hover template with journalistic context
    hover_template = (
        "<b>%{hovertext}</b><br>"
        "Score: %{z:.2f}<br>"
        "2015 baseline: %{customdata[0]:.2f}<br>"
        "Change: %{customdata[1]:+.2f} points"
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=hover_template)
    for frame in fig.frames:
        for trace in frame.data:
            trace.hovertemplate = hover_template
    fig.update_layout(
        title={
            "text": "Press freedom scores in Europe, 2015 to 2025",
            "font": {"size": 18, "color": TEXT_COLOR, "family": "Arial, sans-serif"},
            "x": 0.5,
            "xanchor": "center",
        },
        coloraxis_colorbar=dict(
            title=dict(
                text="Press Freedom<br>(0=Worst, 100=Best)",
                font=dict(size=12, color=TEXT_COLOR, family="Arial, sans-serif"),
            ),
            tickfont=dict(size=11, color=TEXT_COLOR, family="Arial, sans-serif"),
            thickness=20,
            len=0.7,
            x=0.98,
            xanchor="right",
        ),
        paper_bgcolor=FIGURE_BG,
        plot_bgcolor=FIGURE_BG,
        font=dict(family="Arial, sans-serif", color=TEXT_COLOR),
        margin=dict(l=0, r=60, t=80, b=40),
        geo=dict(
            bgcolor=FIGURE_BG,
            showland=True,
            landcolor=LAND_COLOR,
            showocean=True,
            oceancolor=FIGURE_BG,
            coastlinecolor="#d0d0ce",
            projection_type="natural earth",
            lataxis_range=[35, 72],
            lonaxis_range=[-15, 45],
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
                    "label": "▶ Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {
                        "frame": {"duration": 0, "redraw": True},
                        "fromcurrent": True,
                        "transition": {"duration": 0}
                    }],
                    "label": "⏸ Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 85},
            "showactive": True,
            "type": "buttons",
            "x": 0.05,
            "xanchor": "left",
            "y": 0,
            "yanchor": "top",
            "bgcolor": "#ffffff",
            "bordercolor": "#d0d0ce",
            "borderwidth": 1,
            "font": {"size": 12, "color": TEXT_COLOR, "family": "Arial, sans-serif"},
        }]
    )
    
    return fig


def build_change_figure(frame: pd.DataFrame) -> go.Figure:
    top_gains = frame.nlargest(5, "change").sort_values("change", ascending=True)
    top_declines = frame.nsmallest(5, "change").sort_values("change", ascending=True)
    display = pd.concat([top_declines, top_gains], ignore_index=True)
    display["change"] = display["change"].round(2)

    display = display.assign(display_country=display["country"].map(display_country))
    colors = [GAIN if value > 0 else DECLINE for value in display["change"]]
    x_min = -32
    x_max = 10

    fig = go.Figure(
        go.Bar(
            x=display["change"],
            y=display["display_country"],
            orientation="h",
            marker_color=colors,
            width=0.5,
            cliponaxis=False,
            hovertemplate="%{y}<br>Change: %{x:.2f}<extra></extra>",
        )
    )
    fig.add_vline(x=0, line_width=1, line_color="#555555")

    fig.update_layout(
        title={
            "text": "Largest changes in press freedom scores, 2015 to 2025",
            "font": {"size": 18, "color": TEXT_COLOR, "family": "Arial, sans-serif"},
            "x": 0.5,
            "xanchor": "center",
        },
        xaxis_title="Score change (2025 minus 2015)",
        yaxis_title="",
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(129, 159, 166, 0.25)",
            zeroline=False,
            tickfont=dict(size=11, color=TEXT_COLOR, family="Arial, sans-serif"),
            range=[x_min, x_max],
        ),
        yaxis=dict(
            tickfont=dict(size=11, color=TEXT_COLOR, family="Arial, sans-serif"),
            automargin=True,
        ),
        paper_bgcolor=FIGURE_BG,
        plot_bgcolor=FIGURE_BG,
        font=dict(family="Arial, sans-serif", color=TEXT_COLOR),
        margin=dict(l=0, r=40, t=68, b=40),
        bargap=0.4,
        height=390,
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

    map_figure.write_html(MAP_PATH, include_plotlyjs="cdn")
    change_figure.write_html(CHANGE_FIG_PATH, include_plotlyjs="cdn")

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
