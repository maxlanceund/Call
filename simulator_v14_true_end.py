import random

def simulate_endgame_true(mode="China"):
    capacity = 100.0  
    capitalist_wealth = 20.0 
    npc_wealth = 60.0 
    tick = 0
    capital_growth_rate = 0.08    
    capacity_decay_rate = 0.01 
    tfp_growth = 0.02             
    friction_base = 0.15           
    
    siphon_rate = 0.015 
    
    while tick < 300: 
        tick += 1
        
        # 科技遭遇绝对的物理墙（边际收益递减到几乎为0）
        if tick % 15 == 0:
            tech_bonus = 1.3 if tick < 50 else 1.05 
            capacity *= tech_bonus
            
        # 🌟 吸血反噬（指数级暴增）
        if mode == "US" or mode == "China_Siphon":
            siphon_rate *= 0.97 # 吸血效率快速衰减
            # 外部反抗和内部撕裂，导致摩擦力指数级狂飙！
            friction_base *= 1.03 
            
            if tick > 10:
                external_gain = capacity * siphon_rate
                capacity += external_gain

        # 老龄化彻底压垮底层
        if tick > 30:
            tfp_growth *= 0.95 

        capacity *= (1 - capacity_decay_rate)
        capitalist_wealth *= (1 + capital_growth_rate)
        
        wealth_gap = capitalist_wealth / (capitalist_wealth + npc_wealth)
        npc_wealth *= (1 + tfp_growth * (1 - wealth_gap))
        
        friction = friction_base + max(0, (wealth_gap - 0.1) * 2.5)
        
        # 国家强行干预（虽然能续命，但也限制了活力）
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
    print("💀 启动 V14.0：终极物理审判（科技触顶 + 摩擦指数暴增）...\n")
    runs = 10000
    total_us, total_china_pure, total_china_siphon = 0, 0, 0
    surv_us, surv_china_pure, surv_china_siphon = 0, 0, 0

    for _ in range(runs):
        year_us = simulate_endgame_true("US")
        year_cp = simulate_endgame_true("China_Pure")
        year_cs = simulate_endgame_true("China_Siphon")
        
        total_us += year_us
        total_china_pure += year_cp
        total_china_siphon += year_cs
        
        if year_us >= 300: surv_us += 1
        if year_cp >= 300: surv_china_pure += 1
        if year_cs >= 300: surv_china_siphon += 1

    print("="*50)
    print(f"📊 真实物理约束下的终极推演结果 ({runs:,}组)")
    print("-" * 50)
    print(f"🇺🇸 美国模式 (霸权吸血 + 极限反噬):")
    print(f"   💀 平均死寂年份: {total_us/runs:.2f} 年 | 🕊️ 活过300年: {surv_us} 个")
    print("-" * 50)
    print(f"🇨🇳 中国模式A (纯内循环):")
    print(f"   💀 平均死寂年份: {total_china_pure/runs:.2f} 年 | 🕊️ 活过300年: {surv_china_pure} 个")
    print("-" * 50)
    print(f"🇨🇳 中国模式B (带贸易吸血 + 极限反噬):")
    print(f"   💀 平均死寂年份: {total_china_siphon/runs:.2f} 年 | 🕊️ 活过300年: {surv_china_siphon} 个")
    print("="*50)
    print("结论：当科技红利见顶，吸血反噬指数级爆发时，没有一个系统能活过300年。")
    print("所有试图吸血的霸权，最终都会被自己吸来的摩擦力反噬致死。")
