import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_logo(mode='dark'):
    fig, ax = plt.subplots(figsize=(10, 10), dpi=120)
    fig.patch.set_facecolor('#0D1117' if mode == 'dark' else '#F4F1EA')
    ax.set_facecolor('#0D1117' if mode == 'dark' else '#F4F1EA')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    text_color = '#FFFFFF' if mode == 'dark' else '#1A1A1A'
    accent_color = '#58A6FF' # GitHub 蓝

    if mode == 'dark':
        # 暗黑风：画一个 >_ 
        ax.text(30, 45, ">", fontsize=150, color=text_color, family='monospace', weight='bold')
        # 画光标方块
        rect = patches.Rectangle((58, 28), 12, 8, linewidth=0, facecolor=accent_color)
        ax.add_patch(rect)
    else:
        # 古白风：画 [ C ]
        ax.text(15, 40, "[", fontsize=140, color=text_color, family='monospace')
        ax.text(42, 40, "C", fontsize=140, color=text_color, family='monospace', weight='bold')
        ax.text(72, 40, "]", fontsize=140, color=text_color, family='monospace')

    # 保存图片
    filename = f"call_logo_{mode}.png"
    plt.savefig(filename, bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor())
    print(f"已生成: {filename}")

draw_logo('dark')
draw_logo('paper')
