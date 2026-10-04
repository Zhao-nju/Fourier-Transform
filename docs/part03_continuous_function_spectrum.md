# Part 3: 连续函数的 FT 以及 Spectrum

连续 Fourier transform 处理的是连续函数 `f(t)`，其典型形式为：

```text
F(omega) = integral f(t) exp(-i omega t) dt
```

这里 `omega` 是角频率。也可以使用普通频率 `f`，两者关系为：

```text
omega = 2 pi f
```

## 3.1 连续 FT 和离散计算的关系

理论中的连续积分在计算机中必须离散化。常见做法是：

1. 选择一个有限时间区间。
2. 用固定采样间隔生成网格。
3. 用 DFT/FFT 近似连续 Fourier transform。

这会引入两个重要限制：

- 有限窗口会导致 spectral leakage。
- 有限采样率会限制可解析最高频率。

## 3.2 Amplitude Spectrum 和 Power Spectrum

Fourier 系数通常是复数，因此常见谱量包括：

- amplitude spectrum: `|F|`
- power spectrum: `|F|^2`
- power spectral density: 单位频率上的功率分布

在物理问题中，power spectrum 常用来描述能量在不同频率或尺度上的分布。

## 3.3 一个典型例子：Gaussian

Gaussian 函数的 Fourier transform 仍然是 Gaussian。这使它成为检验连续 FT 数值近似的好例子。

运行示例：

```bash
conda run -n meteoro python examples/part03_continuous_spectrum.py
```

输出图展示连续函数的采样结果及其数值 spectrum。

