import numpy as np
from scipy import stats
import random

class RandomGenerator:
    @staticmethod
    def simple_random(N: int, count: int = 10000) -> np.ndarray:
        """
        使用简单取模方法生成[0, N-1]范围内的随机数
        :param N: 范围上限
        :param count: 生成数量
        :return: 随机数数组
        """
        return np.array([random.randint(0, N-1) for _ in range(count)])
    
    @staticmethod
    def uniform_random(N: int, count: int = 10000) -> np.ndarray:
        """
        生成[0, N-1]范围内的均匀分布随机数
        :param N: 范围上限
        :param count: 生成数量
        :return: 随机数数组
        """
        return np.random.randint(0, N, count)
    
    @staticmethod
    def normal_random(N: int, count: int = 10000, mean: float = None, std: float = None) -> np.ndarray:
        """
        生成[0, N-1]范围内的正态分布随机数
        :param N: 范围上限
        :param count: 生成数量
        :param mean: 均值，默认为N/2
        :param std: 标准差，默认为N/6
        :return: 随机数数组
        """
        if mean is None:
            mean = N / 2
        if std is None:
            std = N / 6
            
        # 生成正态分布随机数
        numbers = np.random.normal(mean, std, count)
        
        # 将数值映射到[0, N-1]范围
        numbers = np.clip(numbers, 0, N-1)
        return numbers.astype(int)
    
    @staticmethod
    def exponential_random(N: int, count: int = 10000, scale: float = None) -> np.ndarray:
        """
        生成[0, N-1]范围内的指数分布随机数
        :param N: 范围上限
        :param count: 生成数量
        :param scale: 尺度参数，默认为N/4
        :return: 随机数数组
        """
        if scale is None:
            scale = N / 4
            
        # 生成指数分布随机数
        numbers = np.random.exponential(scale, count)
        
        # 将数值映射到[0, N-1]范围
        numbers = np.clip(numbers, 0, N-1)
        return numbers.astype(int)
    
    @staticmethod
    def poisson_random(N: int, count: int = 10000, lambda_param: float = None) -> np.ndarray:
        """
        生成[0, N-1]范围内的泊松分布随机数
        :param N: 范围上限
        :param count: 生成数量
        :param lambda_param: 泊松参数，默认为N/2
        :return: 随机数数组
        """
        if lambda_param is None:
            lambda_param = N / 2
            
        # 生成泊松分布随机数
        numbers = np.random.poisson(lambda_param, count)
        
        # 将数值映射到[0, N-1]范围
        numbers = np.clip(numbers, 0, N-1)
        return numbers.astype(int)
    
    @staticmethod
    def chi_square_random(N: int, count: int = 10000, df: int = None) -> np.ndarray:
        """
        生成[0, N-1]范围内的卡方分布随机数
        :param N: 范围上限
        :param count: 生成数量
        :param df: 自由度，默认为N/2
        :return: 随机数数组
        """
        if df is None:
            df = int(N / 2)
            
        # 生成卡方分布随机数
        numbers = np.random.chisquare(df, count)
        
        # 将数值映射到[0, N-1]范围
        numbers = np.clip(numbers, 0, N-1)
        return numbers.astype(int)
    
    @staticmethod
    def mixed_distribution(N: int, count: int = 10000, 
                          weights: list = None) -> np.ndarray:
        """
        生成混合分布的随机数
        :param N: 范围上限
        :param count: 生成数量
        :param weights: 各分布的权重，默认为均匀权重
        :return: 随机数数组
        """
        if weights is None:
            weights = [0.2, 0.2, 0.2, 0.2, 0.2]  # 均匀权重
            
        # 确保权重和为1
        weights = np.array(weights) / sum(weights)
        
        # 计算每个分布生成的随机数数量
        counts = np.random.multinomial(count, weights)
        
        # 生成各分布的随机数
        numbers = []
        numbers.extend(RandomGenerator.uniform_random(N, counts[0]))
        numbers.extend(RandomGenerator.normal_random(N, counts[1]))
        numbers.extend(RandomGenerator.exponential_random(N, counts[2]))
        numbers.extend(RandomGenerator.poisson_random(N, counts[3]))
        numbers.extend(RandomGenerator.chi_square_random(N, counts[4]))
        
        # 打乱顺序
        random.shuffle(numbers)
        return np.array(numbers)

def main():
    # 测试各种分布
    N = 100
    count = 10000
    
    # 生成各种分布的随机数
    simple_nums = RandomGenerator.simple_random(N, count)
    uniform_nums = RandomGenerator.uniform_random(N, count)
    normal_nums = RandomGenerator.normal_random(N, count)
    exp_nums = RandomGenerator.exponential_random(N, count)
    poisson_nums = RandomGenerator.poisson_random(N, count)
    chi_nums = RandomGenerator.chi_square_random(N, count)
    mixed_nums = RandomGenerator.mixed_distribution(N, count)
    
    # 打印基本统计信息
    distributions = {
        "简单取模": simple_nums,
        "均匀分布": uniform_nums,
        "正态分布": normal_nums,
        "指数分布": exp_nums,
        "泊松分布": poisson_nums,
        "卡方分布": chi_nums,
        "混合分布": mixed_nums
    }
    
    for name, nums in distributions.items():
        print("\n{}统计信息:".format(name))
        print("均值: {:.2f}".format(np.mean(nums)))
        print("标准差: {:.2f}".format(np.std(nums)))
        print("最小值: {}".format(np.min(nums)))
        print("最大值: {}".format(np.max(nums)))
        print("中位数: {:.2f}".format(np.median(nums)))

if __name__ == "__main__":
    main() 