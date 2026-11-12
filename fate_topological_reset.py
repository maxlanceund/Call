import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 100, 1000)

# 蓝线：宇宙信息熵（呈现指数级暴涨）
S_A = np.exp(0.06 * t) 

# 红线：系统容量上限（由于某种原因停止了扩容，固定在临界值）
S_BH_limit = 50 

plt.figure(figsize=(10, 6))

# 寻找相变的临界点
phase_transition_idx = np.argmax(S_A > S_BH_limit)

# 截断并制造断崖式暴跌
if S_A[phase_transition_idx] > S_BH_limit:
    S_A[phase_transition_idx:] = S_BH_limit
    drop_start = phase_transition_idx
    drop_end = drop_start + 30
    if drop_end < len(t):
        S_A[drop_start:drop_end] = np.linspace(S_BH_limit, 0, 30)
        # 模拟重启后的新一轮循环（重新开始积累）
        S_A[drop_end:] = np.exp(0.03 * (t[drop_end:] - t[drop_end])) * 0.5 

plt.plot(t, S_A, color='purple', linewidth=4, label='System Entropy Evolution (S_A)')
plt.axhline(y=S_BH_limit, color='red', linestyle='--', linewidth=3, label='Critical Capacity Limit (S_BH)')

# 标注相变点
plt.axvline(x=t[phase_transition_idx], color='black', linestyle=':', linewidth=2)
plt.text(t[phase_transition_idx]+2, S_BH_limit-10, 'Global Topological Reset\n(Forced Formatting)', 
         color='black', fontsize=12, fontweight='bold')

plt.title('Fate B: The Topological Reset (Rural Dog Universe)', fontsize=16, fontweight='bold')
plt.xlabel('Time (t)', fontsize=12)
plt.ylabel('Entropy (S_A)', fontsize=12)
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()

plt.savefig('fate_topological_reset.png', dpi=300)
print("Fate B 已生成！")
