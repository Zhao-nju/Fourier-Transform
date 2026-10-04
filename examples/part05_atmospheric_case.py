"""Part 5 example: a simple atmospheric time-series spectrum."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from fourier_transform_lab import power_spectrum
from fourier_transform_lab.plotting import set_english_plot_style


def main() -> None:
    rng = np.random.default_rng(2026)
    sample_interval_hours = 1.0
    total_days = 20
    hours = np.arange(0.0, total_days * 24.0, sample_interval_hours)

    background = 285.0
    diurnal = 4.0 * np.sin(2 * np.pi * hours / 24.0 - 0.8)
    synoptic = 2.5 * np.sin(2 * np.pi * hours / (5.0 * 24.0) + 0.5)
    noise = rng.normal(0.0, 0.7, size=hours.size)
    temperature = background + diurnal + synoptic + noise

    anomaly = temperature - np.mean(temperature)
    sample_rate_per_hour = 1.0 / sample_interval_hours
    freq, power = power_spectrum(anomaly, sample_rate_per_hour)

    valid = freq > 0
    period_hours = 1.0 / freq[valid]
    period_power = power[valid]
    order = np.argsort(period_hours)

    set_english_plot_style()
    fig, axes = plt.subplots(2, 1, figsize=(9, 6), constrained_layout=True)

    axes[0].plot(hours / 24.0, temperature, color="#2563eb", linewidth=1.5)
    axes[0].set_title("Synthetic Near-Surface Temperature")
    axes[0].set_xlabel("Time (days)")
    axes[0].set_ylabel("Temperature (K)")
    axes[0].grid(True, alpha=0.25)

    axes[1].plot(period_hours[order], period_power[order], color="#dc2626", linewidth=1.8)
    axes[1].axvline(24, color="#111827", linestyle="--", linewidth=1.0, label="24 h")
    axes[1].axvline(120, color="#059669", linestyle="--", linewidth=1.0, label="120 h")
    axes[1].set_xscale("log")
    axes[1].set_xlim(4, 300)
    axes[1].set_title("Period Spectrum")
    axes[1].set_xlabel("Period (hours)")
    axes[1].set_ylabel("Power")
    axes[1].legend()
    axes[1].grid(True, alpha=0.25, which="both")

    output = Path("outputs/part05_atmospheric_case.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

