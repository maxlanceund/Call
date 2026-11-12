import numpy as np
from scipy.integrate import solve_ivp

G = 6.67430e-8; c = 2.99792458e10; Msun = 1.98847e33

def eos_hard(rho):
    P = 1.0e5 * rho**3.0
    return P, rho + P / (c**2)

def eos_soft(rho):
    P = 1.5e5 * rho**2.0
    return P, rho + P / (c**2)

def tov_equations(r, y, eos_func):
    m, P, y_love = y
    if P <= 0: return [0, 0, 0]
    rho = (P / 1e5)**(1/3) if eos_func == eos_hard else (P / 1.5e5)**(1/2)
    _, eps = eos_func(rho)
    dm_dr = 4 * np.pi * r**2 * eps
    dp_dr = -G * (eps + P / c**2) * (m + 4 * np.pi * r**3 * P / c**2) / (r * (r - 2 * G * m / c**2))
    F = (1 - 4 * np.pi * r**2 * (eps - P / c**2)) / (1 - 2 * G * m / (r * c**2))
    Q = (4 * np.pi * (5 * eps + 9 * P / c**2 + (eps + P / c**2) * dp_dr) - 6 / r**2) / (1 - 2 * G * m / (r * c**2))
    dy_dr = -(y_love**2 + y_love * F + r**2 * Q) / r
    return [dm_dr, dp_dr, dy_dr]

def solve_star(central_pressure, eos_func):
    def surface_event(r, y): return y[1]
    surface_event.terminal = True
    try:
        sol = solve_ivp(tov_equations, [1.0, 2e6], [0.0, central_pressure, 2.0],
                        args=(eos_func,), events=surface_event, rtol=1e-6, atol=1e-8, max_step=1000.0)
        R = sol.t[-1]; M = sol.y[0, -1] / Msun; y_R = sol.y[2, -1]
        Lambda = (2 / 3) * ((1 + y_R) / 2) / ((G * M * Msun / (R * c**2))**5)
        return M, Lambda 
    except:
        return np.nan, np.nan

test_pressures = np.linspace(1e28, 1e35, 30)
hard_data, soft_data = [], []
for p in test_pressures:
    m_h, l_h = solve_star(p, eos_hard)
    hard_data.append([m_h, l_h])
    m_s, l_s = solve_star(p, eos_soft)
    soft_data.append([m_s, l_s])

# 强制保存全部数据，绝不过滤！
np.savetxt("data_hard_core.csv", np.array(hard_data), delimiter=",", header="Mass,Lambda", comments="")
np.savetxt("data_soft_core.csv", np.array(soft_data), delimiter=",", header="Mass,Lambda", comments="")
print("全部数据已计算完毕并强制写入 CSV。")
print("====== HARD_CORE ======")
for row in hard_data: print(row)
print("====== SOFT_CORE ======")
for row in soft_data: print(row)
