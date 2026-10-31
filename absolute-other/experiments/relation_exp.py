import random
import math

random.seed(42)

# 1. 生成 SBM 图
N = 200
n_comm = N // 2
p_in, p_out = 0.3, 0.05
labels = [0]*n_comm + [1]*n_comm

adj = [[] for _ in range(N)]
for i in range(N):
    for j in range(i+1, N):
        p = p_in if labels[i] == labels[j] else p_out
        if random.random() < p:
            adj[i].append(j)
            adj[j].append(i)

# 2. 内在属性
d = 10
X = [[random.gauss(0, 1) for _ in range(d)] for _ in range(N)]

# 3. 消息传递生成身份
K = 5
alpha = 0.6
H = [row[:] for row in X]

for t in range(K):
    new_H = []
    for i in range(N):
        if adj[i]:
            neigh_mean = [sum(H[j][k] for j in adj[i]) / len(adj[i]) for k in range(d)]
        else:
            neigh_mean = [0.0]*d
        h_new = [(1-alpha)*H[i][k] + alpha*neigh_mean[k] for k in range(d)]
        new_H.append(h_new)
    H = new_H

# 4. 最近质心分类器
def centroid_classifier(features, labels, n_classes=2):
    centroids = []
    for c in range(n_classes):
        idx = [i for i in range(len(labels)) if labels[i] == c]
        centroid = [sum(features[i][k] for i in idx) / len(idx) for k in range(len(features[0]))]
        centroids.append(centroid)
    correct = 0
    for i in range(len(features)):
        dists = [sum((features[i][k] - centroids[c][k])**2 for k in range(len(features[0]))) for c in range(n_classes)]
        pred = dists.index(min(dists))
        if pred == labels[i]:
            correct += 1
    return correct / len(features)

acc_H = centroid_classifier(H, labels)
acc_X = centroid_classifier(X, labels)

# 5. 真正的谱嵌入：幂迭代 + deflation，求第二特征向量
def mat_vec(adj, v):
    return [sum(v[j] for j in adj[i]) for i in range(len(adj))]

def power_iter(adj, n_iter=300):
    n = len(adj)
    v = [random.random() for _ in range(n)]
    for _ in range(n_iter):
        nv = mat_vec(adj, v)
        norm = math.sqrt(sum(x*x for x in nv))
        if norm < 1e-12:
            break
        v = [x/norm for x in nv]
    Av = mat_vec(adj, v)
    lam = sum(v[i]*Av[i] for i in range(n))
    return v, lam

def deflated_mat_vec(adj, v1, lam1, v):
    Av = mat_vec(adj, v)
    dot = sum(v1[i]*v[i] for i in range(len(v)))
    return [Av[i] - lam1*v1[i]*dot for i in range(len(v))]

def power_iter_deflated(adj, v1, lam1, n_iter=300):
    n = len(adj)
    v = [random.random() for _ in range(n)]
    for _ in range(n_iter):
        nv = deflated_mat_vec(adj, v1, lam1, v)
        norm = math.sqrt(sum(x*x for x in nv))
        if norm < 1e-12:
            break
        v = [x/norm for x in nv]
    return v

v1, lam1 = power_iter(adj)
v2 = power_iter_deflated(adj, v1, lam1)
spec_embed = [[v2[i]] for i in range(N)]
acc_G = centroid_classifier(spec_embed, labels)

# 6. 输出
print(f"acc_H (身份 H 预测社区): {acc_H:.4f}")
print(f"acc_X (内在属性 X 预测社区): {acc_X:.4f}")
print(f"acc_G (谱嵌入预测社区): {acc_G:.4f}")
print()
print("核心结论：")
print(f"  acc_H - acc_X = {acc_H - acc_X:.4f}（应显著大于 0）")
print(f"  acc_H / acc_G = {acc_H / acc_G:.4f}（应接近 1）")
