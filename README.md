# UCUG 1808 — Gendered Gym Space, Body Image, and Resistance Training Avoidance

亚洲女大学生校园健身房空间、身体意象与阻力训练回避研究

Course: Sport in Society (UCUG 1808), 25/26 Spring Semester  
Due: 11 May 2026

## Current Status

The project now uses the collected data rather than the earlier expected-results scaffold.

- Quantitative data: questionnaire platform aggregate export plus a participant-level text-version response matrix.
- Core analytic sample: 32 female college students after screening.
- Qualitative data: three semi-structured interview QA transcripts.
- Analysis style: descriptive and exploratory, using aggregate summaries, participant-level scale scores, Spearman correlations, non-parametric group comparisons, figures, and thematic coding.
- Final report: `report/main.tex` and `report/main.pdf`.

Because the core sample is small ($N=32$), the project treats participant-level Cronbach's alpha, Spearman correlations, and Mann--Whitney group comparisons as exploratory. It does **not** claim regressions, mediation analysis, prediction models, or causal effects.

## Project Structure

```text
├── src/                          # Reusable Python helpers
│   ├── data_loader.py            # Survey aggregate parser, participant matrix loader, interview loader
│   ├── participant_analysis.py    # Participant-level scoring and group flags
│   ├── qualitative_analysis.py    # Interview theme coding and quote selection
│   ├── preprocessing.py          # Construct labels, aggregate summaries, participant scoring
│   ├── analysis.py               # Frequency, reliability, correlation, group-comparison helpers
│   └── visualization.py          # Chinese-font charts for report figures
├── scripts/
│   └── build_notebooks.py        # Rebuild notebooks from the current workflow
├── notebooks/                    # Executable analysis notebooks
│   ├── 01_data_overview.ipynb
│   ├── 02_scale_analysis.ipynb
│   ├── 03_descriptive_statistics.ipynb
│   ├── 04_inferential_analysis.ipynb
│   ├── 05_qualitative_analysis.ipynb
│   └── 06_participant_level_analysis.ipynb
├── data/
│   └── processed/                # Versioned processed outputs for reproducibility
├── output/                       # Ignored scratch tables from local analysis runs
├── report/                       # LaTeX report
│   ├── main.tex
│   ├── main.pdf
│   ├── references.bib
│   ├── sections/
│   └── figures/                  # Versioned figures used by the report
├── paper/                        # Local reference PDFs
├── proposal/                     # Proposal, used as background only
├── AGENTS.md                     # Agent/project operating notes
├── CLAUDE.md                     # Claude entrypoint, tracked intentionally
├── pyproject.toml
├── uv.lock
└── Final Group Research Project.pdf
```

## Quick Start

### 1. Install Python Dependencies

```bash
uv sync
```

### 2. Execute Notebooks

Use the project virtual environment rather than a system Jupyter install:


```bash
uv run python -m jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```

This writes processed CSV files under `data/processed/` and report figures under `report/figures/`.

### 3. Compile the Report

```bash
cd report
xelatex main
biber main
xelatex main
xelatex main
```

The compiled PDF is `report/main.pdf`.

## Research Questions

- **RQ1**: How do the campus gym's spatial environment and gym intimidation shape female college students' avoidance of resistance training?
- **RQ2**: To what extent do internalized social-media body ideals shape women's exercise preferences?
- **RQ3**: How do female students negotiate between exercising for health and avoiding deviation from digital aesthetic norms?

## Data and Measures

The survey uses 5-point slider/Likert-style items adapted for this project around four aggregate constructs:

- Spatial pressure / training anxiety
- Social-media aesthetic internalization
- Training self-efficacy
- Intervention preference

The qualitative component uses three semi-structured interviews. The project should not describe this material as a focus group.

## Report Notes

- The report is built with XeLaTeX, `ctex`, and `biblatex-apa`.
- Formatting targets the assignment requirements: APA 7, Times New Roman 11pt, 1.5 line spacing.
- `xiong2021fanshen` is intentionally retained in `report/references.bib` because it is required for the Chinese women's fitness narrative argument.
- The cover page still needs final group/member names if they are not yet filled in.

## LaTeX Setup

### Windows

MiKTeX is recommended:

1. Install MiKTeX from <https://miktex.org/download>.
2. Install or enable on-demand installation for `biber`.
3. Confirm required fonts are available: Times New Roman, SimSun, SimHei, KaiTi.
4. Verify:

```bash
xelatex --version
biber --version
```

### macOS

MacTeX is recommended. If using BasicTeX, install the needed packages:

```bash
brew install --cask basictex
eval "$(/usr/libexec/path_helper)"
sudo tlmgr update --self
sudo tlmgr install ctex fontspec biblatex-apa biber booktabs tabularx enumitem longtable subcaption setspace ragged2e
```

On macOS, replace the Windows CJK fonts in `report/main.tex` if needed, for example:

```latex
\setCJKmainfont{Songti SC}[BoldFont=Heiti SC, ItalicFont=STKaiti]
```

### Linux

```bash
sudo apt install texlive-xetex texlive-lang-chinese texlive-bibtex-extra biber
```

## Reproducibility Checklist

Before submission:

```bash
uv run python -m jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
cd report
xelatex main && biber main && xelatex main && xelatex main
```

Then check that `report/main.log` has no undefined citations.

## License

Course project for educational purposes.
