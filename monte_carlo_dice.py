
import random
import math
import argparse
import matplotlib.pyplot as plt

def simulate_two_dice(n_rolls: int):
    counts = {s: 0 for s in range(2, 13)}
    for _ in range(n_rolls):
        s = random.randint(1,6) + random.randint(1,6)
        counts[s] += 1
    probs = {s: counts[s]/n_rolls for s in counts}
    return counts, probs

def analytical_probs():
    ways = {2:1,3:2,4:3,5:4,6:5,7:6,8:5,9:4,10:3,11:2,12:1}
    total = 36
    return {s: ways[s]/total for s in ways}

def plot_probs(sim_probs, ana_probs):
    sums = list(range(2,13))
    sim = [sim_probs[s] for s in sums]
    ana = [ana_probs[s] for s in sums]
    plt.figure(figsize=(8,5))
    width = 0.35
    x = range(len(sums))
    # Без вказання кольорів, згідно з вимогами (використовується стиль matplotlib за замовчуванням)
    plt.bar([i - width/2 for i in x], sim, width=width, label="Монте-Карло")
    plt.bar([i + width/2 for i in x], ana, width=width, label="Аналітично")
    plt.xticks(list(x), sums)
    plt.ylabel("Ймовірність")
    plt.xlabel("Сума на двох кубиках")
    plt.title("Розподіл сум: Монте-Карло vs Аналітичний")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Монте-Карло для двох кубиків")
    parser.add_argument("-n", "--n_rolls", type=int, default=100000, help="К-ть кидків")
    args = parser.parse_args()
    counts, sim_probs = simulate_two_dice(args.n_rolls)
    ana = analytical_probs()
    print("Кидків:", args.n_rolls)
    for s in range(2,13):
        print(f"Сума {s:>2}: сим = {sim_probs[s]*100:5.2f}%, теор = {ana[s]*100:5.2f}%")
    plot_probs(sim_probs, ana)
