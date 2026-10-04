# Part 2: 散点序列的 Fourier Transformation

实际数据通常不是连续函数，而是一串离散采样点：

```text
x[0], x[1], x[2], ..., x[N-1]
```

这些点可能来自传感器、模式输出、再分析资料或实验观测。对这种有限长度序列，使用 discrete Fourier transform, DFT。

## 2.1 DFT 定义

对长度为 `N` 的序列 `x[n]`，DFT 定义为：

```text
X[k] = sum_{n=0}^{N-1} x[n] exp(-i 2 pi k n / N)
```

其中：

- `n` 是原始序列索引
- `k` 是频率索引
- `X[k]` 是第 `k` 个频率 bin 上的复数系数

复数系数的模长表示该频率成分强弱，相位表示该频率成分相对原点的偏移。

## 2.2 频率轴

如果采样间隔是 `d` 秒，那么采样率是：

```text
sample_rate = 1 / d
```

频率分辨率为：

```text
delta_f = sample_rate / N
```

能够解析的最高频率是 Nyquist frequency：

```text
f_N = sample_rate / 2
```

这意味着采样率必须足够高，否则高频信号会 alias 到低频。

## 2.3 FFT 的角色

FFT 不是新的数学变换，而是 DFT 的快速算法。直接 DFT 复杂度是 `O(N^2)`，FFT 通常是 `O(N log N)`。

本项目保留了一个可读的 DFT 和递归 FFT 实现，方便理解数学结构；正式科学计算时可使用 `numpy.fft` 或 `scipy.fft`。

## 2.4 运行示例

```bash
conda run -n meteoro python examples/part02_discrete_sequence.py
```

该脚本生成一个由多个正弦波叠加而成的离散序列，并画出单边功率谱。图中所有文本均为英文。

