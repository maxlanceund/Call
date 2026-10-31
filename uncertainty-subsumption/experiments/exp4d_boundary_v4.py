"""实验四 v4：硬边界，无任何加速机制
测试 H4：E=0 是硬边界，信号不能在边界后释放。
D(t) = 每步实际翻转数 / 样本数。
不写紧急模式，不写修复加速。看 D 是否自发出现尖峰。
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
    E = E0
    D_curve, E_curve = [], []
    for t in range(T + 1):
        E_curve.append(E)
        if E <= 0:
            D_curve.append(0.0)
            continue
        flips = 0
        new_states = []
        for s in states:
            s2 = list(net.step(s))
            if rng.random() < p_noise:
                s2[rng.randint(0, N - 1)] ^= 1
                flips += 1
            new_states.append(tuple(s2))
        states = new_states
        D_curve.append(flips / n_trials)
        E -= 1
    return D_curve, E_curve


if __name__ == "__main__":
    N, K, n_trials = 20, 2, 2000
    print("=" * 50)
    print("实验四 v4：硬边界，无加速机制")
    print("=" * 50)
    for E0 in [100, 200, 500]:
        T = E0
        D, E = run(N, K, E0, T, n_trials, seed=42)
        crash = next((t for t, e in enumerate(E) if e <= 0), T)
        print(f"\nE0={E0}  crash={crash}")
        print(f"  D 平均 = {sum(D)/len(D):.4f}")
        print(f"  D 最大 = {max(D):.4f} (t={D.index(max(D))})")
        print(f"  边界前 20 步 D = {[round(x,3) for x in D[max(0,crash-20):crash]]}")
        print(f"  边界后 5 步 D  = {[round(x,3) for x in D[crash:crash+5]]}")
