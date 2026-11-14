"""实验二：控制的有效性幻觉
组B1：只验证不控制
组B2：验证+控制
组B3：有锚点
测：感知不确定性 vs 真实不确定性
"""
import random, statistics

def run(has_anchor, use_control, noise_level, T, n_trials, seed,
        anchor_value=0.8, verify_cost_scale=40.0,
        control_cost=3.0, control_effect=0.5, trigger_threshold=0.6):
    perceived_vars = []
    true_vars = []
    for trial in range(n_trials):
        rng = random.Random(seed * 10000 + trial)
        control_active = 0
        current_noise = noise_level
        perceived_signals = []
        true_signals = []

        for t in range(T):
            # 真实信号：原始噪声
            true_s = 0.7 + rng.gauss(0, noise_level)
            true_signals.append(true_s)

            # 感知信号：如果控制生效，信号被压缩
            signal_noise = noise_level
            if control_active > 0:
                signal_noise *= (1 - control_effect)
                control_active -= 1
            perceived_s = 0.7 + rng.gauss(0, signal_noise)
            perceived_signals.append(perceived_s)

            # 系统行为决策
            if has_anchor:
                E = max(anchor_value, perceived_s)
            else:
                E = perceived_s

            if E < trigger_threshold:
                verify_cost = verify_cost_scale * (current_noise ** 2)
                if verify_cost <= control_cost:
                    current_noise = max(0.01, current_noise * 0.8)
                elif use_control:
                    control_active = 3

        perceived_vars.append(statistics.pvariance(perceived_signals))
        true_vars.append(statistics.pvariance(true_signals))

    return statistics.mean(perceived_vars), statistics.mean(true_vars)


if __name__ == "__main__":
    T = 100
    n_trials = 30
    noise = 0.4

    print("=" * 80)
    print("实验二：控制的有效性幻觉")
    print("噪声 = %.2f  T = %d  trials = %d" % (noise, T, n_trials))
    print("=" * 80)
    print("%-30s | %14s | %14s | %14s" % (
        "组", "感知不确定性", "真实不确定性", "差距"))
    print("-" * 80)

    groups = [
        ("B1: 只验证不控制", False, False),
        ("B2: 验证 + 控制", False, True),
        ("B3: 有锚点", True, False),
    ]

    for label, has_anchor, use_control in groups:
        pv, tv = run(has_anchor, use_control, noise, T, n_trials, seed=42)
        gap = tv - pv
        print("%-30s | %14.4f | %14.4f | %14.4f" % (label, pv, tv, gap))

    print()
    print("=" * 80)
    print("解读：")
    print("  B1：感知≈真实（没有控制，系统看到的就是真实噪声）")
    print("  B2：感知<真实（控制压缩了信号，系统'感觉'更确定，但真实噪声没变）")
    print("  B3：锚点让两者都不重要")
    print()
    print("  如果B2的感知显著低于真实，且B1感知≈真实，")
    print("  则'控制降低的是感知不确定性而非真实不确定性'成立——")
    print("  这就是控制的有效性幻觉。")
    print("=" * 80)
