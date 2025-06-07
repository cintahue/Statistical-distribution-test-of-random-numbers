import os
import numpy as np
from random_generator import RandomGenerator

OUTPUT_DIR = 'output_bin'
FILE_SIZE = 128 * 1024  # 128KB
N = 256  # 0~255, 适合uint8

generator = RandomGenerator()

distributions = {
    'SimpleModulo': generator.simple_random,
    'Uniform': generator.uniform_random,
    'Normal': generator.normal_random,
    'Exponential': generator.exponential_random,
    'Poisson': generator.poisson_random,
    'ChiSquare': generator.chi_square_random,
    'Mixed': generator.mixed_distribution
}

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

for name, func in distributions.items():
    # 生成随机数
    numbers = func(N, FILE_SIZE)
    # 保证为uint8类型
    numbers = np.clip(numbers, 0, 255).astype(np.uint8)
    file_path = os.path.join(OUTPUT_DIR, f'{name}.bin')
    numbers.tofile(file_path)
    print(f'Generated {file_path}')

print('All distribution bin files generated in', OUTPUT_DIR) 