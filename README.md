# The Map That Kept Changing

**Data Bit No. 1 — Data Journalism**  
**Date: Spring 2026**  
**Author:** Nadine Daum  
[View article](https://rawcdn.githack.com/NadineDaum/data-bit-1-nadine/9350b1cab43588ce0d69523f50847b625e51104c/article.html)

This project is an interactive data journalism piece about changes in European press freedom scores between 2015 and 2025. It uses the **Reporters Without Borders World Press Freedom Index**, accessed through **World Bank Data360**.

The piece asks:

> How did European press freedom scores move over the past decade?

The article shows divergence: some countries gained ground, others declined sharply, and several high-scoring countries also shifted over time.

## Scope

In this project, "Europe" refers to a Europe-focused RSF/Data360 country subset used for the analysis. It is not the same as European Union membership. Countries such as Türkiye, Russia, Armenia and Georgia are included when they are part of the project subset and have usable data for both 2015 and 2025.

## Final output

The final product is `article.html`, a browser-viewable article that includes:

- an animated map of European press freedom scores from 2015 to 2025;
- a decade-change bar chart showing the largest increases and decreases;
- a list view with country-level scores and changes;
- a short journalistic interpretation with source notes and a methodological caveat.

## Data

**Source:** World Bank Data360 version of the Reporters Without Borders World Press Freedom Index  
**Dataset:** Press Freedom Index, 2002–2025  
**Original organization:** Reporters Without Borders / RSF

The raw data is stored in:

```text
data/raw/RWB_PFI.csv
```

Processed data files are stored in:

```text
data/processed/
```

## Reproduction

1. Install the Python dependencies:

```bash
pip install -r requirements.txt
```

2. Run the data pipeline scripts from the project root:

```bash
python scripts/acquisition.py
python scripts/cleaning.py
python scripts/analysis.py
python scripts/list_data_builder.py
python scripts/visualization.py
```

3. Open the article locally:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000/article.html` in a browser.

## Project structure

```text
article.html                 Main interactive article
assets/css/                  Article and animation styling
assets/js/                   Article interactions and inline country data
data/raw/                    Original downloaded data
data/processed/              Cleaned and analysis-ready data
figures/                     Generated Plotly HTML figures
scripts/                     Acquisition, cleaning, analysis, and visualization scripts
requirements.txt             Python dependencies
```

## AI use

AI tools were used to support code editing, debugging, documentation checks, and wording refinement. The analysis, editorial choices, data interpretation, and final review remain the author's responsibility.
