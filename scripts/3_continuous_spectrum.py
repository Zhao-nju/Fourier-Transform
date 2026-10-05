"""Part 3 example: numerical spectrum of a sampled continuous function."""

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
    n = 1024
    dt = 0.02
    time = (np.arange(n) - n // 2) * dt
    sigma = 0.45
    function = np.exp(-(time**2) / (2 * sigma**2))

    shifted = np.fft.ifftshift(function)
    spectrum = np.fft.fftshift(np.fft.fft(shifted)) * dt
    freq = np.fft.fftshift(np.fft.fftfreq(n, d=dt))
    amplitude = np.abs(spectrum)

    set_english_plot_style()
    fig, axes = plt.subplots(2, 1, figsize=(9, 6), constrained_layout=True)

    axes[0].plot(time, function, color="#2563eb", linewidth=2.0)
    axes[0].set_title("Sampled Gaussian Function")
    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("Amplitude")
    axes[0].grid(True, alpha=0.25)

    axes[1].plot(freq, amplitude, color="#dc2626", linewidth=2.0)
    axes[1].set_xlim(-6, 6)
    axes[1].set_title("Numerical Amplitude Spectrum")
    axes[1].set_xlabel("Frequency")
    axes[1].set_ylabel("Amplitude")
    axes[1].grid(True, alpha=0.25)

    output = Path("docs/figures/part03_continuous_spectrum.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
