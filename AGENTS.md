# AGENTS.md — UCUG 1808 Research Project

## Project Overview

本课程作业研究"亚洲女大学生校园健身房空间、身体意象与阻力训练回避"，采用混合方法设计（量化问卷 + 质性焦点小组）。课程为 UCUG 1808 Sport in Society，截止日期 2026-05-11。

## Key Files

- `Final Group Research Project.pdf` — 课程作业要求（6000–8000 词，APA 7，Times New Roman 11pt 1.5 倍行距）
- `亚洲女大学生校园健身房空间、身体意象与阻力训练回避研究.pdf` — 当前论文草稿（含预期结果的预测性脚手架）
- `proposal/亚洲女大学生校园健身房空间身体意象与阻力训练回避研究_proposal.pdf` — 开题报告

## Architecture

### Notebooks（按顺序运行）

1. `01_data_overview` — 加载原始问卷数据，缺失值检查，基础清洗
2. `02_scale_analysis` — SEAM / SATAQ-4 短版信度检验（Cronbach's α），计算子量表得分
3. `03_descriptive_statistics` — 人口统计、健身房使用习惯、量表得分分布可视化
4. `04_inferential_analysis` — 相关分析、组间比较（对应 RQ1–3）
5. `05_qualitative_analysis` — 焦点小组转录文本的主题分析

### src/ 模块

- `data_loader.py` — `load_survey()`, `load_focus_group()`, `save_processed()`
- `preprocessing.py` — `clean_survey()`, `reverse_score()`, `compute_scale_score()`
- `analysis.py` — `descriptive()`, `cronbach_alpha()`, `pearson_corr()`, `independent_ttest()`, `chi_square_test()`
- `visualization.py` — `likert_barplot()`, `correlation_heatmap()`, `save_fig()`

### report/ (LaTeX)

- XeLaTeX + ctex 中文支持 + biblatex-apa
- `sections/01_introduction.tex` 和 `02_literature_review.tex` 已从草稿 PDF 转写填充
- `04_results.tex`、`05_discussion.tex`、`06_conclusion.tex` 为 TODO 框架，等真实数据后填写

## Conventions

- 量表采用 5 点 Likert（1=非常不同意，5=非常同意）
- 15 题短版分为 3 个子量表：空间压迫/训练焦虑(Q1–5)、社交媒体审美内化(Q6–10)、阻力训练回避与张力(Q11–15)
- Q2 为反向计分题
- 统计以描述为主、探索性关联为辅，强调效应量和谨慎解释
- APA 7 引用格式

## Data Notes

- `data/` 目录已 gitignore，存放问卷原始数据和处理后数据
- Notebook 中的 `TODO` 标记处需根据实际列名替换
- 当前所有"预期结果"为预测性草稿，必须根据真实数据重写

## Build Commands

```bash
# Python 环境
uv sync

# LaTeX 编译
cd report && xelatex main && biber main && xelatex main && xelatex main
```
