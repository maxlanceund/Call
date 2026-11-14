import statistics

def run(N, frac_edge, s_internal, s_edge, c, P_crit, seed):
    """单轮决策：退出动机来自信号落差；退出成本 c 决定是否触发退出。"""
    n_edge = int(N * frac_edge)
    n_internal = N - n_edge
    signals = [s_internal] * n_internal + [s_edge] * n_edge
    max_s = max(signals)
    participating = 0
    for s in signals:
        motivation = (max_s - s) / max_s
        if motivation <= c:
            participating += 1
    return participating / N


if __name__ == "__main__":
    N = 1000
    frac_edge = 0.8
    P_crit = 0.5
    n_trials = 20

    print("=" * 60)
    print("信号-交换稳定性实验")
    print("N=%d  edge=%.2f  P_crit=%.2f" % (N, frac_edge, P_crit))
    print("=" * 60)

    print("")
    print("[情形一] 高不平等 (100 vs 10, 落差=0.9) + 低退出成本")
    for c in [0.1, 0.3, 0.5, 0.8]:
        Ps = []
        for trial in range(n_trials):
            P = run(N, frac_edge, 100.0, 10.0, c, P_crit, trial)
            Ps.append(P)
        avg = statistics.mean(Ps)
        std = statistics.stdev(Ps) if len(Ps) > 1 else 0
        status = "稳定" if avg > P_crit else "崩溃"
        print("  c=%.2f  参与率=%.4f +/- %.4f  -> %s" % (c, avg, std, status))

    print("")
    print("[情形二] 高不平等 + 高退出成本")
    for c in [0.9, 0.95, 0.99, 1.0]:
        Ps = []
        for trial in range(n_trials):
            P = run(N, frac_edge, 100.0, 10.0, c, P_crit, trial)
            Ps.append(P)
        avg = statistics.mean(Ps)
        std = statistics.stdev(Ps) if len(Ps) > 1 else 0
        status = "稳定" if avg > P_crit else "崩溃"
        print("  c=%.2f  参与率=%.4f +/- %.4f  -> %s" % (c, avg, std, status))

    print("")
    print("[情形三] 低不平等 (100 vs 80, 落差=0.2) - 对照")
    for c in [0.1, 0.3, 0.5]:
        Ps = []
        for trial in range(n_trials):
            P = run(N, frac_edge, 100.0, 80.0, c, P_crit, trial)
            Ps.append(P)
        avg = statistics.mean(Ps)
        std = statistics.stdev(Ps) if len(Ps) > 1 else 0
        status = "稳定" if avg > P_crit else "崩溃"
        print("  c=%.2f  参与率=%.4f +/- %.4f  -> %s" % (c, avg, std, status))
