"""Qualitative coding helpers for the interview QA material."""

from __future__ import annotations

import pandas as pd


THEME_RULES = {
    "空间可见性与镜面凝视": ["镜子", "注视", "看", "公开", "可见"],
    "新手门槛与动作错误羞耻": ["动作不标准", "不会", "不懂", "新手", "慌", "器械"],
    "男性主导氛围与距离感": ["男生", "男性", "压迫", "男性化", "大重量"],
    "策略性协商而非彻底退出": ["人少", "朋友", "同伴", "早上", "不戴眼镜", "忽视"],
    "审美影响的有限性与多元化": ["社交媒体", "主流审美", "身材", "健康", "好看", "不认同"],
    "新手友好/女性友好干预需求": ["课程", "workshop", "分区", "指导", "女生", "零基础", "隔板"],
}


def code_interviews(interviews: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply keyword-assisted theme coding to interview answer segments."""
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
    """Select representative quotes used in the report tables."""
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
