import numpy as np
import matplotlib.pyplot as plt

# === 纯 NumPy 实现量子纠缠度 (Concurrence) 计算，无需 scipy ===
def concurrence(rho):
    # Pauli Y 矩阵
    Y = np.array([[0, -1j], [1j, 0]])
    YY = np.kron(Y, Y)
    rho_tilde = YY @ rho.conj() @ YY
    # 计算 rho * rho_tilde 的特征值
    M = rho @ rho_tilde
    eigenvalues = np.linalg.eigvals(M)
    # 取实部并保证非负，开方
    sqrt_eigenvalues = np.sqrt(np.clip(np.real(eigenvalues), 0, None))
    sqrt_eigenvalues = np.sort(sqrt_eigenvalues)[::-1]
    # 计算纠缠度
    return max(0, sqrt_eigenvalues[0] - sqrt_eigenvalues[1] - sqrt_eigenvalues[2] - sqrt_eigenvalues[3])

# === 1. 制备初始纠缠态 (Bell态 |Φ+>) ===
state_00 = np.array([1, 0, 0, 0])
state_11 = np.array([0, 0, 0, 1])
psi_entangled = (state_00 + state_11) / np.sqrt(2)
rho_initial = np.outer(psi_entangled, psi_entangled.conj())

time = np.linspace(0, 10, 100)

# === 2. 物理环境设定 (不作弊) ===
# 根据主流理论，引力越强，时间越慢，环境噪声越大，退相干率 gamma 越大。
gamma_bottom = 0.8  # 塔底：强引力，退相干快
gamma_top = 0.2     # 塔顶：弱引力，退相干慢

data_mainstream_bottom = []
data_mainstream_top = []
data_theory_bottom = []
data_theory_top = []

for t in time:
    # --- 主流预测 (红虚线) ---
    # 密度矩阵的非对角项随时间指数衰减 e^(-gamma * t)
    decay_bottom = np.exp(-gamma_bottom * t)
    decay_top = np.exp(-gamma_top * t)
    
    # 构造退相干后的密度矩阵
    rho_m_bottom = rho_initial.copy()
    rho_m_bottom[0, 3] *= decay_bottom
    rho_m_bottom[3, 0] *= decay_bottom
    
    rho_m_top = rho_initial.copy()
    rho_m_top[0, 3] *= decay_top
    rho_m_top[3, 0] *= decay_top
    
    data_mainstream_bottom.append(concurrence(rho_m_bottom))
    data_mainstream_top.append(concurrence(rho_m_top))

    # --- 你的理论预测 (紫线) ---
    # 核心假说：强引力(塔底)导致底层拓扑折叠，拉近了距离，**抵消**了潮汐退相干。
    # 数学表达：在强引力下，有效退相干率 gamma_effective = gamma * (1 - 拓扑保护率)
    # 假设拓扑保护能抵消 90% 的退相干 (即只有10%的退相干生效)
    theory_protection_bottom = 0.9 
    
    decay_bottom_theory = np.exp(-gamma_bottom * (1 - theory_protection_bottom) * t)
    rho_t_bottom = rho_initial.copy()
    rho_t_bottom[0, 3] *= decay_bottom_theory
    rho_t_bottom[3, 0] *= decay_bottom_theory
    
    data_theory_bottom.append(concurrence(rho_t_bottom))
    
    # 塔顶引力弱，没有拓扑保护，你的理论预测和主流完全一样
    data_theory_top.append(concurrence(rho_m_top))

# === 3. 绘图与输出 ===
plt.figure(figsize=(10, 6))
plt.plot(time, data_mainstream_bottom, 'r--', linewidth=3, label='Mainstream: Tower Bottom (Strong Gravity)')
plt.plot(time, data_mainstream_top, 'r:', linewidth=3, label='Mainstream: Tower Top (Weak Gravity)')
plt.plot(time, data_theory_bottom, 'purple', linewidth=4, label='This Theory: Tower Bottom (Topo-Protected)')
plt.plot(time, data_theory_top, 'm:', linewidth=3, label='This Theory: Tower Top (Unprotected)')

plt.title("Unbiased Simulation: Entanglement vs. Decoherence", fontsize=16)
plt.xlabel("Evolution Time (t)", fontsize=14)
plt.ylabel("Concurrence (0 to 1)", fontsize=14)
plt.legend(loc='lower left', fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('fair_quantum_experiment.png', dpi=300)

# 打印实验结论
print("=== 实验数据结果 ===")
print(f"初始纠缠度: {data_mainstream_bottom[0]:.4f}")
print(f"主流模型-塔底(强引力)最终纠缠度: {data_mainstream_bottom[-1]:.4f}")
print(f"本理论-塔底(拓扑保护)最终纠缠度: {data_theory_bottom[-1]:.4f}")
print("结论：在同等噪声下，如果强引力真的导致拓扑折叠，塔底的纠缠度应该显著高于主流预测。")
