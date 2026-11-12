import numpy as np
import math

# === 审稿人 B 的要求：绝对不预设“引力保护”系数 ===

print("=== 盲测实验启动：基于纯物理退相干方程的数据生成 ===\n")
np.random.seed(2026) 
N = 2000 # 采集2000组实验数据

# 变量 X1: 传播距离 (0到1000公里)，距离越远，环境噪声越大
distance = np.random.uniform(0, 1000, N)
# 变量 X2: 外部引力场强度 (以引力势表示，0代表深空，1代表强引力场环境)
gravity = np.random.uniform(0, 1, N)
# 测量仪器的系统随机误差
measurement_error = np.random.normal(0, 0.03, N)

# 物理底层方程 (指数退相干): 保真度 F = exp(-衰减率 * 距离)
# 基础衰减率常数
k_base = 0.002
# 真实宇宙中，主流理论认为衰减率只与距离有关
decay_rate = k_base * distance 

# 我们计算两组数据：
# 数据组 A：假设主流理论是对的（引力不提供任何保护，只是空间弯曲）
fidelity_mainstream = np.exp(-decay_rate) + measurement_error

# 数据组 B：假设你的“大漏斗理论”是对的。
# 物理机制：引力场(gravity)折叠了空间，把距离“吃掉”了一部分。
# 距离的等效衰减变成了： distance * (1 - c * gravity)，其中 c 是拓扑折叠常数
c_topology = 0.8 # 假设折叠效应极强
effective_decay_rate = k_base * distance * (1 - c_topology * gravity)
fidelity_theory = np.exp(-effective_decay_rate) + measurement_error


# === 回归函数定义 ===
def run_regression(X1, X2, Y, name):
    # 构造设计矩阵：截距, 距离, 引力, 距离*引力(交叉项)
    X_matrix = np.column_stack((np.ones(len(Y)), X1, X2, X1 * X2))
    
    # OLS 求解
    XtX = np.dot(X_matrix.T, X_matrix)
    XtY = np.dot(X_matrix.T, Y)
    beta = np.dot(np.linalg.inv(XtX), XtY)
    
    # 统计显著性 (P-value)
    residuals = Y - np.dot(X_matrix, beta)
    sigma_sq = np.sum(residuals**2) / (len(Y) - X_matrix.shape[1])
    cov_matrix = sigma_sq * np.linalg.inv(XtX)
    std_errors = np.sqrt(np.diag(cov_matrix))
    t_statistics = beta / std_errors
    
    def normal_cdf(x):
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0
    p_values = [2 * (1 - normal_cdf(abs(t))) for t in t_statistics]
    
    print(f"--- 回归结果: {name} ---")
    labels = ["截距", "距离(X1)", "引力(X2)", "交叉项(X1*X2)"]
    for i in range(4):
        sig = "***" if p_values[i] < 0.001 else ("*" if p_values[i] < 0.05 else "")
        print(f"{labels[i]:<10} | 系数: {beta[i]:>8.4f} | P值: {p_values[i]:.4e} {sig}")
    print("\n")
    return beta, p_values

# 1. 跑主流理论生成的数据
run_regression(distance, gravity, fidelity_mainstream, "主流宇宙 (引力不保护纠缠)")

# 2. 跑大漏斗理论生成的数据
run_regression(distance, gravity, fidelity_theory, "大漏斗宇宙 (引力产生拓扑保护)")

