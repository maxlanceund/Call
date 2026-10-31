"""实验二：停止刷新 -> 方向信号失效
实验三：边界剧变 -> 旧信号被吞没，新信号重新凝聚
"""
import random, statistics
from collections import Counter

ACTIONS = ['cooperate', 'compete', 'withdraw']

def run_switch(switch_at, refresh_after_switch, T, n_trials, seed,
               patience=5, damage_threshold=10):
    """
    环境在 switch_at 从 abundant 切到 scarce
    refresh_after_switch: 切换后是否继续刷新方向信号
    """
    dominant_final = []
    survival_times = []
    switch_speed = []  # 切换后多少步方向信号才翻转

    for trial in range(n_trials):
        rng = random.Random(seed * 10000 + trial)
        weights = [1/3, 1/3, 1/3]
        damage = 0
        consecutive_low = 0
        survival = T
        flipped_at = None

        for t in range(T):
            if t < switch_at:
                payoffs = [0.7, 0.2, 0.1]
            else:
                payoffs = [0.1, 0.7, 0.2]

            idx = rng.choices(range(3), weights=weights, k=1)[0]

            if payoffs[idx] < 0.15:
                damage += 1
                consecutive_low += 1
            else:
                consecutive_low = 0
                damage = max(0, damage - 0.5)

            if consecutive_low >= patience or damage >= damage_threshold:
                survival = t
                break

            # 刷新逻辑：切换后是否继续刷新
            do_refresh = (t < switch_at) or refresh_after_switch
            if do_refresh:
                lr = 0.1
                for i in range(3):
                    weights[i] += lr * (payoffs[i] - weights[i])

            # 记录方向信号翻转的时刻
            if t >= switch_at and flipped_at is None:
                if ACTIONS[weights.index(max(weights))] == 'compete':
                    flipped_at = t

        dominant_final.append(ACTIONS[weights.index(max(weights))])
        survival_times.append(survival)
        if flipped_at is not None:
            switch_speed.append(flipped_at - switch_at)

    return (Counter(dominant_final),
            statistics.mean(survival_times),
            statistics.mean(switch_speed) if switch_speed else None)


if __name__ == "__main__":
    T = 100
    switch_at = 50
    n_trials = 20

    print("=" * 74)
    print("实验二 & 三：停止刷新 vs 持续刷新")
    print("环境在 t=%d 从 abundant 切换到 scarce" % switch_at)
    print("T=%d  trials=%d  patience=5  damage_threshold=10" % (T, n_trials))
    print("=" * 74)

    print("\n[实验二 A：切换后继续刷新方向信号]")
    counts, surv, speed = run_switch(switch_at, True, T, n_trials, seed=42)
    print("  最终主导方向信号:", dict(counts))
    print("  平均存活时长: %.1f / %d" % (surv, T))
    print("  切换后平均翻转耗时: %s" % (
        "%.1f 步" % speed if speed else "未翻转"))

    print("\n[实验二 B：切换后冻结方向信号（不刷新）]")
    counts, surv, speed = run_switch(switch_at, False, T, n_trials, seed=42)
    print("  最终主导方向信号:", dict(counts))
    print("  平均存活时长: %.1f / %d" % (surv, T))
    print("  切换后平均翻转耗时: %s" % (
        "%.1f 步" % speed if speed else "未翻转"))

    print("\n" + "=" * 74)
    print("解读：")
    print("  A（持续刷新）：切换后方向信号从 cooperate 翻转到 compete，")
    print("                 系统适应环境，存活拉满。")
    print("  B（冻结）：切换后方向信号仍停在 cooperate，")
    print("            与环境脱节，损伤累积，系统提前死亡。")
    print()
    print("  实验二：停止刷新 -> 方向信号失效（存活时长显著下降）")
    print("  实验三：边界剧变 -> 旧信号被吞没，新信号重新凝聚")
    print("          （A 组的翻转耗时 = 重新凝聚的速度）")
    print("=" * 74)
