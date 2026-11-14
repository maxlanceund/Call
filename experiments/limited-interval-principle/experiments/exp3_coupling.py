"""实验三 v2：耦合检验
边界加速 → 竞争加剧 → 少数类型垄断 → 选项收缩
关键：选择概率为 w_i^gamma，gamma 随信号强度升高
"""
import math, random, statistics

def run(N, T, C, theta, profile, tau,
        confirm_threshold, window, n_trials, seed, gamma_scale=0.5):
    results = []
    for trial in range(n_trials):
        rng = random.Random(seed * 10000 + trial)
        # 异质但接近均匀的权重
        w = [rng.uniform(0.5, 1.0) for _ in range(N)]
        total = sum(w)
        w = [x / total for x in w]

        last_t = [-1] * N
        count = [0] * N

        for t in range(T + 1):
            dt = T - t
            if profile == 'spike':
                intensity = 1.0 + 50.0 * math.exp(-(dt / tau) ** 2)
            elif profile == 'flat':
                intensity = 1.0
            elif profile == 'decay':
                intensity = 0.6 + 0.4 * (1 - t / T)
            else:
                raise ValueError(profile)

            if intensity < theta:
                pool = 0
            else:
                pool = int(round(intensity * N))

            budget = min(C, pool)

            if budget > 0:
                gamma = 1.0 + (intensity - 1.0) * gamma_scale
                if gamma < 0.1:
                    gamma = 0.1
                probs = [w_i ** gamma for w_i in w]
                s = sum(probs)
                probs = [p / s for p in probs]
                for _ in range(budget):
                    idx = rng.choices(range(N), weights=probs, k=1)[0]
                    count[idx] += 1
                    last_t[idx] = t

        options = sum(1 for i in range(N)
                      if count[i] >= confirm_threshold
                      and (T - last_t[i]) <= window)
        results.append(options)

    return statistics.mean(results), statistics.stdev(results)


if __name__ == "__main__":
    N, T, C = 30, 100, 10
    theta = 0.5
    tau = 8
    confirm_threshold = 1
    window = 10
    n_trials = 30

    print("=" * 60)
    print("实验三 v2：耦合检验")
    print("N=%d  T=%d  C=%d  theta=%.1f  tau=%d" % (N, T, C, theta, tau))
    print("confirm_threshold=%d  window=%d  trials=%d" % (
        confirm_threshold, window, n_trials))
    print("=" * 60)

    for profile, label in [
        ('spike', 'A 有边界加速'),
        ('flat',  'B 无边界加速（信号恒定）'),
        ('decay', 'C 无边界加速（信号缓降）'),
    ]:
        mean, std = run(N, T, C, theta, profile, tau,
                        confirm_threshold, window, n_trials, seed=42)
        print("\n[%s]" % label)
        print("  边界处选项数 = %.2f +/- %.2f  (满分 %d)" % (mean, std, N))

    print("\n" + "=" * 60)
    print("解读：")
    print("  A 明显低于 B、C -> 边界加速与选项收缩耦合")
    print("  A ≈ B ≈ C     -> 四特征只是并列")
    print("=" * 60)
