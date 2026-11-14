import numpy as np
import matplotlib.pyplot as plt

# === 参数设定 ===
gamma = 0.05  # 环境退相干系数
D = 10.0      # 距离（比如1000km）
alpha = 0.1   # 无形之手的拓扑增益系数

# 演化时间
dt = 0.01
T = 100
steps = int(T/dt)

# 初始条件：完美纠缠态
C = 1.0

# 存储数据
C_mainstream = []
C_theory = []
C_solution_math = []
time_axis = []

# 欧拉法迭代求解
for i in range(steps):
    t = i * dt
    time_axis.append(t)
    
    # 1. 主流退相干（纯指数衰减）
    # dC/dt = -gamma * D * C
    dC_main = -gamma * D * C
    C_mainstream.append(C)
    
    # 2. 你的大漏斗理论（微分方程）
    # dC/dt = -gamma * D * C + alpha * G * C * (1 - C)
    # 我们假设此时引力场 G = 10
    G = 10.0
    dC_theory = -gamma * D * C + alpha * G * C * (1 - C)
    
    C_theory.append(C)
    
    # 更新 C (分离两个系统，各自演化)
    if i == 0:
        C_main = C
        C_theo = C
    else:
        C_main += dC_main * dt
        C_theo += dC_theory * dt
    
    # 防止数值溢出
    C_main = max(0, C_main)
    C_theo = max(0, min(1, C_theo))
    
    # 将两个演化的当前值存入
    C_mainstream[-1] = C_main
    C_theory[-1] = C_theo

# 数学解析解（理论稳态值）
steady_state_math = 1 - (gamma * D) / (alpha * 10.0)

# === 绘图 ===
plt.figure(figsize=(10, 6))
plt.plot(time_axis, C_mainstream, 'r--', linewidth=3, label='Mainstream: Exponential Decay')
plt.plot(time_axis, C_theory, 'purple', linewidth=4, label='This Theory: Non-linear ODE Evolution')

# 画出数学稳态线
plt.axhline(y=steady_state_math, color='gold', linestyle=':', linewidth=2, 
            label=f'Mathematical Steady State (\(C^* = {steady_state_math:.2f}\))')

plt.title("ODE Simulation: Entanglement Dynamics with Topological Protection", fontsize=16)
plt.xlabel("Evolution Time (t)", fontsize=14)
plt.ylabel("Entanglement Fidelity (C)", fontsize=14)
plt.ylim(0, 1.1)
plt.legend(loc='upper right', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('ode_entanglement_dynamics.png', dpi=300)
print(f"=== 数学ODE模拟完成 ===")
print(f"理论预测稳态纠缠度: {steady_state_math:.4f}")
print(f"主流预测 100 时间后纠缠度: {C_mainstream[-1]:.4f}")
print(f"大漏斗方程 100 时间后纠缠度: {C_theory[-1]:.4f}")
