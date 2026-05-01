"""Visualization utilities for survey and qualitative data."""

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output" / "plots"

# Consistent style
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


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


def slider_distribution_plot(slider_options, labels, title: str = "") -> plt.Figure:
    """Stacked percentage bar chart for aggregate slider bins."""
    bins = ["1–1.8分", "1.9–2.6分", "2.7–3.4分", "3.5–4.2分", "4.3–5分"]
    plot_df = slider_options.pivot_table(
        index="q_num", columns="option", values="count", aggfunc="sum", fill_value=0
    ).reindex(columns=bins, fill_value=0)
    pct_df = plot_df.div(plot_df.sum(axis=1), axis=0) * 100
    pct_df.index = [labels.get(q, f"Q{q}") for q in pct_df.index]

    fig, ax = plt.subplots(figsize=(10, max(4, len(pct_df) * 0.55)))
    colors = ["#b2182b", "#ef8a62", "#f7f7f7", "#67a9cf", "#2166ac"]
    pct_df.plot(kind="barh", stacked=True, ax=ax, color=colors, edgecolor="white")
    ax.set_xlabel("百分比 (%)")
    ax.set_ylabel("")
    ax.set_xlim(0, 100)
    ax.set_title(title)
    ax.legend(title="滑动条分段", bbox_to_anchor=(1.02, 1), loc="upper left")
    return fig


def horizontal_frequency_plot(freq_df, title: str = "", xlabel: str = "百分比 (%)") -> plt.Figure:
    """Horizontal percentage bar chart for aggregate frequency tables."""
    frame = freq_df.dropna(subset=["pct"]).sort_values("pct")
    fig, ax = plt.subplots(figsize=(8, max(3.5, len(frame) * 0.45)))
    ax.barh(frame["option"], frame["pct"], color="#4c78a8")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("")
    ax.set_title(title)
    ax.set_xlim(0, max(100, frame["pct"].max() * 1.1 if len(frame) else 100))
    return fig
