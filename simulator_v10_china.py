import random

def simulate_china(is_state_intervention=False):
    capacity = 100.0  
    capitalist_wealth = 20.0 # 初始资本较高
    npc_wealth = 60.0 
    tick = 0
    capital_growth_rate = 0.08    
    capacity_decay_rate = 0.01 # 环境与资源压力比美国大
    tfp_growth = 0.02             
    friction_base = 0.15           # 初始人口基数大，基础摩擦力高
    
    while tick < 200: 
        tick += 1
        
        # 🌟 举国体制外挂：极高频的科技突破（五年规划、十年计划）
        if is_state_intervention:
            if tick % 10 == 0:
                capacity *= 1.5 # 强行扩容（AI、新能源、特高压）
                friction_base *= 0.85 
        else:
            # 自由放任：科技突破慢
            if tick % 20 == 0:
                capacity *= 1.2

        capacity *= (1 - capacity_decay_rate)
        capitalist_wealth *= (1 + capital_growth_rate)
        
        wealth_gap = capitalist_wealth / (capitalist_wealth + npc_wealth)
        npc_wealth *= (1 + tfp_growth * (1 - wealth_gap))
        
        friction = friction_base + max(0, (wealth_gap - 0.1) * 2.5)
        
        # 🌟 举国体制外挂：强行干预，打断资本复利（反垄断、共同富裕、房产税）
        if is_state_intervention and (capitalist_wealth > npc_wealth * 1.5 or friction > 0.8):
            # 国家强制收割 50% 的资本，补贴底层
            seized = capitalist_wealth * 0.5
            capitalist_wealth -= seized
            npc_wealth += seized * 0.8
            friction_base = 0.15 # 强行降摩擦
            capital_growth_rate = 0.06 # 强行限制资本无序扩张
        else:
            # 自由放任下爆发的暴力社会革命（周期律）
            if capitalist_wealth > npc_wealth * 1.2 and friction > 0.9:
                seized = capitalist_wealth * 0.7
                capitalist_wealth -= seized
                npc_wealth += seized * 0.8
                friction_base = 0.15

        total_load = capitalist_wealth + (friction_base + friction) * 10
        
        if total_load >= capacity:
            return tick # 死机年份
            
    return 200

if __name__ == "__main__":
    print("🇨🇳 启动 V10.0：中国模式对照实验 (自由放任 vs 举国干预)...\n")
    
    runs = 10000
    total_c, total_d = 0, 0
    max_c, max_d = 0, 0
    surv_c, surv_d = 0, 0
    
    for _ in range(runs):
        year_c = simulate_china(is_state_intervention=False)
        year_d = simulate_china(is_state_intervention=True)
        
        total_c += year_c
        total_d += year_d
        if year_c > max_c: max_c = year_c
        if year_d > max_d: max_d = year_d
        if year_c >= 200: surv_c += 1
        if year_d >= 200: surv_d += 1

    print("="*50)
    print(f"📊 对照实验结果 (共 {runs:,} 组对比)")
    print("-" * 50)
    print(f"🇨🇳 系统 C (纯自由放任 / 资本狂欢):")
    print(f"   💀 平均死寂年份: {total_c/runs:.2f} 年")
    print(f"   ⏳ 最长存活: {max_c} 年 | 🕊️ 活过200年: {surv_c} 个")
    print("-" * 50)
    print(f"🇨🇳 系统 D (国家强力干预 / 科技+重分配):")
    print(f"   💀 平均死寂年份: {total_d/runs:.2f} 年")
    print(f"   ⏳ 最长存活: {max_d} 年 | 🕊️ 活过200年: {surv_d} 个")
    print("="*50)
    print("结论：没有外部吸血，全靠内部疯狂续命。")
    print("举国体制的干预，本质是在用国家权力强行对抗资本的物理热力学。")
