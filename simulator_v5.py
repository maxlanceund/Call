import time

class CalibratedUniverse:
    def __init__(self):
        # 初始常量设定
        self.capacity = 100.0  # 初始生态环境/社会总承载力
        self.capitalist_wealth = 10.0 # 初始顶层1%财富占用
        self.npc_wealth = 50.0 # 初始底层99%财富占用（用于观测被挤压程度）
        self.tick = 0
        self.is_dead = False
        
        # 真实数据校准参数
        self.capital_growth_rate = 0.08    # 顶层财富年增速 8%
        self.capacity_decay_rate = 0.008   # 承载力年衰减 0.8%
        self.tfp_growth = 0.02             # 全要素生产率基线 2%
        self.friction_base = 0.1           # 基础社会摩擦力

    def run_year(self):
        if self.is_dead: return
        self.tick += 1
        
        # 1. 生态环境承载力衰减（对应超载日提前）
        self.capacity = self.capacity * (1 - self.capacity_decay_rate)
        
        # 2. 顶层财富指数级扩张（对应复利与资产泡沫）
        self.capitalist_wealth = self.capitalist_wealth * (1 + self.capital_growth_rate)
        
        # 3. 底层财富与产出（受制于TFP和财富挤压）
        # 随着资本财富占比越来越大，底层获取的增量越来越少
        wealth_gap = self.capitalist_wealth / (self.capitalist_wealth + self.npc_wealth)
        self.npc_wealth = self.npc_wealth * (1 + self.tfp_growth * (1 - wealth_gap))
        
        # 4. 动态摩擦力（基尼系数扩大导致的社会内耗、维稳成本、信任缺失）
        # 当资本财富是底层财富的2倍以上时，摩擦力开始非线性飙升
        friction = self.friction_base + max(0, (wealth_gap - 0.1) * 2.5)
        
        # 5. 计算系统总负载（资本占用的资源 + 摩擦内耗）
        total_load = self.capitalist_wealth + (self.friction_base + friction) * 10
        
        # 输出数据（每年打印一次）
        print(f"年份 {self.tick:03d} | 环境承载: {self.capacity:.1f} | 资本占用: {self.capitalist_wealth:.1f} | 底层财富: {self.npc_wealth:.1f} | 摩擦力: {friction:.2f} | 负载: {total_load:.1f}")

        # 6. 相变判定：资本占用+内耗 > 环境承载力
        if total_load >= self.capacity:
            self.is_dead = True
            print("\n" + "="*60)
            print(f"💥 [系统崩溃] 在第 {self.tick} 年，触发【死寂均衡】强制格式化！")
            print(f"环境承载力已萎缩至: {self.capacity:.1f}")
            print(f"资本负载 + 社会摩擦力高达: {total_load:.1f}")
            print("资本无止境的复利，最终撑爆了萎缩的承载力。底层系统彻底断供。")
            print("="*60)

# ==========================================
# 启动真实数据推演
# ==========================================
print("🌌 启动 DE-Sim v5.0 (宏观经济学与生态学校准模型)...\n")
time.sleep(1)

universe = CalibratedUniverse()

# 模拟未来 60 年（数据图表化）
for i in range(60):
    if universe.is_dead: break
    universe.run_year()
    # 为了防止刷屏太快，停顿0.1秒
    time.sleep(0.1) 
