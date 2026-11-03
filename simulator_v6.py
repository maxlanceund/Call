import time

class TechUniverse:
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

    def run_year(self):
        if self.is_dead: return
        self.tick += 1
        
        # 🌟 引入科技革命（负熵注入）
        # 假设在第 15 年、30 年、45 年，系统爆发技术奇点
        if self.tick == 15 or self.tick == 30 or self.tick == 45:
            self.tech_boost_count += 1
            print(f"\n⚡ [第 {self.tick} 年] 爆发第 {self.tech_boost_count} 次科技革命！(如：AI、可控核聚变)")
            self.capacity *= 1.8  # 承载力瞬间拉高 80%
            self.friction_base *= 0.7 # 科技提高了效率，基础摩擦力降低
            self.capital_growth_rate += 0.02 # 但科技让资本的扩张速度更快了
            print("承载力（蓝线）大幅抬高，系统获得喘息空间！\n")

        # 1. 常规衰减
        self.capacity = self.capacity * (1 - self.capacity_decay_rate)
        
        # 2. 资本扩张（注意：科技革命后资本扩张更快了）
        self.capitalist_wealth = self.capitalist_wealth * (1 + self.capital_growth_rate)
        
        # 3. 底层财富（科技带来的红利，被资本大量抽走，底层只能喝汤）
        wealth_gap = self.capitalist_wealth / (self.capitalist_wealth + self.npc_wealth)
        self.npc_wealth = self.npc_wealth * (1 + self.tfp_growth * (1 - wealth_gap))
        
        # 4. 动态摩擦力（基尼系数导致的内耗）
        friction = self.friction_base + max(0, (wealth_gap - 0.1) * 2.5)
        
        # 5. 计算系统负载
        total_load = self.capitalist_wealth + (self.friction_base + friction) * 10
        
        print(f"年份 {self.tick:03d} | 环境承载: {self.capacity:.1f} | 资本占用: {self.capitalist_wealth:.1f} | 底层财富: {self.npc_wealth:.1f} | 摩擦力: {friction:.2f} | 负载: {total_load:.1f}")

        # 6. 相变判定
        if total_load >= self.capacity:
            self.is_dead = True
            print("\n" + "="*60)
            print(f"💥 [系统崩溃] 在第 {self.tick} 年，触发【死寂均衡】强制格式化！")
            print(f"虽然经历了 {self.tech_boost_count} 次科技革命，但资本的复利膨胀最终吞噬了所有红利。")
            print(f"环境承载力: {self.capacity:.1f} | 最终资本占用+内耗: {total_load:.1f}")
            print("="*60)

# ==========================================
# 启动推演
# ==========================================
print("🌌 启动 DE-Sim v6.0 (引入科技革命与耗散结构)...\n")
time.sleep(1)

universe = TechUniverse()

for i in range(80):
    if universe.is_dead: break
    universe.run_year()
    time.sleep(0.05)
