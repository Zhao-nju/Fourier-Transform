# Fourier Transform Lab

这是一个面向学习、展示和复现实验的 Fourier transform GitHub 项目。

项目主线不是单纯封装一个 FFT 工具包，而是围绕五个循序渐进的 part 组织：

1. **Fourier transform 简介**
2. **散点序列的 Fourier transform**
3. **连续函数的 FT 以及 spectrum**
4. **Python 工具使用**
5. **大气科学简单应用案例**

代码层只承担支撑作用：提供可读的 DFT/FFT 实现、频率轴计算、功率谱计算和示例图生成。文档层负责解释概念、公式、物理意义和应用场景。

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

## Study Path

### Part 1: Fourier Transform 简介

目标是建立直觉：Fourier transform 将信号从“时间/空间域”改写到“频率/波数域”，回答一个核心问题：

> 一个复杂变化中，包含哪些周期或尺度的成分？

这一部分从 do-mi-sol 三和弦开始，说明复杂声音可以看成多个 pressure signals 的叠加；随后用 Stull 第 8.4.2 节的比湿序列例子，展示离散信号如何由 cosine 和 sine 成分重建。

入口文档：[docs/part01_intro.md](docs/part01_intro.md)

运行示例：

```bash
PYTHONPATH=src conda run -n meteoro python scripts/1-chord.py
PYTHONPATH=src conda run -n meteoro python scripts/1-stull-842.py
```

### Part 2: 散点序列的 Fourier Transform

这一部分讨论有限长度、离散采样序列的 DFT。主线从一个问题开始：

> 为什么只用 cosine 不能表示一般离散序列，为什么还需要 sine？

随后引入 DFT 公式、周期延拓、Fourier coefficient、spectrum、Nyquist frequency，以及 cosine/sine 作为 frequency basis 的线性代数解释。最后通过 Stull 比湿序列画出 amplitude spectrum 和去均值后的 power spectrum。

入口文档：[docs/part02_dft.md](docs/part02_dft.md)

运行示例：

```bash
PYTHONPATH=src conda run -n meteoro python scripts/2-spectrum.py
```

### Part 3: 连续函数的 FT 以及 Spectrum

这里从连续函数出发，解释 Fourier series、continuous Fourier transform、correlation function、amplitude spectrum 和 power spectrum 的物理意义。

入口文档：[docs/part03_function_ft.md](docs/part03_function_ft.md)

运行示例：

```bash
PYTHONPATH=src conda run -n meteoro python scripts/3-square-wave.py
PYTHONPATH=src conda run -n meteoro python scripts/part03_continuous_spectrum.py
```

### Part 4: Python 工具使用

这一部分说明如何用 `numpy.fft` 完成基础频谱分析，并解释常见问题：频率轴、归一化、单边谱、采样率、窗函数和去趋势。

入口文档：[docs/part04_python_tools.md](docs/part04_python_tools.md)

### Part 5: 大气科学简单应用案例

用合成气象时间序列做一个小案例：温度变化中包含日变化、天气尺度变化和噪声。通过 Fourier spectrum 识别主要周期。

入口文档：[docs/part05_atmospheric_case.md](docs/part05_atmospheric_case.md)

运行示例：

```bash
PYTHONPATH=src conda run -n meteoro python scripts/part05_atmospheric_case.py
```

## Run Tests

```bash
PYTHONPATH=src conda run -n meteoro python -m pytest
```

## Notes

- 文档和图是这个项目的主体，代码主要用于复现图和检查计算。
- 所有示例图的标题、坐标轴、图例和标注均使用英文，并设置 Arial 字体。
- 当前 Part 1 和 Part 2 已完成主要内容整理，后续可以继续细化 Part 3-5。
