# 随机数统计分布测试工具

这是一个用于生成和测试不同分布随机数的工具包。它提供了多种随机数生成方法，以及相应的统计检验和可视化功能，并支持批量生成标准格式的二进制随机数文件，便于使用专业工具（如国密/国产随机性评测工具箱）进行测评。同时，该工具还提供了详细的性能监控功能，帮助分析不同分布的性能特征。

## 功能特点

1. 随机数生成
   - 简单取模（Simple Modulo）
   - 均匀分布（Uniform）
   - 正态分布（Normal）
   - 指数分布（Exponential）
   - 泊松分布（Poisson）
   - 卡方分布（Chi-Square）
   - 混合分布（Mixed）

2. 统计检验
   - 均匀性检验
   - 独立性检验
   - 间隔分布检验
   - 游程检验
   - 熵检验

3. 可视化
   - 直方图
   - 箱线图
   - Q-Q图

4. 数据导出
   - 每个数的出现频率表（csv）
   - 每个数的间隔分布表（csv）
   - 各分布的标准格式二进制随机数文件（bin），可直接用于专业评测工具

5. 性能监控
   - 随机数生成耗时统计
   - 统计检验耗时统计
   - 内存使用监控
   - 性能瓶颈分析

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 统计分析与可视化

```bash
# 测试所有分布
python main.py

# 测试特定分布
python main.py --distribution normal

# 自定义参数
python main.py --N 1000 --count 50000 --distribution uniform --output results
```

参数说明：
- `--N`: 随机数范围上限（默认100）
- `--count`: 生成随机数的数量（默认10000）
- `--distribution`: 要测试的分布类型（默认"all"）
- `--output`: 输出目录（默认"output"）

支持的分布类型：
- simple: Simple Modulo
- uniform: Uniform
- normal: Normal
- exponential: Exponential
- poisson: Poisson
- chi_square: Chi-Square
- mixed: Mixed
- all: 所有分布

### 2. 批量生成标准格式的分布随机数bin文件

运行如下脚本即可：

```bash
python generate_all_distributions_bin.py
```

- 脚本会在当前目录下自动创建 `output_bin` 文件夹。
- 每种分布各生成一个128KB的二进制文件，文件名如：
  - `SimpleModulo.bin`
  - `Uniform.bin`
  - `Normal.bin`
  - `Exponential.bin`
  - `Poisson.bin`
  - `ChiSquare.bin`
  - `Mixed.bin`
- 文件内容为uint8类型的随机数，适用于国密/国产随机性评测工具箱。
- 可直接将这些文件复制到评测工具目录下进行批量测评。

### 3. 作为模块使用

```python
from random_generator import RandomGenerator
from visualization import DistributionVisualizer
from statistical_tests import StatisticalTester

generator = RandomGenerator()
visualizer = DistributionVisualizer(N=100, count=10000)
tester = StatisticalTester(N=100, count=10000)

numbers = generator.uniform_random(100, 10000)
results = tester.run_all_tests(numbers)
visualizer.plot_histograms("histogram.png")
visualizer.plot_boxplots("boxplot.png")
visualizer.plot_qq_plots("qq_plot.png")
```

## 输出说明

1. 统计检验结果
   - `{distribution}_test_results.txt`: 包含所有统计检验的详细结果
2. 可视化图表
   - `{distribution}_histogram.png`: 直方图
   - `{distribution}_boxplot.png`: 箱线图
   - `{distribution}_qq_plot.png`: Q-Q图
3. 数据表格
   - `{distribution}_frequency.csv`: 每个数的出现频率表
   - `{distribution}_gaps.csv`: 每个数的间隔分布表
4. 标准格式二进制文件
   - `output_bin/*.bin`: 各分布的128KB随机数文件

## 项目结构

```
.
├── main.py                        # 主程序
├── random_generator.py            # 随机数生成器
├── visualization.py               # 可视化工具
├── statistical_tests.py           # 统计检验工具
├── generate_all_distributions_bin.py # 批量生成分布随机数bin文件
├── requirements.txt               # 依赖包列表
├── README.md                      # 项目说明
└── output_bin/                    # 生成的bin文件目录
```

## 依赖包

- numpy
- scipy
- matplotlib
- seaborn
- pandas
- statsmodels
- psutil (用于性能监控)

## 专业工具测评说明

1. 运行 `generate_all_distributions_bin.py` 生成标准格式的随机数文件。
2. 将 `output_bin` 文件夹下的 `.bin` 文件复制到专业评测工具目录或者上传到随机数测试网站测评。

   （本人使用的是密评工具百宝箱https://tools.huijusa.cn/randomness进行随机测试）
3. 查看评测工具或测评网站输出的测试结果。

## 注意事项

1. 确保安装了所有必要的依赖包。
2. 文件大小和格式已适配主流国产/国密评测工具。
3. 输出目录会自动创建，如果已存在则会被覆盖。
4. 所有图表和结果文件使用UTF-8编码保存。

## 性能监控说明

运行脚本时，将显示以下性能信息：

1. 初始内存使用情况
2. 对于每种分布：
   - 随机数生成耗时
   - 随机数生成后的内存使用
   - 统计检验耗时
   - 统计检验后的内存使用
3. 可视化图表生成：
   - 生成耗时
   - 最终内存使用
   - 总内存增长
4. 内存使用最多的前3个代码位置

示例输出：
```
初始内存使用: 45.23 MB
测试均匀分布...
随机数生成耗时: 0.1234 秒
随机数生成后内存使用: 48.56 MB
统计检验耗时: 0.5678 秒
统计检验后内存使用: 52.34 MB
...
可视化图表生成耗时: 1.2345 秒
最终内存使用: 55.67 MB
总内存增长: 10.44 MB

内存使用最多的前3个位置:
123 blocks: 2.5 MB
  File "random_generator.py", line 45
456 blocks: 1.8 MB
  File "statistical_tests.py", line 78
789 blocks: 1.2 MB
  File "visualization.py", line 112
```

这些性能信息可以帮助：
- 比较不同分布生成随机数的效率
- 分析统计检验的计算开销
- 监控内存使用模式和增长情况
- 定位可能的性能瓶颈 