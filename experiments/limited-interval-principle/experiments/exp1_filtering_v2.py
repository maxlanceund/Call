"""实验一 v2：输入筛选 -> 边界加速形态（弱版本）
假设 H1：筛选强度与加速放大倍数呈倒 U 形
弱版本核心：系统识别到边界才加速。可见信号太少时，识别失败，不加速。
"""
import math, statistics

def simulate(N, T, C, tau, filter_strength,
             recognize_threshold, n_trials, seed):
    visible = max(1, int(N * (1 - filter_strength)))

    # 弱版本：系统需要至少 recognize_threshold 种可见信号才能识别边界
    boundary_recognized = (visible >= recognize_threshold)

    amps = []
    for k in range(n_trials):
        D = []
        for t in range(T + 1):
            dt = T - t
            if boundary_recognized:
                intensity = 1.0 + 50.0 * math.exp(-(dt / tau) ** 2)
            else:
                intensity = 1.0
            d = min(C, intensity * visible) / N
            D.append(d)

        mid = statistics.mean(D[int(0.2 * T):int(0.6 * T)])
        peak = max(D[max(0, T - 5):])
        amps.append(peak / max(mid, 1e-6))

    return statistics.mean(amps), statistics.stdev(amps)


if __name__ == "__main__":
    N, T, C, tau = 30, 100, 10, 8
    threshold = 3
    n_trials = 10

    print("=" * 72)
    print("实验一 v2：筛选强度 -> 边界加速（弱版本）")
    print("N=%d  T=%d  C=%d  tau=%d" % (N, T, C, tau))
    print("识别阈值：可见信号 >= %d 时系统识别到边界" % threshold)
    print("=" * 72)
    print("%10s | %8s | %8s | %12s" % (
        "筛选强度", "可见信号", "识别边界", "加速放大倍数"))
    print("-" * 72)

    results = []
    for fs in [0.0, 0.3, 0.5, 0.6, 0.7, 0.8, 0.83, 0.87, 0.9, 0.93, 0.97]:
        visible = max(1, int(N * (1 - fs)))
        recognized = "是" if visible >= threshold else "否"
        amp, amp_sd = simulate(N, T, C, tau, fs, threshold, n_trials, seed=42)
        results.append((fs, visible, amp))
        print("%10.2f | %8d | %8s | %8.2f +/- %.2f" % (
            fs, visible, recognized, amp, amp_sd))

    amps = [r[2] for r in results]
    peak_idx = amps.index(max(amps))
    is_inverted_u = (0 < peak_idx < len(amps) - 1
                     and amps[0] < amps[peak_idx]
                     and amps[-1] < amps[peak_idx])

    print("\n" + "=" * 72)
    print("峰值：筛选强度 = %.2f，放大倍数 = %.2f" % (
        results[peak_idx][0], results[peak_idx][2]))
    print("倒 U 形检验：%s" % ("成立" if is_inverted_u else "不成立"))
    print("=" * 72)
