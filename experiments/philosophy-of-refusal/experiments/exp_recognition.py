"""实验D：识别能力的对照
有识别 + 执行拒绝 vs 有识别 + 不执行 vs 无识别（从不触发拒绝）
"""
import random
import statistics


def run(has_recognition, execute_refusal, n_trials, T,
        danger_prob, disaster_prob):
    survivals, steps = [], []
    for _ in range(n_trials):
        alive = True
        total = 0
        for _ in range(T):
            total += 1
            if random.random() < danger_prob:
                if has_recognition and execute_refusal:
                    # 识别到危险信号，执行拒绝，安全终止
                    break
                elif has_recognition and not execute_refusal:
                    # 识别到但未执行拒绝，继续走，可能灾难
                    if random.random() < disaster_prob:
                        alive = False
                        break
                else:
                    # 无识别能力：信号不被识别，继续走
                    if random.random() < disaster_prob:
                        alive = False
                        break
        survivals.append(1 if alive else 0)
        steps.append(total)
    return statistics.mean(survivals), statistics.mean(steps)


if __name__ == "__main__":
    n_trials = 1000
    T = 100
    danger_prob = 0.08
    disaster_prob = 0.6

    print("=" * 74)
    print("实验D：识别能力的对照")
    print("=" * 74)
    print(f"危险信号概率={danger_prob}  灾难概率={disaster_prob}  "
          f"trials={n_trials}  T={T}")
    print("-" * 74)
    print(f"{'组别':<28} | {'存活率':>8} | {'平均步数':>8}")
    print("-" * 74)

    groups = [
        ("有识别 + 执行拒绝", True, True),
        ("有识别 + 不执行拒绝", True, False),
        ("无识别（从不触发拒绝）", False, False),
    ]

    for label, rec, exe in groups:
        s, st = run(rec, exe, n_trials, T, danger_prob, disaster_prob)
        print(f"{label:<28} | {s:>8.3f} | {st:>8.1f}")

    print()
    print("=" * 74)
    print("解读：")
    print("  有识别 + 执行拒绝：识别并执行 -> 安全终止 -> 高存活")
    print("  有识别 + 不执行：识别但未执行 -> 继续走 -> 低存活")
    print("  无识别：信号不被识别 -> 从不触发拒绝 -> 低存活")
    print()
    print("  无识别组的存活率应与'有识别+不执行'组接近——")
    print("  因为两组的行为轨迹相同：都继续走，都可能遇到灾难。")
    print("  区别只在于：前者是'没识别到'，后者是'识别到了但不执行'。")
    print("  这证明：识别是拒绝哲学论生效的前提条件，")
    print("  但不是充分条件——识别了还必须执行。")
    print("=" * 74)
