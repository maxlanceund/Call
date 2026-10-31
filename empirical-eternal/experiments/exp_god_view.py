"""实验D：上帝视角对照
有限代理 vs 超时间代理，对同一个“永恒命题”的判定差异。
"""

class FiniteAgent:
    def __init__(self, max_steps):
        self.max_steps = max_steps

    def judge(self, p_true_forever):
        for _ in range(self.max_steps):
            if not p_true_forever:
                return "REFUTED"
        return "SUSPENDED"


class GodViewAgent:
    """直接访问无限未来的真值表"""
    def judge(self, p_true_forever):
        if p_true_forever:
            return "VERIFIED"
        else:
            return "REFUTED"


if __name__ == "__main__":
    print("=" * 60)
    print("实验D：上帝视角对照")
    print("=" * 60)
    print("%-16s | %-12s | %-12s" % ("代理类型", "P全真时", "P偶尔假时"))
    print("-" * 60)

    finite = FiniteAgent(max_steps=10000)
    god = GodViewAgent()

    print("%-16s | %-12s | %-12s" % (
        "有限代理", finite.judge(True), finite.judge(False)))
    print("%-16s | %-12s | %-12s" % (
        "上帝视角代理", god.judge(True), god.judge(False)))

    print("\n" + "=" * 60)
    print("解读：")
    print("  有限代理：P全真 -> SUSPENDED（认知悬置）")
    print("  上帝视角：P全真 -> VERIFIED（可判定）")
    print("  差异的来源不是'永恒'本身，而是认知结构的有限性。")
    print("  这正是论文的立场：认知悬置是有限认知的产物，")
    print("  不是'永恒真理不存在'的本体论断言。")
    print("=" * 60)
