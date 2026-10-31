"""实验一：客观不朽
节点移除后，它的信息仍然保留在邻居的记忆中。
"""
import random
import statistics


def run(N, avg_degree, T, n_trials, seed):
    """构建随机图，每个节点记住邻居的指纹。
    移除一个节点，测它的信息还保留在多少节点的记忆里。
    """
    rng = random.Random(seed)
    # 构建随机图
    edges = set()
    target_edges = N * avg_degree // 2
    while len(edges) < target_edges:
        a, b = rng.sample(range(N), 2)
        if a > b:
            a, b = b, a
        edges.add((a, b))
    # 每个节点的邻居
    neighbors = {i: set() for i in range(N)}
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    # 每个节点的记忆：存储所有邻居的指纹（这里指纹就是邻居的 ID）
    memories = {i: set(neighbors[i]) for i in range(N)}
    # 移除一个随机节点
    removed = rng.randrange(N)
    # 测：removed 的信息还保留在多少节点的记忆中
    retained = sum(1 for i in range(N)
                   if i != removed and removed in memories[i])
    return retained, len(neighbors[removed])


if __name__ == "__main__":
    print("=" * 70)
    print("实验一：客观不朽")
    print("节点移除后，它的信息还保留在邻居的记忆中")
    print("=" * 70)
    print("%8s | %8s | %12s | %12s | %12s" % (
        "N", "平均度", "移除节点度数", "保留节点数", "保留率"))
    print("-" * 70)

    for N, avg_degree in [(100, 4), (100, 8), (500, 4), (500, 8), (1000, 6)]:
        retained, degree = run(N, avg_degree, T=1, n_trials=1, seed=42)
        print("%8d | %8d | %12d | %12d | %12.3f" % (
            N, avg_degree, degree, retained, retained / max(degree, 1)))

    print()
    print("解读：如果保留率接近 1，说明节点移除后，")
    print("它的信息仍然完整保留在邻居的记忆中——客观不朽成立。")
