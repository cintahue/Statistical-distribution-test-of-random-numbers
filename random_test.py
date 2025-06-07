import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
from collections import defaultdict
import random
from typing import List, Dict, Tuple
import seaborn as sns

class RandomNumberTester:
    def __init__(self, N: int = 100):
        """
        初始化随机数测试器
        :param N: 随机数范围 [0, N-1]
        """
        self.N = N
        self.random_numbers = []
        
    def generate_random_numbers(self, count: int = 10000) -> List[int]:
        """
        使用C语言风格的rand()%N方法生成随机数
        :param count: 要生成的随机数数量
        :return: 随机数列表
        """
        self.random_numbers = [random.randint(0, self.N-1) for _ in range(count)]
        return self.random_numbers
    
    def test_frequency_distribution(self) -> Dict[str, float]:
        """
        测试1：频率分布测试
        统计每个数字出现的频率，并与理论均匀分布进行比较
        :return: 测试结果统计
        """
        if not self.random_numbers:
            raise ValueError("请先生成随机数")
            
        # 计算实际频率
        freq = defaultdict(int)
        for num in self.random_numbers:
            freq[num] += 1
            
        # 计算理论频率
        expected_freq = len(self.random_numbers) / self.N
        
        # 计算卡方统计量
        chi_square = sum((freq[i] - expected_freq) ** 2 / expected_freq 
                        for i in range(self.N))
        
        # 计算p值
        p_value = 1 - stats.chi2.cdf(chi_square, self.N - 1)
        
        return {
            "chi_square": chi_square,
            "p_value": p_value,
            "is_uniform": p_value > 0.05
        }
    
    def test_gap_distribution(self) -> Dict[str, float]:
        """
        测试2：间隔分布测试
        统计每个数字重复出现的间隔分布
        :return: 测试结果统计
        """
        if not self.random_numbers:
            raise ValueError("请先生成随机数")
            
        gaps = defaultdict(list)
        last_pos = defaultdict(int)
        
        # 计算间隔
        for i, num in enumerate(self.random_numbers):
            if num in last_pos:
                gaps[num].append(i - last_pos[num])
            last_pos[num] = i
            
        # 计算间隔的统计特性
        gap_stats = {}
        for num in range(self.N):
            if num in gaps:
                gap_list = gaps[num]
                gap_stats[num] = {
                    "mean": np.mean(gap_list),
                    "std": np.std(gap_list),
                    "min": min(gap_list),
                    "max": max(gap_list)
                }
                
        return gap_stats
    
    def test_serial_correlation(self) -> Dict[str, float]:
        """
        测试3：序列相关性测试
        检查相邻随机数之间的相关性
        :return: 测试结果统计
        """
        if not self.random_numbers:
            raise ValueError("请先生成随机数")
            
        # 计算自相关系数
        series = pd.Series(self.random_numbers)
        autocorr = series.autocorr()
        
        return {
            "autocorrelation": autocorr,
            "is_independent": abs(autocorr) < 0.1
        }
    
    def test_runs(self) -> Dict[str, float]:
        """
        测试4：游程测试
        检查随机数序列中的上升和下降趋势
        :return: 测试结果统计
        """
        if not self.random_numbers:
            raise ValueError("请先生成随机数")
            
        runs = 1
        for i in range(1, len(self.random_numbers)):
            if self.random_numbers[i] != self.random_numbers[i-1]:
                runs += 1
                
        # 计算理论游程数
        n = len(self.random_numbers)
        expected_runs = (2 * n - 1) / 3
        variance = (16 * n - 29) / 90
        
        # 计算Z统计量
        z = (runs - expected_runs) / np.sqrt(variance)
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
        
        return {
            "runs": runs,
            "expected_runs": expected_runs,
            "z_score": z,
            "p_value": p_value,
            "is_random": p_value > 0.05
        }
    
    def test_entropy(self) -> Dict[str, float]:
        """
        测试5：熵测试
        计算随机数序列的信息熵
        :return: 测试结果统计
        """
        if not self.random_numbers:
            raise ValueError("请先生成随机数")
            
        # 计算频率
        freq = defaultdict(int)
        for num in self.random_numbers:
            freq[num] += 1
            
        # 计算概率
        probs = [freq[i] / len(self.random_numbers) for i in range(self.N)]
        
        # 计算熵
        entropy = -sum(p * np.log2(p) for p in probs if p > 0)
        
        # 计算最大可能熵
        max_entropy = np.log2(self.N)
        
        return {
            "entropy": entropy,
            "max_entropy": max_entropy,
            "entropy_ratio": entropy / max_entropy
        }
    
    def plot_distribution(self):
        """
        绘制随机数分布图
        """
        if not self.random_numbers:
            raise ValueError("请先生成随机数")
            
        plt.figure(figsize=(12, 6))
        
        # 绘制直方图
        plt.subplot(1, 2, 1)
        plt.hist(self.random_numbers, bins=self.N, alpha=0.7)
        plt.title('随机数分布直方图')
        plt.xlabel('随机数值')
        plt.ylabel('频率')
        
        # 绘制Q-Q图
        plt.subplot(1, 2, 2)
        stats.probplot(self.random_numbers, dist="uniform", plot=plt)
        plt.title('Q-Q图')
        
        plt.tight_layout()
        plt.show()
    
    def plot_gap_distribution(self):
        """
        绘制间隔分布图
        """
        if not self.random_numbers:
            raise ValueError("请先生成随机数")
            
        gaps = defaultdict(list)
        last_pos = defaultdict(int)
        
        # 计算间隔
        for i, num in enumerate(self.random_numbers):
            if num in last_pos:
                gaps[num].append(i - last_pos[num])
            last_pos[num] = i
            
        # 绘制间隔分布
        plt.figure(figsize=(12, 6))
        for num in range(min(5, self.N)):  # 只显示前5个数字的间隔分布
            if num in gaps:
                sns.kdeplot(gaps[num], label=f'数字 {num}')
        
        plt.title('随机数间隔分布')
        plt.xlabel('间隔长度')
        plt.ylabel('密度')
        plt.legend()
        plt.show()

