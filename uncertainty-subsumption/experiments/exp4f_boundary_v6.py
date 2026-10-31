"""实验四 v6：H4 弱版本 - 系统识别边界
系统策略：v(t) = min(v_max, R(t) / τ(t))
不写任何加速机制。看 v(t) 是否自发产生尖峰。
"""
import random, sys, os, statistics, math, argparse
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def run_one(W, T, a, v_max, seed):
    rng = random.Random(seed)
    R = W
    v_curve, R_curve = [], []
    for t in range(T + 1):
        tau = max(1, T - t)
        v = min(v_max, R / tau)
        v_curve.append(v)
        R_curve.append(R)
        if t == T:
            break
        R = max(0.0, R + a - v)
    return v_curve, R_curve


def run(W, T, a, v_max, n_trials, seed):
    v_all, R_all = [], []
    for i in range(n_trials):
        v, R = run_one(W, T, a, v_max, seed * 10000 + i)
        v_all.append(v)
        R_all.append(R)
    n = len(v_all[0])
    avg_v = [sum(c[t] for c in v_all) / n_trials for t in range(n)]
    avg_R = [sum(c[t] for c in R_all) / n_trials for t in range(n)]
    return avg_v, avg_R


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", type=float, default=1.0)
    args = parser.parse_args()

    W, T, v_max, n_trials = 100.0, 100, 50.0, 200
    seeds = list(range(1, 11))

    print("=" * 60)
    print(f"实验四 v6：H4 弱版本 - 系统识别边界")
    print(f"W={W}  T={T}  a={args.a}  v_max={v_max}")
    print(f"seeds={len(seeds)}  trials/seed={n_trials}")
    print("=" * 60)

    all_v, all_R = [], []
    for s in seeds:
        v, R = run(W, T, args.a, v_max, n_trials, seed=s)
        all_v.append(v)
        all_R.append(R)

    avg_v = [statistics.mean(c[t] for c in all_v) for t in range(T + 1)]
    std_v = [statistics.stdev(c[t] for c in all_v) for t in range(T + 1)]
    avg_R = [statistics.mean(c[t] for c in all_R) for t in range(T + 1)]

    print(f"\na={args.a}")
    print(f"{'t':>4} | {'v(t)':>10} | {'std':>8} | {'R(t)':>10}")
    print("-" * 42)
    for t in [0, 10, 20, 50, 70, 80, 90, 95, 98, 99, 100]:
        if t <= T:
            print(f"{t:>4} | {avg_v[t]:>10.4f} | {std_v[t]:>8.4f} | {avg_R[t]:>10.2f}")

    print(f"\n边界前峰值: max(v) = {max(avg_v):.4f} at t={avg_v.index(max(avg_v))}")
    print(f"边界处 v(T) = {avg_v[T]:.4f}")
