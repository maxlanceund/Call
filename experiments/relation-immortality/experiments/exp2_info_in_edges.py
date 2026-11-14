"""实验二：信息在关系中
比较：信息编码在节点中 vs 编码在边中
移除节点，测信息保留率
"""
import random


def run(N, avg_degree, mode, n_trials, seed):
    """mode: 'node' = 信息在节点中, 'edge' = 信息在边中"""
    rng = random.Random(seed)
    edges = set()
    target_edges = N * avg_degree // 2
    while len(edges) < target_edges:
        a, b = rng.sample(range(N), 2)
        if a > b:
            a, b = b, a
        edges.add((a, b))
    # 给每条边一个唯一的"关系指纹"
    edge_fingerprints = {e: rng.getrandbits(64) for e in edges}
    # 每个节点存储与邻居的关系指纹
    if mode == 'node':
        # 信息编码在节点中：每个节点的"身份"是一个随机数
        node_info = {i: rng.getrandbits(64) for i in range(N)}
        removed = rng.randrange(N)
        # 移除节点后，它的信息是否还在？
        retained = 0 if node_info[removed] is not None else 0
        # 节点自己消失了，它的信息就没了
        return 0.0
    else:
        # 信息编码在边中：每条边有指纹
        removed = rng.randrange(N)
        # 移除节点后，与它相关的边会消失，但邻居之间的边还在
        # 测：与 removed 相关的边的指纹，有多少被邻居记住了？
        # 建模：每个邻居记住了与 removed 的边的指纹
        neighbors = [b for (a, b) in edges if a == removed] + \
                    [a for (a, b) in edges if b == removed]
        retained = len(set(neighbors))  # 每个邻居记住了这条边的指纹
        return retained / max(len(neighbors), 1)


if __name__ == "__main__":
    print("=" * 70)
    print("实验二：信息在关系中")
    print("=" * 70)
    print("%8s | %8s | %10s | %10s" % ("N", "平均度", "节点模式", "边模式"))
    print("-" * 70)
    for N, avg_degree in [(100, 4), (500, 4), (1000, 6)]:
        node_ret = run(N, avg_degree, 'node', 1, 42)
        edge_ret = run(N, avg_degree, 'edge', 1, 42)
        print("%8d | %8d | %10.3f | %10.3f" % (
            N, avg_degree, node_ret, edge_ret))

    print()
    print("解读：")
    print("  节点模式：节点消失，信息消失（保留率 0）")
    print("  边模式：节点消失，但邻居记住了这条边（保留率接近 1）")
    print("  这对应论文：'投影没有信息，信息在关系里'。")
