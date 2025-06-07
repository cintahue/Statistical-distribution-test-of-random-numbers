import argparse
from random_generator import RandomGenerator
from visualization import DistributionVisualizer
from statistical_tests import StatisticalTester
import os
import numpy as np
import csv
import time
import psutil
import tracemalloc

def get_memory_usage():
    """获取当前进程的内存使用情况"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # 转换为MB

def create_output_dir():
    """创建输出目录"""
    if not os.path.exists("output"):
        os.makedirs("output")

def save_frequency_table(numbers, N, save_path):
    counts = np.bincount(numbers, minlength=N)
    total = len(numbers)
    with open(save_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Value", "Count", "Frequency"])
        for i in range(N):
            writer.writerow([i, counts[i], counts[i] / total])

def save_gap_table(numbers, N, save_path):
    last_pos = dict()
    gaps_dict = {i: [] for i in range(N)}
    for idx, num in enumerate(numbers):
        if num in last_pos:
            gap = idx - last_pos[num]
            gaps_dict[num].append(gap)
        last_pos[num] = idx
    with open(save_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Value", "Gaps"])
        for i in range(N):
            gap_str = ','.join(str(g) for g in gaps_dict[i])
            writer.writerow([i, gap_str])

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="随机数统计分布测试工具")
    parser.add_argument("--N", type=int, default=100, help="随机数范围上限")
    parser.add_argument("--count", type=int, default=10000, help="生成随机数的数量")
    parser.add_argument("--distribution", type=str, default="all",
                      choices=["simple", "uniform", "normal", "exponential", "poisson", "chi_square", "mixed", "all"],
                      help="要测试的分布类型")
    parser.add_argument("--output", type=str, default="output", help="输出目录")
    args = parser.parse_args()
    
    # 初始化内存跟踪
    tracemalloc.start()
    initial_memory = get_memory_usage()
    print(f"初始内存使用: {initial_memory:.2f} MB")
    
    # 创建输出目录
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # 创建生成器、可视化器和测试器实例
    generator = RandomGenerator()
    visualizer = DistributionVisualizer(args.N, args.count)
    tester = StatisticalTester(args.N, args.count)
    
    # 确定要测试的分布
    distributions = {
        "simple": ("简单取模", generator.simple_random),
        "uniform": ("均匀分布", generator.uniform_random),
        "normal": ("正态分布", generator.normal_random),
        "exponential": ("指数分布", generator.exponential_random),
        "poisson": ("泊松分布", generator.poisson_random),
        "chi_square": ("卡方分布", generator.chi_square_random),
        "mixed": ("混合分布", generator.mixed_distribution)
    }
    
    if args.distribution == "all":
        dists_to_test = distributions
    else:
        dists_to_test = {args.distribution: distributions[args.distribution]}
    
    # 对每种分布进行测试
    for dist_name, (dist_title, dist_func) in dists_to_test.items():
        print("\n测试{}...".format(dist_title))
        
        # 生成随机数
        gen_start_time = time.time()
        numbers = dist_func(args.N, args.count)
        gen_end_time = time.time()
        gen_memory = get_memory_usage()
        
        print(f"随机数生成耗时: {gen_end_time - gen_start_time:.4f} 秒")
        print(f"随机数生成后内存使用: {gen_memory:.2f} MB")
        
        # 进行统计检验
        test_start_time = time.time()
        results = tester.run_all_tests(numbers)
        test_end_time = time.time()
        test_memory = get_memory_usage()
        
        print(f"统计检验耗时: {test_end_time - test_start_time:.4f} 秒")
        print(f"统计检验后内存使用: {test_memory:.2f} MB")
        
        # 保存检验结果
        with open(os.path.join(args.output, "{}_test_results.txt".format(dist_name)), "w", encoding="utf-8") as f:
            f.write("{}的统计检验结果:\n".format(dist_title))
            for result in results:
                f.write("\n{}:\n".format(result['检验类型'] if '检验类型' in result else result['Test']))
                for key, value in result.items():
                    if key not in ["检验类型", "Test"]:
                        f.write("{}: {}\n".format(key, value))
        
        # 保存出现频率表
        save_frequency_table(numbers, args.N, os.path.join(args.output, "{}_frequency.csv".format(dist_name)))
        # 保存间隔分布表
        save_gap_table(numbers, args.N, os.path.join(args.output, "{}_gaps.csv".format(dist_name)))
        
        print("{}的测试完成！结果已保存到{}目录。".format(dist_title, args.output))
    
    # 生成所有分布的可视化图表
    print("\n生成所有分布的可视化图表...")
    viz_start_time = time.time()
    visualizer.plot_histograms(os.path.join(args.output, "all_distributions_histogram.png"))
    visualizer.plot_boxplots(os.path.join(args.output, "all_distributions_boxplot.png"))
    visualizer.plot_qq_plots(os.path.join(args.output, "all_distributions_qq_plot.png"))
    viz_end_time = time.time()
    final_memory = get_memory_usage()
    
    print(f"可视化图表生成耗时: {viz_end_time - viz_start_time:.4f} 秒")
    print(f"最终内存使用: {final_memory:.2f} MB")
    print(f"总内存增长: {final_memory - initial_memory:.2f} MB")
    
    # 获取内存快照
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    print("\n内存使用最多的前3个位置:")
    for stat in top_stats[:3]:
        print(f"{stat.count} blocks: {stat.size/1024/1024:.1f} MB")
        print(f"  {stat.traceback.format()[0]}")
    
    tracemalloc.stop()
    print("可视化图表已生成！")

if __name__ == "__main__":
    main()