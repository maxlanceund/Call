import time
import random

class MicroUniverse:
    def __init__(self, total_memory):
        self.total_memory = total_memory  # 系统的容量上限（贝肯斯坦-霍金熵极限）
        self.used_memory = 0              # 已占用的内存（熵增）
        self.tick = 0                     # 宇宙时钟周期
        self.entities = []                # 宇宙中的进程（生命体）
        self.is_dead = False              # 死寂均衡触发标志

    def add_entity(self, entity):
        self.entities.append(entity)
        print(f" [系统日志] 成功载入进程: {entity.name} (初始内存: {entity.memory_footprint}KB)")

    def run_tick(self):
        if self.is_dead:
            return
            
        self.tick += 1
        print(f"\n--- ⏱️ 宇宙时钟周期 (Tick) {self.tick} ---")
        
        # 计算所有实体新产生的一轮内存消耗
        for entity in self.entities:
            if entity.status == "ACTIVE":
                self.used_memory += entity.generate_garbage()
                entity.check_status(self.tick)
                
                # 达利软钟效应：追求永生的实体，内存占用会呈指数级暴涨
                if entity.is_immortal:
                    entity.memory_footprint *= 1.5 

        print(f" [系统状态] 内存占用: {int(self.used_memory)}KB / {self.total_memory}KB")

        # 触发死寂均衡（OOM Killer）
        if self.used_memory >= self.total_memory:
            self.trigger_dead_equilibrium()

    def trigger_dead_equilibrium(self):
        self.is_dead = True
        print("\n" + "="*50)
        print(" 🚨 [系统警告] 内存溢出！逼近容量上限！")
        print(" 🚨 [死寂均衡触发] 拓扑相变启动，强制退相干与格式化...")
        print("="*50)
        
        for entity in self.entities:
            if entity.is_immortal:
                print(f" ❌ 永生者 {entity.name} 被强制压缩为量子乱码。变成了永远无法动弹的达利软钟。")
            else:
                print(f" ☠️ 普通进程 {entity.name} 被系统回收，释放内存。")
        
        print("\n [系统日志] 宇宙已死寂，等待下一次奇点大爆炸。")
        print("="*50)

class Entity:
    def __init__(self, name, memory_footprint, is_immortal=False):
        self.name = name
        self.memory_footprint = memory_footprint
        self.is_immortal = is_immortal  # 是否开启了赛博永生（拒绝死机）
        self.status = "ACTIVE"

    def generate_garbage(self):
        # 每次运行产生的垃圾数据，模拟熵增
        return random.randint(5, 15) + (self.memory_footprint * 0.1)

    def check_status(self, tick):
        # 模拟衰老与普通人的死亡（释放内存）
        if not self.is_immortal and tick > 2 and random.random() > 0.7:
            self.status = "TERMINATED"
            print(f" [进程终止] {self.name} 自然老化（关机），释放了部分内存。")

# ==========================================
# 启动实验
# ==========================================
print(" 🌌 初始化微观宇宙，设定最大容量: 400KB (极小容量测试)")
universe = MicroUniverse(total_memory=400)

# 1. 放进普通人（会自然死亡）
normal_person = Entity(name="普通NPC_张三", memory_footprint=20, is_immortal=False)

# 2. 放进富豪（强行注入赛博永生，拒绝关机，疯狂爆内存）
rich_man = Entity(name="赛博富豪_马斯克", memory_footprint=50, is_immortal=True)

universe.add_entity(normal_person)
universe.add_entity(rich_man)

# 启动宇宙循环
for i in range(15):
    if universe.is_dead:
        break
    time.sleep(1) # 停顿1秒，方便观察
    universe.run_tick()
