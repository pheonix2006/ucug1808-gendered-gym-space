"""Data preprocessing and construct definitions for the project."""

import pandas as pd


SLIDER_CONSTRUCTS = {
    "空间压迫/训练焦虑": [10, 11, 12, 13, 14, 15],
    "社交媒体审美内化": [21, 22, 23],
    "训练自我效能": [24],
    "干预偏好指数": [25, 26, 27],
}

CONSTRUCT_SCORE_COLUMNS = {
    "空间压迫/训练焦虑": "spatial_pressure",
    "社交媒体审美内化": "media_internalization",
    "训练自我效能": "training_self_efficacy",
    "干预偏好指数": "intervention_preference",
}

QUESTION_LABELS = {
    10: "自由重量区不易接近",
    11: "男性较多时不自在",
    12: "镜子/公开可见增强被评价感",
    13: "担心动作不标准被评价",
    14: "自由重量区男性主导感",
    15: "拥挤感降低停留意愿",
    21: "审美内容影响运动选择",
    22: "担心力量训练不够纤细",
    23: "内化社交媒体女性身材标准",
    24: "健身房训练目标自我效能",
    25: "减少刻板印象会提升参与意愿",
    26: "半私密分区会提升使用意愿",
    27: "女性初学者workshop会提升尝试意愿",
}


def clean_survey(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning: drop duplicates, strip whitespace from string columns."""
    df = df.drop_duplicates()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    return df


def reverse_score(series: pd.Series, max_val: int = 5) -> pd.Series:
    """Reverse score a Likert series (1->5, 2->4, etc.)."""
    return max_val + 1 - series


def encode_ordinal(df: pd.DataFrame, mapping: dict[str, dict]) -> pd.DataFrame:
    """Encode ordinal columns using provided mapping dict."""
    for col, m in mapping.items():
        if col in df.columns:
            df[col] = df[col].map(m)
    return df


def compute_scale_score(
    df: pd.DataFrame,
    items: list[str],
    reverse_items: list[str] | None = None,
    max_val: int = 5,
) -> pd.Series:
    """Compute total/mean score for a scale, handling reverse-scored items."""
    subset = df[items].copy()
    if reverse_items:
        for item in reverse_items:
            if item in subset.columns:
                subset[item] = reverse_score(subset[item], max_val)
    return subset.mean(axis=1, skipna=True)


def attach_slider_constructs(sliders: pd.DataFrame) -> pd.DataFrame:
    """Attach readable item labels and construct names to slider summary rows."""
    out = sliders.copy()
    construct_lookup = {
        q_num: construct
        for construct, q_nums in SLIDER_CONSTRUCTS.items()
        for q_num in q_nums
    }
    out["construct"] = out["q_num"].map(construct_lookup)
    out["short_label"] = out["q_num"].map(QUESTION_LABELS).fillna(out["question"])
    return out


def construct_mean_summary(sliders: pd.DataFrame) -> pd.DataFrame:
    """Summarize constructs from item-level aggregate means.

    Because only aggregate item means are available, this returns construct
    mean-of-item-means and item ranges, not participant-level SDs.
    """
    enriched = attach_slider_constructs(sliders).dropna(subset=["construct"])
    summary = (
        enriched.groupby("construct")
        .agg(
            items=("q_num", lambda s: ", ".join(f"Q{int(x)}" for x in s)),
            item_count=("q_num", "count"),
            mean=("mean", "mean"),
            min_item_mean=("mean", "min"),
            max_item_mean=("mean", "max"),
            valid_n=("valid_n", "min"),
        )
        .reset_index()
    )
    return summary


def score_participant_constructs(df: pd.DataFrame, column_lookup) -> pd.DataFrame:
    """Compute participant-level construct scores from numbered survey columns."""
    scored = df.copy()
    for construct, q_nums in SLIDER_CONSTRUCTS.items():
        score_col = CONSTRUCT_SCORE_COLUMNS[construct]
        item_cols = [column_lookup(scored, q_num) for q_num in q_nums]
        scored[score_col] = scored[item_cols].mean(axis=1, skipna=True)
    return scored
