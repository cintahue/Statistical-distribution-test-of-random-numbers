import numpy as np
import matplotlib.pyplot as plt
from random_generator import RandomGenerator
import seaborn as sns
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 任选其一
matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

class DistributionVisualizer:
    def __init__(self, N: int = 100, count: int = 10000):
        """
        Initialize the visualizer
        :param N: Upper bound of random number range
        :param count: Number of random numbers to generate
        """
        self.N = N
        self.count = count
        self.generator = RandomGenerator()
        self.distribution_names = {
            "简单取模": "Simple Modulo",
            "均匀分布": "Uniform",
            "正态分布": "Normal",
            "指数分布": "Exponential",
            "泊松分布": "Poisson",
            "卡方分布": "Chi-Square",
            "混合分布": "Mixed"
        }
        
    def generate_all_distributions(self):
        """Generate all distributions"""
        return {
            "简单取模": self.generator.simple_random(self.N, self.count),
            "均匀分布": self.generator.uniform_random(self.N, self.count),
            "正态分布": self.generator.normal_random(self.N, self.count),
            "指数分布": self.generator.exponential_random(self.N, self.count),
            "泊松分布": self.generator.poisson_random(self.N, self.count),
            "卡方分布": self.generator.chi_square_random(self.N, self.count),
            "混合分布": self.generator.mixed_distribution(self.N, self.count)
        }
    
    def plot_histograms(self, save_path: str = None):
        """
        Plot histograms for all distributions
        :param save_path: Path to save the image, if None then show the image
        """
        distributions = self.generate_all_distributions()
        
        # 设置图表样式
        plt.style.use('default')
        fig, axes = plt.subplots(3, 3, figsize=(15, 15))
        axes = axes.ravel()
        
        # 添加全局参数说明
        plt.suptitle("Histograms of All Distributions (N={}, count={})".format(self.N, self.count), fontsize=18)
        
        for idx, (name, numbers) in enumerate(distributions.items()):
            eng_name = self.distribution_names[name]
            # 绘制直方图
            sns.histplot(data=numbers, bins=30, ax=axes[idx], kde=True)
            axes[idx].set_title("{} Distribution (N={}, count={})".format(eng_name, self.N, self.count))
            axes[idx].set_xlabel("Value")
            axes[idx].set_ylabel("Frequency")
            
            # 添加统计信息
            stats_text = "Mean: {:.2f}\n".format(np.mean(numbers))
            stats_text += "Std: {:.2f}\n".format(np.std(numbers))
            stats_text += "Median: {:.2f}".format(np.median(numbers))
            axes[idx].text(0.95, 0.95, stats_text,
                         transform=axes[idx].transAxes,
                         verticalalignment='top',
                         horizontalalignment='right',
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # 隐藏多余的子图
        for idx in range(len(distributions), len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
        plt.close()
    
    def plot_boxplots(self, save_path: str = None):
        """
        Plot boxplots for all distributions
        :param save_path: Path to save the image, if None then show the image
        """
        distributions = self.generate_all_distributions()
        
        # 准备数据
        data = []
        labels = []
        for name, numbers in distributions.items():
            data.append(numbers)
            labels.append(self.distribution_names[name])
        
        # 设置图表样式
        plt.style.use('default')
        plt.figure(figsize=(12, 6))
        
        # 添加全局参数说明
        plt.title("Boxplot Comparison of Distributions (N={}, count={})".format(self.N, self.count), fontsize=16)
        
        # 绘制箱线图
        sns.boxplot(data=data)
        plt.xticks(range(len(distributions)), labels, rotation=45)
        plt.ylabel("Value")
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
        plt.close()
    
    def plot_qq_plots(self, save_path: str = None):
        """
        Plot Q-Q plots for all distributions
        :param save_path: Path to save the image, if None then show the image
        """
        from scipy import stats
        distributions = self.generate_all_distributions()
        
        # 设置图表样式
        plt.style.use('default')
        fig, axes = plt.subplots(3, 3, figsize=(15, 15))
        axes = axes.ravel()
        
        # 添加全局参数说明
        plt.suptitle("Q-Q Plots of All Distributions (N={}, count={})".format(self.N, self.count), fontsize=18)
        
        for idx, (name, numbers) in enumerate(distributions.items()):
            eng_name = self.distribution_names[name]
            # 计算理论分位数
            theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(numbers)))
            
            # 计算实际分位数
            actual_quantiles = np.sort(numbers)
            
            # 绘制Q-Q图
            axes[idx].scatter(theoretical_quantiles, actual_quantiles, alpha=0.5)
            axes[idx].plot([min(theoretical_quantiles), max(theoretical_quantiles)],
                         [min(theoretical_quantiles), max(theoretical_quantiles)],
                         'r--', alpha=0.5)
            axes[idx].set_title("{} Q-Q Plot (N={}, count={})".format(eng_name, self.N, self.count))
            axes[idx].set_xlabel("Theoretical Quantiles")
            axes[idx].set_ylabel("Sample Quantiles")
        
        # 隐藏多余的子图
        for idx in range(len(distributions), len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
        plt.close()

def main():
    # 创建可视化器实例
    visualizer = DistributionVisualizer(N=100, count=10000)
    
    # 生成并保存所有图表
    visualizer.plot_histograms("histograms.png")
    visualizer.plot_boxplots("boxplots.png")
    visualizer.plot_qq_plots("qq_plots.png")
    
    print("All plots have been generated!")

if __name__ == "__main__":
    main() 