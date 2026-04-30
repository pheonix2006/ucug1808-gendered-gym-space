# UCUG 1808 — Spatial Environment, Body Image, and Resistance Training Avoidance

亚洲女大学生校园健身房空间、身体意象与阻力训练回避研究

Course: Sport in Society (UCUG 1808), 25/26 Spring Semester
Due: 11 May 2026

## Project Structure

```
├── src/                          # 可复用 Python 工具函数
│   ├── data_loader.py            #   问卷 / 焦点小组数据加载
│   ├── preprocessing.py          #   清洗、反向计分、量表得分计算
│   ├── analysis.py               #   描述统计、Cronbach's α、相关、t 检验、χ²
│   └── visualization.py          #   Likert 柱状图、相关热力图
├── notebooks/                    # Jupyter Notebooks（按顺序运行）
│   ├── 01_data_overview.ipynb    #   数据概览与清洗
│   ├── 02_scale_analysis.ipynb   #   SEAM & SATAQ-4 信效度分析
│   ├── 03_descriptive_statistics.ipynb  #   描述性统计与分布可视化
│   ├── 04_inferential_analysis.ipynb    #   RQ1–3 推断统计分析
│   └── 05_qualitative_analysis.ipynb    #   焦点小组主题分析
├── report/                       # LaTeX 论文（XeLaTeX + biblatex-apa）
│   ├── main.tex                  #   主文件
│   ├── references.bib            #   APA 7 参考文献
│   ├── sections/                 #   各章节 .tex
│   └── figures/                  #   论文插图
├── data/                         # 数据文件（已 gitignore）
├── paper/                        # 参考文献 PDF
├── proposal/                     # 开题报告
├── pyproject.toml                # Python 依赖
└── Final Group Research Project.pdf  # 课程作业要求
```

## Environment Setup

```bash
# 安装依赖（需要 Python 3.11+ 和 uv）
uv sync
```

## LaTeX Compilation

```bash
cd report
xelatex main
biber main
xelatex main
xelatex main
```

## Research Questions

- **RQ1**: 校园健身房的空间环境与 gym intimidation 如何影响女性大学生对阻力训练的回避？
- **RQ2**: 社交媒体审美规范的内化在多大程度上塑造女性学生的运动偏好？
- **RQ3**: 女性学生如何在"为了健康而运动"与"害怕偏离数字审美规范"之间进行协商？

## Measures

- **SEAM** (Social Exercise Anxiety Measure, Levinson et al., 2013) — 情境化短版改编
- **SATAQ-4** (Sociocultural Attitudes Towards Appearance Questionnaire, Schaefer et al., 2015) — 情境化短版改编
- **Focus Group** — 半结构化焦点小组访谈

## Data

问卷和焦点小组数据存放于 `data/` 目录（已加入 `.gitignore`），不纳入版本控制。

## License

Course project for educational purposes.
