import random
import matplotlib.pyplot as plt

class MicroUniverse:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.used_memory = 0.0
        self.tick = 0
        self.entities = []
        self.is_dead = False
        self.history_used = []
        self.history_limit = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def run_tick(self):
        if self.is_dead:
            self.history_used.append(self.total_memory)
            self.history_limit.append(self.total_memory)
            return
            
        self.tick += 1
        current_tick_usage = 0.0
        base_entropy = random.uniform(1.0, 5.0) 

        for entity in self.entities:
            if entity.status == "ACTIVE":
                consumption = entity.consume(self.tick)
                current_tick_usage += consumption
                
                if not entity.is_immortal and self.tick > 50 and random.random() > 0.95:
                    entity.status = "TERMINATED"

        self.used_memory += current_tick_usage + base_entropy
        self.history_used.append(self.used_memory)
        self.history_limit.append(self.total_memory)

        if self.used_memory >= self.total_memory:
            self.trigger_dead_equilibrium()

    def trigger_dead_equilibrium(self):
        self.is_dead = True
        print("\n🚨 [死寂均衡触发] 在第 " + str(self.tick) + " 个周期，系统内存溢出！")
        print("系统强制格式化，所有进程坍缩。\n")
        self.used_memory = 0 
        for e in self.entities:
            if e.is_immortal:
                e.status = "DALI_CLOCK"

class Entity:
    def __init__(self, name, base_consumption, is_immortal=False, exponential_growth=False):
        self.name = name
        self.base_consumption = base_consumption
        self.is_immortal = is_immortal
        self.exponential_growth = exponential_growth
        self.status = "ACTIVE"

    def consume(self, tick):
        if self.status != "ACTIVE":
            return 0
        if self.exponential_growth:
            return self.base_consumption * (1.05 ** tick)
        else:
            if tick > 80: return 0
            return self.base_consumption

universe = MicroUniverse(total_memory=3000)
universe.add_entity(Entity("底层NPC", base_consumption=2, is_immortal=False, exponential_growth=False))
universe.add_entity(Entity("普通打工人", base_consumption=3, is_immortal=False, exponential_growth=False))
universe.add_entity(Entity("赛博永生富豪", base_consumption=10, is_immortal=True, exponential_growth=True))

print("🌌 启动 DE-Sim v2.0 (多智能体演化)...")
for i in range(150):
    if universe.is_dead:
        break
    universe.run_tick()

plt.figure(figsize=(10, 6))
plt.plot(universe.history_used, label='System Entropy (S_A)', color='red')
plt.axhline(y=universe.total_memory, color='blue', linestyle='--', label='Critical Capacity Limit')
plt.title('Dead-Equilibrium Simulation (Multi-Agent)')
plt.xlabel('Time (Ticks)')
plt.ylabel('Memory Usage (KB)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('dead_equilibrium_curve.png')
print("📊 曲线图已生成：dead_equilibrium_curve.png")
