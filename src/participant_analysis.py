"""Participant-level scoring helpers for the survey response matrix."""

from __future__ import annotations

import pandas as pd

from src.data_loader import option_column, question_column
from src.preprocessing import (
    CONSTRUCT_SCORE_COLUMNS,
    SLIDER_CONSTRUCTS,
    score_participant_constructs,
)


def build_participant_scores(participants: pd.DataFrame) -> pd.DataFrame:
    """Create a de-identified participant-level scoring table."""
    scored = score_participant_constructs(participants, question_column)
    avoidance_map = {"从未": 1, "很少": 2, "有时": 3, "经常": 4, "总是": 5}
    strength_col = question_column(scored, 8)
    scored["avoidance_frequency_score"] = scored[question_column(scored, 16)].map(avoidance_map)
    scored["free_weight_user"] = scored[option_column(scored, 7, "自由重量区")].eq("已选")
    scored["systematic_strength_training"] = scored[strength_col].isin(
        ["目前正在规律进行", "以前有规律进行过"]
    )

    keep = {
        "序号": "respondent_no",
        question_column(scored, 3): "age",
        question_column(scored, 4): "exercise_frequency",
        question_column(scored, 5): "campus_gym_use",
        strength_col: "strength_training_experience",
        question_column(scored, 16): "avoidance_frequency",
        "avoidance_frequency_score": "avoidance_frequency_score",
        "free_weight_user": "free_weight_user",
        "systematic_strength_training": "systematic_strength_training",
    }
    for score_col in CONSTRUCT_SCORE_COLUMNS.values():
        keep[score_col] = score_col
    return scored[list(keep)].rename(columns=keep)


def participant_item_columns(participants: pd.DataFrame) -> dict[str, list[str]]:
    """Map construct labels to participant-level item columns."""
    return {
        construct: [question_column(participants, q_num) for q_num in q_nums]
        for construct, q_nums in SLIDER_CONSTRUCTS.items()
    }
