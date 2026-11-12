import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# 自动寻找解压出来的所有 .dat 文件
files = glob.glob('*.dat')
if not files:
    print("没找到数据文件！")
    exit()

# 找最大的文件（通常是样本最全的）
target_file = max(files, key=os.path.getsize)
print(f"正在读取真实引力波数据: {target_file}")

# 读取数据（跳过表头）
try:
    # LIGO 的 dat 文件有时候用空格，有时候用制表符，这里用 np.loadtxt 自动处理
    data = np.loadtxt(target_file)
except Exception as e:
    print(f"读取失败，尝试用 pandas 或其他方式: {e}")
    # 备用方案：读取前 50000 行
    data = []
    with open(target_file, 'r') as f:
        for i, line in enumerate(f):
            if i == 0: continue
            try:
                data.append([float(x) for x in line.split()])
            except: continue
            if len(data) >= 50000: break
    data = np.array(data)

print(f"成功加载数据！形状为: {data.shape} (行数, 列数)")

# 一般来说，LIGO 的列包含 m1, m2, 自旋，最后几列是 lambda1, lambda2, lambda_tilde
# 我们取最后三列分别画图
fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor='black')

for i in range(3):
    col_idx = -(3 - i)
    axes[i].hist(data[:, col_idx], bins=100, color=['cyan', 'magenta', 'yellow'][i], alpha=0.7, edgecolor='black', density=True)
    axes[i].set_title(f'Column {col_idx} (Last {3-i}th)', color='white')
    axes[i].tick_params(colors='white')
    axes[i].set_facecolor('black')
    for spine in axes[i].spines.values():
        spine.set_color('white')

plt.suptitle(f'GW170817 Posterior Samples: {os.path.basename(target_file)}', color='white', fontsize=16)
plt.tight_layout()
plt.savefig('ligo_lambda_check.png', dpi=150, bbox_inches='tight', facecolor='black')
print("✅ 图表已保存为 ligo_lambda_check.png")
