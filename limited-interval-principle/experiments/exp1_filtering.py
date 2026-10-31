"""实验一：输入筛选强度 -> 边界加速形态
假设 H1：筛选强度与加速放大倍数呈倒 U 形关系
- 弱筛选：中段信号已饱和，边界不特殊
- 中筛选：中段被压住，边界前爆发，尖峰最陡
- 强筛选：连边界前的信号源都被筛掉，加速起不来
"""
import math, statistics

def simulate(N, T, C, tau, filter_strength, n_trials, seed):
    visible = max(1, int(N * (1 - filter_strength)))
    # 信号源因子：可见类型太少时，边界前也爆发不起来
    source_factor = min(1.0, visible / 10.0)

    amps = []
    for k in range(n_trials):
        D = []
        for t in range(T + 1):
            dt = T - t
            intensity = 1.0 + 50.0 * math.exp(-(dt / tau) ** 2) * source_factor
            d = min(C, intensity * visible) / N
            D.append(d)

        mid_region = D[int(0.2 * T):int(0.6 * T)]
        mid = statistics.mean(mid_region)
        peak = max(D[max(0, T - 5):])
        amp = peak / max(mid, 1e-6)
        amps.append(amp)

    return statistics.mean(amps), statistics.stdev(amps)


if __name__ == "__main__":
    N, T, C, tau = 30, 100, 10, 8
    n_trials = 20

    print("=" * 66)
    print("实验一：筛选强度 -> 边界加速形态")
    print("N=%d  T=%d  C=%d  tau=%d  trials=%d" % (N, T, C, tau, n_trials))
    print("=" * 66)
    print("%10s | %8s | %10s | %12s" % (
        "筛选强度", "可见类型", "中段密度", "加速放大倍数"))
    print("-" * 66)

    results = []
    for fs in [0.0, 0.3, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.93, 0.95, 0.97]:
        visible = max(1, int(N * (1 - fs)))
        amp, amp_sd = simulate(N, T, C, tau, fs, n_trials, seed=42)
        mid_d = min(C, visible) / N
        results.append((fs, visible, mid_d, amp))
        print("%10.2f | %8d | %10.3f | %8.2f +/- %.2f" % (
            fs, visible, mid_d, amp, amp_sd))

    # 找峰值
    best = max(results, key=lambda x: x[3])
    print("\n" + "=" * 66)
    print("峰值出现在 筛选强度 = %.2f (可见类型 = %d)" % (best[0], best[1]))
    print("加速放大倍数 = %.2f" % best[3])

    # 倒 U 形检验
    amps = [r[3] for r in results]
    peak_idx = amps.index(max(amps))
    is_inverted_u = (0 < peak_idx < len(amps) - 1
                     and amps[0] < amps[peak_idx]
                     and amps[-1] < amps[peak_idx])
    print("\n倒 U 形检验：%s" % ("成立" if is_inverted_u else "不成立"))
    print("  (要求峰值不在两端，且两端都低于峰值)")
    print("=" * 66)
