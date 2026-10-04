"""Part 1 example: decompose a simple C major chord idea."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from fourier_transform_lab.plotting import set_english_plot_style


def main() -> None:
    sample_rate = 44_100
    duration = 0.04
    time = np.arange(0.0, duration, 1.0 / sample_rate)

    frequencies = {
        "C note": 261.6,
        "E note": 329.6,
        "G note": 392.0,
    }

    envelope = np.ones_like(time)
    fade_samples = int(0.006 * sample_rate)
    fade = np.linspace(0.0, 1.0, fade_samples)
    envelope[:fade_samples] = fade
    envelope[-fade_samples:] = fade[::-1]

    components = {
        name: envelope * np.sin(2 * np.pi * freq * time)
        for name, freq in frequencies.items()
    }
    chord = sum(components.values()) / len(components)

    set_english_plot_style()
    fig = plt.figure(figsize=(12, 6.2), constrained_layout=True)
    grid = fig.add_gridspec(3, 2, width_ratios=[1.0, 1.25])
    left_axes = [fig.add_subplot(grid[i, 0]) for i in range(3)]
    mixed_ax = fig.add_subplot(grid[:2, 1])
    chord_ax = fig.add_subplot(grid[2, 1])

    colors = ["#2563eb", "#dc2626", "#059669"]
    panel_labels = ["(a)", "(b)", "(c)"]
    for ax, (name, freq), color, label in zip(
        left_axes, frequencies.items(), colors, panel_labels, strict=True
    ):
        pressure = components[name]
        ax.plot(time * 1000, pressure, color=color, linewidth=1.5)
        ax.set_title(f"{label} {name}: {freq:.1f} Hz", color=color, pad=4)
        ax.set_ylim(-1.15, 1.15)
        ax.set_ylabel("Pressure")
        ax.grid(True, alpha=0.25)

    left_axes[-1].set_xlabel("Time (ms)")

    for (name, _), color in zip(frequencies.items(), colors, strict=True):
        mixed_ax.plot(time * 1000, components[name], color=color, linewidth=1.3, label=name)
    mixed_ax.set_title("(d) Three Signals Overlapped")
    mixed_ax.set_ylabel("Pressure")
    mixed_ax.legend(loc="upper right")
    mixed_ax.grid(True, alpha=0.25)

    chord_ax.plot(time * 1000, chord, color="#111827", linewidth=1.7)
    chord_ax.set_title("(e) Combined Chord Pressure")
    chord_ax.set_xlabel("Time (ms)")
    chord_ax.set_ylabel("Pressure")
    chord_ax.grid(True, alpha=0.25)

    output = Path("docs/figures/part01_chord.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
