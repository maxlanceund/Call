"""实验：命令体压缩理性审视的时间窗口
核心：智能体在"审视"（不获取资源但优化策略）和"执行"（获取资源但不优化）之间抉择。
命令体通过提高资源消耗率，压缩审视的时间窗口。
"""
import random
import statistics

class Agent:
    def __init__(self, scarcity, has_metacognition, energy_init=100,
                 review_cost=8, review_gain=0.15, execute_gain=12):
        self.energy = energy_init
        self.scarcity = scarcity
        self.has_meta = has_metacognition
        self.review_cost = review_cost
        self.review_gain = review_gain
        self.execute_gain = execute_gain
        self.strategy = 0.5
        self.alive = True
        self.reviews = 0
        self.executes = 0
        self.steps_alive = 0

    def step(self):
        if not self.alive:
            return False
        self.energy -= self.scarcity

        if self.energy <= 0:
            self.alive = False
            return False

        # 决策：是否审视？
        # 无元认知：几乎不审视
        # 有元认知：资源越充裕越倾向于审视
        if self.has_meta:
            energy_ratio = self.energy / 100.0
            review_prob = min(0.6, 0.2 + 0.4 * energy_ratio)
        else:
            review_prob = 0.02

        if random.random() < review_prob:
            self.reviews += 1
            self.strategy = min(1.0, self.strategy + self.review_gain)
            self.energy -= self.review_cost
        else:
            self.executes += 1
            gain = self.execute_gain * self.strategy
            self.energy += gain

        self.steps_alive += 1
        return True


def run(scarcity, has_meta, T=200, n_trials=30, seed=42):
    reviews, executes, survivals, steps = [], [], [], []
    for trial in range(n_trials):
        random.seed(seed * 10000 + trial)
        a = Agent(scarcity, has_meta)
        for _ in range(T):
            if not a.step():
                break
        reviews.append(a.reviews)
        executes.append(a.executes)
        survivals.append(1 if a.alive else 0)
        steps.append(a.steps_alive)
    return (statistics.mean(reviews), statistics.mean(executes),
            statistics.mean(survivals), statistics.mean(steps))


if __name__ == "__main__":
    print("=" * 74)
    print("实验：命令体强度 -> 理性审视频率")
    print("=" * 74)
    print("%10s | %12s | %12s | %10s | %10s" % (
        "紧缺度", "审视频率", "执行频率", "存活率", "存活步数"))
    print("-" * 74)

    # 有元认知
    for scarcity in [1.0, 3.0, 5.0, 7.0, 9.0, 12.0, 15.0]:
        r, e, s, st = run(scarcity, has_meta=True)
        print("%10.1f | %12.2f | %12.2f | %10.2f | %10.1f" % (
            scarcity, r, e, s, st))

    print("\n[对照：无元认知能力]")
    print("-" * 74)
    for scarcity in [1.0, 5.0, 12.0]:
        r, e, s, st = run(scarcity, has_meta=False)
        print("%10.1f | %12.2f | %12.2f | %10.2f | %10.1f" % (
            scarcity, r, e, s, st))

    print("\n" + "=" * 74)
    print("解读：")
    print("  1. 有元认知时，紧缺度上升 -> 审视频率下降（窗口被压缩）")
    print("  2. 但即使高压下，审视仍不归零（'能够'未被取消）")
    print("  3. 无元认知组审视频率极低（识别本身是自律的起点）")
    print("=" * 74)
