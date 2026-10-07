# Part 4: Python 中的 `numpy.fft`

## 4.1 函数综述

<br>

做 Fourier analysis 时，最常用的工具是 NumPy 中的 `numpy.fft` 模块，具体细节可以参考https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html

### FFTs

| [`fft`](https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html#numpy.fft.fft)(a, n, axis, norm, out) | Compute the one-dimensional discrete Fourier Transform.      |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [`ifft`](https://numpy.org/doc/stable/reference/generated/numpy.fft.ifft.html#numpy.fft.ifft)(a, n, axis, norm, out) | Compute the one-dimensional inverse discrete Fourier Transform. |
| [`fft2`](https://numpy.org/doc/stable/reference/generated/numpy.fft.fft2.html#numpy.fft.fft2)(a, s, axes, norm, out) | Compute the 2-dimensional discrete Fourier Transform.        |
| [`ifft2`](https://numpy.org/doc/stable/reference/generated/numpy.fft.ifft2.html#numpy.fft.ifft2)(a, s, axes, norm, out) | Compute the 2-dimensional inverse discrete Fourier Transform. |
| [`fftn`](https://numpy.org/doc/stable/reference/generated/numpy.fft.fftn.html#numpy.fft.fftn)(a, s, axes, norm, out) | Compute the N-dimensional discrete Fourier Transform.        |
| [`ifftn`](https://numpy.org/doc/stable/reference/generated/numpy.fft.ifftn.html#numpy.fft.ifftn)(a, s, axes, norm, out) | Compute the N-dimensional inverse discrete Fourier Transform. |



### Real FFTs

包括rfft(a[, n, axis, norm, out]), irfft(a[, n, axis, norm, out]), rfft2等一系列函数

针对具有Hermitian symmetry的序列（i.e., a real spectrum.）具有hfft, hrfft函数




### Helper routines

| [`fftfreq`](https://numpy.org/doc/stable/reference/generated/numpy.fft.fftfreq.html#numpy.fft.fftfreq)(n, d, device) | Return the Discrete Fourier Transform sample frequencies.    |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [`rfftfreq`](https://numpy.org/doc/stable/reference/generated/numpy.fft.rfftfreq.html#numpy.fft.rfftfreq)(n, d, device) | Return the Discrete Fourier Transform sample frequencies (for usage with rfft, irfft). |
| [`fftshift`](https://numpy.org/doc/stable/reference/generated/numpy.fft.fftshift.html#numpy.fft.fftshift)(x, axes) | Shift the zero-frequency component to the center of the spectrum. |
| [`ifftshift`](https://numpy.org/doc/stable/reference/generated/numpy.fft.ifftshift.html#numpy.fft.ifftshift)(x, axes) | The inverse of [`fftshift`](https://numpy.org/doc/stable/reference/generated/numpy.fft.fftshift.html#numpy.fft.fftshift). |



##  4.2 numpy.fft.fft

- fft.**fft**(*a*, *n=None*, *axis=-1*, *norm=None*, *out=None*)

  This function computes the one-dimensional *n*-point discrete Fourier Transform (DFT).
  
  Parameters:
  
  * **a** array_likeInput array, can be complex.
  
  * **n** int, optional Length of the transformed axis of the output. .
  * **axis** int, optional Axis over which to compute the FFT. If not given, the last axis is used.
  * **norm**{“backward”, “ortho”, “forward”}, optional Normalization mode (see [`numpy.fft`](https://numpy.org/doc/stable/reference/routines.fft.html#module-numpy.fft)). Default is “backward”. Indicates which direction of the forward/backward pair of transforms is scaled and with what normalization factor.

​	Returns:

​	**out** complex ndarray



以下为1个简单的案例：

```python
q = np.array([8, 9, 9, 6, 10, 3, 5, 6])

f = np.fft.fft(q, norm='forward')
```



`np.fft.fft(x)` 返回的频率顺序不是从负频率到正频率，而是：
$$
0,\ 1,\ 2,\ldots,\frac{N}{2},\ -\frac{N}{2}+1,\ldots,-1
$$

对应的物理频率由 `np.fft.fftfreq` 给出：

```python
n = 8
freq = np.fft.fftfreq(len(f), d=1.0/8.0)
# 0.  1.  2.  3. -4. -3. -2. -1.
```



如果想画 two-sided spectrum，可以直接画：

```python
amplitude = np.abs(f) / len(f)

plt.plot(freq, amplitude)
```

不过这种图的频率顺序不适合直接阅读。常见做法是使用 `fftshift` 把负频率移动到左侧：

```python
freq_shifted = np.fft.fftshift(freq)
amplitude_shifted = np.fft.fftshift(amplitude)

plt.plot(freq_shifted, amplitude_shifted) # [-4., -3., -2., -1.,  0.,  1.,  2.,  3.]
```

这里的关键是：DFT frequency index 是周期性的，满足 $k\equiv k-N$。因此对于 $N=8$：

$$
7\equiv 7-8=-1.
$$

所以 $k=7$ 并不是高频信号，而是等价于 $k=-1$，也就是最低阶的负频率。真正达到 Nyquist frequency 的最高频率是 $k=4$。在 full two-sided `fftfreq` 里，Nyquist 项通常显示为 $-4$；在 one-sided `rfftfreq` 里，它显示为 $+4$。



## 4.3 实数信号：`rfft` 和 `rfftfreq`

<br>

大多数观测时间序列都是 real-valued signal。对于实数信号，负频率部分和正频率部分是共轭对称的，因此通常只需要看 non-negative frequencies。

这时可以使用：

```python
X = np.fft.rfft(x)
freq = np.fft.rfftfreq(len(x))
```

对于同一个实数序列，`np.fft.fft(x)` 和 `np.fft.rfft(x)` 在 non-negative frequency 上给出相同的 Fourier coefficients。区别只是：

- `fft` 返回完整的 two-sided result，包括正频率和负频率
- `rfft` 利用实数序列的 Hermitian symmetry，只返回 one-sided result

可以这样理解：

```python
X_full = np.fft.fft(x)
X_one = np.fft.rfft(x)

np.allclose(X_full[: len(X_one)], X_one)
```

对于 real-valued input，上面的结果应为 `True`。因此，`rfft` 不是另一种不同的 Fourier transform，而是 `fft` 在实数输入情形下的精简输出。

`rfft` 只返回：

$$
0\le f\le f_N,
$$

其中 $f_N$ 是 Nyquist frequency：

$$
f_N=\frac{1}{2\Delta t}.
$$

这就是 one-sided spectrum 的常用计算方式。



## 4.4 Amplitude spectrum

<br>

如果只想看每个频率成分的 amplitude，可以计算：

```python
X = np.fft.rfft(x)
freq = np.fft.rfftfreq(len(x), d=dt)

amplitude = np.abs(X) / len(x)
amplitude[1:-1] *= 2
```

这里乘以 2 的原因是：对于 real-valued signal，正频率和负频率原本共同贡献一个 real oscillation。使用 one-sided spectrum 时，我们把负频率那一半的贡献合并到正频率上。

需要注意：

- $f=0$ 是 mean，不乘以 2
- 如果 $N$ 为偶数，Nyquist frequency 也不乘以 2
- 中间频率乘以 2

所以代码中常见的 `amplitude[1:-1] *= 2` 适用于 $N$ 为偶数的情况。更严谨的写法是：

```python
amplitude = np.abs(X) / len(x)

if len(q) % 2 == 0:
    amplitude[1:-1] *= 2
else:
    amplitude[1:] *= 2
```



## 4.5 Power spectrum

<br>

Power spectrum 常用于表示不同频率对 variance 或 energy 的贡献。一个简单写法是：

```python
power = np.abs(f) ** 2

if len(q) % 2 == 0:
    power[1:-1] *= 2
else:
    power[1:] *= 2
```

在实际分析中，通常先去除均值：

```python
x_anom = x - np.mean(x)
```

否则 $f=0$ 处的 mean component 可能很大，会压低其它频率成分在图中的可见性。



## 4.6 Power spectral density

<br>

Power spectrum 和 power spectral density 不完全一样。

- power spectrum 表示每个 discrete frequency bin 上的 power
- power spectral density 表示单位频率上的 power

如果频率分辨率为：

$$
\Delta f=\frac{1}{N\Delta t},
$$

那么一种常见近似是：

```python
psd = power / (freq[1] - freq[0])
```

是否需要使用 power spectrum 或 power spectral density，取决于你想回答的问题：

- 比较不同频率 bin 的强弱：power spectrum 通常够用
- 比较不同采样长度或不同频率分辨率的数据：PSD 更合适



## 4.7 一个完整例子

<br>

下面的例子构造一个包含两个周期成分的 signal：

```python
import numpy as np
import matplotlib.pyplot as plt

dt = 0.05
t = np.arange(0, 20, dt)

x = (
    1.5 * np.sin(2 * np.pi * 0.5 * t)
    + 0.6 * np.sin(2 * np.pi * 2.0 * t)
)

x_anom = x - np.mean(x)

X = np.fft.rfft(x_anom)
freq = np.fft.rfftfreq(len(x_anom), d=dt)

amplitude = np.abs(X) / len(x_anom)
if len(x_anom) % 2 == 0:
    amplitude[1:-1] *= 2
else:
    amplitude[1:] *= 2

plt.plot(freq, amplitude)
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.xlim(0, 4)
plt.show()
```

图中应该能看到两个 peak，分别接近：

$$
f=0.5,\qquad f=2.0.
$$



## 4.8 常见问题

<br>

做 FFT 时最容易出错的是 frequency axis 和 normalization。

常见检查包括：

- 采样间隔 $\Delta t$ 是否正确传给 `fftfreq` 或 `rfftfreq`
- 是否需要先去除 mean 或 trend
- 是否应该画 one-sided spectrum，而不是 two-sided spectrum
- amplitude spectrum 是否正确处理了正负频率合并
- 记录长度是否足够，频率分辨率 $\Delta f=1/(N\Delta t)$ 是否满足需求
- 采样频率是否足够高，Nyquist frequency 是否覆盖目标频率
- 是否需要 window function 来降低 spectral leakage



## 4.9 小结

<br>

NumPy FFT 的核心函数：

- `np.fft.fft`: 计算完整 complex FFT
- `np.fft.fftfreq`: 生成完整频率轴
- `np.fft.fftshift`: 调整 two-sided spectrum 的显示顺序
- `np.fft.rfft`: 计算 real-valued signal 的 non-negative frequency FFT
- `np.fft.rfftfreq`: 生成 `rfft` 对应的频率轴

实际分析时最推荐的流程是：

1. 确认 $\Delta t$
2. 去均值或去趋势
3. 用 `rfft` 和 `rfftfreq` 计算 one-sided spectrum
4. 根据需求计算 amplitude、power 或 PSD
5. 结合物理背景解释谱峰和频率范围
