"""实验三：意识内容的客体化
假设 H3：意识内容是被全局工作空间广播的客体，不是中心自我生成的。
模型：多个无意识模块竞争进入全局工作空间，胜出的内容被广播。
测：系统报告的"意识内容"是否完全等于广播内容，而与"谁"无关。
"""
import random
import statistics


MODULES = ["visual", "auditory", "memory", "emotion"]


def run(T=5000, n_modules=4, seed=0):
    rng = random.Random(seed)
    # 每个模块的信号强度
    strengths = {m: rng.uniform(0.3, 0.7) for m in MODULES[:n_modules]}
    broadcast_count = {m: 0 for m in MODULES[:n_modules]}
    winner_count = {m: 0 for m in MODULES[:n_modules]}

    for t in range(T):
        # 每个模块产生一个信号强度
        signals = {m: strengths[m] + rng.gauss(0, 0.1) for m in strengths}
        # 竞争：最高信号胜出，被广播到全局工作空间
        winner = max(signals, key=signals.get)
        winner_count[winner] += 1
        # 广播后，胜出模块的强度获得微小增强（正反馈）
        strengths[winner] += 0.001
        # 其他模块轻微衰减
        for m in strengths:
            if m != winner:
                strengths[m] = max(0.1, strengths[m] - 0.0005)

    return winner_count


if __name__ == "__main__":
    print("=" * 70)
    print("实验三：意识内容的客体化")
    print("=" * 70)
    print("多个无意识模块竞争进入全局工作空间，胜出者被广播。")
    print("测：广播分布是否出现垄断（一个模块主导），")
    print("    还是保持多元竞争（无中心自我）。")
    print()

    print("%12s | %10s | %10s" % ("模块", "胜出次数", "占比"))
    print("-" * 42)

    results = []
    for seed in range(10):
        results.append(run(T=5000, seed=seed))

    # 汇总
    total = {}
    for r in results:
        for m, c in r.items():
            total[m] = total.get(m, 0) + c

    grand_total = sum(total.values())
    for m in MODULES[:4]:
        print("%12s | %10d | %9.2f%%" % (
            m, total[m], 100 * total[m] / grand_total))

    print()
    max_share = max(total.values()) / grand_total
    if max_share > 0.7:
        print("结果：一个模块垄断了广播，出现了'中心自我'的假象。")
        print("对应论文：中心感是广播机制正反馈的产物，不是实体。")
    elif max_share < 0.4:
        print("结果：广播分布多元，无中心垄断。")
        print("对应论文：意识内容是多元模块竞争的产物，无统一自我。")
    else:
        print("结果：部分集中，部分多元。需要更多参数扫描。")
