"""Data loading utilities for survey and focus group data."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_survey(filepath: str | None = None, **kwargs) -> pd.DataFrame:
    """Load survey data from raw directory. Supports csv and xlsx."""
    path = Path(filepath) if filepath else DATA_DIR / "raw" / "survey.xlsx"
    if path.suffix == ".xlsx":
        return pd.read_excel(path, **kwargs)
    return pd.read_csv(path, **kwargs)


def load_focus_group(filepath: str | None = None, **kwargs) -> pd.DataFrame:
    """Load focus group transcription data."""
    path = Path(filepath) if filepath else DATA_DIR / "raw" / "focus_group.csv"
    return pd.read_csv(path, **kwargs)


def save_processed(df: pd.DataFrame, filename: str) -> Path:
    """Save processed DataFrame to data/processed/."""
    out = DATA_DIR / "processed" / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    return out
