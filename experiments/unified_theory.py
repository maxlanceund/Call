import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# 1. 绘制真正的“引力大漏斗” (上宽下窄)
z = np.linspace(0, 15, 100)
theta = np.linspace(0, 2*np.pi, 100)
Z, Theta = np.meshgrid(z, theta)
R = 12 - Z * 0.75 
X = R * np.cos(Theta)
Y = R * np.sin(Theta)

ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.25, edgecolor='none')

# 2. 定义两个纠缠粒子 A 和 B
z_A, z_B = 12, 12
theta_A, theta_B = np.pi/6, np.pi + np.pi/6
r_wall = 12 - z_A * 0.75

x_A, y_A = r_wall * np.cos(theta_A), r_wall * np.sin(theta_A)
x_B, y_B = r_wall * np.cos(theta_B), r_wall * np.sin(theta_B)

# 放大红色粒子，更显眼
ax.scatter([x_A, x_B], [y_A, y_B], [z_A, z_B], color='red', s=200, label='Particles A & B', zorder=5, depthshade=False)

# 3. 宏观相对论路径 (蓝色实线)
theta_path = np.linspace(theta_A, theta_B, 100)
r_path = 12 - z_A * 0.75
x_path = r_path * np.cos(theta_path)
y_path = r_path * np.sin(theta_path)
z_path = np.full_like(theta_path, z_A)
ax.plot(x_path, y_path, z_path, color='blue', linewidth=5, label='Relativity: Light-speed limited path')

# 4. 微观量子纠缠路径 (黄色虚线，在底部奇点汇聚)
# 稍微偏移一点点文字，避免重叠
ax.plot([x_A, 0, x_B], [y_A, 0, y_B], [z_A, 0.5, z_B], color='gold', linewidth=4, linestyle='--', label='Quantum: Zero Distance Link')
ax.scatter([0], [0], [0.5], color='gold', s=200, marker='*', zorder=6) 

# 5. 添加酷炫的文本标注 (调整了位置和大小)
ax.text(0, 0, 17, 'SUPER FUNNEL UNIVERSE', color='black', fontsize=16, fontweight='bold', ha='center')
ax.text(0, 0, -2, 'Global Singularity (Topological Reset)', color='#B8860B', fontsize=11, fontweight='bold', ha='center')
ax.text(6, -6, 12, 'Relativity', color='blue', fontsize=14, fontweight='bold')
ax.text(4, 4, 6, 'Quantum Entanglement', color='#DAA520', fontsize=14, fontweight='bold')

# 6. 视角调整：让 3D 透视感更强
ax.view_init(elev=25, azim=45) 
ax.set_title('Unified Field Theory: The Cosmic Funnel', fontsize=18, pad=20)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.set_box_aspect((1, 1, 1.5)) 

ax.legend(loc='upper right', fontsize=11)
plt.tight_layout()

plt.savefig('unified_theory.png', dpi=300)
print("图已更新生成！")
