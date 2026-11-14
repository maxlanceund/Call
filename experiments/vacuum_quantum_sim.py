import numpy as np
import matplotlib.pyplot as plt

# === 纯 NumPy 计算纠缠度函数 ===
def concurrence(rho):
    Y = np.array([[0, -1j], [1j, 0]])
    YY = np.kron(Y, Y)
    rho_tilde = YY @ rho.conj() @ YY
    M = rho @ rho_tilde
    eigenvalues = np.linalg.eigvals(M)
    sqrt_eigenvalues = np.sqrt(np.clip(np.real(eigenvalues), 0, None))
    sqrt_eigenvalues = np.sort(sqrt_eigenvalues)[::-1]
    return max(0, sqrt_eigenvalues[0] - sqrt_eigenvalues[1] - sqrt_eigenvalues[2] - sqrt_eigenvalues[3])

# === 1. 初始完美纠缠态 (Bell态) ===
state_00 = np.array([1, 0, 0, 0])
state_11 = np.array([0, 0, 0, 1])
psi = (state_00 + state_11) / np.sqrt(2)
rho_init = np.outer(psi, psi.conj())

# === 2. 设定理想真空环境 ===
time = np.linspace(0, 100, 1000) # 拉长时间，看极限演化

# 因为是绝对真空，基础环境退相干率为 0
gamma_env = 0.0 

# 但引力场依然存在（模拟在强引力场附近悬停）
# 主流认为，引力场本身的潮汐力会导致极其微弱的引力退相干 (gamma_gravity)
gamma_gravity = 0.005 

data_mainstream = []
data_theory = []

for t in time:
    # --- 主流物理（红线） ---
    # 即使在真空，引力带来的时空扭曲也会让波函数产生微小的相位随机化
    # 纠缠度缓慢下降
    decay_m = np.exp(-gamma_gravity * t)
    rho_m = rho_init.copy()
    rho_m[0, 3] *= decay_m
    rho_m[3, 0] *= decay_m
    data_mainstream.append(concurrence(rho_m))

    # --- 你的大漏斗理论（紫线） ---
    # 在真空+引力场下，大漏斗的“拓扑折叠”效应完全凸显
    # 引力强，导致底层空间距离直接坍缩为0。底层连通性死死锁住纠缠。
    # 在数学上，拓扑保护抵消了引力退相干
    topology_protection = 1.0 # 100% 保护
    decay_t = np.exp(-gamma_gravity * (1 - topology_protection) * t)
    rho_t = rho_init.copy()
    rho_t[0, 3] *= decay_t
    rho_t[3, 0] *= decay_t
    data_theory.append(concurrence(rho_t))

# === 3. 绘图结果 ===
plt.figure(figsize=(10, 6))
plt.plot(time, data_mainstream, 'r--', linewidth=3, label='Mainstream: Gravitational Tidal Decoherence')
plt.plot(time, data_theory, 'purple', linewidth=4, label='This Theory: Topological Protection (Invisible Hand)')

plt.title("Vacuum Simulation: Pure Gravity vs. Topological Entanglement", fontsize=16)
plt.xlabel("Evolution Time in Vacuum (t)", fontsize=14)
plt.ylabel("Entanglement Fidelity (Concurrence)", fontsize=14)
plt.legend(loc='center right', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('vacuum_quantum_sim.png', dpi=300)

print("=== 纯真空模拟结果 ===")
print(f"模拟时间结束(t=100)时：")
print(f"主流引力退相干预测: {data_mainstream[-1]:.4f}")
print(f"本理论拓扑保护预测: {data_theory[-1]:.4f}")
print("结论：在纯真空中，所有杂音剔除，如果引力真的折叠了底层空间，纠缠度将如紫线般完美保持。")
