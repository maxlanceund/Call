import random

def simulate_endgame(mode="China"):
    capacity = 100.0  
    capitalist_wealth = 20.0 
    npc_wealth = 60.0 
    tick = 0
    capital_growth_rate = 0.08    
    capacity_decay_rate = 0.01 
    tfp_growth = 0.02             
    friction_base = 0.15           
    
    # 初始吸血效率
    siphon_rate = 0.015 
    
    while tick < 300: 
        tick += 1
        
        # 科技突破
        if tick % 15 == 0:
            tech_bonus = 1.5 if tick < 50 else 1.2
            capacity *= tech_bonus
            friction_base *= 0.9
        
        # 吸血机制（带反噬和衰减）
        if mode == "US" or mode == "China_Siphon":
            # 随着时间推移，外部资源被抽干，吸血效率每年衰减 2%
            siphon_rate *= 0.98 
            # 持续吸血导致外部反抗，摩擦力逐年增加
            friction_base += (0.01 * tick) 
            
            if tick > 10:
                external_gain = capacity * siphon_rate
                capacity += external_gain

        if tick > 30:
            tfp_growth *= 0.98 

        capacity *= (1 - capacity_decay_rate)
        capitalist_wealth *= (1 + capital_growth_rate)
        
        wealth_gap = capitalist_wealth / (capitalist_wealth + npc_wealth)
        npc_wealth *= (1 + tfp_growth * (1 - wealth_gap))
        
        friction = friction_base + max(0, (wealth_gap - 0.1) * 2.5)
        
        # 国家强行干预
        if capitalist_wealth > npc_wealth * 1.5 or friction > 0.8:
            seized = capitalist_wealth * 0.4
            capitalist_wealth -= seized
            npc_wealth += seized * 0.7
            friction_base = 0.15 
            capital_growth_rate = max(0.02, capital_growth_rate - 0.01)
            tfp_growth = max(0.005, tfp_growth - 0.005)

        total_load = capitalist_wealth + (friction_base + friction) * 10
        
        if total_load >= capacity:
            return tick
            
    return 300

if __name__ == "__main__":
    print("🌍 启动 V13.0：大国终极博弈（吸血衰减与反噬摩擦）...\n")
    runs = 10000
    total_us, total_china_pure, total_china_siphon = 0, 0, 0
    surv_us, surv_china_pure, surv_china_siphon = 0, 0, 0

    for _ in range(runs):
        year_us = simulate_endgame("US")
        year_cp = simulate_endgame("China_Pure")
        year_cs = simulate_endgame("China_Siphon")
        
        total_us += year_us
        total_china_pure += year_cp
        total_china_siphon += year_cs
        
        if year_us >= 300: surv_us += 1
        if year_cp >= 300: surv_china_pure += 1
        if year_cs >= 300: surv_china_siphon += 1

    print("="*50)
    print(f"📊 终极推演结果 ({runs:,}组)")
    print("-" * 50)
    print(f"🇺🇸 美国模式 (霸权吸血 + 反噬摩擦):")
    print(f"   💀 平均死寂年份: {total_us/runs:.2f} 年 | 🕊️ 活过300年: {surv_us} 个")
    print("-" * 50)
    print(f"🇨🇳 中国模式A (纯内循环):")
    print(f"   💀 平均死寂年份: {total_china_pure/runs:.2f} 年 | 🕊️ 活过300年: {surv_china_pure} 个")
    print("-" * 50)
    print(f"🇨🇳 中国模式B (带贸易吸血 + 反噬摩擦):")
    print(f"   💀 平均死寂年份: {total_china_siphon/runs:.2f} 年 | 🕊️ 活过300年: {surv_china_siphon} 个")
    print("="*50)
    print("结论：当吸血效率衰减且反噬摩擦暴增时，所有的吸血外挂最终都会失效。")
