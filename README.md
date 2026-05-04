# The Map That Kept Changing

**Data Bit No. 1 — Data Journalism**
**Date: Spring 2026**  
**Author:** Nadine Daum  
[View the article](https://rawcdn.githack.com/NadineDaum/data-bit-1-nadine/056523793fecaf50d811e125097532b0a910eb83/article.html)

This project is an interactive data journalism piece about changes in European press freedom scores between **2015 and 2025**. It uses the **Reporters Without Borders World Press Freedom Index**, accessed through **World Bank Data360**, to compare country-level movement over time.

The piece asks a descriptive question:

> How did European press freedom scores move over the past decade?

The article shows divergence: some countries gained ground, others declined sharply, and several high-scoring countries also shifted over time.

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
