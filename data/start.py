from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def create_tip_visualizations() -> List[Path]:
    """Create basic visualizations from seaborn's 'tips' dataset and save images.

    Returns a list of saved file paths.
    """
    sns.set_theme(style="whitegrid", context="talk")

    output_dir = Path(__file__).resolve().parent / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)

    tips: pd.DataFrame = sns.load_dataset("tips").dropna()

    saved_paths: List[Path] = []

    def save_figure(fig: plt.Figure, filename: str) -> None:
        path = output_dir / filename
        fig.savefig(path, bbox_inches="tight", dpi=150)
        plt.close(fig)
        saved_paths.append(path)

    # 1) Scatter with regression line: total_bill vs tip
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(
        data=tips,
        x="total_bill",
        y="tip",
        ax=ax,
        scatter_kws={"alpha": 0.6, "s": 40},
        line_kws={"color": "crimson"},
    )
    ax.set_title("Tip vs Total Bill")
    ax.set_xlabel("Total Bill ($)")
    ax.set_ylabel("Tip ($)")
    save_figure(fig, "scatter_tip_vs_total_bill.png")

    # 2) Average tip by day (bar chart)
    tips_mean_by_day = (
        tips.groupby("day", as_index=False)["tip"].mean().sort_values("day")
    )
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=tips_mean_by_day, x="day", y="tip", ax=ax, color="#4C78A8")
    ax.set_title("Average Tip by Day")
    ax.set_xlabel("Day")
    ax.set_ylabel("Average Tip ($)")
    save_figure(fig, "bar_avg_tip_by_day.png")

    # 3) Correlation heatmap for numeric columns
    corr = tips.select_dtypes(include=["number"]).corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_title("Feature Correlation (Tips Dataset)")
    save_figure(fig, "heatmap_corr.png")

    return saved_paths


if __name__ == "__main__":
    paths = create_tip_visualizations()
    for p in paths:
        print(f"Saved: {p}")