def main():
    # 创建测试器实例
    tester = RandomNumberTester(N=100)
    
    # 生成随机数
    numbers = tester.generate_random_numbers(count=10000)
    
    # 运行所有测试
    print("\n1. 频率分布测试:")
    freq_results = tester.test_frequency_distribution()
    print(f"卡方值: {freq_results['chi_square']:.2f}")
    print(f"P值: {freq_results['p_value']:.4f}")
    print(f"是否均匀分布: {freq_results['is_uniform']}")
    
    print("\n2. 间隔分布测试:")
    gap_results = tester.test_gap_distribution()
    for num, stats in gap_results.items():
        print(f"数字 {num}:")
        print(f"  平均间隔: {stats['mean']:.2f}")
        print(f"  标准差: {stats['std']:.2f}")
    
    print("\n3. 序列相关性测试:")
    corr_results = tester.test_serial_correlation()
    print(f"自相关系数: {corr_results['autocorrelation']:.4f}")
    print(f"是否独立: {corr_results['is_independent']}")
    
    print("\n4. 游程测试:")
    runs_results = tester.test_runs()
    print(f"游程数: {runs_results['runs']}")
    print(f"期望游程数: {runs_results['expected_runs']:.2f}")
    print(f"P值: {runs_results['p_value']:.4f}")
    
    print("\n5. 熵测试:")
    entropy_results = tester.test_entropy()
    print(f"信息熵: {entropy_results['entropy']:.4f}")
    print(f"最大可能熵: {entropy_results['max_entropy']:.4f}")
    print(f"熵比率: {entropy_results['entropy_ratio']:.4f}")
    
    # 绘制分布图
    tester.plot_distribution()
    tester.plot_gap_distribution()

if __name__ == "__main__":
    main() 