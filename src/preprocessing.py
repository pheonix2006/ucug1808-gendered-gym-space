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

SLIDER_CONSTRUCTS_EN = {
    "空间压迫/训练焦虑": "Spatial Pressure / Training Anxiety",
    "社交媒体审美内化": "Social Media Appearance Internalization",
    "训练自我效能": "Training Self-Efficacy",
    "干预偏好指数": "Intervention Preference Index",
}

QUESTION_LABELS_EN = {
    10: "Free-weight area not easily accessible",
    11: "Uncomfortable when many men present",
    12: "Mirrors/open visibility increase evaluation",
    13: "Fear of incorrect form being judged",
    14: "Free-weight area feels male-dominated",
    15: "Crowding reduces willingness to stay",
    21: "Appearance content influences exercise choice",
    22: "Worry strength training won't look slender",
    23: "Internalize social media body standards",
    24: "Gym training goal self-efficacy",
    25: "Fewer stereotypes would increase participation",
    26: "Semi-private partitioning would increase use",
    27: "Women's beginner workshop would increase willingness",
}

OPTION_TRANSLATIONS = {
    # Q7 - Gym area use
    "跑步机/椭圆机等有氧区": "Treadmill/Elliptical (Cardio)",
    "拉伸/瑜伽区": "Stretching/Yoga Area",
    "固定器械区": "Fixed Machine Area",
    "自由重量区（哑铃、杠铃等）": "Free-Weight Area",
    "功能训练区": "Functional Training Area",
    "我基本不进入健身房": "Rarely Enter the Gym",
    # Q8 - Strength training experience
    "完全没有": "None at All",
    "有一点尝试，但不系统": "Some Unsyst. Attempts",
    "以前有规律进行过": "Previously Regular",
    "目前正在规律进行": "Currently Regular",
    # Q9 - Exercise goals
    "减脂/变瘦": "Fat Loss/Slimming",
    "塑形/线条": "Toning/Sculpting",
    "增强体能": "Improving Fitness",
    "提高力量": "Building Strength",
    "保持健康": "Maintaining Health",
    "缓解压力": "Stress Relief",
    "社交需求": "Social Needs",
    "其他 [详情]": "Other",
    # Q16 - Avoidance frequency
    "从未": "Never",
    "很少": "Rarely",
    "有时": "Sometimes",
    "经常": "Often",
    "总是": "Always",
    # Q17 - Avoidance reasons
    "男性太多": "Too Many Men",
    "不会使用器械": "Don't Know Equipment",
    "不知道从哪里开始": "Don't Know Where to Start",
    "没有同伴": "No Companion",
    "害怕动作出错": "Fear of Incorrect Form",
    "布局/氛围太有压迫感": "Layout/Atmosphere Too Intimidating",
    "不想练出明显肌肉": "Don't Want Visible Muscle",
    # Q18 - Coping strategies
    "选择人少的时间去": "Go During Off-Peak Hours",
    "只停留在有氧/固定器械区": "Stay in Cardio/Fixed Machines",
    "找朋友/同伴一起去": "Go with Friends/Companions",
    "放弃原本想做的力量训练": "Give Up Intended Strength Training",
    "离开健身房": "Leave the Gym",
    "其他": "Other",
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
