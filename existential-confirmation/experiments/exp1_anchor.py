"""实验一 v2：确认锚点结构
组A：有不可撤销的内部锚点
组B：无锚点，只能依赖外部信号
修正：验证成本随噪声指数增长，超过控制成本时转向控制
"""
import random, statistics

def run(has_anchor, noise_level, T, n_trials, seed,
        anchor_value=0.8, verify_cost_scale=40.0,
        control_cost=3.0, control_effect=0.5, trigger_threshold=0.6):
    verify_total = []
    control_total = []
    for trial in range(n_trials):
        rng = random.Random(seed * 10000 + trial)
        verify_count = 0
        control_count = 0
        control_active = 0
        current_noise = noise_level

        for t in range(T):
            signal_noise = current_noise
            if control_active > 0:
                signal_noise *= (1 - control_effect)
                control_active -= 1
            s = 0.7 + rng.gauss(0, signal_noise)

            if has_anchor:
                E = max(anchor_value, s)
            else:
                E = s

            if E < trigger_threshold:
                # 验证成本随噪声平方增长
                verify_cost = verify_cost_scale * (current_noise ** 2)
                if verify_cost <= control_cost:
                    verify_count += 1
                    current_noise = max(0.01, current_noise * 0.8)
                else:
                    control_count += 1
                    control_active = 3

        verify_total.append(verify_count)
        control_total.append(control_count)

    return (statistics.mean(verify_total),
            statistics.mean(control_total))


if __name__ == "__main__":
    T = 50
    n_trials = 30

    print("=" * 80)
    print("实验一 v2：确认锚点结构")
    print("组A=有锚点  组B=无锚点  T=%d  trials=%d" % (T, n_trials))
    print("验证成本 = 40 × 噪声²，控制成本 = 3.0")
    print("=" * 80)
    print("%8s | %12s | %12s | %12s | %12s" % (
        "噪声", "A验证", "A控制", "B验证", "B控制"))
    print("-" * 80)

    for noise in [0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]:
        a_v, a_c = run(True, noise, T, n_trials, seed=42)
        b_v, b_c = run(False, noise, T, n_trials, seed=42)
        print("%8.2f | %12.2f | %12.2f | %12.2f | %12.2f" % (
            noise, a_v, a_c, b_v, b_c))

    print()
    print("=" * 80)
    print("解读：")
    print("  组A：验证和控制应接近零（锚点让外部信号不重要）")
    print("  组B：低噪声时验证为主；高噪声时验证成本爆炸，转向控制")
    print("  临界噪声：验证成本 = 控制成本 → 40×n²=3 → n≈0.27")
    print("=" * 80)
