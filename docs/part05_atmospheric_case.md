# Part 5: 大气科学简单应用案例

Fourier transformation 在大气科学中常用于识别不同时间尺度或空间尺度上的变化。

一个简单例子是近地面温度时间序列。它可能包含：

- 日变化，约 24 小时周期
- 天气尺度变化，约数天周期
- 高频噪声，来自局地扰动或观测误差

## 5.1 合成案例

本项目用合成温度序列演示：

```text
temperature = background + diurnal cycle + synoptic variation + noise
```

其中：

- diurnal cycle 对应 24 小时周期
- synoptic variation 对应 5 天周期
- noise 模拟小尺度随机扰动

## 5.2 频谱解释

做 Fourier analysis 后，power spectrum 中应出现接近以下周期的峰值：

- `24 h`
- `120 h`

这说明 Fourier spectrum 可以帮助我们从混合时间序列中识别主要周期。

## 5.3 运行示例

```bash
conda run -n meteoro python examples/part05_atmospheric_case.py
```

输出图包含时间序列和 period spectrum。图中文字为英文，便于直接用于报告。

## 5.4 后续可扩展方向

这个案例可以继续扩展为：

- 使用真实站点温度观测
- 使用 ERA5 再分析资料
- 对纬向风做频率谱分析
- 对二维空间场做 wave-number spectrum
- 对湍流速度做 energy spectrum

