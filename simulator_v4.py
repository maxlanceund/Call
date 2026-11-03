import math
import time

class Region:
    def __init__(self, name, base_friction):
        self.name = name
        self.base_friction = base_friction # 基础地理摩擦力

class Entity:
    def __init__(self, name, energy, is_immortal=False):
        self.name = name
        self.energy = energy
        self.is_immortal = is_immortal
        self.status = "ALIVE"

class Universe:
    def __init__(self, initial_capacity):
        self.initial_capacity = initial_capacity
        self.current_capacity = initial_capacity
        self.total_entropy = 0.0 # 宏观熵（系统污染度）
        self.tick = 0
        self.is_dead = False

    def calculate_dynamic_friction(self, region):
        # 动态摩擦力：地理基础摩擦 + 系统熵增导致的物流成本（拥堵、内耗）
        entropy_penalty = (self.total_entropy / self.initial_capacity) * 0.5
        return min(0.9, region.base_friction + entropy_penalty) # 摩擦系数上限0.9

    def run_tick(self):
        if self.is_dead: return
        self.tick += 1
        
        # 1. 计算动态摩擦力
        current_friction = self.calculate_dynamic_friction(Hella)
        
        # 2. 底层NPC的产出与消耗
        total_npc_production = 0
        for e in npc_list:
            if e.status == "ALIVE":
                # NPC每次产生一点资源，但维持生存要消耗资源
                produced = 10.0 * (1 - (self.total_entropy / self.initial_capacity)) # 熵越高，土地越贫瘠
                e.energy += (produced - 8.0) 
                total_npc_production += produced
                if e.energy <= 0:
                    e.status = "DEAD"

        # 3. 资本的剥削与增长（Logistic Growth 非线性反馈）
        cap = capitalist_list[0]
        if cap.status == "ALIVE":
            # 资本家剥削NPC，但受制于动态摩擦力
            exploited_energy = total_npc_production * (1 - current_friction)
            cap.energy += exploited_energy
            
            #  capitalists的“内存占用”由他的能量转化而来，但受限于系统当前承载力
            # 引入非线性阻力：(1 - 当前占用 / 最大容量)
            cap_memory_usage = cap.energy * 0.5
            growth_potential = 1.0 - (cap_memory_usage / self.current_capacity)
            if growth_potential > 0:
                # 此时资本家才能顺利扩张
                self.total_entropy += cap_memory_usage * 0.1
            else:
                # 资源见顶，系统卡顿
                pass

        # 4. 宏观相变：环境承载力随系统熵增而自发衰减
        # 这是一个非线性衰减函数：当熵值接近初始容量时，承载力断崖式下跌
        decay_factor = 1.0 - math.exp((self.total_entropy - self.initial_capacity) / (self.initial_capacity * 0.2))
        self.current_capacity = self.initial_capacity * max(0.1, decay_factor)

        # 5. 判定是否死机（占据的内存 + 熵 >= 容量）
        total_load = cap.energy * 0.5 + self.total_entropy

        if self.tick % 5 == 0 or (self.current_capacity - total_load) < 500:
            print(f"Tick {self.tick:02d} | 负载: {int(total_load):4d} | 动态容量: {int(self.current_capacity):4d} | 系统熵: {int(self.total_entropy):4d} | 摩擦力: {current_friction:.2f}")

        if total_load >= self.current_capacity:
            self.is_dead = True
            print("\n" + "="*50)
            print(f"💥 [第 {self.tick} 周期] 触发真正的拓扑相变！")
            print(f"最终总负载: {int(total_load)} > 环境自衰减容量: {int(self.current_capacity)}")
            print("由于底层NPC被抽干，且环境承载力随熵增崩溃，系统直接死机。")
            print("那个赛博永生者，最终变成了系统里一团毫无意义的量子乱码（达利软钟）。")
            print("="*50)

# ==========================================
# 初始化 V4.0 沙盒
# ==========================================
print("🌌 启动 DE-Sim v4.0 (引入非线性反馈与动态摩擦力)...\n")
time.sleep(1)

Hella = Region("西南大山", base_friction=0.2) # 初始基础摩擦力
npc_list = [Entity(f"大山村民_{i}", 50) for i in range(1, 6)] # 增加NPC样本量
capitalist_list = [Entity("赛博永生富豪", 100)]

universe = Universe(initial_capacity=5000)

for i in range(100):
    if universe.is_dead: break
    universe.run_tick()
    time.sleep(0.2)
