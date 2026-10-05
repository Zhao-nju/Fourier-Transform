"""Part 2 example: spectrum of the Stull specific-humidity sequence."""

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


def main() -> None:
    q = np.array([8, 9, 9, 6, 10, 3, 5, 6], dtype=float)
    n_points = q.size
    n = np.arange(n_points)
    coeffs = np.fft.fft(q) / n_points
    amplitude = np.abs(coeffs)
    power = amplitude**2
    anomaly_coeffs = np.fft.fft(q - np.mean(q)) / n_points
    anomaly_power = np.abs(anomaly_coeffs) ** 2

    positive_n = np.arange(0, n_points // 2 + 1)

    set_english_plot_style()
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), constrained_layout=True)

    axes[0].stem(n, amplitude, linefmt="#2563eb", markerfmt="o", basefmt=" ")
    axes[0].axvline(n_points / 2, color="#dc2626", linestyle="--", linewidth=1.2, label="Nyquist")
    axes[0].set_title("Two-Sided Amplitude Spectrum")
    axes[0].set_xlabel("Frequency Index n")
    axes[0].set_ylabel("Amplitude")
    axes[0].set_xticks(n)
    axes[0].legend()
    axes[0].grid(True, alpha=0.25)

    axes[1].stem(positive_n, anomaly_power[positive_n], linefmt="#059669", markerfmt="s", basefmt=" ")
    axes[1].axvline(n_points / 2, color="#dc2626", linestyle="--", linewidth=1.2, label="Nyquist")
    axes[1].set_title("Power Spectrum After Mean Removal")
    axes[1].set_xlabel("Frequency Index n")
    axes[1].set_ylabel("Power")
    axes[1].set_xticks(positive_n)
    axes[1].legend()
    axes[1].grid(True, alpha=0.25)

    output = Path("docs/figures/part02_q_spectrum.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
