# Part 4: Python 中的 `numpy.fft`

实际做 Fourier analysis 时，最常用的工具是 NumPy 中的 `numpy.fft` 模块。Part 4 不再开发新的项目工具，而是专门说明如何使用 `numpy.fft`，以及如何解释它的输出。



## 4.1 基本流程

假设我们有一个等间隔采样的时间序列：

\[
x_0,x_1,\ldots,x_{N-1}.
\]

采样间隔为 \(\Delta t\)，采样频率为：

\[
f_s=\frac{1}{\Delta t}.
\]

用 NumPy 计算 FFT 的基本流程是：

```python
import numpy as np

dt = 0.25
t = np.arange(0, 64, dt)
x = np.sin(2 * np.pi * 0.5 * t)

X = np.fft.fft(x)
freq = np.fft.fftfreq(x.size, d=dt)
```

其中：

- `x` 是原始序列
- `X` 是 complex Fourier coefficients
- `freq` 是每个 Fourier coefficient 对应的 frequency
- `d=dt` 表示相邻采样点之间的间隔



## 4.2 `fft` 和 `fftfreq`

`np.fft.fft(x)` 返回的频率顺序不是从负频率到正频率，而是：

\[
0,\ 1,\ 2,\ldots,\frac{N}{2},\ -\frac{N}{2}+1,\ldots,-1
\]

对应的物理频率由 `np.fft.fftfreq` 给出：

```python
X = np.fft.fft(x)
freq = np.fft.fftfreq(len(x), d=dt)
```

如果想画 two-sided spectrum，可以直接画：

```python
amplitude = np.abs(X) / len(x)

plt.plot(freq, amplitude)
```

不过这种图的频率顺序不适合直接阅读。常见做法是使用 `fftshift` 把负频率移动到左侧：

```python
freq_shifted = np.fft.fftshift(freq)
amplitude_shifted = np.fft.fftshift(amplitude)

plt.plot(freq_shifted, amplitude_shifted)
```



## 4.3 实数信号：`rfft` 和 `rfftfreq`

大多数观测时间序列都是 real-valued signal。对于实数信号，负频率部分和正频率部分是共轭对称的，因此通常只需要看 non-negative frequencies。

这时可以使用：

```python
X = np.fft.rfft(x)
freq = np.fft.rfftfreq(len(x), d=dt)
```

`rfft` 只返回：

\[
0\le f\le f_N,
\]

其中 \(f_N\) 是 Nyquist frequency：

\[
f_N=\frac{1}{2\Delta t}.
\]

这就是 one-sided spectrum 的常用计算方式。



## 4.4 Amplitude spectrum

如果只想看每个频率成分的 amplitude，可以计算：

```python
X = np.fft.rfft(x)
freq = np.fft.rfftfreq(len(x), d=dt)

amplitude = np.abs(X) / len(x)
amplitude[1:-1] *= 2
```

这里乘以 2 的原因是：对于 real-valued signal，正频率和负频率原本共同贡献一个 real oscillation。使用 one-sided spectrum 时，我们把负频率那一半的贡献合并到正频率上。

需要注意：

- \(f=0\) 是 mean，不乘以 2
- 如果 \(N\) 为偶数，Nyquist frequency 也不乘以 2
- 中间频率乘以 2

所以代码中常见的 `amplitude[1:-1] *= 2` 适用于 \(N\) 为偶数的情况。更严谨的写法是：

```python
amplitude = np.abs(X) / len(x)

if len(x) % 2 == 0:
    amplitude[1:-1] *= 2
else:
    amplitude[1:] *= 2
```



## 4.5 Power spectrum

Power spectrum 常用于表示不同频率对 variance 或 energy 的贡献。一个简单写法是：

```python
X = np.fft.rfft(x)
freq = np.fft.rfftfreq(len(x), d=dt)

power = (np.abs(X) ** 2) / len(x) ** 2

if len(x) % 2 == 0:
    power[1:-1] *= 2
else:
    power[1:] *= 2
```

在实际分析中，通常先去除均值：

```python
x_anom = x - np.mean(x)
```

否则 \(f=0\) 处的 mean component 可能很大，会压低其它频率成分在图中的可见性。



## 4.6 Power spectral density

Power spectrum 和 power spectral density 不完全一样。

- power spectrum 表示每个 discrete frequency bin 上的 power
- power spectral density 表示单位频率上的 power

如果频率分辨率为：

\[
\Delta f=\frac{1}{N\Delta t},
\]

那么一种常见近似是：

```python
psd = power / (freq[1] - freq[0])
```

是否需要使用 power spectrum 或 power spectral density，取决于你想回答的问题：

- 比较不同频率 bin 的强弱：power spectrum 通常够用
- 比较不同采样长度或不同频率分辨率的数据：PSD 更合适



## 4.7 一个完整例子

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

\[
f=0.5,\qquad f=2.0.
\]



## 4.8 常见问题

做 FFT 时最容易出错的是 frequency axis 和 normalization。

常见检查包括：

- 采样间隔 \(\Delta t\) 是否正确传给 `fftfreq` 或 `rfftfreq`
- 是否需要先去除 mean 或 trend
- 是否应该画 one-sided spectrum，而不是 two-sided spectrum
- amplitude spectrum 是否正确处理了正负频率合并
- 记录长度是否足够，频率分辨率 \(\Delta f=1/(N\Delta t)\) 是否满足需求
- 采样频率是否足够高，Nyquist frequency 是否覆盖目标频率
- 是否需要 window function 来降低 spectral leakage



## 4.9 小结

NumPy FFT 的核心函数很少：

- `np.fft.fft`: 计算完整 complex FFT
- `np.fft.fftfreq`: 生成完整频率轴
- `np.fft.fftshift`: 调整 two-sided spectrum 的显示顺序
- `np.fft.rfft`: 计算 real-valued signal 的 non-negative frequency FFT
- `np.fft.rfftfreq`: 生成 `rfft` 对应的频率轴

实际分析时最推荐的流程是：

1. 确认 \(\Delta t\)
2. 去均值或去趋势
3. 用 `rfft` 和 `rfftfreq` 计算 one-sided spectrum
4. 根据需求计算 amplitude、power 或 PSD
5. 结合物理背景解释谱峰和频率范围
