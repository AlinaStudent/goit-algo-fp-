
import uuid
import time
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, key, color="#6CA6CD"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val, node_ref=node)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

def hex_gradient(n, start="#12304A", end="#C6E3FF"):
    """
    Генерує n кольорів у 16-ковому форматі від темного до світлого.
    """
    def h2rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    def rgb2h(r,g,b):
        return f"#{r:02X}{g:02X}{b:02X}"
    rs, gs, bs = h2rgb(start)
    re, ge, be = h2rgb(end)
    if n <= 1:
        return [start]
    out = []
    for i in range(n):
        t = i / (n - 1)
        r = round(rs + (re - rs) * t)
        g = round(gs + (ge - gs) * t)
        b = round(bs + (be - bs) * t)
        out.append(rgb2h(r,g,b))
    return out

def collect_nodes(root):
    """Повертає список вузлів у довільному порядку для підрахунку N."""
    order = []
    q = deque([root])
    while q:
        cur = q.popleft()
        if cur is None:
            continue
        order.append(cur)
        q.append(cur.left)
        q.append(cur.right)
    return [n for n in order if n is not None]

def draw_tree(tree_root, node_colors=None, pause=None, title=None):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)
    labels = {node_id: data['label'] for node_id, data in tree.nodes(data=True)}
    if node_colors is None:
        colors = [data.get('color', '#6CA6CD') for _, data in tree.nodes(data=True)]
    else:
        colors = [node_colors.get(node_id, '#6CA6CD') for node_id, _ in tree.nodes(data=True)]
    plt.clf()
    plt.title(title or "")
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.axis('off')
    plt.pause(pause if pause is not None else 0.5)

def bfs_iterative(root, pause=0.6):
    """Обхід у ширину з чергою. Без рекурсії. Поступова зміна кольорів."""
    nodes = collect_nodes(root)
    palette = hex_gradient(len(nodes))
    idx = 0
    node_color = {}
    q = deque([root])
    visited = set()
    plt.figure(figsize=(8,5))
    while q:
        cur = q.popleft()
        if cur is None or cur.id in visited:
            continue
        visited.add(cur.id)
        node_color[cur.id] = palette[idx]
        idx += 1
        draw_tree(root, node_colors=node_color, pause=pause, title="BFS (черга)")
        if cur.left: q.append(cur.left)
        if cur.right: q.append(cur.right)
    plt.show()

def dfs_iterative(root, pause=0.6):
    """Обхід у глибину зі стеком (preorder: node, left, right). Без рекурсії."""
    nodes = collect_nodes(root)
    palette = hex_gradient(len(nodes))
    idx = 0
    node_color = {}
    stack = [root]
    visited = set()
    plt.figure(figsize=(8,5))
    while stack:
        cur = stack.pop()
        if cur is None or cur.id in visited:
            continue
        visited.add(cur.id)
        node_color[cur.id] = palette[idx]
        idx += 1
        draw_tree(root, node_colors=node_color, pause=pause, title="DFS (стек)")
        # Важливо: спочатку правий, потім лівий — щоб лівий обробився першим
        if cur.right: stack.append(cur.right)
        if cur.left: stack.append(cur.left)
    plt.show()

def build_sample_tree():
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)
    return root

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Візуалізація обходів бінарного дерева (BFS/DFS)")
    parser.add_argument("--mode", choices=["bfs","dfs"], default="bfs", help="Тип обходу")
    parser.add_argument("--pause", type=float, default=0.6, help="Пауза між кроками (сек)")
    args = parser.parse_args()

    root = build_sample_tree()
    if args.mode == "bfs":
        bfs_iterative(root, pause=args.pause)
    else:
        dfs_iterative(root, pause=args.pause)
