import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math


def add_nodes(n, G):
    pos = {}
    G.add_nodes_from([i + 1 for i in range(n)])
    for i in range(1, n + 1):
        depth = math.floor(math.log(i, 2))
        x = i - (2 ** (depth) + 2 ** (depth - 1))
        # depth * 2 + (i - 2 ** (depth + 1) + 1)
        # if i == 1: x = 0
        pos[i] = np.array([x, n - depth])
        if (i * 2) <= n:
            G.add_edge(i, i * 2)
        if i * 2 + 1 <= n:
            G.add_edge(i, i * 2 + 1)
    return pos
def visualize(n,color_dict :dict):
    """
    n: total number of nodes
    color_dict = { n : "overhead_node" } only for n where color is needed
    """
    G = nx.Graph()
    pos = add_nodes(n, G)
    color_map = []
    for node in G:
        if node in color_dict.keys():
            if color_dict[node] == "overhead_node":
                color_map.append("red")
            elif color_dict[node] == "overcover_node":
                color_map.append("green")
            elif color_dict[node] == "covered_node":
                color_map.append("blue")
        else:
            color_map.append('white')
    nx.draw_networkx(G, pos,node_color=color_map, with_labels=True, font_weight='bold')
    plt.show()
