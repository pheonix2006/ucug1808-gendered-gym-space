"""Rebuild project notebooks so they reflect the actual aggregate data workflow."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = ROOT / "notebooks"


def md(text: str):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text: str):
    return nbf.v4.new_code_cell(text.strip())


def write_notebook(filename: str, cells: list) -> None:
    nb = nbf.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3 (.venv via uv)",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    }
    nbf.write(nb, NOTEBOOK_DIR / filename)


COMMON_SETUP = """
import sys
from pathlib import Path

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(ROOT))

import pandas as pd
pd.set_option("display.max_colwidth", 120)
"""


def main() -> None:
    NOTEBOOK_DIR.mkdir(exist_ok=True)

    write_notebook(
        "01_data_overview.ipynb",
        [
            md("# 01 — 数据概览与清洗\n\n解析问卷平台导出的汇总 Excel，并确认真实样本量、题型和可分析的数据粒度。"),
            code(COMMON_SETUP),
            md("## 1. 解析问卷汇总导出"),
            code(
                """
from src.data_loader import parse_survey_export
from src.preprocessing import attach_slider_constructs

parsed = parse_survey_export(ROOT / "data" / "问卷原始数据.xlsx")
questions = parsed["questions"]
options = parsed["options"]
sliders = attach_slider_constructs(parsed["sliders"])

print(f"Questions: {len(questions)}")
display(questions.head(12))
"""
            ),
            md("## 2. 核心有效样本\n\n第 1、2 题为筛选题；第 3 题开始的核心样本为符合纳入条件的女性在校大学生。"),
            code(
                """
screening = questions[questions["q_num"].isin([1, 2, 3])]
display(screening[["q_num", "question", "valid_n"]])
print("Core analytic N =", int(questions.loc[questions["q_num"].eq(3), "valid_n"].iloc[0]))
"""
            ),
            md("## 3. 题项频数与缺失标记\n\n多选题导出中少数选项为空白，不能可靠地区分为 0 还是平台导出缺失；脚本保留 `count_status` 以免误读。单选题若只有一个选项缺失且总数可由有效样本推出，则标记为 `inferred_from_valid_n`。"),
            code(
                """
display(options[options["q_num"].isin([16, 17, 18])][["q_num", "option", "count", "pct", "count_status"]])
"""
            ),
            md("## 4. 保存结构化数据"),
            code(
                """
out_dir = ROOT / "data" / "processed"
out_dir.mkdir(parents=True, exist_ok=True)
questions.to_csv(out_dir / "survey_questions.csv", index=False, encoding="utf-8-sig")
options.to_csv(out_dir / "survey_options.csv", index=False, encoding="utf-8-sig")
sliders.to_csv(out_dir / "survey_slider_items.csv", index=False, encoding="utf-8-sig")
print(out_dir)
"""
            ),
        ],
    )

    write_notebook(
        "02_scale_analysis.ipynb",
        [
            md("# 02 — 量表/构念汇总\n\n当前问卷文件是汇总导出，不是逐名参与者作答矩阵。因此 Cronbach's alpha、McDonald's omega 和个体层面的量表总分不能从该文件计算。本 notebook 报告可由汇总数据支持的题项均值、构念均值和高分段比例。"),
            code(COMMON_SETUP),
            code(
                """
from src.data_loader import parse_survey_export
from src.preprocessing import attach_slider_constructs, construct_mean_summary
from src.analysis import slider_bin_agreement

parsed = parse_survey_export(ROOT / "data" / "问卷原始数据.xlsx")
sliders = attach_slider_constructs(parsed["sliders"])
agreement = slider_bin_agreement(parsed["options"]).merge(
    sliders[["q_num", "short_label", "construct", "mean"]],
    on="q_num",
    how="left",
)
constructs = construct_mean_summary(parsed["sliders"])
"""
            ),
            md("## 1. 滑动条题项均值"),
            code('display(sliders[["q_num", "short_label", "construct", "valid_n", "mean"]])'),
            md("## 2. 构念均值（题项均值的平均）"),
            code("display(constructs)"),
            md("## 3. 高分段比例\n\n高分段定义为平台导出的 3.5--4.2 与 4.3--5 两个分段之和。"),
            code('display(agreement[["q_num", "short_label", "mean", "low_pct", "mid_pct", "high_pct"]])'),
        ],
    )

    write_notebook(
        "03_descriptive_statistics.ipynb",
        [
            md("# 03 — 描述性统计与可视化\n\n生成论文需要的样本、健身房使用、回避原因和策略性应对图表。"),
            code(COMMON_SETUP),
            code(
                """
from src.data_loader import parse_survey_export
from src.analysis import frequency_table
from src.preprocessing import QUESTION_LABELS, attach_slider_constructs
from src.visualization import horizontal_frequency_plot, slider_distribution_plot

parsed = parse_survey_export(ROOT / "data" / "问卷原始数据.xlsx")
questions, options = parsed["questions"], parsed["options"]
sliders = attach_slider_constructs(parsed["sliders"])
fig_dir = ROOT / "report" / "figures"
fig_dir.mkdir(parents=True, exist_ok=True)
"""
            ),
            md("## 1. 人口与运动概况"),
            code(
                """
