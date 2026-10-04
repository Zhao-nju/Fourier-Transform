"""Shared plotting helpers for examples."""

from __future__ import annotations

import matplotlib.pyplot as plt


def set_english_plot_style() -> None:
    """Use English-friendly default fonts and compact scientific styling."""
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "legend.fontsize": 10,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
        }
    )

