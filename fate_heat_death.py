import numpy as np
import matplotlib.pyplot as plt

# 时间轴（模拟宇宙的极遥远未来）
t = np.linspace(0, 100, 1000)

# 归一化数据（为了图表直观，我们用相对的指数增长来表现）
# 蓝线：宇宙实际信息熵 (S_A)
# 红线：宇宙视界容量上限 (S_BH)
S_A = np.exp(0.02 * t)         # 内部信息缓慢增加
S_BH = np.exp(0.08 * t)        # 暗能量导致空间加速膨胀，容量上限狂飙

plt.figure(figsize=(10, 6))
plt.plot(t, S_A, color='blue', linewidth=3, label='Actual Information Entropy (S_A)')
plt.plot(t, S_BH, color='red', linestyle='--', linewidth=3, label='Cosmological Horizon Capacity (S_BH)')

# 填充差距，代表越来越空旷、没有因果联系的死寂空间
plt.fill_between(t, S_A, S_BH, color='gray', alpha=0.15, label='Dead Space (No Causal Contact)')

plt.title('Fate A: The Heat Death (City Dog Universe)', fontsize=16, fontweight='bold')
plt.xlabel('Time (Trillions of Years into the Future)', fontsize=12)
plt.ylabel('Normalized Entropy / Capacity', fontsize=12)
plt.yscale('log') # 使用对数坐标才能看清巨大的差距
plt.legend(fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()

plt.savefig('fate_heat_death.png', dpi=300)
print("Fate A 已生成！")
