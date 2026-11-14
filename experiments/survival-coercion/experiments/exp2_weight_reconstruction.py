"""实验二：把中国因素推到极端上界，看权重还剩多少
纯算术重构，不依赖外部数据
"""

def main():
    print("=" * 70)
    print("实验二：权重重构 —— 中国因素的极端上界")
    print("=" * 70)
    print("基准分解（Hicks & Devaraj, 2015）:")
    print("  2000-2010 制造业岗位流失中：")
    print("    生产率提升（自动化）: 87.8%")
    print("    贸易因素:            13.4%")
    print()

    baseline_trade = 13.4
    scenarios = [
        ("基准：贸易因素全部归中国", baseline_trade),
        ("Autor et al. 上界：贸易解释1/4", 25.0),
        ("人为翻倍：13.4% × 2", baseline_trade * 2),
        ("极端上界：贸易因素占40%", 40.0),
    ]

    print("%-38s | %10s | %10s | %12s" % (
        "情景", "中国因素", "自动化剩余", "倍数(自动化/中国)"))
    print("-" * 78)

    for label, trade_share in scenarios:
        auto_share = 100.0 - trade_share
        ratio = auto_share / trade_share if trade_share > 0 else float('inf')
        print("%-38s | %9.1f%% | %9.1f%% | %11.2fx" % (
            label, trade_share, auto_share, ratio))

    print()
    print("=" * 70)
    print("结论：")
    print("  即使把中国因素的权重推到极端上界（40%），")
    print("  自动化/生产率仍然是它的 1.5 倍以上。")
    print("  在基准和主流估计下，自动化是中国的 3-7 倍。")
    print("  '中国是主因'在数量级上不成立。")
    print("=" * 70)

if __name__ == "__main__":
    main()
