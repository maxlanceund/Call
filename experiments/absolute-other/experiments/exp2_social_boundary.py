"""实验二修正版：社会反馈与自我边界
假设 H2："我"的边界由社会反馈的统计结构动态塑造。
高共享：Other 与 Self 高度同向 -> projection 趋向 +1（边界模糊）
低共享：Other 与 Self 系统性反向 -> projection 趋向 -1（边界清晰）
"""
import random
import statistics


def run(shared_ratio, T=3000, seed=0, lr=0.01, agree_prob=0.85):
    rng = random.Random(seed)
    projection = 0.0
    trace = []

    for t in range(T):
        true_state = rng.choice([0, 1])
        # Self 观测：90% 准确
        if rng.random() < 0.9:
            self_obs = true_state
        else:
            self_obs = 1 - true_state

        # Other 观测
        if rng.random() < shared_ratio:
            # 共享：与 Self 高度同向
            if rng.random() < agree_prob:
                other_obs = self_obs
            else:
                other_obs = 1 - self_obs
        else:
            # 不共享：与 Self 系统性反向
            if rng.random() < agree_prob:
                other_obs = 1 - self_obs
            else:
                other_obs = self_obs

        # Hebbian 学习：同向时 projection 增加，反向时减少
        s = 2 * self_obs - 1
        o = 2 * other_obs - 1
        projection += lr * s * o
        projection = max(-1.0, min(1.0, projection))
        trace.append(projection)

    return statistics.mean(trace[-500:]), trace


if __name__ == "__main__":
    print("=" * 70)
    print("实验二修正版：社会反馈与自我边界")
    print("=" * 70)
    print("高共享：Other 与 Self 高度同向（85% 一致）")
    print("低共享：Other 与 Self 系统性反向（85% 相反）")
    print("测：projection 的收敛值。")
    print("  projection > 0：Self 把 Other 当作自己的延伸（边界模糊）")
    print("  projection < 0：Self 把 Other 当作自己的对立面（边界清晰）")
    print()

    print("%10s | %12s | %12s" % ("共享比例", "projection 均值", "projection 标准差"))
    print("-" * 50)

    results = []
    for label, ratio in [("0.90（高）", 0.90), ("0.70（中高）", 0.70),
                          ("0.50（中）", 0.50), ("0.30（中低）", 0.30),
                          ("0.10（低）", 0.10)]:
        vals = []
        for seed in range(10):
            p, _ = run(ratio, T=3000, seed=seed)
            vals.append(p)
        results.append((label, statistics.mean(vals), statistics.stdev(vals)))
        print("%10s | %12.3f | %12.3f" % (
            label, statistics.mean(vals), statistics.stdev(vals)))

    print()
    print("=" * 70)
    print("解读：")
    print("  如果高共享的 projection 显著大于低共享的 projection，")
    print("  则 H2 成立：'我'的边界被社会反馈的统计结构塑造。")
    print("=" * 70)
