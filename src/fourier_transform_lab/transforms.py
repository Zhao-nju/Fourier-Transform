"""Core Fourier transform utilities."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


ComplexArray = NDArray[np.complex128]
FloatArray = NDArray[np.float64]


def _as_complex_vector(values: ArrayLike) -> ComplexArray:
    array = np.asarray(values, dtype=np.complex128)
    if array.ndim != 1:
        raise ValueError("Fourier transforms in this package expect a 1-D input.")
    if array.size == 0:
        raise ValueError("Input must contain at least one sample.")
    return array


def dft(values: ArrayLike) -> ComplexArray:
    """Compute the discrete Fourier transform directly in O(n^2) time."""
    x = _as_complex_vector(values)
    n = x.size
    indices = np.arange(n)
    exponent = -2j * np.pi * np.outer(indices, indices) / n
    return np.exp(exponent) @ x


def idft(values: ArrayLike) -> ComplexArray:
    """Compute the inverse discrete Fourier transform."""
    spectrum = _as_complex_vector(values)
    n = spectrum.size
    indices = np.arange(n)
    exponent = 2j * np.pi * np.outer(indices, indices) / n
    return (np.exp(exponent) @ spectrum) / n


def fft(values: ArrayLike) -> ComplexArray:
    """Compute a recursive FFT, falling back to direct DFT for odd lengths."""
    x = _as_complex_vector(values)
    n = x.size

    if n == 1:
        return x.copy()
    if n % 2 == 1:
        return dft(x)

    even = fft(x[::2])
    odd = fft(x[1::2])
    twiddle = np.exp(-2j * np.pi * np.arange(n // 2) / n) * odd
    return np.concatenate([even + twiddle, even - twiddle])


def ifft(values: ArrayLike) -> ComplexArray:
    """Compute the inverse FFT."""
    spectrum = _as_complex_vector(values)
    return np.conjugate(fft(np.conjugate(spectrum))) / spectrum.size


def fftfreq(n: int, d: float = 1.0) -> FloatArray:
    """Return DFT sample frequencies, matching NumPy's frequency-bin order."""
    if n <= 0:
        raise ValueError("n must be positive.")
    if d <= 0:
        raise ValueError("Sample spacing d must be positive.")

    positive_end = (n - 1) // 2 + 1
    negative_start = -(n // 2)
    bins = np.concatenate([np.arange(0, positive_end), np.arange(negative_start, 0)])
    return bins.astype(np.float64) / (n * d)


def power_spectrum(values: ArrayLike, sample_rate: float) -> tuple[FloatArray, FloatArray]:
    """Return non-negative frequencies and single-sided power spectrum."""
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive.")

    x = _as_complex_vector(values)
    spectrum = fft(x)
    freq = fftfreq(x.size, d=1.0 / sample_rate)
    mask = freq >= 0
    power = (np.abs(spectrum[mask]) ** 2) / x.size
    return freq[mask], power.astype(np.float64)


def convolution_fft(left: ArrayLike, right: ArrayLike) -> ComplexArray:
    """Compute a linear convolution using FFT zero-padding."""
    a = _as_complex_vector(left)
    b = _as_complex_vector(right)
    output_size = a.size + b.size - 1
    padded_size = 1 << (output_size - 1).bit_length()

    padded_a = np.zeros(padded_size, dtype=np.complex128)
    padded_b = np.zeros(padded_size, dtype=np.complex128)
    padded_a[: a.size] = a
    padded_b[: b.size] = b

    result = ifft(fft(padded_a) * fft(padded_b))
    return result[:output_size]

