"""Part 2 example: Fourier transform of a discrete sequence."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from fourier_transform_lab import power_spectrum
from fourier_transform_lab.plotting import set_english_plot_style


def main() -> None:
    sample_rate = 64.0
    duration = 2.0
    time = np.arange(0.0, duration, 1.0 / sample_rate)
    signal = (
        1.0 * np.sin(2 * np.pi * 4 * time)
        + 0.6 * np.sin(2 * np.pi * 11 * time + 0.4)
        + 0.25 * np.cos(2 * np.pi * 19 * time)
    )

    freq, power = power_spectrum(signal, sample_rate)

    set_english_plot_style()
    fig, axes = plt.subplots(2, 1, figsize=(9, 6), constrained_layout=True)

    axes[0].plot(time, signal, color="#2563eb", linewidth=1.8)
    axes[0].scatter(time, signal, color="#111827", s=10, alpha=0.55)
    axes[0].set_title("Discrete Sample Sequence")
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Amplitude")
    axes[0].grid(True, alpha=0.25)

    axes[1].stem(freq, power, linefmt="#dc2626", markerfmt="o", basefmt=" ")
    axes[1].set_xlim(0, 32)
    axes[1].set_title("Power Spectrum from DFT")
    axes[1].set_xlabel("Frequency (Hz)")
    axes[1].set_ylabel("Power")
    axes[1].grid(True, alpha=0.25)

    output = Path("outputs/part02_discrete_sequence.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

