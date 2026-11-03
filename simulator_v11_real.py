import random

def simulate_china_real():
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
        
        # 科技突破（边际收益递减：越往后越难）
        if tick % 15 == 0:
            tech_bonus = 1.5 if tick < 50 else 1.1 # 早期科技红利大，后期卡脖子
            capacity *= tech_bonus
            friction_base *= 0.9
        
        # 老龄化拖累（TFP逐年下降）
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
            # 副作用：资本家躺平，复利和生产力下降
            capital_growth_rate = max(0.02, capital_growth_rate - 0.01)
            tfp_growth = max(0.005, tfp_growth - 0.005)

        total_load = capitalist_wealth + (friction_base + friction) * 10
        
        if total_load >= capacity:
            return tick
            
    return 200

if __name__ == "__main__":
    print("🇨🇳 启动 V11.0：真实物理约束下的中国模式...\n")
    runs = 10000
    total_years = 0
    max_year = 0
    surv_200 = 0

    for _ in range(runs):
        year = simulate_china_real()
        total_years += year
        if year > max_year: max_year = year
        if year >= 200: surv_200 += 1

    print("="*50)
    print(f"📊 真实参数约束下的推演结果 ({runs:,}组)")
    print(f"💀 平均死寂年份: {total_years/runs:.2f} 年")
    print(f"⏳ 最长存活: {max_year} 年 | 🕊️ 活过200年: {surv_200} 个")
    print("="*50)
    print("结论：把科技瓶颈、老龄化、资本躺平因素算进去后，")
    print("没有任何系统能靠单纯的干预实现真正的永生。")
