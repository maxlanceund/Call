import numpy as np
from scipy.integrate import solve_ivp
import os

# ==========================================
# 1. 真实物理常数 (CGS 单位制)
# ==========================================
G = 6.67430e-8       # 引力常数 (cm^3 / g s^2)
c = 2.99792458e10    # 光速 (cm/s)
Msun = 1.98847e33    # 太阳质量 (g)

# ==========================================
# 2. 状态方程 (EoS)
# ==========================================
def eos_hard(rho):
    K = 1.0e5; Gamma = 3.0 
    P = K * rho**Gamma
    eps = rho + P / (c**2)
    return P, eps

def eos_soft(rho):
    K = 1.5e5; Gamma = 2.0 
    P = K * rho**Gamma
    eps = rho + P / (c**2)
    return P, eps

# ==========================================
# 3. TOV 方程与潮汐形变
# ==========================================
def tov_equations(r, y, eos_func):
    m, P, y_love = y
    if P <= 0: return [0, 0, 0]
    
    rho = (P / 1e5)**(1/3) if eos_func == eos_hard else (P / 1.5e5)**(1/2)
    _, eps = eos_func(rho)
    
    dm_dr = 4 * np.pi * r**2 * eps
    
    num_p = -G * (eps + P / c**2) * (m + 4 * np.pi * r**3 * P / c**2)
    den_p = r * (r - 2 * G * m / c**2)
    dp_dr = num_p / den_p
    
    F = (1 - 4 * np.pi * r**2 * (eps - P / c**2)) / (1 - 2 * G * m / (r * c**2))
    Q = (4 * np.pi * (5 * eps + 9 * P / c**2 + (eps + P / c**2) * dp_dr) - 6 / r**2) / (1 - 2 * G * m / (r * c**2))
    dy_dr = -(y_love**2 + y_love * F + r**2 * Q) / r
    
    return [dm_dr, dp_dr, dy_dr]

def solve_star(central_pressure, eos_func):
    r0 = 1.0; m0 = 0.0; y0 = 2.0
    
    def surface_event(r, y): return y[1]
    surface_event.terminal = True
    
    sol = solve_ivp(
        tov_equations, [r0, 2e6], [m0, central_pressure, y0],
        args=(eos_func,), events=surface_event, 
        rtol=1e-6, atol=1e-8, max_step=1000.0
    )
    
    R = sol.t[-1]
    M = sol.y[0, -1] / Msun
    y_R = sol.y[2, -1]
    
    k2 = (1 + y_R) / 2
    C = G * M * Msun / (R * c**2)
    Lambda = (2 / 3) * k2 / (C**5)
    
    return M, Lambda 

# ==========================================
# 4. 跑数据并输出为 CSV
# ==========================================
print("开始计算 TOV 方程...")
test_pressures = np.linspace(1e30, 1e35, 15) # 扫描中心压强

hard_data = []
soft_data = []

for p in test_pressures:
    m_h, l_h = solve_star(p, eos_hard)
    hard_data.append([m_h, l_h])
    
    m_s, l_s = solve_star(p, eos_soft)
    soft_data.append([m_s, l_s])

# 只筛选质量在 1.0 到 2.5 太阳质量范围内的数据
hard_valid = [row for row in hard_data if 1.0 <= row[0] <= 2.5]
soft_valid = [row for row in soft_data if 1.0 <= row[0] <= 2.5]

# 保存为 CSV 文件
np.savetxt("data_hard_core.csv", np.array(hard_valid), delimiter=",", header="Mass(Msun),Lambda", comments="")
np.savetxt("data_soft_core.csv", np.array(soft_valid), delimiter=",", header="Mass(Msun),Lambda", comments="")

print("✅ 数据计算完毕！已生成 data_hard_core.csv 和 data_soft_core.csv")
