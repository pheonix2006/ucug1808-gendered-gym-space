"""Run the project analysis from the available aggregate survey and interviews."""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.analysis import frequency_table, slider_bin_agreement
from src.data_loader import load_interviews, parse_survey_export
from src.preprocessing import QUESTION_LABELS, attach_slider_constructs, construct_mean_summary
from src.visualization import horizontal_frequency_plot, slider_distribution_plot

DATA_PROCESSED = ROOT / "data" / "processed"
REPORT_FIGURES = ROOT / "report" / "figures"
OUTPUT_TABLES = ROOT / "output" / "tables"


THEME_RULES = {
    "空间可见性与镜面凝视": ["镜子", "注视", "看", "公开", "可见"],
    "新手门槛与动作错误羞耻": ["动作不标准", "不会", "不懂", "新手", "慌", "器械"],
    "男性主导氛围与距离感": ["男生", "男性", "压迫", "男性化", "大重量"],
    "策略性协商而非彻底退出": ["人少", "朋友", "同伴", "早上", "不戴眼镜", "忽视"],
    "审美影响的有限性与多元化": ["社交媒体", "主流审美", "身材", "健康", "好看", "不认同"],
    "新手友好/女性友好干预需求": ["课程", "workshop", "分区", "指导", "女生", "零基础", "隔板"],
}


def ensure_dirs() -> None:
    for path in (DATA_PROCESSED, REPORT_FIGURES, OUTPUT_TABLES):
        path.mkdir(parents=True, exist_ok=True)


def remove_legacy_interview_outputs() -> None:
    """Remove old filenames from the earlier focus-group wording."""
    for directory in (DATA_PROCESSED, OUTPUT_TABLES):
        for path in directory.glob("focus_group_*.csv"):
            path.unlink(missing_ok=True)


def save_table(df: pd.DataFrame, name: str) -> None:
    df.to_csv(OUTPUT_TABLES / f"{name}.csv", index=False, encoding="utf-8-sig")


def safe_name(text: str) -> str:
    """Return a filesystem-safe compact name for generated assets."""
    aliases = {
        "空间压迫/训练焦虑": "spatial_anxiety",
        "社交媒体审美内化": "media_internalization",
        "训练自我效能": "training_self_efficacy",
        "干预接受度": "intervention_acceptance",
    }
    if text in aliases:
        return aliases[text]
    return (
        text.replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
        .replace("：", "_")
        .replace(":", "_")
    )


