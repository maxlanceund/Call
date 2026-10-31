"""实验一：自我指针绑定
假设 H1："我"是一个为了整合内部信号而操作性地绑定到某个载体上的指针。
系统接收 Body A 的特权内部信号，对 Body B 没有内部信号。
测：系统能否自发学会把内部状态与 Body A 绑定。
"""
import random
import statistics


class World:
    def __init__(self, rng):
        self.rng = rng

    def step(self):
        # 两个身体有相同的外部运动，但只有 A 产生内部信号
        action_a = self.rng.choice([-1, 0, 1])
        action_b = self.rng.choice([-1, 0, 1])
        # 内部信号：只有 A 有
        internal_a = action_a
        # 外部结果：动作影响各自位置
        pos_a = action_a + self.rng.gauss(0, 0.1)
        pos_b = action_b + self.rng.gauss(0, 0.1)
        return {
            "internal_a": internal_a,
            "action_a": action_a,
            "action_b": action_b,
            "pos_a": pos_a,
            "pos_b": pos_b,
        }


class Agent:
    def __init__(self):
        # 对两个身体的绑定权重，初始随机
        self.w_a = random.uniform(0, 1)
        self.w_b = random.uniform(0, 1)

    def predict(self, internal_signal, action_a, action_b, body):
        if body == "A":
            return internal_signal * self.w_a
        else:
            return internal_signal * self.w_b

    def learn(self, internal_signal, action_a, action_b,
              actual_a, actual_b, lr=0.01):
        # 用预测误差更新绑定权重
        err_a = actual_a - self.predict(internal_signal, action_a, action_b, "A")
        err_b = actual_b - self.predict(internal_signal, action_a, action_b, "B")
        self.w_a += lr * err_a * internal_signal
        self.w_b += lr * err_b * internal_signal


def run(T=2000, seed=0):
    rng = random.Random(seed)
    world = World(rng)
    agent = Agent()
    w_a_curve, w_b_curve = [], []
    for t in range(T):
        s = world.step()
        # 用 internal_a 预测 pos_a 和 pos_b
        agent.learn(s["internal_a"], s["action_a"], s["action_b"],
                    s["pos_a"], s["pos_b"])
        w_a_curve.append(agent.w_a)
        w_b_curve.append(agent.w_b)
    return w_a_curve, w_b_curve


if __name__ == "__main__":
    print("=" * 70)
    print("实验一：自我指针绑定")
    print("=" * 70)
    print("系统只接收 Body A 的内部信号，对 Body B 没有内部信号。")
    print("测：绑定权重 w_a 和 w_b 是否分化。")
    print()

    all_wa, all_wb = [], []
    for seed in range(10):
        wa, wb = run(T=2000, seed=seed)
        all_wa.append(wa[-1])
        all_wb.append(wb[-1])

    print("%12s | %12s | %12s" % ("", "最终 w_a", "最终 w_b"))
    print("-" * 42)
    print("%12s | %10.3f | %10.3f" % (
        "均值", statistics.mean(all_wa), statistics.mean(all_wb)))
    print("%12s | %10.3f | %10.3f" % (
        "标准差", statistics.stdev(all_wa), statistics.stdev(all_wb)))

    print()
    if statistics.mean(all_wa) > statistics.mean(all_wb) * 2:
        print("结果：绑定权重显著分化，系统自发把内部信号绑定到 Body A。")
        print("对应论文：'我'是一个操作化的指针，不是预设的实体。")
    else:
        print("结果：绑定权重未显著分化，H1 被削弱。")
