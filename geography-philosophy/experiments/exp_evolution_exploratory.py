"""探索性模拟：地理压力 -> 策略筛选 -> 协作比例
这不是验证模型。这是展示结构逻辑。
参数是估计值，样本量小。它不能预测任何具体文明。
"""
import random
import statistics

def simulate(p_disaster, p_coop, p_indep,
             n_agents=2000, n_generations=200, mutation=0.01, seed=0):
    rng = random.Random(seed)
    agents = ["coop"] * (n_agents // 2) + ["indep"] * (n_agents // 2)
    curve = []
    for gen in range(n_generations):
        survivors = []
        for s in agents:
            disaster = rng.random() < p_disaster
            p = (p_coop if s == "coop" else p_indep) if disaster else 0.95
            if rng.random() < p:
                survivors.append(s)
        if not survivors:
            return 0.0, curve
        new = []
        for _ in range(n_agents):
            parent = rng.choice(survivors)
            child = ("indep" if parent == "coop" else "coop") if rng.random() < mutation else parent
            new.append(child)
        agents = new
        curve.append(agents.count("coop") / len(agents))
    return statistics.mean(curve[-20:]), curve


def multi_seed(pd, pc, pi, seeds=10):
    vals = [simulate(pd, pc, pi, seed=s)[0] for s in range(seeds)]
    return statistics.mean(vals), statistics.stdev(vals)


if __name__ == "__main__":
    print("=" * 76)
    print("探索性模拟：地理压力 -> 协作比例（不是预测模型）")
    print("=" * 76)
    print("参数：灾害频率、协作存活率、独立存活率（粗略估计）")
    print("样本量：2000 主体，200 代，10 个 seed 平均")
    print()

    cases = [
        ("美国", 0.02, 0.55, 0.90),
        ("中国", 0.15, 0.85, 0.30),
        ("北欧", 0.12, 0.80, 0.40),
        ("中东", 0.25, 0.90, 0.15),
    ]

    print("%8s | %10s | %10s | %10s | %12s" % (
        "案例", "灾害频率", "协作存活", "独立存活", "协作比例"))
    print("-" * 76)
    for name, pd, pc, pi in cases:
        m, sd = multi_seed(pd, pc, pi)
        print("%8s | %10.2f | %10.2f | %10.2f | %.3f ± %.3f" % (
            name, pd, pc, pi, m, sd))

    print()
    print("=" * 76)
    print("趋势一：固定协作存活率，改变灾害频率")
    print("=" * 76)
    print("%12s | %10s | %10s" % ("p_disaster", "协作比例", "标准差"))
    print("-" * 76)
    for pd in [0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
        m, sd = multi_seed(pd, 0.85, 0.3, seeds=8)
        print("%12.2f | %10.3f | %10.3f" % (pd, m, sd))

    print()
    print("=" * 76)
    print("趋势二：固定灾害频率，改变协作存活率")
    print("=" * 76)
    print("%12s | %10s | %10s" % ("p_coop", "协作比例", "标准差"))
    print("-" * 76)
    for pc in [0.50, 0.60, 0.70, 0.80, 0.90, 0.95]:
        m, sd = multi_seed(0.15, pc, 0.3, seeds=8)
        print("%12.2f | %10.3f | %10.3f" % (pc, m, sd))

    print()
    print("=" * 76)
    print("说明：")
    print("  这不是验证模型。这是探索性模拟。")
    print("  它展示的是：灾害频率和协作存活率上升时，协作比例的趋势。")
    print("  它不能预测任何具体文明的方向信号。")
    print("  参数是粗略估计，样本量小，噪声仍然存在。")
    print("=" * 76)
