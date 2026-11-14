"""实验四修正版：边界加速 (H4)
引入能量池。系统消耗能量维持确定性。
能量接近耗尽时，进入紧急模式（停止更新，全力修复），信号密度升高。
能量耗尽时，修复停止，系统崩塌，确定性归零。
"""
import random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from core.boolean_network import BooleanNetwork, state_entropy


def run(N, K, E0, T, n_trials, seed, p_noise=0.05):
    rng = random.Random(seed)
    net = BooleanNetwork(N, K, seed=seed)
    states = [tuple(rng.randint(0, 1) for _ in range(N)) for _ in range(n_trials)]
    for _ in range(30):
        states = [net.step(s) for s in states]
    attractor = states[0]
    E = E0
    E_thresh = E0 * 0.15
    H_curve, D_curve, E_curve = [], [], []
    for t in range(T + 1):
        H = state_entropy(states)
        H_curve.append(H)
        D_curve.append(max(0.0, (N - H) / N))
        E_curve.append(E)
        if t == T:
            break
        emergency = E < E_thresh
        if not emergency:
            states = [net.step(s) for s in states]
        new_states = []
        for s in states:
            s2 = list(s)
            if rng.random() < p_noise:
                s2[rng.randint(0, N - 1)] ^= 1
            repair_p = 0.3 if emergency else 0.05
            if rng.random() < repair_p:
                s2[rng.randint(0, N - 1)] = attractor[rng.randint(0, N - 1)]
            new_states.append(tuple(s2))
        states = new_states
        E -= (3 + 0.5 * H) if emergency else (1 + 0.2 * H)
        if E < 0:
            E = 0
    return H_curve, D_curve, E_curve


if __name__ == "__main__":
    N, K, n_trials = 20, 2, 2000
    print("=" * 50)
    print("实验四修正版：边界加速 (H4)")
    print(f"N={N}  K={K}  样本={n_trials}")
    print("=" * 50)
    for E0 in [500, 1000, 2000]:
        T = 500
        H, D, E = run(N, K, E0, T, n_trials, seed=42)
        crash = next((t for t, e in enumerate(E) if e <= 0), T)
        print(f"\nE0={E0}  资源耗尽 t={crash}")
        for t in [0, 50, 100, crash // 2, max(0, crash - 30), max(0, crash - 10), crash]:
            if 0 <= t < len(D):
                print(f"  t={t:3d}  H={H[t]:.3f}  D={D[t]:.4f}  E={E[t]:.1f}")
