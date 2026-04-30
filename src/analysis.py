"""Statistical analysis: descriptive stats, reliability, correlation, regression."""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats import reliability as sm_rel


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
