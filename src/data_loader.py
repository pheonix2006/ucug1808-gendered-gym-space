"""Data loading utilities for the UCUG 1808 survey and interview data.

The survey file in ``data/`` is an aggregate export from the questionnaire
platform.  A later text-version export in ``data/processed/`` contains one
row per respondent, which supports exploratory participant-level scoring.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFAULT_SURVEY_FILE = DATA_DIR / "问卷原始数据.xlsx"
DEFAULT_PARTICIPANT_SURVEY_FILE = DATA_DIR / "processed" / "问卷数据_文本版.xlsx"
QUESTION_RE = re.compile(r"第\s*(\d+)\s*题[:：]\s*(.*?)\s*\[(.*?)\]\s*$", re.S)


def normalize_text(value: object) -> str:
    """Normalize questionnaire export text while keeping Chinese punctuation."""
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).replace("\xa0", " ")).strip()


def parse_number(value: object) -> float | None:
    """Parse a numeric value from the export; blank cells become ``None``."""
    text = normalize_text(value).replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_percent(value: object) -> float | None:
    """Parse a percent string such as ``59.38%`` as a 0--100 value."""
    text = normalize_text(value).replace("%", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def load_survey(filepath: str | None = None, header: int | None = None, **kwargs) -> pd.DataFrame:
    """Load the questionnaire export as a raw three-column DataFrame."""
    path = Path(filepath) if filepath else DEFAULT_SURVEY_FILE
    if path.suffix == ".xlsx":
        return pd.read_excel(path, header=header, **kwargs)
    return pd.read_csv(path, header=header, **kwargs)


def question_column(df: pd.DataFrame, q_num: int) -> str:
    """Return the participant-level column that starts with a question number."""
    prefix = f"{q_num}、"
    matches = [col for col in df.columns if isinstance(col, str) and col.startswith(prefix)]
    if not matches:
        raise KeyError(f"Question column Q{q_num} not found")
    return matches[0]


def option_column(df: pd.DataFrame, q_num: int, option_keyword: str) -> str:
    """Return a multi-select option column by question number and option text."""
    prefix = f"{q_num}、"
    matches = [
        col
        for col in df.columns
        if isinstance(col, str) and col.startswith(prefix) and option_keyword in col
    ]
    if not matches:
        raise KeyError(f"Option column Q{q_num} containing {option_keyword!r} not found")
    return matches[0]


def load_participant_survey(
    filepath: str | Path | None = None,
    core_only: bool = True,
    **kwargs,
) -> pd.DataFrame:
    """Load the participant-level text-version survey export.

    By default this returns the core analytic sample: respondents with Q3 age
    present, i.e. those who passed the student and gender screening questions.
    IP/source metadata remain in the raw Excel file but are not needed for
    scoring or reporting.
    """
    path = Path(filepath) if filepath else DEFAULT_PARTICIPANT_SURVEY_FILE
    df = pd.read_excel(path, **kwargs)
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].map(normalize_text)
    if core_only:
        age_col = question_column(df, 3)
        df = df[df[age_col].ne("") & df[age_col].notna()].copy()
    return df


def parse_survey_export(filepath: str | None = None) -> dict[str, pd.DataFrame]:
    """Parse the aggregate survey export into tidy tables.

    Returns
    -------
    dict
        ``questions``: one row per question.
        ``options``: one row per option/bin frequency.
        ``sliders``: one row per slider item with exported mean and total score.

    Notes
    -----
    The export contains aggregate frequencies only.  Participant-level
    reliability, correlation, t-test, and regression are therefore not
    recoverable from this file.
    """
    raw = load_survey(filepath=filepath)
    rows = raw.fillna("").values.tolist()
    questions: list[dict[str, object]] = []
    options: list[dict[str, object]] = []
    sliders: list[dict[str, object]] = []

    i = 0
    while i < len(rows):
        first = normalize_text(rows[i][0])
        match = QUESTION_RE.search(first)
        if not match:
            i += 1
            continue

        q_num = int(match.group(1))
        question = normalize_text(match.group(2))
        q_type = normalize_text(match.group(3))
        block_start = i
        i += 1
        block: list[list[object]] = []
        while i < len(rows):
            next_first = normalize_text(rows[i][0])
            if QUESTION_RE.search(next_first):
                break
            block.append(rows[i])
            i += 1

        valid_n = None
        total_score = None
        mean = None
        header_kind = "option"

        for row in block:
            cell = normalize_text(row[0])
            if cell.startswith("本题有效填写人次"):
                valid_n = parse_number(row[1])
            if "总分值" in cell and "平均值" in cell:
                total_match = re.search(r"总分值[:：]?\s*([0-9.]+)", cell)
                mean_match = re.search(r"平均值为[:：]?\s*([0-9.]+)", cell)
                total_score = float(total_match.group(1)) if total_match else None
                mean = float(mean_match.group(1)) if mean_match else None
            if cell == "分段":
                header_kind = "bin"

        option_rows: list[dict[str, object]] = []
        capture = False
        for row in block:
            label = normalize_text(row[0])
            if label in {"选项", "分段"}:
                capture = True
                header_kind = "bin" if label == "分段" else "option"
                continue
            if label.startswith("本题有效填写人次"):
                capture = False
                continue
            if not capture or not label or "总分值" in label:
                continue
            count = parse_number(row[1])
            pct = parse_percent(row[2])
            option_rows.append(
                {
                    "q_num": q_num,
                    "question": question,
                    "type": q_type,
                    "kind": header_kind,
                    "option": label,
                    "count": count,
                    "pct": pct,
                    "count_status": "reported" if count is not None else "missing",
                }
            )

        if q_type == "单选题" and valid_n is not None:
            missing = [row for row in option_rows if row["count"] is None]
            reported_total = sum(row["count"] or 0 for row in option_rows)
            if len(missing) == 1 and reported_total < valid_n:
                inferred = valid_n - reported_total
                missing[0]["count"] = inferred
                missing[0]["pct"] = inferred / valid_n * 100
                missing[0]["count_status"] = "inferred_from_valid_n"

        questions.append(
            {
                "q_num": q_num,
                "question": question,
                "type": q_type,
                "valid_n": valid_n,
                "total_score": total_score,
                "mean": mean,
                "source_row": block_start + 1,
            }
        )
        options.extend(option_rows)
        if q_type == "滑动条":
            sliders.append(
                {
                    "q_num": q_num,
                    "question": question,
                    "valid_n": valid_n,
                    "total_score": total_score,
                    "mean": mean,
                }
            )

    return {
        "questions": pd.DataFrame(questions),
        "options": pd.DataFrame(options),
        "sliders": pd.DataFrame(sliders),
    }


def load_interviews(filepath: str | None = None, **kwargs) -> pd.DataFrame:
    """Load parsed interview QA data from Markdown files or a CSV file."""
    if filepath:
        path = Path(filepath)
        if path.suffix.lower() == ".csv":
            return pd.read_csv(path, **kwargs)
        return parse_interview_markdown(path)

    frames = [
        parse_interview_markdown(path)
        for path in sorted(DATA_DIR.glob("采访对象_*_QA.md"))
    ]
    if not frames:
        return pd.DataFrame(columns=["participant", "question_no", "question", "answer", "source_file"])
    return pd.concat(frames, ignore_index=True)


def parse_interview_markdown(path: Path) -> pd.DataFrame:
    """Parse one interview Markdown file into question/answer rows."""
    text = path.read_text(encoding="utf-8-sig")
    participant_match = re.search(r"采访对象\s*[_ ]?(\d+)", path.stem)
    participant = participant_match.group(1) if participant_match else path.stem
    pattern = re.compile(
        r"\*\*Q(\d+)[:：](.*?)\*\*\s*\n\s*A[:：](.*?)(?=\n\s*\*\*Q\d+[:：]|\Z)",
        re.S,
    )
    records = []
    for match in pattern.finditer(text):
        records.append(
            {
                "participant": participant,
                "question_no": int(match.group(1)),
                "question": normalize_text(match.group(2)),
                "answer": normalize_text(match.group(3).strip()),
                "source_file": str(path),
            }
        )
    return pd.DataFrame(records)


def load_focus_group(filepath: str | None = None, **kwargs) -> pd.DataFrame:
    """Backward-compatible alias for the interview loader."""
    return load_interviews(filepath=filepath, **kwargs)


def parse_focus_group_markdown(path: Path) -> pd.DataFrame:
    """Backward-compatible alias for the interview Markdown parser."""
    return parse_interview_markdown(path)


def save_processed(df: pd.DataFrame, filename: str) -> Path:
    """Save processed DataFrame to data/processed/."""
    out = DATA_DIR / "processed" / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    return out
