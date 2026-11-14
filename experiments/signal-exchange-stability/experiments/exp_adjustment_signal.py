import random

def run(N, frac_edge, s_internal, s_edge_init, c_mean, c_std,
        P_crit, P_warn, T, shock_start, shock_per_round,
        adjust_start, adjust_rate, use_adjustment, seed):
    """
    每个边缘节点有自己的退出成本 c_i ~ N(c_mean, c_std)。
    动机 > c_i 的节点退出。这使得 P 逐渐下降，而非一轮崩塌。
    """
    rng = random.Random(seed)
    n_edge = int(N * frac_edge)
    n_internal = N - n_edge
    # 每个边缘节点一个 c_i
    c_edge = [max(0.01, rng.gauss(c_mean, c_std)) for _ in range(n_edge)]
    s_edge = s_edge_init
    P_curve = []
    for t in range(T + 1):
        if t >= shock_start:
            s_edge = max(0.0, s_edge - shock_per_round)
        max_s = max(s_internal, s_edge)
        # 内部节点：永远参与（动机为 0）
        participating = n_internal
        for ci in c_edge:
            motivation = (max_s - s_edge) / max_s if max_s > 0 else 0
            if motivation <= ci:
                participating += 1
        P = participating / N
        P_curve.append(P)
        if P < P_crit:
            break
        if use_adjustment and t >= adjust_start and P < P_warn:
            s_edge = min(s_edge + adjust_rate, s_internal)
    return P_curve


if __name__ == "__main__":
    N = 1000
    frac_edge = 0.8
    s_internal = 100.0
    s_edge_init = 70.0
    c_mean = 0.5
    c_std = 0.15
    P_crit = 0.5
    P_warn = 0.85
    T = 300
    shock_start = 5
    shock_per_round = 2.0

    print("=" * 60)
    print("H3：调整信号的作用（异质节点 + 渐进冲击）")
    print("N=%d  edge=%.2f  c_mean=%.2f  c_std=%.2f" % (
        N, frac_edge, c_mean, c_std))
    print("冲击：第%d轮起，每轮 -%.1f  |  P_crit=%.2f  P_warn=%.2f" % (
        shock_start, shock_per_round, P_crit, P_warn))
    print("=" * 60)

    print("")
    print("[对照组] 只冲击，无调整")
    P = run(N, frac_edge, s_internal, s_edge_init, c_mean, c_std,
            P_crit, P_warn, T, shock_start, shock_per_round,
            adjust_start=T+1, adjust_rate=0, use_adjustment=False, seed=0)
    print("  最终参与率=%.4f  轮数=%d  -> %s" % (
        P[-1], len(P)-1, "稳定" if P[-1] > P_crit else "崩溃"))

    print("")
    print("[组A] 冲击 + 调整，每轮 +2")
    P = run(N, frac_edge, s_internal, s_edge_init, c_mean, c_std,
            P_crit, P_warn, T, shock_start, shock_per_round,
            adjust_start=shock_start, adjust_rate=2.0, use_adjustment=True, seed=0)
    print("  最终参与率=%.4f  轮数=%d  -> %s" % (
        P[-1], len(P)-1, "稳定" if P[-1] > P_crit else "崩溃"))

    print("")
    print("[组B] 冲击 + 调整，每轮 +5")
    P = run(N, frac_edge, s_internal, s_edge_init, c_mean, c_std,
            P_crit, P_warn, T, shock_start, shock_per_round,
            adjust_start=shock_start, adjust_rate=5.0, use_adjustment=True, seed=0)
    print("  最终参与率=%.4f  轮数=%d  -> %s" % (
        P[-1], len(P)-1, "稳定" if P[-1] > P_crit else "崩溃"))

    print("")
    print("[组C] 冲击 + 调整，每轮 +10（强）")
    P = run(N, frac_edge, s_internal, s_edge_init, c_mean, c_std,
            P_crit, P_warn, T, shock_start, shock_per_round,
            adjust_start=shock_start, adjust_rate=10.0, use_adjustment=True, seed=0)
    print("  最终参与率=%.4f  轮数=%d  -> %s" % (
        P[-1], len(P)-1, "稳定" if P[-1] > P_crit else "崩溃"))

    print("")
    print("[组D] 冲击 + 调整，但滞后到第50轮才启动")
    P = run(N, frac_edge, s_internal, s_edge_init, c_mean, c_std,
            P_crit, P_warn, T, shock_start, shock_per_round,
            adjust_start=50, adjust_rate=10.0, use_adjustment=True, seed=0)
    print("  最终参与率=%.4f  轮数=%d  -> %s" % (
        P[-1], len(P)-1, "稳定" if P[-1] > P_crit else "崩溃"))
