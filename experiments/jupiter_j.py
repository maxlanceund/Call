import numpy as np
import time

def get_legendre(cos_theta):
    """
    手写勒让德多项式，代替 SciPy，速度快且免安装
    """
    x = cos_theta
    P2 = 0.5 * (3 * x**2 - 1)
    P4 = 0.125 * (35 * x**4 - 30 * x**2 + 3)
    P6 = 0.0625 * (231 * x**6 - 315 * x**4 + 105 * x**2 - 5)
    return P2, P4, P6

def calc_j_moments(rho_func, steps=200):
    print(f"正在计算，网格分辨率: {steps}x{steps} ...")
    start_time = time.time()
    
    # 构建二维网格 (r, theta)
    r = np.linspace(0, 1.0, steps)
    theta = np.linspace(0, np.pi, steps)
    R, THETA = np.meshgrid(r, theta)
    
    # 计算密度分布
    RHO = rho_func(R, THETA)
    
    # 计算体积元权重 dV
    dr = 1.0 / (steps - 1)
    dtheta = np.pi / (steps - 1)
    dV = 2 * np.pi * R**2 * np.sin(THETA) * dr * dtheta
    
    # 积分计算质量
    mass = np.sum(RHO * dV)
    
    # 直接调用手写的勒让德多项式
    COS_T = np.cos(THETA)
    P2, P4, P6 = get_legendre(COS_T)
    
    # 积分计算 J2, J4, J6
    J2 = - np.sum(RHO * R**2 * P2 * dV) / mass
    J4 = - np.sum(RHO * R**4 * P4 * dV) / mass
    J6 = - np.sum(RHO * R**6 * P6 * dV) / mass
    
    print(f"计算耗时: {time.time() - start_time:.2f} 秒\n")
    return mass, J2, J4, J6

# 定义自转导致的椭球形状
def get_R_limit(theta, R_core, flattening=0.06):
    return R_core / np.sqrt(np.cos(theta)**2 + (1-flattening)**2 * np.sin(theta)**2)

# 模型 A：传统致密核心
def rho_dense(R, THETA):
    R_core = get_R_limit(THETA, R_core=0.1)
    return np.where(R <= R_core, 10.0, 0.5)

# 模型 B：你的拓扑均匀化/稀释核心
def rho_dilute(R, THETA):
    R_core = get_R_limit(THETA, R_core=0.63)
    core_density = 0.1 + 1.5 / (1 + np.exp(10 * (R - 0.3)))
    return np.where(R <= R_core, core_density, 0.1)

# 执行计算
m_a, j2_a, j4_a, j6_a = calc_j_moments(rho_dense)
m_b, j2_b, j4_b, j6_b = calc_j_moments(rho_dilute)

# 真实观测数据（朱诺号）
real_j2 = 14696.5
real_j4 = -586.6
real_j4_j2_ratio = real_j4 / real_j2

print(f"--- 模型 A (传统致密核心) ---")
print(f"J2: {j2_a:.4e}, J4: {j4_a:.4e}, J6: {j6_a:.4e}")
print(f"J4/J2 比例: {j4_a / j2_a:.5f}\n")

print(f"--- 模型 B (你的拓扑均匀化) ---")
print(f"J2: {j2_b:.4e}, J4: {j4_b:.4e}, J6: {j6_b:.4e}")
print(f"J4/J2 比例: {j4_b / j2_b:.5f}\n")

print(f"--- 朱诺号真实观测 ---")
print(f"J2: {real_j2:.4e}, J4: {real_j4:.4e}")
print(f"J4/J2 比例: {real_j4_j2_ratio:.5f}\n")

print("--- 结论对比 ---")
print(f"致密核心模型误差: {abs((j4_a/j2_a) - real_j4_j2_ratio) / real_j4_j2_ratio * 100:.2f}%")
print(f"拓扑均匀化误差: {abs((j4_b/j2_b) - real_j4_j2_ratio) / real_j4_j2_ratio * 100:.2f}%")

