"""Statistical analysis helpers.

Most classical inferential functions require participant-level data.  The
actual survey export currently available for this project is aggregate
frequency data, so aggregate-safe helpers are provided alongside the standard
functions.
"""

import pandas as pd
import numpy as np
from scipy import stats


def descriptive(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Compute descriptive statistics (M, SD, min, max, skew, kurtosis)."""
    cols = columns or df.select_dtypes(include="number").columns.tolist()
    sub = df[cols]
    result = sub.agg(["count", "mean", "std", "min", "max"]).T
    result["skew"] = sub.skew()
    result["kurtosis"] = sub.kurtosis()
    result.columns = ["N", "Mean", "SD", "Min", "Max", "Skew", "Kurtosis"]
    return result


def cronbach_alpha(df: pd.DataFrame, items: list[str]) -> float:
    """Compute Cronbach's alpha for a set of items."""
    data = df[items].dropna()
    k = len(items)
    if k < 2 or len(data) < 2:
        return np.nan
    item_vars = data.var(axis=0, ddof=1)
    total_var = data.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_vars.sum() / total_var)


def unavailable_for_aggregate(reason: str = "participant-level data are unavailable") -> float:
    """Return NaN for statistics that cannot be computed from aggregate exports."""
    return np.nan


def slider_bin_agreement(options: pd.DataFrame) -> pd.DataFrame:
    """Compute low/mid/high-bin percentages for slider items.

    The questionnaire platform exported sliders in five bins.  We treat the
    top two bins (3.5--5) as agreement/high endorsement and the bottom two
    bins (1--2.6) as disagreement/low endorsement.
    """
    bins = options[options["kind"].eq("bin")].copy()
    bins["count"] = pd.to_numeric(bins["count"], errors="coerce").fillna(0)
    totals = bins.groupby("q_num")["count"].transform("sum")
    bins["within_item_pct"] = np.where(totals > 0, bins["count"] / totals * 100, np.nan)
    low_labels = {"1–1.8分", "1.9–2.6分"}
    high_labels = {"3.5–4.2分", "4.3–5分"}
    grouped = []
    for q_num, frame in bins.groupby("q_num"):
        grouped.append(
            {
                "q_num": q_num,
                "low_pct": frame.loc[frame["option"].isin(low_labels), "within_item_pct"].sum(),
                "mid_pct": frame.loc[frame["option"].eq("2.7–3.4分"), "within_item_pct"].sum(),
                "high_pct": frame.loc[frame["option"].isin(high_labels), "within_item_pct"].sum(),
                "n": frame["count"].sum(),
            }
        )
    return pd.DataFrame(grouped)


def frequency_table(options: pd.DataFrame, q_num: int) -> pd.DataFrame:
    """Return a clean frequency table for one non-slider question."""
    cols = ["option", "count", "pct", "count_status"]
    out = options.loc[options["q_num"].eq(q_num), cols].copy()
    out["count"] = pd.to_numeric(out["count"], errors="coerce")
    out["pct"] = pd.to_numeric(out["pct"], errors="coerce")
    return out


def pearson_corr(x: pd.Series, y: pd.Series) -> tuple[float, float]:
    """Pearson correlation with p-value."""
    mask = x.notna() & y.notna()
    r, p = stats.pearsonr(x[mask], y[mask])
    return r, p


def point_biserial(x: pd.Series, y: pd.Series) -> tuple[float, float]:
    """Point-biserial correlation (x binary, y continuous)."""
    return pearson_corr(x, y)


def independent_ttest(
    group1: pd.Series, group2: pd.Series
) -> tuple[float, float]:
    """Independent samples t-test."""
    t, p = stats.ttest_ind(group1.dropna(), group2.dropna())
    return t, p


def chi_square_test(table: pd.crosstab) -> tuple[float, float, int]:
    """Chi-square test of independence. Returns chi2, p, dof."""
    chi2, p, dof, _ = stats.chi2_contingency(table)
    return chi2, p, dof
