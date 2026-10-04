# Fourier Transform Lab

A small, readable Python project for learning and experimenting with Fourier transforms.

The package includes:

- A direct discrete Fourier transform (`dft`) and inverse transform (`idft`)
- A recursive Cooley-Tukey fast Fourier transform (`fft`) and inverse transform (`ifft`)
- Frequency-bin helpers, power spectrum calculation, and FFT-based convolution
- A demo script that generates a clean signal and spectrum figure
- Unit tests comparing the implementation against NumPy

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

If you use the `meteoro` conda environment:

```bash
conda run -n meteoro python -m pip install -e ".[dev]"
conda run -n meteoro python -m pytest
```

## Run the Demo

```bash
python -m fourier_transform_lab.cli --output outputs/demo_spectrum.png
```

The demo creates a two-tone signal, transforms it into frequency space, and saves a figure.

## Example

```python
import numpy as np
from fourier_transform_lab import fft, fftfreq, power_spectrum

sample_rate = 128.0
t = np.arange(0.0, 1.0, 1.0 / sample_rate)
signal = np.sin(2 * np.pi * 8 * t) + 0.5 * np.sin(2 * np.pi * 20 * t)

spectrum = fft(signal)
freq = fftfreq(signal.size, d=1.0 / sample_rate)
freq_psd, power = power_spectrum(signal, sample_rate)
```

## Project Layout

```text
fourier-transform-lab/
├── src/fourier_transform_lab/
│   ├── __init__.py
│   ├── cli.py
│   └── transforms.py
├── examples/
│   └── generate_demo.py
├── tests/
│   └── test_transforms.py
└── .github/workflows/tests.yml
```

## Development Notes

This project is intentionally compact. The direct DFT is useful for understanding the math, while the FFT is suitable for faster experiments on moderate-size signals. For production-scale signal processing, use `numpy.fft` or `scipy.fft`.

