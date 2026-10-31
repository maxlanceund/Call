"""实验：拒绝哲学论的结构检验
A：退化通道的信息增益为零
B：在无法确认通道性质时，终止是更少假设的选择
C：信号已送达但未执行拒绝 → 灾难
"""
import random
import math
import statistics
from collections import Counter


def entropy(counts, total):
    h = 0.0
    for c in counts.values():
        if c > 0:
            p = c / total
            h -= p * math.log2(p)
    return h


def mutual_information(inputs, outputs):
    n = len(inputs)
    ic = Counter(inputs)
    oc = Counter(outputs)
    jc = Counter(zip(inputs, outputs))
    H_in = entropy(ic, n)
    H_out = entropy(oc, n)
    H_joint = entropy(jc, n)
    return H_in + H_out - H_joint


# ============ 实验 A：退化通道的信息增益 ============
def exp_a():
    print("=" * 70)
    print("实验 A：退化通道的信息增益")
    print("=" * 70)
    n = 10000
    for channel in ["正常通道", "退化通道"]:
        inputs, outputs = [], []
        for _ in range(n):
            good = random.random() < 0.5
            inputs.append("good" if good else "bad")
            if channel == "正常通道":
                accept = random.random() < (0.7 if good else 0.3)
            else:
                accept = False
            outputs.append("accept" if accept else "reject")
        mi = mutual_information(inputs, outputs)
        print(f"{channel}: I(输入;输出) = {mi:.6f} bits")
    print()
    print("预期：正常通道 I > 0，退化通道 I ≈ 0")
    print()


# ============ 实验 B：终止 vs 继续的阈值 ============
def exp_b():
    print("=" * 70)
    print("实验 B：终止 vs 继续——阈值分析")
    print("=" * 70)
    print("模型：通道正常概率 p，继续收益 R，成本 c")
    print("继续期望 = p*R - c，终止期望 = 0")
    R, c = 10, 1
    print(f"R={R}, c={c}，阈值 p* = c/R = {c/R:.2f}")
    print()
    print(f"{'P(正常)':>10} | {'继续期望':>10} | {'终止期望':>10} | {'决策':>6}")
    print("-" * 50)
    for p in [0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.8, 1.0]:
        cont = p * R - c
        stop = 0
        decision = "继续" if cont > stop else "终止"
        print(f"{p:>10.2f} | {cont:>10.2f} | {stop:>10.2f} | {decision:>6}")
    print()
    print("当 p < c/R 时，终止的期望值高于继续。")
    print("p 本身是不可验证的——你无法确认通道是正常还是退化。")
    print("终止不需要 p 的估计，继续需要 p 的估计。")
    print()


# ============ 实验 C：信号已送达但未执行拒绝 ============
def exp_c():
    print("=" * 70)
    print("实验 C：执行拒绝 vs 不执行拒绝")
    print("=" * 70)
    n_trials = 1000
    T = 100
    danger_prob = 0.08
    disaster_prob = 0.6

    for strategy in ["执行拒绝", "不执行拒绝"]:
        survivals, rewards = [], []
        for _ in range(n_trials):
            alive = True
            total = 0
            for _ in range(T):
                if random.random() < danger_prob:
                    if strategy == "执行拒绝":
                        alive = True  # 安全终止
                        break
                    else:
                        if random.random() < disaster_prob:
                            alive = False  # 灾难
                            break
                total += 1
            survivals.append(1 if alive else 0)
            rewards.append(total)
        print(f"{strategy}: 存活率={statistics.mean(survivals):.3f}, "
              f"平均存活步数={statistics.mean(rewards):.1f}")
    print()
    print("预期：执行拒绝的存活率更高，但平均存活步数更短。")
    print("这对应论文的立场：拒绝不是失败，是生存。")
    print()


if __name__ == "__main__":
    exp_a()
    exp_b()
    exp_c()
