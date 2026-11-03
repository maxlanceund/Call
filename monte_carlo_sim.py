import random
import time

# ==========================================
# 算力榨干版：蒙特卡洛微观宇宙推演
# ==========================================
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
        
        # 科技革命
        if tick % tech_interval == 0:
            capacity *= 1.8
            friction_base *= 0.7
            capital_growth_rate += 0.02

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
            return tick # 宇宙死机，返回年份
            
    return 150 # 活到了 150 年

if __name__ == "__main__":
    print("🌌 启动蒙特卡洛云端万界推演...")
    print("⏱️ 系统设定：最多运行 20 分钟，尽可能多地模拟平行宇宙！\n")
    
    start_time = time.time()
    TIME_LIMIT = 20 * 60 # 20分钟（1200秒）
    
    total_runs = 0
    total_crash_years = 0
    min_crash = 150
    max_crash = 0
    survived_150 = 0
    
    # 记录特定周期的分布
    tech_dist = {}

    while True:
        # 1. 检查是否超时
        if time.time() - start_time > TIME_LIMIT:
            print("\n⏳ [系统日志] 到达 20 分钟算力上限，强行终止推演，生成报告！")
            break
            
        total_runs += 1
        
        # 2. 随机生成初始条件
        tech_interval = random.randint(10, 20)
        start_capacity = random.uniform(90.0, 110.0)
        
        # 3. 跑一次模拟
        crash_year = simulate_universe(tech_interval, start_capacity)
        
        # 4. 累计数据
        total_crash_years += crash_year
        if crash_year < min_crash: min_crash = crash_year
        if crash_year > max_crash: max_crash = crash_year
        if crash_year >= 150: survived_150 += 1
        
        # 5. 每隔 100 万次宇宙生灭，打印一次进度
        if total_runs % 1000000 == 0:
            elapsed = int(time.time() - start_time)
            print(f"  [进度] 已推演 {total_runs:,} 个平行宇宙 | 耗时: {elapsed} 秒")

    # ==========================================
    # 最终输出大数据报告
    # ==========================================
    avg_crash = total_crash_years / total_runs
    death_rate = (total_runs - survived_150) / total_runs * 100

    print("\n" + "="*50)
    print(f"📊 [大数据推演报告] 终极物理审判")
    print(f"🌌 累计模拟宇宙总数: {total_runs:,} 个")
    print(f"💀 最终死寂均衡发生平均年数: {avg_crash:.2f} 年")
    print(f"⏳ 最长存活宇宙: {max_crash} 年")
    print(f"⚡ 最短命宇宙: {min_crash} 年")
    print(f"🕊️ 活到150年以上的宇宙数量: {survived_150:,} 个")
    print(f"📉 宇宙毁灭率: {death_rate:.4f}%")
    print("="*50)
    print("结论：无论初始条件如何随机，系统都无法逃脱物理承载力与资本复利的终极碰撞。")
