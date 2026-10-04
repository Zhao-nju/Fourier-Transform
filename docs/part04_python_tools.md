# Part 4: Python 工具使用

Python 中最常用的 Fourier analysis 工具有：

- `numpy.fft`
- `scipy.fft`
- `matplotlib`
- `xarray` 和 `pandas`，用于处理带坐标的数据

本项目的 `fourier_transform_lab` 包提供教学实现，便于对照理解。

## 4.1 NumPy FFT 基本流程

```python
import numpy as np

sample_rate = 128.0
signal = ...

spectrum = np.fft.fft(signal)
freq = np.fft.fftfreq(signal.size, d=1.0 / sample_rate)
```

如果只看实数信号的非负频率，可使用：

```python
mask = freq >= 0
freq_pos = freq[mask]
power_pos = np.abs(spectrum[mask]) ** 2 / signal.size
```

## 4.2 本项目工具

```python
from fourier_transform_lab import fft, fftfreq, power_spectrum

spectrum = fft(signal)
freq = fftfreq(signal.size, d=1.0 / sample_rate)
freq_pos, power = power_spectrum(signal, sample_rate)
```

这些函数主要用于学习和小规模实验。大型科学计算建议使用 NumPy 或 SciPy。

## 4.3 常见注意事项

频谱分析中最常见的问题包括：

- 采样率不清楚，导致频率轴错误。
- 没有去除均值，导致 zero-frequency peak 过强。
- 序列长度太短，频率分辨率不足。
- 没有加窗，导致 spectral leakage。
- 混淆 amplitude spectrum 和 power spectrum。

## 4.4 推荐工作流

1. 检查采样间隔是否固定。
2. 去除均值或趋势。
3. 必要时加 window function。
4. 计算 FFT。
5. 建立正确频率轴。
6. 画单边谱或双边谱。
7. 用物理背景解释谱峰。

