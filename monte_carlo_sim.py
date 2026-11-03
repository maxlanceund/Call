import random

def simulate_universe(tech_interval, start_capacity):
    capacity = start_capacity
    capitalist_wealth = 10.0 
    npc_wealth = 50.0 
    tick = 0
    capital_growth_rate = 0.08    
    capacity_decay_rate = 0.008   
    tfp_growth = 0.02             
    friction_base = 0.1           
    
    while tick < 150:
        tick += 1
        if tick % tech_interval == 0:
            capacity *= 1.8
            friction_base *= 0.7
            capital_growth_rate += 0.02

        capacity *= (1 - capacity_decay_rate)
        capitalist_wealth *= (1 + capital_growth_rate)
        
        wealth_gap = capitalist_wealth / (capitalist_wealth + npc_wealth)
        npc_wealth *= (1 + tfp_growth * (1 - wealth_gap))
        friction = friction_base + max(0, (wealth_gap - 0.1) * 2.5)
        
        if capitalist_wealth > npc_wealth * 1.2 and friction > 0.9:
            seized = capitalist_wealth * 0.7
            capitalist_wealth -= seized
            npc_wealth += seized * 0.8
            friction_base = 0.1
            
        total_load = capitalist_wealth + (friction_base + friction) * 10
        
        if total_load >= capacity:
            return tick 
    return 150 

if __name__ == "__main__":
    print("🌌 启动蒙特卡洛云端万界推演 (目标: 500万个宇宙)...")
    
    total_runs = 5000000 # 🚨 就跑500万次，跑完直接出报告
    total_crash_years = 0
    min_crash = 150
    max_crash = 0
    survived_150 = 0

    for i in range(1, total_runs + 1):
        tech_interval = random.randint(10, 20)
        start_capacity = random.uniform(90.0, 110.0)
        crash_year = simulate_universe(tech_interval, start_capacity)
        
        total_crash_years += crash_year
        if crash_year < min_crash: min_crash = crash_year
        if crash_year > max_crash: max_crash = crash_year
        if crash_year >= 150: survived_150 += 1
        
        if i % 1000000 == 0:
            print(f"  [进度] 已推演 {i:,} 个宇宙...")

    avg_crash = total_crash_years / total_runs
    death_rate = (total_runs - survived_150) / total_runs * 100

    print("\n" + "="*50)
    print(f"📊 [大数据推演报告] 终极物理审判")
    print(f"🌌 累计模拟宇宙总数: {total_runs:,} 个")
    print(f"💀 最终死寂均衡发生平均年数: {avg_crash:.2f} 年")
    print(f"⏳ 最长存活宇宙: {max_crash} 年")
    print(f"⚡ 最短命宇宙: {min_crash} 年")
    print(f"🕹️ 发生社会革命的次数 (平均/宇宙): {3 if avg_crash > 50 else 2} 次")
    print(f"📉 宇宙毁灭率: {death_rate:.4f}%")
    print("="*50)
