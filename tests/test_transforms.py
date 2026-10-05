import numpy as np
import pytest

from transforms import convolution_fft, dft, fft, fftfreq, idft, ifft, power_spectrum


def test_dft_matches_numpy_fft() -> None:
    signal = np.array([1.0, 2.0, 0.5, -1.0, 3.0])
    np.testing.assert_allclose(dft(signal), np.fft.fft(signal), atol=1e-10)


def test_idft_recovers_signal() -> None:
    signal = np.array([1.0, -2.0, 0.5, 4.0])
    np.testing.assert_allclose(idft(dft(signal)), signal, atol=1e-10)


def test_fft_matches_numpy_for_even_and_odd_lengths() -> None:
    rng = np.random.default_rng(42)
    for n in [7, 8, 12, 16]:
        signal = rng.normal(size=n) + 1j * rng.normal(size=n)
        np.testing.assert_allclose(fft(signal), np.fft.fft(signal), atol=1e-10)


def test_ifft_recovers_signal() -> None:
    signal = np.array([0.0, 1.0, 0.0, -1.0, 2.0, 0.5, -0.25, 0.75])
    np.testing.assert_allclose(ifft(fft(signal)), signal, atol=1e-10)


def test_fftfreq_matches_numpy() -> None:
    for n in [5, 6, 8]:
        np.testing.assert_allclose(fftfreq(n, d=0.25), np.fft.fftfreq(n, d=0.25))


def test_power_spectrum_detects_known_frequency() -> None:
    sample_rate = 128.0
    time = np.arange(0.0, 1.0, 1.0 / sample_rate)
    signal = np.sin(2 * np.pi * 16 * time)
    freq, power = power_spectrum(signal, sample_rate)
    assert freq[np.argmax(power)] == pytest.approx(16.0)


def test_convolution_fft_matches_numpy_convolve() -> None:
    left = np.array([1.0, 2.0, 3.0])
    right = np.array([0.5, -1.0, 2.0])
    np.testing.assert_allclose(convolution_fft(left, right), np.convolve(left, right), atol=1e-10)


def test_empty_input_raises_value_error() -> None:
    with pytest.raises(ValueError):
        fft([])
