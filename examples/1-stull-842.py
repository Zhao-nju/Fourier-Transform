"""Part 1 example: Stull section 8.4.2 discrete Fourier transform."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

from fourier_transform_lab.plotting import set_english_plot_style


def main() -> None:
    q = np.array([8, 9, 9, 6, 10, 3, 5, 6], dtype=float)
    n_points = q.size
    k = np.arange(n_points)
    k_fine = np.linspace(0, n_points, 900)

    coeffs = np.fft.fft(q) / n_points
    cosine_terms = {}
    sine_terms = {}
    for n in range(n_points):
        angle = 2 * np.pi * n * k_fine / n_points
        cosine_terms[f"cos n = {n}"] = coeffs[n].real * np.cos(angle)
        if n in [1, 3, 5, 7]:
            sine_terms[f"sin n = {n}"] = -coeffs[n].imag * np.sin(angle)

    cosine_sum = sum(cosine_terms.values())
    sine_sum = sum(sine_terms.values())
    reconstructed = cosine_sum + sine_sum

    set_english_plot_style()
    fig = plt.figure(figsize=(15.5, 9.2), constrained_layout=True)
    grid = fig.add_gridspec(8, 4, width_ratios=[1.0, 1.0, 1.15, 1.15])

    cosine_axes = [fig.add_subplot(grid[row, 0]) for row in range(n_points)]
    sine_axes = [fig.add_subplot(grid[start : start + 2, 1]) for start in range(0, 8, 2)]
    total_ax = fig.add_subplot(grid[2:6, 2:])

    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    for n, ax in enumerate(cosine_axes):
        contribution = cosine_terms[f"cos n = {n}"]
        amplitude = abs(coeffs[n].real)
        ax.plot(k_fine, contribution, color=colors[n % len(colors)], linewidth=1.25)
        ax.axhline(0, color="#111827", linewidth=0.7)
        ax.set_xlim(0, n_points)
        ax.set_title(f"cos n = {n}", fontsize=8.5, pad=1.5)
        if n == 0:
            ax.set_yticks([0, amplitude])
        else:
            ax.set_yticks([-amplitude, 0, amplitude])
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
        ax.grid(True, alpha=0.22)
        if n != n_points - 1:
            ax.tick_params(labelbottom=False)
        else:
            ax.set_xlabel("Index k")

    for ax, n in zip(sine_axes, [1, 3, 5, 7], strict=True):
        contribution = sine_terms[f"sin n = {n}"]
        amplitude = abs(coeffs[n].imag)
        ax.plot(k_fine, contribution, color=colors[n % len(colors)], linewidth=1.4)
        ax.axhline(0, color="#111827", linewidth=0.7)
        ax.set_xlim(0, n_points)
        ax.set_title(f"sin n = {n}", fontsize=9.5, pad=2)
        ax.set_yticks([-amplitude, 0, amplitude])
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
        ax.grid(True, alpha=0.22)
        if n != 7:
            ax.tick_params(labelbottom=False)
        else:
            ax.set_xlabel("Index k")

    total_ax.plot(k_fine, reconstructed, color="#111827", linewidth=1.9, label="Cosine + sine sum")
    total_ax.scatter(k, q, color="#dc2626", s=48, marker="s", label="Original data")
    total_ax.set_title("Total Reconstruction")
    total_ax.set_xlabel("Index k")
    total_ax.set_ylabel("q (g kg$^{-1}$)")
    total_ax.set_xlim(0, n_points)
    total_ax.set_ylim(2, 11)
    total_ax.legend(loc="upper right")
    total_ax.grid(True, alpha=0.25)

    output = Path("docs/figures/part01_stull_842.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
