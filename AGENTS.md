# AGENTS.md — UCUG 1808 Research Project

## Project Overview

本课程作业研究“亚洲女大学生校园健身房空间、身体意象与阻力训练回避”，采用混合方法设计：量化问卷汇总数据 + 三位受访者的半结构式访谈。课程为 UCUG 1808 Sport in Society，截止日期为 2026-05-11。

当前报告已经从早期预测性草稿改为基于真实数据的版本。后续改动应以 `report/main.tex` 及其分章节文件为准；`proposal/` 只用于理解原始研究意图，不应覆盖最终报告中的真实数据口径。

## Key Files

- `Final Group Research Project.pdf` — 课程作业要求（6000–8000 词，APA 7，Times New Roman 11pt，1.5 倍行距，并包含 AI disclosure）。
- `report/main.tex` — 最终论文主文件。
- `report/main.pdf` — 当前编译后的论文 PDF。
- `report/sections/` — 论文各章节；methodology、results、discussion、conclusion 已按真实数据重写。
- `report/references.bib` — APA 7 参考文献库，保留老师要求的 `xiong2021fanshen`。
- `proposal/亚洲女大学生校园健身房空间身体意象与阻力训练回避研究_proposal.pdf` — 开题报告，只作背景参考。

## Data Reality

- `data/问卷原始数据.xlsx` 是问卷平台导出的汇总表，不是逐名参与者的原始作答矩阵。
- 核心有效样本为 32 名女性在校大学生。第 1、2 题为筛选题，第 3 题之后为核心样本。
- 因为没有个体层面矩阵，不能计算真正的 Cronbach's alpha、个体层面相关、t 检验、回归或中介模型。
- 当前统计以描述性结果、题项均值、高分段比例、频数表和访谈主题整合为主。
- 质性材料来自 `data/采访对象_*_QA.md` 三份半结构式访谈，不再写作 focus group。
- `data/processed/` 中的结构化处理后数据已纳入版本控制，方便小组成员复现；原始 `data/` 文件是否追踪以仓库当前状态为准。

## Architecture

### Notebooks（按顺序运行）

1. `notebooks/01_data_overview.ipynb` — 解析问卷汇总导出，确认题型、有效样本与缺失/推断标记。
2. `notebooks/02_scale_analysis.ipynb` — 汇总滑动条题项均值、构念均值和高分段比例；明确说明不能做信度检验。
3. `notebooks/03_descriptive_statistics.ipynb` — 描述性统计与论文图表生成。
4. `notebooks/04_inferential_analysis.ipynb` — 按 RQ1–3 做描述性整合，而非个体层面推断统计。
5. `notebooks/05_qualitative_analysis.ipynb` — 三份访谈 QA 的主题编码与代表性引语整理。

运行 notebooks 时优先使用项目虚拟环境：

```bash
uv run python -m jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```

### src/ 模块

- `src/data_loader.py` — `parse_survey_export()`, `load_interviews()`, `save_processed()`；保留 `load_focus_group()` 兼容别名。
- `src/preprocessing.py` — 问卷题项标签、构念定义、滑动条构念合并和构念均值汇总。
- `src/analysis.py` — 汇总数据可支持的频数表、高/中/低分段比例，以及保留的通用统计工具。
- `src/visualization.py` — 中文字体设置、频数图和滑动条分布图。

### scripts/

- `scripts/run_analysis.py` — 一键解析真实数据，生成 `data/processed/`、`output/tables/` 和 `report/figures/`。
- `scripts/build_notebooks.py` — 根据当前真实分析流程重建五个 notebooks。

### report/

- 使用 XeLaTeX + `ctex` 中文支持 + `biblatex-apa`。
- 图表位于 `report/figures/`，由 `scripts/run_analysis.py` 或 notebooks 生成。
- 参考文献应优先使用 `paper/` 中已有 PDF；本地没有的书籍可用可靠线上书目信息核对。`xiong2021fanshen` 必须保留。

## Current Substantive Findings

- RQ1：空间压迫、男性主导感、拥挤感和动作错误羞耻是自由重量区回避的核心机制。
- RQ2：社交媒体审美会影响运动选择，但“害怕力量训练让自己不够纤细/女性化”在本样本中不是主要原因。
- RQ3：受访者更多采取时间错峰、同伴陪伴、固定器械/有氧区替代、减少被看见等协商策略，而非完全退出健身房。
- 干预偏好集中在女性初学者 workshop、半私密分区和更少刻板印象的空间文化。

## Build Commands

```bash
# Python 环境
uv sync

# 生成处理后数据、图表和表格
uv run python scripts/run_analysis.py

# 重建 notebooks（只有修改 notebook 模板时需要）
uv run python scripts/build_notebooks.py

# 执行 notebooks
uv run python -m jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb

# LaTeX 编译
cd report
xelatex main
biber main
xelatex main
xelatex main
```

## Conventions

- 不要把汇总问卷数据误写成个体层面 raw survey data。
- 不要声称完成了 Cronbach's alpha、相关、t 检验或回归，除非未来获得逐名参与者数据。
- 不要把三位受访者访谈写成 focus group。
- 报告讨论应保持谨慎：强调探索性、小样本、汇总数据限制和混合方法三角互证。
- APA 7 引用格式；课程要求的 AI disclosure 已加入 `report/main.tex`。
