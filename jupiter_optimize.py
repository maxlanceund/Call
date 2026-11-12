import numpy as np

def get_legendre(cos_theta):
    x = cos_theta
    P2 = 0.5 * (3 * x**2 - 1)
    P4 = 0.125 * (35 * x**4 - 30 * x**2 + 3)
    P6 = 0.0625 * (231 * x**6 - 315 * x**4 + 105 * x**2 - 5)
    return P2, P4, P6

def calc_j_ratio(rho_func, steps=100, **kwargs):
    r = np.linspace(0, 1.0, steps)
    theta = np.linspace(0, np.pi, steps)
    R, THETA = np.meshgrid(r, theta)
    
    RHO = rho_func(R, THETA, **kwargs)
    
    dr = 1.0 / (steps - 1)
    dtheta = np.pi / (steps - 1)
    dV = 2 * np.pi * R**2 * np.sin(THETA) * dr * dtheta
    
    mass = np.sum(RHO * dV)
    
    COS_T = np.cos(THETA)
    P2, P4, P6 = get_legendre(COS_T)
    
    J2 = - np.sum(RHO * R**2 * P2 * dV) / mass
    J4 = - np.sum(RHO * R**4 * P4 * dV) / mass
    
    return J4 / J2 if J2 != 0 else 0

def get_R_limit(theta, R_core, flattening):
    return R_core / np.sqrt(np.cos(theta)**2 + (1-flattening)**2 * np.sin(theta)**2)

def rho_topo(R, THETA, R_core=0.6, steep=5.0, flat=0.06):
    """参数可调的超均匀拓扑模型"""
    R_limit = get_R_limit(THETA, R_core, flat)
    # 假设核心密度随半径平滑下降（模拟拓扑均匀化）
    core_density = 0.05 + 1.5 / (1 + np.exp(steep * (R - R_core * 0.8)))
    return np.where(R <= R_limit, core_density, 0.05)

# 目标比例（朱诺号观测值）
target_ratio = -586.6 / 14696.5 

best_error = 100.0
best_params = {}

print(f"目标 J4/J2 比例: {target_ratio:.5f}")
print("正在全自动暴力扫描参数，寻找完美物理模型...\n")

# 参数扫描循环（穷举网格）
for R_core in np.linspace(0.4, 0.8, 9):
    for steep in [2, 4, 6, 8, 10]:
        for flat in [0.05, 0.06, 0.07, 0.08]:
            ratio = calc_j_ratio(rho_topo, R_core=R_core, steep=steep, flat=flat)
            error = abs(ratio - target_ratio) / abs(target_ratio) * 100
            
            if error < best_error:
                best_error = error
                best_params = {
                    '核心半径延伸(R_core)': R_core,
                    '密度过渡陡度(steep)': steep,
                    '自转扁率(flat)': flat,
                    '计算得出的J4/J2': ratio
                }

print("--- 穷举完成 ---")
print(f"最佳物理参数组合:")
for key, val in best_params.items():
    print(f"{key}: {val}")
print(f"\n与朱诺号真实观测的最小误差: {best_error:.2f}%")

# 用最佳参数重新打印一遍J2和J4，看看实际物理量级
def print_best_details():
    steps = 200
    r = np.linspace(0, 1.0, steps)
    theta = np.linspace(0, np.pi, steps)
    R, THETA = np.meshgrid(r, theta)
    RHO = rho_topo(R, THETA, **{k: v for k, v in best_params.items() if k in ['R_core', 'steep', 'flat']})
    
    dV = 2 * np.pi * R**2 * np.sin(THETA) * (1/(steps-1)) * (np.pi/(steps-1))
    mass = np.sum(RHO * dV)
    COS_T = np.cos(THETA)
    P2, P4, _ = get_legendre(COS_T)
    
    j2 = - np.sum(RHO * R**2 * P2 * dV) / mass
    j4 = - np.sum(RHO * R**4 * P4 * dV) / mass
    print(f"\n--- 最佳模型细节 ---")
    print(f"模拟的 J2 系数: {j2:.4e}")
    print(f"模拟的 J4 系数: {j4:.4e}")

print_best_details()
