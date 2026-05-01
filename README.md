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
│   ├── figures/                  #   论文插图
│   ├── build.sh                  #   编译脚本 (macOS / Linux / Git Bash)
│   └── build.bat                 #   编译脚本 (Windows CMD，双击即用)
├── data/                         # 数据文件（已 gitignore）
├── paper/                        # 参考文献 PDF
├── proposal/                     # 开题报告
├── pyproject.toml                # Python 依赖
└── Final Group Research Project.pdf  # 课程作业要求
```

## Quick Start

### 1. Python 环境

```bash
# 需要已安装 Python 3.11+ 和 uv
uv sync
```

### 2. LaTeX 编译

#### 方式 A：一键脚本（推荐）

```bash
# Windows：双击 report/build.bat，或在 Git Bash 中运行：
bash report/build.sh
```

#### 方式 B：手动编译

```bash
cd report
xelatex main
biber main
xelatex main
xelatex main
```

编译成功后输出 `report/main.pdf`。

---

## LaTeX 环境配置指南

如果还没有安装 LaTeX，按以下步骤操作：

### Windows（推荐 MiKTeX）

1. **安装 MiKTeX**
   - 下载：https://miktex.org/download
   - 运行安装程序，保持默认选项即可
   - 首次编译时会自动下载缺失宏包

2. **安装 biber**
   - 打开 MiKTeX Console → Packages → 搜索 `biber` → 安装

3. **确认字体**
   - 本项目使用 **Times New Roman**（系统自带）、**SimSun / SimHei / KaiTi**（Windows 自带）
   - 如果字体缺失，`main.tex` 中的 `\setmainfont` 和 `\setCJKmainfont` 需要替换为已安装字体

4. **验证安装**
   ```bash
   xelatex --version
   biber --version
   ```

### macOS（推荐 MacTeX）

1. **安装 MacTeX**
   - 下载：https://www.tug.org/mactex/ （完整版约 5GB）
   - 或安装精简版 BasicTeX 后手动补包：
     ```bash
     brew install --cask basictex
     eval "$(/usr/libexec/path_helper)"
     sudo tlmgr update --self
     sudo tlmgr install ctex fontspec biblatex-apa biber booktabs tabularx enumitem longtable subcaption setspace ragged2e
     ```

2. **安装字体**
   - macOS 无 SimSun/SimHei，需替换 `main.tex` 中的 CJK 字体为系统已有字体，例如：
     ```latex
     \setCJKmainfont{Songti SC}[BoldFont=Heiti SC, ItalicFont=STKaiti]
     ```

### Linux（推荐 TeX Live）

```bash
# Ubuntu / Debian
sudo apt install texlive-full   # 完整安装（约 5GB）
# 或最小安装 + 按需补包
sudo apt install texlive-xetex texlive-lang-chinese texlive-bibtex-extra biber

# 验证
xelatex --version
biber --version
```

### VS Code 编辑（可选）

推荐安装以下扩展以获得 LaTeX 语法高亮和编译支持：

- **LaTeX Workshop**（搜索 `ms-vscode.latex-workshop`）
- 配置 `.vscode/settings.json`：
  ```json
  {
    "latex-workshop.latex.tools": [
      { "name": "xelatex", "command": "xelatex", "args": ["-synctex=1", "-interaction=nonstopmode", "%DOC%"] },
      { "name": "biber", "command": "biber", "args": ["%DOCFILE%"] }
    ],
    "latex-workshop.latex.recipes": [
      {
        "name": "xelatex -> biber -> xelatex x2",
        "tools": ["xelatex", "biber", "xelatex", "xelatex"]
      }
    ]
  }
  ```

---

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
