import numpy as np
import matplotlib.pyplot as plt

# 模拟漏斗的径向坐标 (从上往下)
r = np.linspace(100, 10, 500) # 距离中心奇点的距离

# 真实的下坠速度 (引力漏斗，越靠近底部速度越快)
v_true_drop = -1.0 * (100 / r)**0.5  # 负值表示向内坠落

# 观测到的“膨胀速度” (视错觉投影)
v_observed_expansion = 0.7 * (r / 100) # 表面上看，距离越远，退行速度越快(哈勃定律)

plt.figure(figsize=(12, 6))

# 画真实的物理下坠
plt.plot(r, v_true_drop, color='red', linewidth=3, label='True Radial Descent (Into the Funnel)')

# 画观测到的视错觉
plt.plot(r, v_observed_expansion, color='blue', linestyle='--', linewidth=3, label='Observed Expansion (Hubble Redshift Illusion)')

# 填色区分
plt.fill_between(r, v_true_drop, 0, color='red', alpha=0.1)
plt.fill_between(r, v_observed_expansion, 0, color='blue', alpha=0.1)

plt.title('Cosmic Funnel Illusion: Descent vs. Expansion', fontsize=14)
plt.xlabel('Radius from Global Singularity (r)', fontsize=12)
plt.ylabel('Velocity (Arbitrary Units)', fontsize=12)
plt.axhline(0, color='black', linewidth=1)

# 添加文字标注
plt.text(60, -0.6, 'Everyone is falling inward', fontsize=12, color='red')
plt.text(60, 0.3, 'We think we are drifting apart', fontsize=12, color='blue')

plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('funnel_illusion.png', dpi=300)
plt.show()
