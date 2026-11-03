import random

def simulate_interstellar(is_colonized=False):
    capacity = 100.0  
    capitalist_wealth = 20.0 
    npc_wealth = 60.0 
    tick = 0
    capital_growth_rate = 0.08    
    capacity_decay_rate = 0.01 
    tfp_growth = 0.02             
    friction_base = 0.15           
    
    while tick < 500: # 延长到500年，看能不能活过星际时代
        tick += 1
        
        # 🚀 50年后：星际殖民爆发（引入外部星系算力）
        if is_colonized and tick == 50:
            # 强行把容量拉大 10 倍，并且每年持续获取星系资源
            capacity *= 10.0 
            print(f" [系统日志] 第 {tick} 年：人类实现星际殖民！容量暴增！")
            
        if is_colonized and tick > 50:
            # 星际资源虹吸（每年额外获得 2% 容量），但运输成本导致摩擦剧增
            capacity += capacity * 0.02
            friction_base *= 1.02 # 星际维持成本剧增

        # 科技突破（依然是边际递减）
        if tick % 15 == 0:
            tech_bonus = 1.3 if tick < 100 else 1.05 
            capacity *= tech_bonus

        # 老龄化依然在拖后腿
        if tick > 30:
            tfp_growth *= 0.95 

        capacity *= (1 - capacity_decay_rate)
        
        # 星际时代的资本复利更加疯狂
        if is_colonized and tick > 50:
            capital_growth_rate += 0.02 # 资本疯狂扩张
        capitalist_wealth *= (1 + capital_growth_rate)
        
        wealth_gap = capitalist_wealth / (capitalist_wealth + npc_wealth)
        npc_wealth *= (1 + tfp_growth * (1 - wealth_gap))
        
        friction = friction_base + max(0, (wealth_gap - 0.1) * 2.5)
        
        # 国家干预/社会革命
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
            
    return 500

if __name__ == "__main__":
    print("🌌 启动 V15.0：大宇宙星际殖民推演...\n")
    runs = 10000
    total_earth, total_star = 0, 0
    surv_earth, surv_star = 0, 0

    for _ in range(runs):
        year_e = simulate_interstellar(False)
        year_s = simulate_interstellar(True)
        
        total_earth += year_e
        total_star += year_s
        if year_e >= 500: surv_earth += 1
        if year_s >= 500: surv_star += 1

    print("="*50)
    print(f"📊 星际变量推演结果 ({runs:,}组)")
    print("-" * 50)
    print(f"🌍 地球模式 (永远困在地球):")
    print(f"   💀 平均死寂年份: {total_earth/runs:.2f} 年 | 🕊️ 活过500年: {surv_earth} 个")
    print("-" * 50)
    print(f"🚀 星际模式 (50年后开启星际殖民):")
    print(f"   💀 平均死寂年份: {total_star/runs:.2f} 年 | 🕊️ 活过500年: {surv_star} 个")
    print("="*50)
    print("结论：星际扩容能提供极其漫长的时间，但星际级的资本复利和星系间的阶级隔离，")
    print("最终依然会演化成更大尺度的死寂均衡。")
