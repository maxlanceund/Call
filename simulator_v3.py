import random
import time

class Region:
    def __init__(self, name, friction):
        self.name = name
        self.friction = friction # 地理摩擦力（运输损耗率）

class Entity:
    def __init__(self, name, energy, region, is_immortal=False):
        self.name = name
        self.energy = energy
        self.region = region
        self.is_immortal = is_immortal
        self.status = "ALIVE"

class Universe:
    def __init__(self, total_capacity):
        self.capacity = total_capacity
        self.used_energy = 0.0
        self.entropy = 0.0 # 污染/无效垃圾数据（熵增）
        self.tick = 0
        self.is_dead = False

    def run_tick(self):
        if self.is_dead: return
        self.tick += 1
        
        # 1. 黑天鹅事件：在第30个周期，环境突变（比如气候灾难/核战），容量暴降
        if self.tick == 30:
            print("\n⚠️ [突发新闻] 全球气候剧变！生态系统承载力暴跌 20%！")
            self.capacity = self.capacity * 0.8

        # 2. 底层 NPC 的工作（在西南大山里生产，摩擦力极大）
        npc_production = 0
        for e in npc_list:
            if e.status == "ALIVE":
                # 大山里产出低，且消耗部分能量维持生存
                e.energy += random.uniform(5, 10) - 3 
                npc_production += 5
                if e.energy < 0:
                    e.status = "DEAD"
                    print(f"  💀 [底层悲剧] {e.name} 因为能量耗尽，在{Hella.region.name}饿死了。")

        # 3. 资本的掠夺与传输（从大山把能量抽到平原，还要扣除摩擦力）
        for cap in capitalist_list:
            if cap.status == "ALIVE":
                # 剥削量
                exploit = npc_production * 0.8
                # 计算地理摩擦力损耗：能量从山区传到平原要损失
                loss = exploit * Hella.friction
                # 资本家拿走剩下的
                gained = exploit - loss
                cap.energy += gained
                # 产生熵（资本的无序扩张和垃圾数据）
                self.entropy += gained * 0.2
        
        # 4. 永生者的指数级吃内存（无限制扩张）
        for cap in capitalist_list:
            if cap.status == "ALIVE":
                # 随着周期增加，为了维持“永生”，消耗急剧上升
                cap_consumption = cap.energy * (0.05 * (1.1 ** self.tick)) 
                self.used_energy += cap_consumption
        
        # 5. 计算系统总负载
        total_load = self.used_energy + self.entropy + npc_production
        
        # 6. 信息差与延迟反馈（这就是现实中大家还在狂欢的原因）
        # 只有当负载达到容量的 90% 以上，系统才会报错；之前全是“岁月静好”
        if total_load < self.capacity * 0.9:
            if self.tick % 5 == 0:
                print(f"🌍 [第 {self.tick} 周期] 岁月静好。系统负载: {int(total_load)} / {int(self.capacity)}")
        elif total_load < self.capacity:
            print(f"🌤️ [第 {self.tick} 周期] 轻微卡顿。系统负载: {int(total_load)} / {int(self.capacity)} (注意：开始有点热了)")
        else:
            # 冲破容量红线！
            self.is_dead = True
            print("\n" + "="*50)
            print(f"💥 [第 {self.tick} 周期] 系统内存爆满！触发【死寂均衡】强制格式化！")
            print(f"当前总负载: {int(total_load)}KB > 宇宙容量: {int(self.capacity)}KB")
            print("所有进程断裂，那个不可一世的永生者，被压缩成了无法动弹的量子乱码（达利软钟）。")
            print("="*50)

# ==========================================
# 初始化宇宙 (DE-Sim v3.0)
# ==========================================
print("🌌 启动 DE-Sim v3.0 (引入地理摩擦与资本掠夺算法)...")
time.sleep(1)

# 定义地理区域
Hella = Region("西南大山(高摩擦)", friction=0.3) # 摩擦力极大，传输损耗高

# 创建底层 NPC（在大山里）
npc_list = [Entity(f"大山村民_{i}", 100, Hella) for i in range(1, 4)]

# 创建永生富豪（在平原，通过剥削大山里的NPC获取能量）
capitalist_list = [Entity("赛博永生富豪", 500, Region("沿海平原", friction=0.05))]

# 设定总容量
universe = Universe(total_capacity=8000)

# 开跑
for i in range(60):
    if universe.is_dead: break
    universe.run_tick()
    time.sleep(0.5) # 稍微停一下，方便看滚动的字
