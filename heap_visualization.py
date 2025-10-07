
import uuid
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, key, color="#87CEEB"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())

def array_to_heap_tree(arr):
    """Створює бінарне дерево з масиву-купі: i -> (2i+1, 2i+2). Повертає корінь і список вузлів."""
    if not arr:
        return None, []
    nodes = [Node(v) for v in arr]
    for i in range(len(arr)):
        li, ri = 2*i + 1, 2*i + 2
        if li < len(arr):
            nodes[i].left = nodes[li]
        if ri < len(arr):
            nodes[i].right = nodes[ri]
    return nodes[0], nodes

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
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

def draw_heap_from_array(arr, title="Бінарна купа (піраміда)"):
    """
    Візуалізація бінарної купи, заданої масивом.
    Масив може бути мін-/макс-купою; функція просто відображає структуру.
    """
    root, nodes = array_to_heap_tree(arr)
    if root is None:
        raise ValueError("Порожній масив.")
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(tree, root, pos)
    colors = [data.get('color', '#87CEEB') for _, data in tree.nodes(data=True)]
    labels = {nid: data['label'] for nid, data in tree.nodes(data=True)}
    plt.figure(figsize=(8,5))
    plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Приклад: мін-купа
    heap_array = [1, 3, 5, 7, 9, 11, 13, 15]
    draw_heap_from_array(heap_array, title="Бінарна купа з масиву: " + str(heap_array))
