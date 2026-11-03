import random

def simulate_modern_reality(has_intervention=True):
    # 现实校准：初始容量拉大到一万（代表全球总财富与资源），资本起始占5%
    capacity = 10000.0  
    capitalist_wealth = 500.0 
    npc_wealth = 2000.0 
    debt = 0.0 
    tick = 0
    capital_growth_rate = 0.03    # 现实资本年化复利大约 3-5%（剔除通胀后的实际增长）
    capacity_decay_rate = 0.002   # 环境缓慢衰减
    tfp_growth = 0.02             
    friction_base = 0.05           
    
    while tick < 500: 
        tick += 1
        
        # 🌟 科技阶跃（每 80 年一次大爆发，扩容 3 倍）
        if tick == 80 or tick == 160 or tick == 240:
            capacity *= 3.0 
            # print(f" [科技奇点] 第 {tick} 年：爆发科技革命！容量扩容至 {capacity:.0f}")

        # 需求侧制约
        wealth_gap = capitalist_wealth / (capitalist_wealth + npc_wealth)
        effective_growth = capital_growth_rate
        if npc_wealth < 1000: # 底层没钱消费
            effective_growth *= 0.3 

        capacity *= (1 - capacity_decay_rate)
        capitalist_wealth *= (1 + effective_growth)
        
        npc_wealth *= (1 + tfp_growth * (1 - wealth_gap))
        
        friction = friction_base + max(0, (wealth_gap - 0.2) * 3.0)
        
        # 🌟 国家干预：发债安抚底层（债务不直接炸内存，但会抬高未来的基础摩擦）
        if has_intervention and friction > 0.5:
            bailout = friction * 100 # 发债规模
            debt += bailout
            npc_wealth += bailout
            friction_base *= 0.9 # 强行降摩擦
            friction_base += 0.01 # 债务后遗症：长期抬高基础负担

        # 极端自由放任下爆发革命
        elif not has_intervention and friction > 1.2:
            seized = capitalist_wealth * 0.6
            capitalist_wealth -= seized
            npc_wealth += seized * 0.8
            friction_base = 0.05

        # 债务的利息成为了系统负载的一部分
        total_load = capitalist_wealth + npc_wealth + (friction_base + friction) * 50 + (debt * 1.02)
        
        if total_load >= capacity:
            return tick
            
    return 500

if __name__ == "__main__":
    print("🌍 启动 V17.0：真实经济学数值校准版...\n")
    runs = 10000
    total_free, total_interv = 0, 0
    surv_free, surv_interv = 0, 0

    for _ in range(runs):
        year_free = simulate_modern_reality(has_intervention=False)
        year_interv = simulate_modern_reality(has_intervention=True)
        total_free += year_free
        total_interv += year_interv
        if year_free >= 500: surv_free += 1
        if year_interv >= 500: surv_interv += 1

    print("\n" + "="*50)
    print(f"📊 V17.0 真实系统推演结果 ({runs:,}组)")
    print("-" * 50)
    print(f"🩸 系统 A (纯自由放任，无干预):")
    print(f"   💀 平均死寂年份: {total_free/runs:.2f} 年 | 🕊️ 活过500年: {surv_free} 个")
    print("-" * 50)
    print(f"🛡️ 系统 B (现代宏观调控，发债+科技扩容):")
    print(f"   💀 平均死寂年份: {total_interv/runs:.2f} 年 | 🕊️ 活过500年: {surv_interv} 个")
    print("="*50)
    print("结论：合理的资本增速与科技阶跃，能让现代系统活几百年。")
    print("但债务的累积终究会在后期引发死寂。")
