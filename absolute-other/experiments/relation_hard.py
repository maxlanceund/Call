import random
import math

# ============ 数据生成 ============
def generate_sbm(N, n_classes, p_in, p_out, seed):
    random.seed(seed)
    n_comm = N // n_classes
    labels = [min(i // n_comm, n_classes - 1) for i in range(N)]
    adj = [[] for _ in range(N)]
    for i in range(N):
        for j in range(i+1, N):
            p = p_in if labels[i] == labels[j] else p_out
            if random.random() < p:
                adj[i].append(j)
                adj[j].append(i)
    return adj, labels

def generate_X(N, D, labels, signal_strength, seed):
    random.seed(seed + 1)
    X = []
    for i in range(N):
        signal = [signal_strength if k == labels[i] % D else 0.0 for k in range(D)]
        noise = [random.gauss(0, 1) for _ in range(D)]
        X.append([signal[k] + noise[k] for k in range(D)])
    return X

# ============ 5折交叉验证 ============
def cross_val_acc(features, labels, n_folds=5, n_classes=3, seed=0):
    N = len(features)
    rng = random.Random(seed)
    indices = list(range(N))
    rng.shuffle(indices)
    fold_size = N // n_folds
    accs = []
    for f in range(n_folds):
        start = f * fold_size
        end = N if f == n_folds - 1 else (f+1) * fold_size
        test_idx = set(indices[start:end])
        train_idx = [i for i in range(N) if i not in test_idx]
        centroids = []
        for c in range(n_classes):
            c_train = [i for i in train_idx if labels[i] == c]
            if c_train:
                centroid = [sum(features[i][k] for i in c_train) / len(c_train) for k in range(len(features[0]))]
            else:
                centroid = [0.0]*len(features[0])
            centroids.append(centroid)
        correct = 0
        for i in test_idx:
            dists = [sum((features[i][k] - centroids[c][k])**2 for k in range(len(features[0]))) for c in range(n_classes)]
            pred = dists.index(min(dists))
            if pred == labels[i]:
                correct += 1
        accs.append(correct / len(test_idx))
    return sum(accs) / len(accs)

# ============ 消息传递 ============
def message_passing(X_init, adj, K=4, alpha=0.5):
    D = len(X_init[0])
    H = [row[:] for row in X_init]
    for t in range(K):
        new_H = []
        for i in range(len(adj)):
            if adj[i]:
                neigh_mean = [sum(H[j][k] for j in adj[i]) / len(adj[i]) for k in range(D)]
            else:
                neigh_mean = [0.0]*D
            h_new = [(1-alpha)*H[i][k] + alpha*neigh_mean[k] for k in range(D)]
            new_H.append(h_new)
        H = new_H
    return H

# ============ 谱嵌入 ============
def mat_vec(adj, v):
    return [sum(v[j] for j in adj[i]) for i in range(len(adj))]

def power_iter(adj, n_iter=200, seed=0):
    rng = random.Random(seed)
    n = len(adj)
    v = [rng.random() for _ in range(n)]
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

def power_iter_deflated(adj, v1, lam1, n_iter=200, seed=0):
    rng = random.Random(seed)
    n = len(adj)
    v = [rng.random() for _ in range(n)]
    for _ in range(n_iter):
        nv = deflated_mat_vec(adj, v1, lam1, v)
        norm = math.sqrt(sum(x*x for x in nv))
        if norm < 1e-12:
            break
        v = [x/norm for x in nv]
    return v

def spectral_embed(adj, seed=0):
    v1, lam1 = power_iter(adj, seed=seed)
    v2 = power_iter_deflated(adj, v1, lam1, seed=seed+100)
    return [[v2[i]] for i in range(len(adj))]

def shuffle_graph(adj, seed):
    rng = random.Random(seed)
    n = len(adj)
    num_edges = sum(len(a) for a in adj) // 2
    new_adj = [[] for _ in range(n)]
    edges_made = 0
    attempts = 0
    while edges_made < num_edges and attempts < num_edges * 100:
        i = rng.randint(0, n-1)
        j = rng.randint(0, n-1)
        if i != j and j not in new_adj[i]:
            new_adj[i].append(j)
            new_adj[j].append(i)
            edges_made += 1
        attempts += 1
    return new_adj

# ============ 单次完整实验 ============
def run_experiment(seed):
    N = 300
    n_classes = 3
    D = 8
    adj, labels = generate_sbm(N, n_classes, p_in=0.3, p_out=0.02, seed=seed)
    X = generate_X(N, D, labels, signal_strength=0.3, seed=seed)

    # 条件1：只用内在属性
    acc_X = cross_val_acc(X, labels, seed=seed)

    # 条件2：只用关系结构（谱嵌入）
    spec = spectral_embed(adj, seed=seed)
    acc_A = cross_val_acc(spec, labels, seed=seed)

    # 条件3：组合
    XA = [X[i] + spec[i] for i in range(N)]
    acc_XA = cross_val_acc(XA, labels, seed=seed)

    # 条件4：盲身份（纯随机噪声 + 消息传递）
    rng = random.Random(seed + 200)
    X_noise = [[rng.gauss(0, 1) for _ in range(D)] for _ in range(N)]
    H_noise = message_passing(X_noise, adj, K=4, alpha=0.5)
    acc_blind = cross_val_acc(H_noise, labels, seed=seed)

    # 条件5：打乱关系后的谱嵌入
    adj_shuf = shuffle_graph(adj, seed=seed+300)
    spec_shuf = spectral_embed(adj_shuf, seed=seed+400)
    acc_A_shuf = cross_val_acc(spec_shuf, labels, seed=seed)

    return {
        'acc_X': acc_X,
        'acc_A': acc_A,
        'acc_XA': acc_XA,
        'acc_blind': acc_blind,
        'acc_A_shuf': acc_A_shuf,
    }

# ============ 多次运行 ============
if __name__ == "__main__":
    seeds = [42, 123, 456, 789, 1024]
    results = [run_experiment(s) for s in seeds]
    keys = results[0].keys()
    avg = {k: sum(r[k] for r in results) / len(results) for k in keys}
    std = {k: math.sqrt(sum((r[k] - avg[k])**2 for r in results) / len(results)) for k in keys}

    print("=" * 65)
    print("实验：身份由什么决定？——关系 vs 属性")
    print("=" * 65)
    print(f"N=300, 社区数=3, 属性维度=8, 5次随机种子平均")
    print()
    print("5折交叉验证准确率（均值 ± 标准差）：")
    print(f"  只用内在属性 X               : {avg['acc_X']:.4f} ± {std['acc_X']:.4f}")
    print(f"  只用关系结构 A（谱嵌入）      : {avg['acc_A']:.4f} ± {std['acc_A']:.4f}")
    print(f"  组合 X + A                    : {avg['acc_XA']:.4f} ± {std['acc_XA']:.4f}")
    print(f"  盲身份（纯噪声 + 关系聚合）    : {avg['acc_blind']:.4f} ± {std['acc_blind']:.4f}")
    print(f"  打乱关系后的谱嵌入             : {avg['acc_A_shuf']:.4f} ± {std['acc_A_shuf']:.4f}")
    print(f"  随机水平                       : 0.3333")
    print()
    print("核心比较：")
    print(f"  acc_A - acc_X = {avg['acc_A'] - avg['acc_X']:.4f}")
    print(f"  acc_blind - acc_X = {avg['acc_blind'] - avg['acc_X']:.4f}")
    print(f"  acc_XA - acc_A = {avg['acc_XA'] - avg['acc_A']:.4f}  （属性增量）")
    print(f"  acc_A - acc_A_shuf = {avg['acc_A'] - avg['acc_A_shuf']:.4f}  （关系增量）")
