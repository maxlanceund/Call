import matplotlib.pyplot as plt
import numpy as np

# 设置画布大小：横向长图 (16:7)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# ==========================================
# 左图：宏观光速延迟 vs 底层全局零延迟
# ==========================================
distances = np.linspace(0.1, 10, 100) # 距离（光年）
relativity_time = distances # 相对论：延迟 = 距离 / 光速
global_refresh_time = np.zeros_like(distances) # 你的理论：零延迟

ax1.plot(distances, relativity_time, color='red', linewidth=4, linestyle='--', label='Mainstream Relativity: Signal Delay ($t = d/c$)')
ax1.plot(distances, global_refresh_time, color='green', linewidth=4, label='This Theory: Zero Delay (Invisible Hand)')
ax1.fill_between(distances, global_refresh_time, relativity_time, color='gray', alpha=0.15, label='Forbidden Zone for Mainstream')

ax1.set_title("A. State Allocation Delay vs. Distance", fontsize=14, fontweight='bold')
ax1.set_xlabel("Distance between entangled particles (Light Years)", fontsize=12)
ax1.set_ylabel("Time to correlate state (Years)", fontsize=12)
ax1.legend(loc='upper left', fontsize=11)
ax1.grid(True, linestyle=':', alpha=0.6)

# ==========================================
# 右图：极端引力下的纠缠保真度反转
# ==========================================
gravity = np.linspace(0, 10, 100) # 引力场强度（0到黑洞边缘）
mainstream_fidelity = np.exp(-0.3 * gravity) # 主流：潮汐力破坏纠缠
your_fidelity = 1 - np.exp(-0.4 * gravity) # 你的理论：拓扑折叠增强纠缠

ax2.plot(gravity, mainstream_fidelity, color='red', linestyle='--', linewidth=4, label='Mainstream: Tidal Decoherence')
ax2.plot(gravity, your_fidelity, color='purple', linewidth=4, label='This Theory: Topological Enhancement')

ax2.axvline(x=8, color='black', linestyle=':', linewidth=2)
ax2.text(8.2, 0.5, 'Event Horizon\n(Extreme Gravity)', color='black', fontsize=11)

ax2.set_title("B. Entanglement Fidelity under Extreme Gravity", fontsize=14, fontweight='bold')
ax2.set_xlabel("Gravitational Field Strength", fontsize=12)
ax2.set_ylabel("Entanglement Fidelity", fontsize=12)
ax2.legend(loc='upper right', fontsize=11)
ax2.grid(True, linestyle=':', alpha=0.6)

# ==========================================
# 全局设置
# ==========================================
plt.suptitle("Falsifiable Predictions of the Finite-Capacity Ontology", fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()

# 保存高分辨率图
plt.savefig('ultimate_falsifiable_prediction.png', dpi=300, bbox_inches='tight')
