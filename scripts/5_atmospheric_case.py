"""Part 5 example: TKE spectrum from 10 Hz eddy-covariance wind data."""

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


DATA_FILE = Path(
    "/Users/lanbo/code/turbulence/10Hz/FI-Sii_EC_20180706_L09_F02/data/"
    "FI-Sii_EC_201807061200_L09_F01.csv"
)
SAMPLE_RATE_HZ = 10.0


def load_wind_components(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    data = np.genfromtxt(
        path,
        delimiter=",",
        names=True,
        usecols=("U", "V", "W"),
        dtype=float,
        encoding=None,
    )
    u = np.asarray(data["U"], dtype=float)
    v = np.asarray(data["V"], dtype=float)
    w = np.asarray(data["W"], dtype=float)
    valid = np.isfinite(u) & np.isfinite(v) & np.isfinite(w)
    return u[valid], v[valid], w[valid]


def one_sided_psd_from_fft(x: np.ndarray, sample_rate: float) -> tuple[np.ndarray, np.ndarray]:
    n = x.size
    x_prime = x - np.mean(x)
    spectrum = np.fft.rfft(x_prime)
    freq = np.fft.rfftfreq(n, d=1.0 / sample_rate)
    psd = (np.abs(spectrum) ** 2) / (sample_rate * n)

    if n % 2 == 0:
        psd[1:-1] *= 2.0
    else:
        psd[1:] *= 2.0
    return freq, psd


def circular_autocovariance(x: np.ndarray) -> np.ndarray:
    x_prime = x - np.mean(x)
    spectrum = np.fft.fft(x_prime)
    return np.fft.ifft(np.abs(spectrum) ** 2).real / x_prime.size


def one_sided_psd_from_autocovariance(
    autocov: np.ndarray,
    sample_rate: float,
) -> tuple[np.ndarray, np.ndarray]:
    n = autocov.size
    freq = np.fft.rfftfreq(n, d=1.0 / sample_rate)
    psd = np.fft.rfft(autocov).real / sample_rate

    if n % 2 == 0:
        psd[1:-1] *= 2.0
    else:
        psd[1:] *= 2.0
    return freq, psd


def main() -> None:
    u, v, w = load_wind_components(DATA_FILE)
    n = min(u.size, v.size, w.size)
    u, v, w = u[:n], v[:n], w[:n]
    time = np.arange(n) / SAMPLE_RATE_HZ

    u_prime = u - np.mean(u)
    v_prime = v - np.mean(v)
    w_prime = w - np.mean(w)
    tke = 0.5 * np.mean(u_prime**2 + v_prime**2 + w_prime**2)

    freq, psd_u = one_sided_psd_from_fft(u, SAMPLE_RATE_HZ)
    _, psd_v = one_sided_psd_from_fft(v, SAMPLE_RATE_HZ)
    _, psd_w = one_sided_psd_from_fft(w, SAMPLE_RATE_HZ)
    tke_spectrum_fft = 0.5 * (psd_u + psd_v + psd_w)

    r_u = circular_autocovariance(u)
    r_v = circular_autocovariance(v)
    r_w = circular_autocovariance(w)
    r_tke = 0.5 * (r_u + r_v + r_w)
    freq_r, tke_spectrum_r = one_sided_psd_from_autocovariance(r_tke, SAMPLE_RATE_HZ)

    positive = freq > 0
    tau = np.arange(n) / SAMPLE_RATE_HZ
    lag_mask = tau <= 60.0

    set_english_plot_style()
    fig, axes = plt.subplots(3, 1, figsize=(9.5, 8.2), constrained_layout=True)

    axes[0].plot(time / 60.0, u_prime, color="#2563eb", linewidth=0.8, label="u'")
    axes[0].plot(time / 60.0, v_prime, color="#dc2626", linewidth=0.8, label="v'", alpha=0.85)
    axes[0].plot(time / 60.0, w_prime, color="#059669", linewidth=0.8, label="w'", alpha=0.85)
    axes[0].set_title("10 Hz Wind Velocity Fluctuations")
    axes[0].set_xlabel("Time (min)")
    axes[0].set_ylabel("Velocity (m s$^{-1}$)")
    axes[0].legend(ncol=3, frameon=False)
    axes[0].grid(True, alpha=0.25)

    axes[1].plot(tau[lag_mask], r_tke[lag_mask], color="#7c3aed", linewidth=1.7)
    axes[1].axhline(0.0, color="#111827", linewidth=0.8)
    axes[1].set_title("TKE Autocovariance")
    axes[1].set_xlabel("Lag (s)")
    axes[1].set_ylabel("$R_{TKE}(\\tau)$")
    axes[1].grid(True, alpha=0.25)

    axes[2].loglog(
        freq[positive],
        tke_spectrum_fft[positive],
        color="#111827",
        linewidth=1.8,
        label="Direct FFT",
    )
    axes[2].loglog(
        freq_r[positive],
        tke_spectrum_r[positive],
        color="#f97316",
        linewidth=1.2,
        linestyle="--",
        label="From autocovariance",
    )
    axes[2].set_title(f"TKE Spectrum (TKE = {tke:.3f} m$^2$ s$^{{-2}}$)")
    axes[2].set_xlabel("Frequency (Hz)")
    axes[2].set_ylabel("TKE Spectrum (m$^2$ s$^{-2}$ Hz$^{-1}$)")
    axes[2].legend(frameon=False)
    axes[2].grid(True, alpha=0.25, which="both")

    output = Path("docs/figures/part05_atmospheric_case.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
