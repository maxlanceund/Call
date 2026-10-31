import numpy as np
import matplotlib.pyplot as plt

def simulate_entropy_evolution(rounds=100, capacity=50.0, mass_rate=1.5, kappa=0.05):
    S_A = 0.1
    entropy_history = []
    for t in range(rounds):
        growth = mass_rate * 0.5 
        if S_A > capacity * 0.8:
            erase = kappa * (mass_rate / capacity) * S_A * (S_A / capacity)**3
        else:
            erase = 0
        S_A = S_A + growth - erase
        if S_A > capacity:
            S_A = capacity
        entropy_history.append(S_A)
    return entropy_history

time_steps = 100
capacities = [30.0, 50.0, 80.0]
plt.figure(figsize=(10, 6))

for cap in capacities:
    history = simulate_entropy_evolution(rounds=time_steps, capacity=cap)
    plt.plot(range(time_steps), history, label=f'Horizon Capacity S_BH = {cap}', linewidth=2)

plt.title('Simulation of Black Hole Information Erasure (Dead-Equilibrium Model)', fontsize=14)
plt.xlabel('Time (t)', fontsize=12)
plt.ylabel('Entanglement Entropy S_A(t)', fontsize=12)
plt.axhline(y=50, color='r', linestyle='--', alpha=0.5, label='Critical Capacity Limit')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)

plt.savefig('entropy_erasure_results.png', dpi=300)
print("✅ 实验完成！结果已保存为 entropy_erasure_results.png")
