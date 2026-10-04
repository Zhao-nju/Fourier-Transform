"""Demo figure generation for the package CLI."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .plotting import set_english_plot_style
from .transforms import power_spectrum


def generate_demo(output_path: str | Path = "outputs/demo_spectrum.png") -> Path:
    sample_rate = 256.0
    duration = 1.0
    time = np.arange(0.0, duration, 1.0 / sample_rate)
    signal = (
        np.sin(2 * np.pi * 12 * time)
        + 0.45 * np.sin(2 * np.pi * 38 * time)
        + 0.15 * np.sin(2 * np.pi * 80 * time)
    )

    freq, power = power_spectrum(signal, sample_rate)

    set_english_plot_style()

    fig, axes = plt.subplots(2, 1, figsize=(9, 6), constrained_layout=True)

    axes[0].plot(time, signal, color="#2563eb", linewidth=1.8)
    axes[0].set_title("Time-Domain Signal")
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Amplitude")
    axes[0].grid(True, alpha=0.25)

    axes[1].stem(freq, power, linefmt="#dc2626", markerfmt="o", basefmt=" ")
    axes[1].set_xlim(0, 100)
    axes[1].set_title("Single-Sided Power Spectrum")
    axes[1].set_xlabel("Frequency (Hz)")
    axes[1].set_ylabel("Power")
    axes[1].grid(True, alpha=0.25)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path
