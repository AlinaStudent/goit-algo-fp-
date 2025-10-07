
from dataclasses import dataclass
from typing import Dict, List, Tuple

Item = Tuple[int, int]  # (cost, calories)

def greedy_algorithm(items: Dict[str, Dict[str,int]], budget: int) -> Tuple[List[str], int, int]:
    """
    Жадібний підхід: сортуємо за співвідношенням calories/cost і додаємо поки вміщується.
    Повертає (список назв, загальна_вартість, загальна_калорійність).
    """
    ratios = sorted(items.items(), key=lambda kv: kv[1]["calories"]/kv[1]["cost"], reverse=True)
    chosen, total_cost, total_cal = [], 0, 0
    for name, data in ratios:
        c, cal = data["cost"], data["calories"]
        if total_cost + c <= budget:
            chosen.append(name)
            total_cost += c
            total_cal += cal
    return chosen, total_cost, total_cal

def dynamic_programming(items: Dict[str, Dict[str,int]], budget: int):
    """
    0/1-рюкзак: кожну страву можна взяти або ні. Вартість — "вага", калорії — "цінність".
    DP по цілих бюджетах від 0..budget. Також відновлюємо оптимальний набір.
    """
    names = list(items.keys())
    costs = [items[n]["cost"] for n in names]
    cals  = [items[n]["calories"] for n in names]
    n = len(names)
    # dp[b] — максимальна калорійність при бюджеті b, використовуючи перші i предметів (ітеративно оновлюємо)
    dp = [0]*(budget+1)
    # для відновлення: зберігаємо рішення (який предмет брали при переході)
    take = [[False]*(budget+1) for _ in range(n)]
    for i in range(n):
        cost, cal = costs[i], cals[i]
        # ідемо у ЗВОРОТНЬОМУ напрямку по бюджету, щоб 0/1, а не unbounded
        for b in range(budget, cost-1, -1):
            if dp[b-cost] + cal > dp[b]:
                dp[b] = dp[b-cost] + cal
                take[i][b] = True
    # Відновлення набору
    res, b, total_cost = [], budget, 0
    for i in range(n-1, -1, -1):
        if take[i][b]:
            res.append(names[i])
            total_cost += costs[i]
            b -= costs[i]
    res.reverse()
    return res, total_cost, dp[budget]

if __name__ == "__main__":
    items = {
      "pizza": {"cost": 50, "calories": 300},
      "hamburger": {"cost": 40, "calories": 250},
      "hot-dog": {"cost": 30, "calories": 200},
      "pepsi": {"cost": 10, "calories": 100},
      "cola": {"cost": 15, "calories": 220},
      "potato": {"cost": 25, "calories": 350}
    }
    budget = 100
    g_pick, g_cost, g_cal = greedy_algorithm(items, budget)
    d_pick, d_cost, d_cal = dynamic_programming(items, budget)
    print("Бюджет:", budget)
    print("Жадібний:", g_pick, "вартість =", g_cost, "калорії =", g_cal)
    print("Динамічне:", d_pick, "вартість =", d_cost, "калорії =", d_cal)
