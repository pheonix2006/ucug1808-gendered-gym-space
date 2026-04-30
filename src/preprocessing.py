"""Data preprocessing: cleaning, encoding, reverse scoring for Likert scales."""

import pandas as pd
import numpy as np


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
