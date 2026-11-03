import time

class RevolutionUniverse:
    def __init__(self):
        self.capacity = 100.0  
        self.capitalist_wealth = 10.0 
        self.npc_wealth = 50.0 
        self.tick = 0
        self.is_dead = False
        
        self.capital_growth_rate = 0.08    
        self.capacity_decay_rate = 0.008   
        self.tfp_growth = 0.02             
        self.friction_base = 0.1           
        self.tech_boost_count = 0
        self.revolution_count = 0

    def run_year(self):
        if self.is_dead: return
        self.tick += 1
        
        # ⚡ 科技革命（外挂）
        if self.tick == 15 or self.tick == 30 or self.tick == 45:
            self.tech_boost_count += 1
            print(f"⚡ [第 {self.tick} 年] 爆发第 {self.tech_boost_count} 次科技革命！")
            self.capacity *= 1.8
            self.friction_base *= 0.7
            self.capital_growth_rate += 0.02

        # 1. 常规衰减
        self.capacity = self.capacity * (1 - self.capacity_decay_rate)
        
        # 2. 资本扩张
        self.capitalist_wealth = self.capitalist_wealth * (1 + self.capital_growth_rate)
        
        # 3. 底层财富与产出
        wealth_gap = self.capitalist_wealth / (self.capitalist_wealth + self.npc_wealth)
        self.npc_wealth = self.npc_wealth * (1 + self.tfp_growth * (1 - wealth_gap))
        
        # 4. 动态摩擦力
        friction = self.friction_base + max(0, (wealth_gap - 0.1) * 2.5)
        
        # 🚨 核心变动：触发“社会革命/财富重分配”机制
        # 当资本家财富是底层财富的 1.2 倍以上，且摩擦力大于 0.9（底层活不下去）
        if self.capitalist_wealth > self.npc_wealth * 1.2 and friction > 0.9:
            self.revolution_count += 1
            print(f"\n🔥🔥 [第 {self.tick} 年] 爆发第 {self.revolution_count} 次社会革命！底层暴力格式化！")
            print(f"    革命前：资本财富 {self.capitalist_wealth:.1f} vs 底层财富 {self.npc_wealth:.1f}")
            
            # 打土豪分田地：资本家财富被强行没收 70%，分给底层
            seized_wealth = self.capitalist_wealth * 0.7
            self.capitalist_wealth -= seized_wealth
            self.npc_wealth += seized_wealth * 0.8 # 20%在革命内耗中蒸发
            
            # 革命后，系统压力释放，摩擦力大幅下降
            self.friction_base = 0.1
            print(f"    革命后：资本财富 {self.capitalist_wealth:.1f} vs 底层财富 {self.npc_wealth:.1f}")
            print("    阶级矛盾暂时缓解，系统摩擦力重置！\n")

        # 5. 计算系统负载
        total_load = self.capitalist_wealth + (self.friction_base + friction) * 10
        
        print(f"年份 {self.tick:03d} | 承载: {self.capacity:.1f} | 资本: {self.capitalist_wealth:.1f} | 底层: {self.npc_wealth:.1f} | 摩擦: {friction:.2f} | 负载: {total_load:.1f}")

        # 6. 死机判定（注意这里用的是重置前的摩擦力来算负载，因为革命当年救了一命）
        if total_load >= self.capacity:
            self.is_dead = True
            print("\n" + "="*60)
            print(f"💥 [系统崩溃] 在第 {self.tick} 年，系统彻底死机。")
            print(f"虽然经历了 {self.tech_boost_count} 次科技革命和 {self.revolution_count} 次社会革命，")
            print(f"但资本复利的癌细胞最终依然吞噬了所有能量。")
            print("="*60)

# ==========================================
# 启动推演
# ==========================================
print("🌌 启动 DE-Sim v7.0 (科技革命 + 社会革命 双重干预)...\n")
time.sleep(1)

universe = RevolutionUniverse()

for i in range(120):
    if universe.is_dead: break
    universe.run_year()
    time.sleep(0.05)
