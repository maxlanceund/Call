import numpy as np
import matplotlib.pyplot as plt

# 设定时间轴
t = np.linspace(0, 100, 1000)

# 定义不同系统的容量上限 (S_BH)
capacities = [30, 50, 80]
colors = ['blue', 'orange', 'green']
labels = [f'Horizon Capacity S_BH = {c}' for c in capacities]

plt.figure(figsize=(10, 6))

for capacity, color, label in zip(capacities, colors, labels):
    # 模拟主方程 dS_A/dt = kappa * S_A 的指数增长，直到达到容量
    S_A = 0.5 * np.exp(0.06 * t) 
    
    # 找到逼近临界容量的时间点 (触发相变)
    phase_transition_idx = np.argmax(S_A > capacity)
    
    if S_A[phase_transition_idx] > capacity:
        # 截断平滑曲线，并制造断崖式暴跌（格式化）
        S_A[phase_transition_idx:] = capacity
        # 模拟格式化相变，熵瞬间归零或变成死寂底线
        drop_start = phase_transition_idx
        drop_end = drop_start + 30
        if drop_end < len(t):
            S_A[drop_start:drop_end] = np.linspace(capacity, 0, 30)
            S_A[drop_end:] = 0 # 达到最大混合态/死寂
            
    plt.plot(t[:phase_transition_idx+30] if phase_transition_idx > 0 else t, 
             S_A[:phase_transition_idx+30] if phase_transition_idx > 0 else S_A, 
             color=color, label=label, linewidth=2)

# 标注临界容量线
plt.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='Critical Capacity Limit (Topological Phase Transition)')

# 图表装饰
plt.title('Simulation of Black Hole Information Erasure (Dead-Equilibrium Model)', fontsize=14)
plt.xlabel('Time (t)', fontsize=12)
plt.ylabel('Entanglement Entropy S_A(t)', fontsize=12)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()

# 保存并展示
plt.savefig('dead_equilibrium_simulation.png', dpi=300)
plt.show()
