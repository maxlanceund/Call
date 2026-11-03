import random

def simulate_china_siphon(has_siphon=False):
    capacity = 100.0  
    capitalist_wealth = 20.0 
    npc_wealth = 60.0 
    tick = 0
    capital_growth_rate = 0.08    
    capacity_decay_rate = 0.01 
    tfp_growth = 0.02             
    friction_base = 0.15           
    
    while tick < 200: 
        tick += 1
        
        # 科技突破（边际收益递减）
        if tick % 15 == 0:
            tech_bonus = 1.5 if tick < 50 else 1.1 
            capacity *= tech_bonus
            friction_base *= 0.9
        
        # 🌟 新增：中国式外部虹吸（假设通过贸易、一带一路抽取外部资源）
        if has_siphon:
            # 每年抽取 1.5% 的外部资源，但初期需要大量基建投入，所以前10年效果不明显
            if tick > 10:
                external_gain = capacity * 0.015
                capacity += external_gain
                # 抽取外部资源会导致外部反噬（摩擦力上升）
                friction_base += 0.005 

        # 老龄化拖累
        if tick > 30:
            tfp_growth *= 0.98 

        capacity *= (1 - capacity_decay_rate)
        capitalist_wealth *= (1 + capital_growth_rate)
        
        wealth_gap = capitalist_wealth / (capitalist_wealth + npc_wealth)
        npc_wealth *= (1 + tfp_growth * (1 - wealth_gap))
        
        friction = friction_base + max(0, (wealth_gap - 0.1) * 2.5)
        
        # 国家强行干预重分配
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
            
    return 200

if __name__ == "__main__":
    print("🇨🇳 启动 V12.0：中国吸血模式对照实验 (纯内循环 vs 贸易虹吸)...\n")
    runs = 10000
    total_no_siphon, total_has_siphon = 0, 0
    surv_no, surv_has = 0, 0

    for _ in range(runs):
        year_no = simulate_china_siphon(False)
        year_has = simulate_china_siphon(True)
        
        total_no_siphon += year_no
        total_has_siphon += year_has
        if year_no >= 200: surv_no += 1
        if year_has >= 200: surv_has += 1

    print("="*50)
    print(f"📊 对照实验结果 ({runs:,}组对比)")
    print("-" * 50)
    print(f"🚫 系统 C (纯内循环，死磕自己):")
    print(f"   💀 平均死寂年份: {total_no_siphon/runs:.2f} 年")
    print(f"   🕊️ 活过200年: {surv_no} 个")
    print("-" * 50)
    print(f"🌍 系统 D (中国式贸易吸血):")
    print(f"   💀 平均死寂年份: {total_has_siphon/runs:.2f} 年")
    print(f"   🕊️ 活过200年: {surv_has} 个")
    print("="*50)
    print("结论：外部虹吸能显著延长寿命，但代价是外部摩擦力上升。")
    print("吸血不是美国的专利，但物理定律决定了：天下没有免费的午餐。")
