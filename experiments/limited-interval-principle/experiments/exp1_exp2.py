"""实验一：输入筛选强度 -> 边界加速形态
实验二：信号竞争强度 -> 选项收缩程度
"""
import math, random, statistics

def simulate(N, T, C, theta, profile, tau,
             confirm_threshold, window, gamma_scale, seed):
    rng = random.Random(seed)
    w = [rng.uniform(0.5, 1.0) for _ in range(N)]
    s = sum(w)
    w = [x / s for x in w]

    last_t = [-1] * N
    count = [0] * N
    visible_curve = []

    for t in range(T + 1):
        dt = T - t
        if profile == 'spike':
            intensity = 1.0 + 50.0 * math.exp(-(dt / tau) ** 2)
        elif profile == 'flat':
            intensity = 1.0
        else:
            raise ValueError(profile)

        if intensity < theta:
            pool = 0
        else:
            pool = int(round(intensity * N))
        visible_curve.append(pool)

        budget = min(C, pool)
        if budget > 0:
            gamma = 1.0 + (intensity - 1.0) * gamma_scale
            if gamma < 0.1:
                gamma = 0.1
            probs = [wi ** gamma for wi in w]
            s2 = sum(probs)
            probs = [p / s2 for p in probs]
            for _ in range(budget):
                idx = rng.choices(range(N), weights=probs, k=1)[0]
                count[idx] += 1
                last_t[idx] = t

    options = sum(1 for i in range(N)
                  if count[i] >= confirm_threshold
                  and (T - last_t[i]) <= window)
    return options, visible_curve


def run_batch(N, T, C, theta, profile, tau,
              confirm_threshold, window, gamma_scale, n_trials, seed):
    opts = []
    amps = []
    for k in range(n_trials):
        o, vis = simulate(N, T, C, theta, profile, tau,
                          confirm_threshold, window, gamma_scale,
                          seed * 10000 + k)
        opts.append(o)
        peak = max(vis[max(0, T - 5):]) if vis else 0
        mid_region = vis[int(0.2 * T):int(0.6 * T)]
        mid = statistics.mean(mid_region) if mid_region else 0
        amp = peak / max(mid, 1.0)
        amps.append(amp)
    return (statistics.mean(opts), statistics.stdev(opts),
            statistics.mean(amps), statistics.stdev(amps))


if __name__ == "__main__":
    T, C, tau = 100, 10, 8
    confirm_threshold, window, gamma_scale = 1, 10, 0.5
    n_trials = 20

    # ========== 实验一：筛选强度 -> 边界加速形态 ==========
    print("=" * 68)
    print("实验一：筛选强度 theta -> 边界加速与选项收缩")
    print("N=30  T=%d  C=%d  tau=%d  trials=%d" % (T, C, tau, n_trials))
    print("=" * 68)
    print("%6s | %10s | %10s | %12s" % ("theta", "选项数", "选项比例", "加速放大倍数"))
    print("-" * 68)

    N1 = 30
    for theta in [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0]:
        m, sd, amp, amp_sd = run_batch(N1, T, C, theta, 'spike', tau,
                                       confirm_threshold, window, gamma_scale,
                                       n_trials, seed=42)
        print("%6.1f | %4.1f±%3.1f | %10.3f | %8.2f±%4.2f" % (
            theta, m, sd, m / N1, amp, amp_sd))

    # ========== 实验二：信号竞争强度 -> 选项收缩 ==========
    print("\n" + "=" * 68)
    print("实验二：信号竞争强度（类型数 N）-> 选项收缩")
    print("T=%d  C=%d  theta=0.5  tau=%d  trials=%d" % (T, C, tau, n_trials))
    print("=" * 68)
    print("%6s | %10s | %10s | %12s" % ("N", "选项数", "选项比例", "加速放大倍数"))
    print("-" * 68)

    for N2 in [10, 20, 30, 50, 100]:
        m, sd, amp, amp_sd = run_batch(N2, T, C, 0.5, 'spike', tau,
                                       confirm_threshold, window, gamma_scale,
                                       n_trials, seed=42)
        print("%6d | %4.1f±%3.1f | %10.3f | %8.2f±%4.2f" % (
            N2, m, sd, m / N2, amp, amp_sd))

    print("\n" + "=" * 68)
    print("解读：")
    print("  实验一：筛选越强，加速放大倍数是否先升后降？选项比例如何变？")
    print("  实验二：竞争越激烈（N 越大），选项比例是否越低？")
    print("=" * 68)
