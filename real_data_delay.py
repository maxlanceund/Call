import numpy as np
import matplotlib.pyplot as plt

# 真实常数：光速 (m/s)
c = 299792458

# 人类目前的真实实验距离 (对数坐标)
distances_m = np.logspace(1, 8, 100) # 从10米到100,000公里
# 真实实验数据点 (阿斯佩实验 1982, 中国墨子号 2017)
real_data_distances = [12, 1200 * 1000] # 12米，1200公里
labels = ["Aspect 1982 (12m)", "Micius 2017 (1200km)"]

# 主流相对论预测的延迟 (秒)
mainstream_delay = distances_m / c

# 你的“无形大手”理论预测的延迟 (秒)
your_delay = np.zeros_like(distances_m)

plt.figure(figsize=(12, 6))
plt.plot(distances_m, mainstream_delay, color='red', linewidth=3, linestyle='--', label='Mainstream: Signal Delay (t = d/c)')
plt.plot(distances_m, your_delay, color='green', linewidth=4, label='This Theory: Zero Delay (Global Refresh)')

# 标注真实的实验数据点
for i, d in enumerate(real_data_distances):
    delay = d / c
    plt.scatter(d, delay, color='blue', s=150, zorder=5, edgecolor='black')
    plt.text(d * 1.2, delay * 1.5, labels[i], fontsize=10, rotation=0)

plt.title("Real-World Test: Can We Measure the Delay Difference?", fontsize=16)
plt.xlabel("Distance (Meters, Log Scale)", fontsize=14)
plt.ylabel("Time to Correlate State (Seconds)", fontsize=14)
plt.xscale('log')
plt.yscale('log')
plt.legend(loc='upper left', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('real_data_delay.png', dpi=300)
