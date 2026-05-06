# The Map That Kept Changing

**Data Bit No. 1 — Data Journalism, Spring 2026**  
**Author:** Nadine Daum  

[View article](https://rawcdn.githack.com/NadineDaum/data-bit-1-nadine/55a13b8ab7cabd869d54190d6d7c45ea9282d01b/press-freedom-map.html)

An interactive data journalism piece on changes in press freedom scores across a Europe-focused RSF/Data360 country subset, 2015–2025.

## Research question

> How did press freedom scores move across Europe over the past decade?

The article shows that Europe did not move in one direction: some countries gained ground, others declined sharply, and several high-scoring countries also shifted over time.

## Final output

The final article is `press-freedom-map.html` and includes:

- an animated map of press freedom scores from 2015 to 2025;
- a change chart showing the largest increases and decreases;
- a sortable list view with country-level scores and changes;
- source notes and a methodological caveat.

## Source and method

The project uses the **Reporters Without Borders World Press Freedom Index**, accessed through **World Bank Data360**.

“Europe” refers to the Europe-focused RSF/Data360 country subset used in this project, not European Union membership. Countries such as Türkiye, Russia, Armenia and Georgia are included when they are part of the project subset and have usable data for both 2015 and 2025.

The raw data is stored in `data/raw/RWB_PFI.csv`. Processed data files are stored in `data/processed/`.

To reproduce the project from the repository root:

```bash
pip install -r requirements.txt
python scripts/acquisition.py
python scripts/cleaning.py
python scripts/analysis.py
python scripts/list_data_builder.py
python scripts/visualization.py
python -m http.server 8000
```

Then visit `http://localhost:8000/press-freedom-map.html` in a browser.

## Project structure

```text
press-freedom-map.html        Final browser-viewable article
assets/favicon.svg            Browser tab icon
assets/css/                   Article and rank-animation styling
assets/js/                    Article interactions and generated inline country data
data/raw/RWB_PFI.csv          Original RSF/Data360 CSV
data/processed/               Cleaned data, change table and consistency checks
data/countries_list.json      Generated country list used for the article table
figures/                      Generated Plotly map and change-chart HTML files
scripts/                      Data acquisition, cleaning, analysis and visualization scripts
requirements.txt              Python dependencies
```

## Statement on AI use

I used AI-supported tools as part of my workflow, including ChatGPT and AI features in other software environments. They were used for support tasks such as brainstorming, reviewing wording, debugging code, checking methodological consistency, and refining documentation.

I did not use AI to autonomously choose the topic, decide the core comparison, interpret the findings, or replace my own review of the data. The data source, analytical scope, visual logic, article structure, and final editorial decisions were selected and checked by me. I also reviewed the generated outputs against the original sources and corrected issues where needed.

I understand the use of AI as part of the production process, not as a substitute for authorship. I am responsible for the final analysis, code, visualizations, writing, and submission.