for q in [3, 4, 5, 7, 8, 9, 20]:
    print("\\nQ", q, questions.loc[questions["q_num"].eq(q), "question"].iloc[0])
    display(frequency_table(options, q))
"""
            ),
            md("## 2. 图表输出"),
            code(
                """
for q_num, filename, title in [
    (7, "gym_area_use.png", "最常使用的健身房区域"),
    (8, "strength_training_experience.png", "力量训练接触程度"),
    (16, "free_weight_avoidance.png", "主动避开自由重量区频率"),
    (17, "avoidance_reasons.png", "回避自由重量区的主要原因"),
    (18, "coping_strategies.png", "不自在时的应对策略"),
    (9, "exercise_goals.png", "当前主要运动目标"),
]:
    fig = horizontal_frequency_plot(frequency_table(options, q_num), title=title)
    fig.savefig(fig_dir / filename, dpi=200)

slider_options = options[options["kind"].eq("bin")]
for construct, frame in sliders.groupby("construct", dropna=True):
    q_nums = frame["q_num"].tolist()
    fig = slider_distribution_plot(
        slider_options[slider_options["q_num"].isin(q_nums)],
        QUESTION_LABELS,
        title=construct,
    )
    aliases = {
        "空间压迫/训练焦虑": "spatial_anxiety",
        "社交媒体审美内化": "media_internalization",
        "训练自我效能": "training_self_efficacy",
        "干预接受度": "intervention_acceptance",
    }
    fig.savefig(fig_dir / f"slider_{aliases.get(construct, construct)}.png", dpi=200)
    print(construct, q_nums)
"""
            ),
        ],
    )

    write_notebook(
        "04_inferential_analysis.ipynb",
        [
            md("# 04 — 研究问题整合分析\n\n本数据集不能进行个体层面的相关、t 检验或回归。本 notebook 以题项均值、高分段比例、多选频数和访谈主题进行研究问题层面的描述性整合。"),
            code(COMMON_SETUP),
            code(
                """
from src.data_loader import parse_survey_export
from src.analysis import frequency_table, slider_bin_agreement
from src.preprocessing import attach_slider_constructs, construct_mean_summary

parsed = parse_survey_export(ROOT / "data" / "问卷原始数据.xlsx")
questions, options = parsed["questions"], parsed["options"]
sliders = attach_slider_constructs(parsed["sliders"])
agreement = slider_bin_agreement(options).merge(
    sliders[["q_num", "short_label", "construct", "mean"]],
    on="q_num",
    how="left",
)
constructs = construct_mean_summary(parsed["sliders"])
"""
            ),
            md("## RQ1: 空间压迫与自由重量区回避"),
            code(
                """
display(constructs[constructs["construct"].eq("空间压迫/训练焦虑")])
display(agreement[agreement["construct"].eq("空间压迫/训练焦虑")][["q_num", "short_label", "mean", "high_pct"]])
display(frequency_table(options, 16))
display(frequency_table(options, 17))
"""
            ),
            md("## RQ2: 社交媒体审美内化与训练偏好"),
            code(
                """
display(constructs[constructs["construct"].eq("社交媒体审美内化")])
display(agreement[agreement["construct"].eq("社交媒体审美内化")][["q_num", "short_label", "mean", "high_pct", "low_pct"]])
display(frequency_table(options, 9))
"""
            ),
            md("## RQ3: 干预偏好与行动建议"),
            code(
                """
display(constructs[constructs["construct"].eq("干预接受度")])
display(agreement[agreement["construct"].eq("干预接受度")][["q_num", "short_label", "mean", "high_pct"]])
display(frequency_table(options, 18))
"""
            ),
        ],
    )

    write_notebook(
        "05_qualitative_analysis.ipynb",
        [
            md("# 05 — 质性主题分析\n\n解析 3 名受访者的 QA Markdown，并按空间可见性、新手门槛、男性主导氛围、策略性协商、审美影响和干预需求进行主题编码。"),
            code(COMMON_SETUP),
            code(
                """
from src.data_loader import load_interviews
from scripts.run_analysis import code_interviews, representative_quotes

interviews = load_interviews()
print(f"QA segments: {len(interviews)}")
display(interviews.head())
"""
            ),
            md("## 1. 主题编码摘要"),
            code(
                """
coded, theme_summary = code_interviews(interviews)
display(theme_summary)
"""
            ),
            md("## 2. 代表性引语"),
            code(
                """
quotes = representative_quotes(interviews)
display(quotes)
"""
            ),
            md("## 3. 保存质性输出"),
            code(
                """
out_dir = ROOT / "data" / "processed"
coded.to_csv(out_dir / "interview_coded.csv", index=False, encoding="utf-8-sig")
theme_summary.to_csv(out_dir / "interview_theme_summary.csv", index=False, encoding="utf-8-sig")
quotes.to_csv(out_dir / "interview_representative_quotes.csv", index=False, encoding="utf-8-sig")
print(out_dir)
"""
            ),
        ],
    )

    print("Notebooks rebuilt in", NOTEBOOK_DIR)


if __name__ == "__main__":
    main()
