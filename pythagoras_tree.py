
"""
Завдання 2. Рекурсія. Фрактал "дерево Піфагора".
Використано matplotlib для візуалізації (без seaborn).
Користувач задає рівень рекурсії (depth).
"""

import math
import argparse
import matplotlib.pyplot as plt

def draw_tree(ax, x, y, length, angle_deg, depth):
    """
    Рекурсивно малює "дерево Піфагора" в стилі прямокутних гілок.
    Це легка для реалізації варіація фрактала: кожна гілка розгалужується на 2
    під кутом ±45°, а довжина зменшується у sqrt(2) раз.
    """
    if depth == 0 or length < 1e-3:
        return

    # Кінцева точка поточної гілки
    rad = math.radians(angle_deg)
    x2 = x + length * math.cos(rad)
    y2 = y + length * math.sin(rad)

    # Малюємо поточну "гілку" (відрізок)
    ax.plot([x, x2], [y, y2], linewidth=max(1.0, depth * 0.7))

    # Рекурсивні гілки
    new_len = length / math.sqrt(2.0)
    draw_tree(ax, x2, y2, new_len, angle_deg + 45.0, depth - 1)
    draw_tree(ax, x2, y2, new_len, angle_deg - 45.0, depth - 1)

def main():
    parser = argparse.ArgumentParser(description="Піфагорове дерево (рекурсія)")
    parser.add_argument("-d", "--depth", type=int, default=10, help="Рівень рекурсії (наприклад, 10)")
    parser.add_argument("-l", "--length", type=float, default=200.0, help="Початкова довжина стовбура")
    args = parser.parse_args()

    fig, ax = plt.subplots(figsize=(8, 8))
    draw_tree(ax, x=0.0, y=0.0, length=args.length, angle_deg=90.0, depth=args.depth)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-args.length, args.length)
    ax.set_ylim(0, args.length * 2)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
