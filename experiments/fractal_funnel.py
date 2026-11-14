import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 10))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off') # 隐藏坐标轴，画纯示意图

# 1. 绘制宇宙大漏斗的外轮廓
top_width = 90
bottom_x = 50
bottom_y = 10
funnel_left = np.linspace(5, bottom_x, 100)
funnel_right = np.linspace(95, bottom_x, 100)
funnel_y = np.linspace(90, bottom_y, 100)

# 填充大漏斗的渐变背景
ax.fill_betweenx(funnel_y, funnel_left, funnel_right, color='lightblue', alpha=0.2)
ax.plot(funnel_left, funnel_y, color='black', linewidth=2, label='Cosmic Event Horizon (Super Funnel)')
ax.plot(funnel_right, funnel_y, color='black', linewidth=2)

# 2. 绘制局部黑洞（小漏斗缓存）
# 小漏斗A
ax.plot([25, 30, 20], [75, 65, 65], color='purple', linewidth=3)
ax.fill_between([20, 30], 65, 75, color='purple', alpha=0.3)
ax.text(25, 77, 'Local Black Hole (Cache A)', ha='center', fontsize=10)

# 小漏斗B
ax.plot([70, 75, 65], [60, 50, 50], color='purple', linewidth=3)
ax.fill_between([65, 75], 50, 60, color='purple', alpha=0.3)
ax.text(70, 62, 'Local Black Hole (Cache B)', ha='center', fontsize=10)

# 3. 绘制底部全局奇点（终极相变点）
ax.scatter(bottom_x, bottom_y, color='red', s=300, zorder=5)
ax.text(bottom_x, bottom_y - 5, 'GLOBAL SINGULARITY\n(Topological Reset)', ha='center', fontsize=12, color='red', fontweight='bold')

# 4. 绘制物质下落的箭头（信息流）
# 表面物质掉入局部黑洞
ax.annotate('', xy=(24, 65), xytext=(15, 85), arrowprops=dict(arrowstyle="->", color="gray", lw=1.5, ls="--"))
ax.annotate('', xy=(71, 50), xytext=(85, 80), arrowprops=dict(arrowstyle="->", color="gray", lw=1.5, ls="--"))

# 局部黑洞漏向全局奇点
ax.annotate('', xy=(50, 15), xytext=(25, 62), arrowprops=dict(arrowstyle="->", color="purple", lw=2, ls="-", alpha=0.7))
ax.annotate('', xy=(50, 15), xytext=(70, 47), arrowprops=dict(arrowstyle="->", color="purple", lw=2, ls="-", alpha=0.7))

# 大漏斗壁上的物质直接下漏
ax.annotate('', xy=(50, 20), xytext=(80, 60), arrowprops=dict(arrowstyle="->", color="gray", lw=2, ls="-."))
ax.annotate('', xy=(50, 20), xytext=(15, 50), arrowprops=dict(arrowstyle="->", color="gray", lw=2, ls="-."))

# 5. 添加高级感文字标注
ax.text(50, 95, 'Fractal Funnel Universe: The Hierarchical Collapse of Information', 
        ha='center', fontsize=16, fontweight='bold')
ax.text(50, 85, 'All causal chains eventually flow to the global singularity before the phase transition.', 
        ha='center', fontsize=11, style='italic')

ax.text(15, 30, 'Safe Caching Zone\n(System is still evolving)', fontsize=12, color='green', fontweight='bold')
ax.text(75, 20, 'Direct Descent\n(Gravity Flow)', fontsize=12, color='gray')

plt.tight_layout()
plt.savefig('fractal_funnel.png', dpi=300)
print("图4已生成！")
