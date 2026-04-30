"""Visualization utilities for survey and qualitative data."""

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output" / "plots"

# Consistent style
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.bbox"] = "tight"


def save_fig(fig: plt.Figure, filename: str) -> Path:
    """Save figure to output/plots/."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    fig.savefig(path)
    return path


def likert_barplot(
    df, items: list[str], labels: list[str] | None = None, title: str = ""
) -> plt.Figure:
    """Stacked bar plot for Likert-scale item distributions."""
    fig, ax = plt.subplots(figsize=(10, max(4, len(items) * 0.6)))
    counts = df[items].apply(lambda col: col.value_counts().sort_index())
    counts = counts.T.fillna(0)
    counts.plot(kind="barh", stacked=True, ax=ax, colormap="RdYlGn")
    ax.set_title(title)
    ax.set_xlabel("Count")
    if labels:
        ax.set_yticklabels(labels)
    return fig


def correlation_heatmap(
    corr_df, title: str = "Correlation Matrix", annot: bool = True
) -> plt.Figure:
    """Heatmap for correlation matrix."""
    fig, ax = plt.subplots(figsize=(8, 6))
    mask = None
    sns.heatmap(
        corr_df, mask=mask, annot=annot, fmt=".2f",
        cmap="coolwarm", center=0, ax=ax, square=True,
    )
    ax.set_title(title)
    return fig
