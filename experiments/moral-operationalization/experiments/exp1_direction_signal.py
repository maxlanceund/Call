"""实验一 v2：方向信号随边界条件变化
修正：系统有容错，连续低收益才死，而不是一次选错就死
"""
import random, statistics
from collections import Counter

ACTIONS = ['cooperate', 'compete', 'withdraw']

def run(env_regime, T, n_trials, seed, refresh=True,
        patience=5, damage_threshold=10):
    """
    patience: 连续多少步低收益才死
    damage_threshold: 累积损伤阈值
    """
    dominant_actions = []
    survival_times = []

    for trial in range(n_trials):
        rng = random.Random(seed * 10000 + trial)
        weights = [1/3, 1/3, 1/3]
        damage = 0
        consecutive_low = 0
        survival = T

        for t in range(T):
            if env_regime == 'abundant':
                payoffs = [0.7, 0.2, 0.1]
            else:
                payoffs = [0.1, 0.7, 0.2]

            idx = rng.choices(range(3), weights=weights, k=1)[0]

            # 容错：累积损伤，而不是一次死
            if payoffs[idx] < 0.15:
                damage += 1
                consecutive_low += 1
            else:
                consecutive_low = 0
                damage = max(0, damage - 0.5)

            # 连续太多步低收益，或累积损伤过高，才死
            if consecutive_low >= patience or damage >= damage_threshold:
                survival = t
                break

            # 刷新方向信号
            if refresh:
                lr = 0.1
                for i in range(3):
                    weights[i] += lr * (payoffs[i] - weights[i])

        dominant = ACTIONS[weights.index(max(weights))]
        dominant_actions.append(dominant)
        survival_times.append(survival)

    return Counter(dominant_actions), statistics.mean(survival_times)


if __name__ == "__main__":
    T = 100
    n_trials = 20

    print("=" * 70)
    print("实验一 v2：方向信号随边界条件变化")
    print("T=%d  trials=%d  patience=5  damage_threshold=10" % (T, n_trials))
    print("=" * 70)

    for regime in ['abundant', 'scarce']:
        counts, surv = run(regime, T, n_trials, seed=42, refresh=True)
        print("\n[环境: %s]" % regime)
        print("  主导方向信号分布:", dict(counts))
        print("  平均存活时长: %.1f / %d" % (surv, T))

    print("\n" + "=" * 70)
    print("解读：")
    print("  丰裕 -> cooperate，稀缺 -> compete")
    print("  且存活时长应该显著高于 26.5 步")
    print("=" * 70)
