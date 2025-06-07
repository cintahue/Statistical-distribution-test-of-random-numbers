import numpy as np
from scipy import stats
from random_generator import RandomGenerator

class StatisticalTester:
    def __init__(self, N: int = 100, count: int = 10000):
        """
        初始化统计测试器
        :param N: 随机数范围上限
        :param count: 生成随机数的数量
        """
        self.N = N
        self.count = count
        self.generator = RandomGenerator()
        
    def test_uniformity(self, numbers: np.ndarray) -> dict:
        """
        进行均匀性检验
        :param numbers: 随机数数组
        :return: 检验结果字典
        """
        # 计算每个数字的频数
        observed = np.bincount(numbers, minlength=self.N)
        expected = np.ones(self.N) * self.count / self.N
        
        # 进行卡方检验
        chi2, p_value = stats.chisquare(observed, expected)
        
        return {
            "检验类型": "均匀性检验",
            "卡方统计量": chi2,
            "p值": p_value,
            "结论": "服从均匀分布" if p_value > 0.05 else "不服从均匀分布"
        }
    
    def test_independence(self, numbers: np.ndarray) -> dict:
        """
        进行独立性检验
        :param numbers: 随机数数组
        :return: 检验结果字典
        """
        # 计算自相关系数
        autocorr = np.correlate(numbers, numbers, mode='full')[len(numbers)-1:]
        autocorr = autocorr / autocorr[0]  # 归一化
        
        # 计算前10个滞后值的自相关系数
        lags = range(1, 11)
        acf = autocorr[1:11]
        
        # 计算95%置信区间
        ci = 1.96 / np.sqrt(len(numbers))
        
        # 判断是否存在显著的自相关
        significant = np.any(np.abs(acf) > ci)
        
        return {
            "检验类型": "独立性检验",
            "最大自相关系数": np.max(np.abs(acf)),
            "显著滞后值": [i for i, v in enumerate(acf, 1) if abs(v) > ci],
            "结论": "序列独立" if not significant else "序列不独立"
        }
    
    def test_gap_distribution(self, numbers: np.ndarray) -> dict:
        """
        进行间隔分布检验
        :param numbers: 随机数数组
        :return: 检验结果字典
        """
        gaps = []
        last_pos = {}
        
        # 计算每个数字的间隔
        for i, num in enumerate(numbers):
            if num in last_pos:
                gaps.append(i - last_pos[num])
            last_pos[num] = i
        
        # 计算间隔的统计特征
        mean_gap = np.mean(gaps)
        std_gap = np.std(gaps)
        
        # 进行指数分布拟合检验
        lambda_est = 1 / mean_gap
        ks_stat, p_value = stats.kstest(gaps, 'expon', args=(0, 1/lambda_est))
        
        return {
            "检验类型": "间隔分布检验",
            "平均间隔": mean_gap,
            "间隔标准差": std_gap,
            "KS统计量": ks_stat,
            "p值": p_value,
            "结论": "间隔服从指数分布" if p_value > 0.05 else "间隔不服从指数分布"
        }
    
    def test_runs(self, numbers: np.ndarray) -> dict:
        """
        进行游程检验
        :param numbers: 随机数数组
        :return: 检验结果字典
        """
        # 计算游程数
        runs = 1
        for i in range(1, len(numbers)):
            if numbers[i] != numbers[i-1]:
                runs += 1
        
        # 计算理论游程数
        n1 = np.sum(numbers == numbers[0])
        n2 = len(numbers) - n1
        expected_runs = 1 + 2 * n1 * n2 / (n1 + n2)
        std_runs = np.sqrt(2 * n1 * n2 * (2 * n1 * n2 - n1 - n2) / 
                          ((n1 + n2)**2 * (n1 + n2 - 1)))
        
        # 计算Z统计量
        z = (runs - expected_runs) / std_runs
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
        
        return {
            "检验类型": "游程检验",
            "实际游程数": runs,
            "理论游程数": expected_runs,
            "Z统计量": z,
            "p值": p_value,
            "结论": "游程数符合随机性" if p_value > 0.05 else "游程数不符合随机性"
        }
    
    def test_entropy(self, numbers: np.ndarray) -> dict:
        """
        进行熵检验
        :param numbers: 随机数数组
        :return: 检验结果字典
        """
        # 计算频数
        counts = np.bincount(numbers, minlength=self.N)
        probs = counts / len(numbers)
        
        # 计算熵
        entropy = -np.sum(probs * np.log2(probs + 1e-10))
        max_entropy = np.log2(self.N)
        
        # 计算熵比率
        entropy_ratio = entropy / max_entropy
        
        return {
            "检验类型": "熵检验",
            "实际熵": entropy,
            "最大熵": max_entropy,
            "熵比率": entropy_ratio,
            "结论": "熵值较高" if entropy_ratio > 0.9 else "熵值较低"
        }
    
    def run_all_tests(self, numbers: np.ndarray) -> list:
        """
        运行所有统计检验
        :param numbers: 随机数数组
        :return: 所有检验结果的列表
        """
        tests = [
            self.test_uniformity,
            self.test_independence,
            self.test_gap_distribution,
            self.test_runs,
            self.test_entropy
        ]
        
        results = []
        for test in tests:
            results.append(test(numbers))
        
        return results

def main():
    # 创建测试器实例
    tester = StatisticalTester(N=100, count=10000)
    
    # 生成各种分布的随机数
    distributions = {
        "均匀分布": tester.generator.uniform_random(100, 10000),
        "正态分布": tester.generator.normal_random(100, 10000),
        "指数分布": tester.generator.exponential_random(100, 10000),
        "泊松分布": tester.generator.poisson_random(100, 10000),
        "卡方分布": tester.generator.chi_square_random(100, 10000),
        "混合分布": tester.generator.mixed_distribution(100, 10000)
    }
    
    # 对每种分布进行测试
    for name, numbers in distributions.items():
        print(f"\n{name}的统计检验结果:")
        results = tester.run_all_tests(numbers)
        for result in results:
            print(f"\n{result['检验类型']}:")
            for key, value in result.items():
                if key != "检验类型":
                    print(f"{key}: {value}")

if __name__ == "__main__":
    main() 