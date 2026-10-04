# Fourier Transform Lab

这是一个面向学习、展示和复现实验的 Fourier transformation GitHub 项目。

项目主线不是单纯封装一个 FFT 工具包，而是围绕五个循序渐进的 part 组织：

1. **Fourier transformation 简介**
2. **散点序列的 Fourier transformation**
3. **连续函数的 FT 以及 spectrum**
4. **Python 工具使用**
5. **大气科学简单应用案例**

代码层只承担支撑作用：提供可读的 DFT/FFT 实现、频率轴计算、功率谱计算和示例图生成。文档层负责解释概念、公式、物理意义和应用场景。

## Repository Structure

```text
fourier-transform-lab/
├── docs/
│   ├── part01_intro.md
│   ├── part02_discrete_sequence.md
│   ├── part03_continuous_function_spectrum.md
│   ├── part04_python_tools.md
│   └── part05_atmospheric_case.md
├── examples/
│   ├── generate_demo.py
│   ├── part02_discrete_sequence.py
│   ├── part03_continuous_spectrum.py
│   └── part05_atmospheric_case.py
├── src/fourier_transform_lab/
│   ├── __init__.py
│   ├── cli.py
│   ├── demo.py
│   ├── plotting.py
│   └── transforms.py
├── tests/
│   └── test_transforms.py
└── .github/workflows/tests.yml
```

## Study Path

### Part 1: Fourier Transformation 简介

目标是建立直觉：Fourier transformation 将信号从“时间/空间域”改写到“频率/波数域”，回答一个核心问题：

> 一个复杂变化中，包含哪些周期或尺度的成分？

入口文档：[docs/part01_intro.md](docs/part01_intro.md)

### Part 2: 散点序列的 Fourier Transformation

这里讨论真实数据中最常见的形式：有限长度、离散采样的序列。重点包括 DFT、FFT、频率 bin、采样间隔、Nyquist frequency 和谱峰解释。

入口文档：[docs/part02_discrete_sequence.md](docs/part02_discrete_sequence.md)

运行示例：

```bash
conda run -n meteoro python examples/part02_discrete_sequence.py
```

### Part 3: 连续函数的 FT 以及 Spectrum

这里从连续函数出发，解释连续 Fourier transform、数值离散化近似、amplitude spectrum、power spectrum 和 Parseval 关系的物理意义。

入口文档：[docs/part03_continuous_function_spectrum.md](docs/part03_continuous_function_spectrum.md)

运行示例：

```bash
conda run -n meteoro python examples/part03_continuous_spectrum.py
```

### Part 4: Python 工具使用

这一部分说明如何用 `numpy.fft`、本项目的教学实现和 Matplotlib 完成基础频谱分析，并解释常见坑：频率轴、归一化、单边谱、采样率、窗函数和去趋势。

入口文档：[docs/part04_python_tools.md](docs/part04_python_tools.md)

### Part 5: 大气科学简单应用案例

用合成气象时间序列做一个小案例：温度变化中包含日变化、天气尺度变化和噪声。通过 Fourier spectrum 识别主要周期。

入口文档：[docs/part05_atmospheric_case.md](docs/part05_atmospheric_case.md)

运行示例：

```bash
conda run -n meteoro python examples/part05_atmospheric_case.py
```

## Install and Test

```bash
conda run -n meteoro python -m pip install -e ".[dev]"
conda run -n meteoro python -m pytest
```

也可以使用普通 Python 环境：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Generate the Demo Figure

```bash
conda run -n meteoro python -m fourier_transform_lab.cli --output docs/figures/demo_spectrum.png
```

所有示例图的标题、坐标轴、图例和标注均使用英文，并设置 Arial 字体，便于论文、报告或课程展示中复用。

## Project Scope

这个仓库适合用来做：

- Fourier transformation 入门项目
- 课程展示材料
- 气象/大气科学中频谱分析的最小示例
- Python FFT 工具使用模板

如果后续要扩展，可以继续加入：

- notebook 版本讲义
- 真实观测数据案例
- 2-D Fourier transform 和空间谱分析
- turbulence energy spectrum 示例
- wavelet transform 对比章节
