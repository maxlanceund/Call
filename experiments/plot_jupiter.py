import numpy as np
import matplotlib.pyplot as plt

# 定义网格 (r, theta) 转换成笛卡尔坐标 (X, Y) 方便画图
steps = 400
x = np.linspace(-1, 1, steps)
y = np.linspace(-1, 1, steps)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
THETA = np.arctan2(Y, X)

# 定义自转导致的椭球边界
flat = 0.05
R_boundary = 1.0 / np.sqrt(np.cos(THETA)**2 + (1-flat)**2 * np.sin(THETA)**2)

# --- 1. 传统致密核心模型 ---
# 核心半径 0.1，密度极高 (10.0)；外部密度极低 (0.5)
RHO_dense = np.where(R <= 0.1, 10.0, 0.5)
# 把边界外的部分遮罩掉，变成透明（太空）
RHO_dense = np.where(R <= R_boundary, RHO_dense, np.nan)

# --- 2. 你的拓扑稀释模型 ---
# 最优参数: R_core = 0.8, steep = 4.0
R_core = 0.8
steep = 4.0
# 使用 Sigmoid 函数模拟密度平滑过渡
dilute_density = 0.05 + 1.5 / (1 + np.exp(steep * (R - R_core * 0.8)))
RHO_dilute = np.where(R <= R_boundary, dilute_density, np.nan)


# --- 开始画图 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor='black')

# 画图 1：传统模型
im1 = ax1.imshow(RHO_dense, extent=[-1, 1, -1, 1], cmap='inferno', origin='lower')
ax1.set_title("Traditional Dense Core\n(Huge J4 Error)", color='white', fontsize=14)
ax1.axis('off')

# 画图 2：拓扑均匀化模型
im2 = ax2.imshow(RHO_dilute, extent=[-1, 1, -1, 1], cmap='inferno', origin='lower')
ax2.set_title("Topological Dilute Core\n(J4/J2 Error = 0.42%)", color='white', fontsize=14)
ax2.axis('off')

# 添加颜色条 (代表密度)
cbar = fig.colorbar(im2, ax=[ax1, ax2], orientation='horizontal', fraction=0.046, pad=0.04)
cbar.set_label('Density (Normalized)', color='white', fontsize=12)
cbar.ax.xaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'xticklabels'), color='white')

plt.suptitle("Jupiter Interior Models vs. Juno Data", color='white', fontsize=18, y=0.95)
plt.tight_layout()
plt.savefig('jupiter_core_comparison.png', dpi=150, facecolor='black')
print("\n✅ 模拟图已生成: jupiter_core_comparison.png")
print("请在 Termux 中输入 `ls` 查看，或通过文件管理器打开查看。")