def code_interviews(interviews: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    coded_rows = []
    for _, row in interviews.iterrows():
        answer = row["answer"]
        themes = [
            theme
            for theme, keywords in THEME_RULES.items()
            if any(keyword in answer for keyword in keywords)
        ]
        if not themes:
            themes = ["其他背景信息"]
        for theme in themes:
            coded_rows.append({**row.to_dict(), "theme": theme})
    coded = pd.DataFrame(coded_rows)
    summary = (
        coded.groupby("theme")
        .agg(
            coded_segments=("answer", "count"),
            participants=("participant", lambda s: ", ".join(sorted(set(map(str, s))))),
        )
        .reset_index()
        .sort_values("coded_segments", ascending=False)
    )
    return coded, summary


def representative_quotes(interviews: pd.DataFrame) -> pd.DataFrame:
    selected = [
        ("空间可见性与镜面凝视", "1", 3),
        ("空间可见性与镜面凝视", "3", 4),
        ("新手门槛与动作错误羞耻", "3", 6),
        ("新手门槛与动作错误羞耻", "2", 15),
        ("男性主导氛围与距离感", "2", 16),
        ("策略性协商而非彻底退出", "1", 8),
        ("策略性协商而非彻底退出", "3", 7),
        ("审美影响的有限性与多元化", "2", 11),
        ("审美影响的有限性与多元化", "3", 8),
        ("新手友好/女性友好干预需求", "2", 17),
        ("新手友好/女性友好干预需求", "3", 12),
    ]
    rows = []
    for theme, participant, question_no in selected:
        match = interviews[
            interviews["participant"].astype(str).eq(participant)
            & interviews["question_no"].eq(question_no)
        ]
        if match.empty:
            continue
        record = match.iloc[0].to_dict()
        rows.append(
            {
                "theme": theme,
                "participant": f"P{participant}",
                "question_no": question_no,
                "quote": record["answer"],
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    ensure_dirs()
    remove_legacy_interview_outputs()

    parsed = parse_survey_export()
    questions = parsed["questions"]
    options = parsed["options"]
    sliders = attach_slider_constructs(parsed["sliders"])
    agreement = slider_bin_agreement(options).merge(
        sliders[["q_num", "question", "short_label", "construct", "mean"]],
        on="q_num",
        how="left",
    )
    constructs = construct_mean_summary(parsed["sliders"])

    questions.to_csv(DATA_PROCESSED / "survey_questions.csv", index=False, encoding="utf-8-sig")
    options.to_csv(DATA_PROCESSED / "survey_options.csv", index=False, encoding="utf-8-sig")
    sliders.to_csv(DATA_PROCESSED / "survey_slider_items.csv", index=False, encoding="utf-8-sig")
    agreement.to_csv(DATA_PROCESSED / "survey_slider_agreement.csv", index=False, encoding="utf-8-sig")
    constructs.to_csv(DATA_PROCESSED / "survey_construct_summary.csv", index=False, encoding="utf-8-sig")

    save_table(questions, "survey_questions")
    save_table(agreement, "survey_slider_agreement")
    save_table(constructs, "survey_construct_summary")
    for q_num, name in {
        3: "age",
        4: "exercise_frequency",
        5: "campus_gym_use",
        7: "gym_area_use",
        8: "strength_training_experience",
        9: "exercise_goals",
        16: "free_weight_avoidance",
        17: "avoidance_reasons",
        18: "coping_strategies",
        19: "social_media_platforms",
        20: "appearance_content_time",
        28: "qualitative_followup_willingness",
    }.items():
        save_table(frequency_table(options, q_num), name)

    slider_options = options[options["kind"].eq("bin")]
    for construct, frame in sliders.groupby("construct", dropna=True):
        q_nums = frame["q_num"].tolist()
        fig = slider_distribution_plot(
            slider_options[slider_options["q_num"].isin(q_nums)],
            QUESTION_LABELS,
            title=construct,
        )
        fig.savefig(REPORT_FIGURES / f"slider_{safe_name(construct)}.png", dpi=200)

    for q_num, filename, title in [
        (7, "gym_area_use.png", "最常使用的健身房区域"),
        (8, "strength_training_experience.png", "力量训练接触程度"),
        (16, "free_weight_avoidance.png", "主动避开自由重量区频率"),
        (17, "avoidance_reasons.png", "回避自由重量区的主要原因"),
        (18, "coping_strategies.png", "不自在时的应对策略"),
        (9, "exercise_goals.png", "当前主要运动目标"),
    ]:
        fig = horizontal_frequency_plot(frequency_table(options, q_num), title=title)
        fig.savefig(REPORT_FIGURES / filename, dpi=200)

    interviews = load_interviews()
    coded, theme_summary = code_interviews(interviews)
    quotes = representative_quotes(interviews)
    interviews.to_csv(DATA_PROCESSED / "interview_qa.csv", index=False, encoding="utf-8-sig")
    coded.to_csv(DATA_PROCESSED / "interview_coded.csv", index=False, encoding="utf-8-sig")
    theme_summary.to_csv(DATA_PROCESSED / "interview_theme_summary.csv", index=False, encoding="utf-8-sig")
    quotes.to_csv(DATA_PROCESSED / "interview_representative_quotes.csv", index=False, encoding="utf-8-sig")
    save_table(theme_summary, "interview_theme_summary")
    save_table(quotes, "interview_representative_quotes")

    print("Survey questions:", len(questions))
    print("Core valid N:", int(questions.loc[questions["q_num"].eq(3), "valid_n"].iloc[0]))
    print("\nConstruct summary")
    print(constructs.to_string(index=False))
    print("\nSlider high endorsement")
    print(agreement[["q_num", "short_label", "mean", "high_pct"]].to_string(index=False))
    print("\nQualitative themes")
    print(theme_summary.to_string(index=False))


if __name__ == "__main__":
    main()
