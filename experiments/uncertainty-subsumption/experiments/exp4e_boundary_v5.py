"""实验四 v5：任务队列，R(t) > 0
系统必须在截止时间 T 前处理完 W 个任务。
没有加速机制，处理速率固定。
测 D(t) 在 T 前的行为。
"""
import random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def run(W, T, rate, n_trials, seed):
    """W: 总任务数
       T: 截止时间
       rate: 每步处理速率（固定）
       n_trials: 并行系统数量
       """
    rng = random.Random(seed)
    remaining = [W] * n_trials
    D_curve, R_curve = [], []
    for t in range(T + 1):
        processed = 0
        new_remaining = []
        for r in remaining:
            take = min(rate, r)
            processed += take
            new_remaining.append(r - take)
        remaining = new_remaining
        D_curve.append(processed / n_trials)
        R_curve.append(sum(remaining) / n_trials)
    return D_curve, R_curve


if __name__ == "__main__":
    n_trials = 2000
    print("=" * 60)
    print("实验四 v5：任务队列，R(t) > 0")
    print("=" * 60)

    # 情形一：任务能在截止时间前处理完
    # W=1000, T=100, 每步 10 → 刚好 1000 步处理完
    print("\n[情形一] 任务刚好能处理完：W=1000, T=100, rate=10")
    D, R = run(W=1000, T=100, rate=10, n_trials=n_trials, seed=42)
    print(f"  t=0    D={D[0]:.2f}  R={R[0]:.1f}")
    print(f"  t=50   D={D[50]:.2f}  R={R[50]:.1f}")
    print(f"  t=80   D={D[80]:.2f}  R={R[80]:.1f}")
    print(f"  t=100  D={D[100]:.2f}  R={R[100]:.1f}")

    # 情形二：任务处理不完，有剩余
    # W=1000, T=100, 每步 5 → 只能处理 500，剩 500
    print("\n[情形二] 任务处理不完：W=1000, T=100, rate=5")
    D, R = run(W=1000, T=100, rate=5, n_trials=n_trials, seed=42)
    print(f"  t=0    D={D[0]:.2f}  R={R[0]:.1f}")
    print(f"  t=50   D={D[50]:.2f}  R={R[50]:.1f}")
    print(f"  t=80   D={D[80]:.2f}  R={R[80]:.1f}")
    print(f"  t=95   D={D[95]:.2f}  R={R[95]:.1f}")
    print(f"  t=99   D={D[99]:.2f}  R={R[99]:.1f}")
    print(f"  t=100  D={D[100]:.2f}  R={R[100]:.1f}")

    # 情形三：任务远超处理能力
    # W=1000, T=100, 每步 1 → 只能处理 100，剩 900
    print("\n[情形三] 任务远超处理能力：W=1000, T=100, rate=1")
    D, R = run(W=1000, T=100, rate=1, n_trials=n_trials, seed=42)
    print(f"  t=0    D={D[0]:.2f}  R={R[0]:.1f}")
    print(f"  t=50   D={D[50]:.2f}  R={R[50]:.1f}")
    print(f"  t=99   D={D[99]:.2f}  R={R[99]:.1f}")
    print(f"  t=100  D={D[100]:.2f}  R={R[100]:.1f}")
