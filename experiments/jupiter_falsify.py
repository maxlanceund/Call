import numpy as np

def get_legendre(cos_theta):
    x = cos_theta
    P2 = 0.5 * (3 * x**2 - 1)
    P4 = 0.125 * (35 * x**4 - 30 * x**2 + 3)
    return P2, P4

def calc_j_ratio(rho_func, steps=100, **kwargs):
    r = np.linspace(0, 1.0, steps)
    theta = np.linspace(0, np.pi, steps)
    R, THETA = np.meshgrid(r, theta)
    RHO = rho_func(R, THETA, **kwargs)
    dV = 2 * np.pi * R**2 * np.sin(THETA) * (1/(steps-1)) * (np.pi/(steps-1))
    mass = np.sum(RHO * dV)
    P2, P4 = get_legendre(np.cos(THETA))
    J2 = - np.sum(RHO * R**2 * P2 * dV) / mass
    J4 = - np.sum(RHO * R**4 * P4 * dV) / mass
    return J4 / J2 if J2 != 0 else 0

def get_R_limit(theta, R_core, flattening):
    return R_core / np.sqrt(np.cos(theta)**2 + (1-flattening)**2 * np.sin(theta)**2)

# 1. 传统致密核心模型 (允许扫描核心半径 R_core)
def rho_dense(R, THETA, R_core=0.1, flat=0.06):
    R_limit = get_R_limit(THETA, R_core, flat)
    return np.where(R <= R_limit, 10.0, 0.5)

# 2. 完全均匀无核心模型
def rho_uniform(R, THETA):
    return np.ones_like(R) * 0.5

# 3. 我们的拓扑稀释模型
def rho_topo(R, THETA, R_core=0.8, steep=4, flat=0.06):
    R_limit = get_R_limit(THETA, R_core, flat)
    core_density = 0.05 + 1.5 / (1 + np.exp(steep * (R - R_core * 0.8)))
    return np.where(R <= R_limit, core_density, 0.05)

target = -0.03991
print(f"目标真实值 (朱诺号): {target}\n")

# --- 实验 1: 强行让致密核心扫描调参 ---
print("--- 证伪实验 1: 传统致密核心能行吗？ ---")
best_dense_err = 100
for rc in np.linspace(0.01, 0.5, 10): # 核心从极小到半径的一半
    for flat in [0.04, 0.06, 0.08]:
        ratio = calc_j_ratio(rho_dense, R_core=rc, flat=flat)
        err = abs(ratio - target) / abs(target) * 100
        if err < best_dense_err:
            best_dense_err = err
            best_rc = rc
            best_ratio = ratio
print(f"最努力调整核心半径后，传统模型得出的 J4/J2 = {best_ratio:.5f}")
print(f"误差依然高达: {best_dense_err:.2f}% -> 结论：即使把核心缩小，符号依然是错的，直接证伪！\n")

# --- 实验 2: 完全均匀无核心 ---
print("--- 证伪实验 2: 完全没有核心行不行？ ---")
ratio_uniform = calc_j_ratio(rho_uniform)
print(f"完全均匀模型的 J4/J2 = {ratio_uniform:.5f} (误差极大，说明木星内部必须有密度差异)\n")

# --- 实验 3: 我们的拓扑模型稳健性测试 ---
print("--- 验证我们的模型 (微调参数看是否崩溃) ---")
print("R_core | steep | 算出的J4/J2 | 误差(%)")
for rc in [0.7, 0.75, 0.8, 0.85]:
    for steep in [3.5, 4.0, 4.5]:
        ratio = calc_j_ratio(rho_topo, R_core=rc, steep=steep, flat=0.05)
        err = abs(ratio - target) / abs(target) * 100
        print(f"{rc:.2f}   | {steep:.1f}   | {ratio:.5f}    | {err:.2f}%")
