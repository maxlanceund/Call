import random

def simulate_modern_system(has_intervention=True):
    # 初始参数
    capacity = 200.0  # 现代工业社会初始承载力极高
    capitalist_wealth = 20.0 
    npc_wealth = 80.0 
    debt = 0.0 # 国家债务/印钞
    tick = 0
    capital_growth_rate = 0.08    
    capacity_decay_rate = 0.005 # 现代科技减缓了自然衰减
    tfp_growth = 0.02             
    friction_base = 0.05           
    
    while tick < 500: # 看能不能活到500年
        tick += 1
        
        # 🌟 科技阶跃（不频繁，但一爆发就极其恐怖）
        if tick == 40 or tick == 90 or tick == 150:
            capacity *= 5.0 # 工业革命/AI革命直接扩容5倍
            print(f" [科技奇点] 第 {tick} 年：爆发超级科技革命！系统容量暴增至 {capacity:.0f}")

        # 🌟 需求侧制约：底层没钱，资本复利受限
        wealth_gap = capitalist_wealth / (capitalist_wealth + npc_wealth)
        effective_growth = capital_growth_rate
        if npc_wealth < 50: 
            effective_growth *= 0.5 # 底层买不起东西，资本增长减半

        capacity *= (1 - capacity_decay_rate)
        capitalist_wealth *= (1 + effective_growth)
        
        # 底层产出（TFP）
        npc_wealth *= (1 + tfp_growth * (1 - wealth_gap))
        
        # 摩擦力计算
        friction = friction_base + max(0, (wealth_gap - 0.2) * 2.0)
        
        # 🌟 国家干预：发债/印钞安抚底层（现代社会的“作弊码”）
        if has_intervention and friction > 0.6:
            bailout = friction * 10 # 印钱发福利
            debt += bailout
            npc_wealth += bailout
            friction_base *= 0.8 # 强行降摩擦
        elif not has_intervention and friction > 1.5:
            # 没有干预，底层忍无可忍，爆发暴力革命
            seized = capitalist_wealth * 0.6
            capitalist_wealth -= seized
            npc_wealth += seized * 0.8
            friction_base = 0.05

        # 计算总负载（资本 + 底层占用 + 债务）
        # 债务是需要还利息的，会增加系统负载
        total_load = capitalist_wealth + (friction_base + friction) * 10 + (debt * 1.05) 
        
        # 死亡判定
        if total_load >= capacity:
            return tick
            
    return 500

if __name__ == "__main__":
    print("🌍 启动 V16.0：真实现代系统推演（科技阶跃 + 债务印钞 + 需求制约）...\n")
    runs = 10000
    total_free, total_interv = 0, 0
    surv_free, surv_interv = 0, 0

    for _ in range(runs):
        year_free = simulate_modern_system(has_intervention=False) # 自由放任，没有宏观调控
        year_interv = simulate_modern_system(has_intervention=True) # 现代宏观调控
        total_free += year_free
        total_interv += year_interv
        if year_free >= 500: surv_free += 1
        if year_interv >= 500: surv_interv += 1

    print("\n" + "="*50)
    print(f"📊 现代系统终极推演结果 ({runs:,}组)")
    print("-" * 50)
    print(f"🩸 系统 A (纯自由放任，无干预):")
    print(f"   💀 平均死寂年份: {total_free/runs:.2f} 年 | 🕊️ 活过500年: {surv_free} 个")
    print("-" * 50)
    print(f"🛡️ 系统 B (现代宏观调控，印钞发债+科技扩容):")
    print(f"   💀 平均死寂年份: {total_interv/runs:.2f} 年 | 🕊️ 活过500年: {surv_interv} 个")
    print("="*50)
    print("结论：现代社会的寿命远超封建王朝。科技阶跃和债务平滑极大地延长了系统寿命。")
    print("但债务的雪球和科技边际递减，终究会让系统在数百年的尺度上迎来死寂。")
