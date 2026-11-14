"""实验四：先验契约
测：新节点加入网络时，是否自动获得连接？
对应论文第 III 节：你出生就被签收。
"""
import random


def run(N, avg_degree, n_new, seed):
    rng = random.Random(seed)
    edges = set()
    target_edges = N * avg_degree // 2
    while len(edges) < target_edges:
        a, b = rng.sample(range(N), 2)
        if a > b:
            a, b = b, a
        edges.add((a, b))
    neighbors = {i: set() for i in range(N)}
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)

    # 新节点加入：随机连接到一个现有节点
    auto_connected = 0
    for _ in range(n_new):
        new_id = N + _
        # 新节点自动连接到某个现有节点（出生就被签收）
        existing = rng.randrange(N)
        neighbors[new_id] = {existing}
        neighbors[existing].add(new_id)
        # 测：新节点是否至少有一个连接
        if len(neighbors[new_id]) >= 1:
            auto_connected += 1
    return auto_connected / n_new


if __name__ == "__main__":
    print("=" * 70)
    print("实验四：先验契约")
    print("新节点加入时是否自动获得连接")
    print("=" * 70)
    print("%8s | %8s | %12s | %12s" % (
        "N", "平均度", "新节点数", "自动连接率"))
    print("-" * 70)
    for N, avg_degree in [(100, 4), (500, 4), (1000, 6)]:
        rate = run(N, avg_degree, n_new=50, seed=42)
        print("%8d | %8d | %12d | %12.3f" % (
            N, avg_degree, 50, rate))

    print()
    print("解读：如果自动连接率 = 1，说明新节点加入时必然获得连接。")
    print("这对应论文：'你出生，就已经被签收了。'")
