# The Map That Kept Changing

**Data Bit No. 1 — Data Journalism, Spring 2026**  
**Author:** Nadine Daum  
[View article](https://rawcdn.githack.com/NadineDaum/data-bit-1-nadine/55a13b8ab7cabd869d54190d6d7c45ea9282d01b/press-freedom-map.html)

An interactive data journalism piece on changes in press freedom scores across a Europe-focused RSF/Data360 country subset, 2015–2025.

The piece asks:

> How did press freedom scores move across Europe over the past decade?

The article shows that Europe did not move in one direction: some countries gained ground, others declined sharply, and several high-scoring countries also shifted over time.


## Note

“Europe” refers to the Europe-focused RSF/Data360 country subset used in this project, not European Union membership. Countries such as Türkiye, Russia, Armenia and Georgia are included when they are part of the project subset and have usable data for both 2015 and 2025.

## Statement on AI use 

I used AI-supported tools as part of my workflow, including ChatGPT and AI features in other software environments. They were used for support tasks such as brainstorming, reviewing wording, debugging code, checking methodological consistency, and refining documentation.

I did not use AI to autonomously choose the topic, decide the core comparison, interpret the findings, or replace my own review of the data. The data source, analytical scope, visual logic, article structure, and final editorial decisions were selected and checked by me. I also reviewed the generated outputs against the original sources and corrected issues where needed.

I understand the use of AI as part of the production process, not as a substitute for authorship. I am responsible for the final analysis, code, visualizations, writing, and submission.

## Project structure

press-freedom-map.html   Final article
assets/             CSS and JavaScript
data/               Raw and processed data
figures/            Generated visualizations
scripts/            Data acquisition, cleaning, analysis and visualization
requirements.txt    Python dependencies


## Final output

The final article is `press-freedom-map.html` and includes:

- an animated map of press freedom scores from 2015 to 2025;
- a change chart showing the largest increases and decreases;
- a sortable list view with country-level scores and changes;
- source notes and a methodological caveat.


## Reproduce the project

Install dependencies:

```bash
pip install -r requirements.txt

