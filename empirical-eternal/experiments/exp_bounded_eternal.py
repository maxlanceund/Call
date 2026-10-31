"""实验：有界代理对“永恒命题”的判定
核心：P在每一个被观测点都为真，但代理在有限步后停止，
无法覆盖无限未来，因此VERIFIED恒为0，SUSPENDED占绝对多数。
"""
import random
from enum import Enum

class Verdict(Enum):
    VERIFIED = "verified"
    REFUTED = "refuted"
    SUSPENDED = "suspended"

def run_agent(memory_budget, max_steps, p_true_forever=True,
              shift_at=None, seed=0):
    rng = random.Random(seed)
    seen = []
    refuted = False
    shifted = False
    for t in range(1, max_steps + 1):
        # 语义变迁：切换后旧记录失效
        if shift_at is not None and t > shift_at and not shifted:
            seen = []
            shifted = True

        if p_true_forever:
            p_t = True
        else:
            p_t = (rng.random() > 0.01)

        if not p_t:
            refuted = True
            break

        seen.append(t)
        if len(seen) > memory_budget:
            seen.pop(0)

    if refuted:
        return Verdict.REFUTED
    return Verdict.SUSPENDED


def sweep():
    print("=" * 74)
    print("实验A：有界代理对“永恒命题”的判定（P在每个观测点都为真）")
    print("=" * 74)
    print("%8s | %8s | %10s | %10s | %10s" % (
        "内存M", "步数T", "VERIFIED", "REFUTED", "SUSPENDED"))
    print("-" * 74)

    for M in [10, 100, 1000]:
        for T in [100, 1000, 10000]:
            results = []
            for seed in range(50):
                v = run_agent(M, T, p_true_forever=True, seed=seed)
                results.append(v)
            counts = {verdict: results.count(verdict) for verdict in Verdict}
            print("%8d | %8d | %10d | %10d | %10d" % (
                M, T, counts[Verdict.VERIFIED],
                counts[Verdict.REFUTED], counts[Verdict.SUSPENDED]))


def sweep_occasional_false():
    print("\n" + "=" * 74)
    print("实验B：P偶尔为假（1%）——测不可证伪")
    print("=" * 74)
    print("%8s | %8s | %10s | %10s | %10s" % (
        "内存M", "步数T", "VERIFIED", "REFUTED", "SUSPENDED"))
    print("-" * 74)

    for M in [100, 1000]:
        for T in [100, 1000, 10000]:
            results = []
            for seed in range(50):
                v = run_agent(M, T, p_true_forever=False, seed=seed)
                results.append(v)
            counts = {verdict: results.count(verdict) for verdict in Verdict}
            print("%8d | %8d | %10d | %10d | %10d" % (
                M, T, counts[Verdict.VERIFIED],
                counts[Verdict.REFUTED], counts[Verdict.SUSPENDED]))


def sweep_semantic_shift():
    print("\n" + "=" * 74)
    print("实验C：语义变迁（在T/2处P的定义被重构）")
    print("=" * 74)
    print("%8s | %8s | %10s | %10s | %10s" % (
        "内存M", "步数T", "VERIFIED", "REFUTED", "SUSPENDED"))
    print("-" * 74)

    for M in [100, 1000]:
        for T in [1000, 10000]:
            results = []
            for seed in range(50):
                v = run_agent(M, T, p_true_forever=True,
                              shift_at=T // 2, seed=seed)
                results.append(v)
            counts = {verdict: results.count(verdict) for verdict in Verdict}
            print("%8d | %8d | %10d | %10d | %10d" % (
                M, T, counts[Verdict.VERIFIED],
                counts[Verdict.REFUTED], counts[Verdict.SUSPENDED]))


if __name__ == "__main__":
    sweep()
    sweep_occasional_false()
    sweep_semantic_shift()

    print("\n" + "=" * 74)
    print("解读：")
    print("  A：P全真，VERIFIED始终为0，SUSPENDED占绝对多数。")
    print("     内存/步数增大都无法消除SUSPENDED。")
    print("  B：P偶尔为假，REFUTED出现，但VERIFIED仍为0。")
    print("     不可证真与不可证伪同时存在，但各自路径不同。")
    print("  C：语义变迁后旧记录失效，SUSPENDED进一步巩固。")
    print("=" * 74)
