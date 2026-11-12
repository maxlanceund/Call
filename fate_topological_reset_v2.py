import numpy as np
import matplotlib.pyplot as plt

# 设定时间轴（从当前一直推到宇宙末日）
t = np.linspace(0, 100, 1000)

plt.figure(figsize=(12, 8))

# 1. 绘制多个局部黑洞（小漏斗）的信息熵累积
# 我们模拟3个不同大小的黑洞，它们都在疯狂吸积
S_local1 = 0.5 * np.exp(0.04 * t)
S_local2 = 0.3 * np.exp(0.045 * t)
S_local3 = 0.2 * np.exp(0.05 * t)

# 总和（宇宙全局信息熵 S_A）
S_total = S_local1 + S_local2 + S_local3
S_BH_limit = 50 # 终极临界容量

# 绘制局部黑洞的信息积累（用虚线表示它们正在被缓存）
plt.plot(t, S_local1, color='#A9A9A9', linestyle=':', linewidth=2, label='Local Cache A (Black Hole)')
plt.plot(t, S_local2, color='#A9A9A9', linestyle=':', linewidth=2)
plt.plot(t, S_local3, color='#A9A9A9', linestyle=':', linewidth=2)

# 绘制总的系统熵演化（用粗紫线，代表所有漏斗的累积）
phase_transition_idx = np.argmax(S_total > S_BH_limit)

# 处理断崖式暴跌（全局格式化）
S_total_mutated = S_total.copy()
if S_total[phase_transition_idx] > S_BH_limit:
    S_total_mutated[phase_transition_idx:] = S_BH_limit
    drop_start = phase_transition_idx
    drop_end = drop_start + 15
    if drop_end < len(t):
        # 暴跌归零
        S_total_mutated[drop_start:drop_end] = np.linspace(S_BH_limit, 0, 15)
        # 归零后的“大爆炸”重启（用星号爆炸图表示）
        S_total_mutated[drop_end:] = 0 

plt.plot(t[:drop_end], S_total_mutated[:drop_end], color='#6A0DAD', linewidth=4, label='Global Entropy (All Funnels Accumulating)')

# 画临界容量红线
plt.axhline(y=S_BH_limit, color='red', linestyle='--', linewidth=3, label='Critical Capacity Limit (S_BH)')

# 2. 绘制大爆炸（拓扑相变点）
reset_t = t[drop_end] if S_total[phase_transition_idx] > S_BH_limit else 0
reset_y = 0

# 用散点画一个向外辐射的爆炸效果（大爆炸/重启）
for i in range(1, 6):
    angle = np.linspace(0, 2*np.pi, 50)
    radius = i * 2
    x_explosion = reset_t + radius * np.cos(angle)
    y_explosion = reset_y + radius * np.sin(angle)
    # 只画下半圆和右半圆（因为左边是过去，上面是原来的系统）
    valid = (x_explosion >= reset_t) & (y_explosion <= S_BH_limit/2)
    plt.plot(x_explosion[valid], y_explosion[valid], color='orange', alpha=0.6, linewidth=2)

# 在爆炸中心画一个极大的星星
plt.scatter(reset_t, reset_y, color='gold', s=1000, marker='*', zorder=10, label='Big Bang (Topological Reset)')

# 添加极其霸气的注释
plt.axvline(x=reset_t, color='black', linestyle=':', linewidth=2)
plt.text(reset_t - 15, S_BH_limit + 5, 'Global Singularity Reached\n(All Caches Full)', fontsize=12, color='purple', fontweight='bold', ha='center')
plt.text(reset_t + 5, 15, 'Forced Formatting\n& Next Big Bang', fontsize=12, color='#D2691E', fontweight='bold')

# 3. 图表装饰
plt.title('Fate: The Cosmic Funnel Reset (All Accumulate, Then Explode)', fontsize=18, fontweight='bold')
plt.xlabel('Time (t)', fontsize=14)
plt.ylabel('Total Entropy / Information Capacity (S_A)', fontsize=14)
plt.ylim(-5, S_BH_limit + 10)
plt.xlim(0, 100)
plt.legend(fontsize=12, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

plt.savefig('fate_cosmic_reset.png', dpi=300)
print("终极重启图已生成！")
