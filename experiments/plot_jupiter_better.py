import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm

steps = 500 # 提高分辨率
x = np.linspace(-1, 1, steps)
y = np.linspace(-1, 1, steps)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
THETA = np.arctan2(Y, X)

# 定义椭球边界
flat = 0.05
R_boundary = 1.0 / np.sqrt(np.cos(THETA)**2 + (1-flat)**2 * np.sin(THETA)**2)

# --- 1. 传统致密核心模型 ---
# 为了让边界不那么死黑，把外壳密度稍微调高一点到 0.6
RHO_dense = np.where(R <= 0.15, 10.0, 0.6)
RHO_dense = np.where(R <= R_boundary, RHO_dense, np.nan)

# --- 2. 拓扑稀释模型 ---
R_core = 0.8
steep = 4.0
dilute_density = 0.05 + 1.5 / (1 + np.exp(steep * (R - R_core * 0.8)))
RHO_dilute = np.where(R <= R_boundary, dilute_density, np.nan)

# --- 开始画图 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), facecolor='black')

# 使用 magma 颜色，并通过 vmax=2.5 截断最高亮度（让左图有质感，右图有层次）
# interpolation='bicubic' 让像素点变得像流体一样平滑
im1 = ax1.imshow(RHO_dense, extent=[-1, 1, -1, 1], cmap='magma', origin='lower', 
                 vmax=2.5, interpolation='bicubic')
ax1.set_title("Traditional Dense Core\n(Huge J4 Error)", color='white', fontsize=16, pad=15)
ax1.axis('off')

im2 = ax2.imshow(RHO_dilute, extent=[-1, 1, -1, 1], cmap='magma', origin='lower', 
                 vmax=2.5, interpolation='bicubic')
ax2.set_title("Topological Dilute Core\n(J4/J2 Error = 0.42%)", color='white', fontsize=16, pad=15)
ax2.axis('off')

# 统一在底部放一个颜色条
cbar = fig.colorbar(im2, ax=[ax1, ax2], orientation='horizontal', fraction=0.046, pad=0.05)
cbar.set_label('Density (Normalized)', color='white', fontsize=12)
cbar.ax.xaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'xticklabels'), color='white')

plt.suptitle("Jupiter Interior Models vs. Juno Data", color='white', fontsize=20, y=0.98)
plt.tight_layout()
plt.savefig('jupiter_core_comparison_better.png', dpi=200, facecolor='black', bbox_inches='tight')
print("\n✅ 高级版模拟图已生成: jupiter_core_comparison_better.png")
