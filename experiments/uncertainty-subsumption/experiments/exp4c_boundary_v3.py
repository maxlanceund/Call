"""实验四 v3：边界加速 (H4) - 正确信号密度定义
D(t) = 每步系统实际做的操作量（翻转数/样本）
"""
import random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from core.boolean_network import BooleanNetwork


def run(N, K, E0, T, n_trials, seed, p_noise=0.02):
    rng = random.Random(seed)
    net = BooleanNetwork(N, K, seed=seed)
    states = [tuple(rng.randint(0, 1) for _ in range(N)) for _ in range(n_trials)]
    for _ in range(30):
        states = [net.step(s) for s in states]
    attractor = states[0]
    E = E0
    E_thresh = E0 * 0.15
    D_curve, E_curve = [], []
    for t in range(T + 1):
        E_curve.append(E)
        if t == T:
            D_curve.append(0)
            break
        emergency = E < E_thresh
        flips = 0
        new_states = []
        for s in states:
            s2 = list(net.step(s)) if not emergency else list(s)
            if rng.random() < p_noise:
                s2[rng.randint(0, N - 1)] ^= 1
                flips += 1
            repair_p = 0.4 if emergency else 0.02
            if rng.random() < repair_p:
                s2[rng.randint(0, N - 1)] = attractor[rng.randint(0, N - 1)]
                flips += 1
            new_states.append(tuple(s2))
        states = new_states
        D_curve.append(flips / n_trials)
        E -= (3 + 0.5 * N) if emergency else (1 + 0.2 * N)
        if E < 0:
            E = 0
    return D_curve, E_curve


if __name__ == "__main__":
    N, K, n_trials = 20, 2, 2000
    print("=" * 50)
    print("实验四 v3：信号密度 = 每步活动量")
    print("=" * 50)
    for E0 in [500, 1000]:
        T = 400
        D, E = run(N, K, E0, T, n_trials, seed=42)
        crash = next((t for t, e in enumerate(E) if e <= 0), T)
        print(f"\nE0={E0}  崩溃 t={crash}")
        for t in [0, 50, 100, 200, max(0, crash-40), max(0, crash-20), max(0, crash-10), crash]:
            if 0 <= t < len(D):
                print(f"  t={t:3d}  D={D[t]:.3f}  E={E[t]:.1f}")
