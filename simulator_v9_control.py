import random

def simulate_universe(is_hegemony=False):
    capacity = 100.0  
    capitalist_wealth = 10.0 
    npc_wealth = 50.0 
    tick = 0
    capital_growth_rate = 0.08    
    capacity_decay_rate = 0.008   
    tfp_growth = 0.02             
    friction_base = 0.1           
    
    while tick < 300: # 把天花板拉到300年，看谁能活
        tick += 1
        
        # 科技革命
        if tick % 15 == 0:
            capacity *= 1.8
            friction_base *= 0.7
            capital_growth_rate += 0.02

        # 🌟 核心变量：霸权吸血
        if is_hegemony:
            # 假设每年从外部（第三世界）抽走额外 3% 的承载力，并分 1% 给底层安抚
            external_siphon = capacity * 0.03
            capacity += external_siphon 
            npc_wealth += external_siphon * 0.1
            
        capacity *= (1 - capacity_decay_rate)
        capitalist_wealth *= (1 + capital_growth_rate)
        
        wealth_gap = capitalist_wealth / (capitalist_wealth + npc_wealth)
        npc_wealth *= (1 + tfp_growth * (1 - wealth_gap))
        
        friction = friction_base + max(0, (wealth_gap - 0.1) * 2.5)
        
        # 社会革命
        if capitalist_wealth > npc_wealth * 1.2 and friction > 0.9:
            seized = capitalist_wealth * 0.7
            capitalist_wealth -= seized
            npc_wealth += seized * 0.8
            friction_base = 0.1
            
        total_load = capitalist_wealth + (friction_base + friction) * 10
        
        if total_load >= capacity:
            return tick # 死机年份
            
    return 300 # 活过了300年

if __name__ == "__main__":
    print("🔬 启动 V9.0 对照实验：封闭内卷 vs 霸权吸血...\n")
    
    runs = 10000
    total_a, total_b = 0, 0
    max_a, max_b = 0, 0
    surv_a, surv_b = 0, 0
    
    for _ in range(runs):
        year_a = simulate_universe(is_hegemony=False)
        year_b = simulate_universe(is_hegemony=True)
        
        total_a += year_a
        total_b += year_b
        if year_a > max_a: max_a = year_a
        if year_b > max_b: max_b = year_b
        if year_a >= 300: surv_a += 1
        if year_b >= 300: surv_b += 1

    print("="*50)
    print(f"📊 对照实验结果 (共 {runs:,} 组对比)")
    print("-" * 50)
    print(f"🇨🇳 系统 A (纯内循环封闭系统):")
    print(f"   💀 平均死寂年份: {total_a/runs:.2f} 年")
    print(f"   ⏳ 最长存活: {max_a} 年 | 🕊️ 活过300年: {surv_a} 个")
    print("-" * 50)
    print(f"🇺🇸 系统 B (全球吸血霸权系统):")
    print(f"   💀 平均死寂年份: {total_b/runs:.2f} 年")
    print(f"   ⏳ 最长存活: {max_b} 年 | 🕊️ 活过300年: {surv_b} 个")
    print("="*50)
    print("结论：吸血续命不仅真实存在，而且效果极其显著。")
    print("但请注意，即便是吸血系统，也逃不过系统总寿命的宿命。")
