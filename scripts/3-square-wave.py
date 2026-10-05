"""Part 3 example: square wave reconstruction from odd sine harmonics."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def set_english_plot_style() -> None:
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


def square_wave_series(theta: np.ndarray, max_harmonic: int) -> np.ndarray:
    result = np.zeros_like(theta)
    for n in range(1, max_harmonic + 1, 2):
        result += np.sin(n * theta) / n
    return 4.0 * result / np.pi


def main() -> None:
    theta = np.linspace(-np.pi, np.pi, 1200)
    ideal = np.where(theta >= 0.0, 1.0, -1.0)

    harmonics = [1, 3, 7, 21]
    colors = ["#2563eb", "#dc2626", "#059669", "#7c3aed"]

    set_english_plot_style()
    fig, ax = plt.subplots(figsize=(8.2, 4.2), constrained_layout=True)

    ax.plot(theta, ideal, color="#111827", linewidth=2.0, label="Ideal square wave")

    for max_harmonic, color in zip(harmonics, colors, strict=True):
        reconstruction = square_wave_series(theta, max_harmonic)
        ax.plot(
            theta,
            reconstruction,
            linewidth=1.7,
            color=color,
            label=f"Odd harmonics up to n={max_harmonic}",
        )

    ax.set_title("Square Wave from Odd Sine Harmonics")
    ax.set_xlabel("Phase")
    ax.set_ylabel("Amplitude")
    ax.set_xlim(-np.pi, np.pi)
    ax.set_ylim(-1.45, 1.45)
    ax.set_xticks([-np.pi, -np.pi / 2, 0.0, np.pi / 2, np.pi])
    ax.set_xticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper left", frameon=False)

    output = Path("docs/figures/part03_square_wave.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
