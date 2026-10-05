# Fourier Transform Lab

这是一个用于学习 Fourier transform 的教学项目，重点是用清晰的文字、公式和 Python 图示理解频率分解、DFT、连续 Fourier transform 和 `numpy.fft` 的使用。

This repository is a learning-oriented Fourier transform project. It is organized as a set of short tutorial parts rather than a standalone FFT package. The code is mainly used to reproduce figures, verify calculations, and support the explanations in the documents.

## Study Path

1. **Part 1: Introduction to Fourier transform**
2. **Part 2: Fourier transform of discrete sequences**
3. **Part 3: Continuous functions, Fourier transform, and spectrum**
4. **Part 4: Python usage with `numpy.fft`**
5. **Part 5: A simple atmospheric-science example**

Parts 1-4 have been substantially revised. Part 5 remains a simple application example that can be expanded later.

## Repository Structure

```text
fourier-transform-lab/
├── docs/
│   ├── figures/
│   │   ├── part01_chord.png
│   │   ├── part01_stull_842.png
│   │   ├── part02_q_spectrum.png
│   │   ├── part03_square_wave.png
│   │   └── part03_continuous_spectrum.png
│   ├── part01_intro.md
│   ├── part02_dft.md
│   ├── part03_function_ft.md
│   ├── part04_python_tools.md
│   └── part05_atmospheric_case.md
├── scripts/
│   ├── 1-chord.py
│   ├── 1-stull-842.py
│   ├── 2-spectrum.py
│   ├── 3-square-wave.py
│   ├── generate_demo.py
│   ├── part02_discrete_sequence.py
│   ├── part03_continuous_spectrum.py
│   └── part05_atmospheric_case.py
├── src/
│   ├── cli.py
│   ├── demo.py
│   ├── plotting.py
│   └── transforms.py
└── tests/
    └── test_transforms.py
```

## Part 1: Introduction

Entry document: [docs/part01_intro.md](docs/part01_intro.md)

Part 1 builds the basic intuition: a complex signal can be decomposed into simpler frequency components. It uses a C-major chord example and the Stull section 8.4.2 specific-humidity sequence to show how sine and cosine components reconstruct a signal.

Reproduce the figures:

```bash
PYTHONPATH=src conda run -n meteoro python scripts/1-chord.py
PYTHONPATH=src conda run -n meteoro python scripts/1-stull-842.py
```

## Part 2: Discrete Sequences and DFT

Entry document: [docs/part02_dft.md](docs/part02_dft.md)

Part 2 focuses on finite, discrete sequences. It explains why cosine terms alone cannot represent a general sequence, why sine terms are needed, how DFT coefficients are interpreted, how spectrum is defined, what Nyquist frequency means, and how sine/cosine functions act as frequency-space basis vectors.

Reproduce the spectrum figure:

```bash
PYTHONPATH=src conda run -n meteoro python scripts/2-spectrum.py
```

## Part 3: Continuous Functions and Spectrum

Entry document: [docs/part03_function_ft.md](docs/part03_function_ft.md)

Part 3 moves from Fourier series to continuous Fourier transform. It includes the square-wave harmonic expansion, the relationship between continuous functions and spectra, and the use of autocorrelation \(R(\tau)\) to understand spectrum in atmospheric turbulence.

Reproduce the figures:

```bash
PYTHONPATH=src conda run -n meteoro python scripts/3-square-wave.py
PYTHONPATH=src conda run -n meteoro python scripts/part03_continuous_spectrum.py
```

## Part 4: Python Usage with `numpy.fft`

Entry document: [docs/part04_python_tools.md](docs/part04_python_tools.md)

Part 4 explains how to use NumPy's FFT routines, including `fft`, `fftfreq`, `fftshift`, `rfft`, and `rfftfreq`. It also discusses two-sided and one-sided spectra, normalization with `norm="forward"` and `norm="backward"`, amplitude spectrum, power spectrum, and PSD.

## Part 5: Atmospheric Example

Entry document: [docs/part05_atmospheric_case.md](docs/part05_atmospheric_case.md)

Part 5 uses a synthetic near-surface temperature time series to show how Fourier spectrum can identify diurnal and synoptic-scale variability.

Reproduce the figure:

```bash
PYTHONPATH=src conda run -n meteoro python scripts/part05_atmospheric_case.py
```

## Run Tests

```bash
PYTHONPATH=src conda run -n meteoro python -m pytest
```

## Notes

- Figures use English labels, legends, and annotations.
- Plot fonts are set to Arial through `src/plotting.py`.
- `trial/` is ignored and is not intended for upload.
