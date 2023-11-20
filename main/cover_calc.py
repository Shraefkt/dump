from visualizer import visualize
from utils import *


def calc_min_cover(a, b) -> list:
    # base cases
    if a == b:
        return [a]
    if b - a == 1 and a % 2 == 1:
        return [a, b]

    # recursive case
    min_cover = []
    if a % 2 == 1:
        min_cover.append(a)
    min_cover += calc_min_cover((a+1) // 2, (b-1) // 2) # recursive call for solving smaller problem
    if b % 2 == 0:
        min_cover.append(b)
    return min_cover

def calc_n_cover(a :int, b: int, n_cover: int, n_nodes: int, debug=False) -> list:
    # get minimal cover with unlimited nodes
    check_same_layer(a,b)
    minimized_overcover_nodes = calc_min_cover(a, b)

    #base case
    if len(minimized_overcover_nodes) <= n_cover:
        return minimized_overcover_nodes
    # recursive case
    minimized_overcover_nodes = minimize_overcover_nodes(minimized_overcover_nodes, n_cover, n_nodes, a, b)
    if debug:
        print(f"#1 Minimized range: {minimized_overcover_nodes}")
    return minimized_overcover_nodes

def minimize_overcover_nodes(minimized_overcover_nodes: list, n_cover: int, n_nodes : int,a,b):
    if len(minimized_overcover_nodes) <= n_cover:
        return minimized_overcover_nodes
    left_merge_result = get_merge_result(minimized_overcover_nodes[0], minimized_overcover_nodes[1])
    right_merge_result = get_merge_result(minimized_overcover_nodes[-1], minimized_overcover_nodes[-2])
    winning_side = 0 # 0-> left, 1-> right

    left_win_result = minimized_overcover_nodes.copy()
    left_win_result.pop(0)
    left_win_result.pop(0)
    left_win_result.insert(0, left_merge_result)

    right_win_result = minimized_overcover_nodes.copy()
    right_win_result.pop()
    right_win_result.pop()
    right_win_result.append(right_merge_result)

    if get_depth(left_merge_result) > get_depth(right_merge_result):
        winning_side = 0
    elif get_depth(right_merge_result) > get_depth(left_merge_result):
        winning_side = 1
    else:
        if get_number_overhead_nodes(a,b,n_nodes,overcover_nodes=left_win_result) >= get_number_overhead_nodes(a,b,n_nodes,overcover_nodes=right_win_result):
            winning_side = 0
        else:
            winning_side = 1

    if winning_side == 0:
        minimized_overcover_nodes = left_win_result.copy()
    elif winning_side == 1:
        minimized_overcover_nodes = right_win_result.copy()
    return minimize_overcover_nodes(minimized_overcover_nodes, n_cover, n_nodes,a,b)

if __name__ == '__main__':
    n_nodes = int(input("Number of documents:"))
    n_nodes = 2 ** get_depth(n_nodes) + n_nodes
    a = convert_to_index_number(int(input("Input lower limit:")),n_nodes)
    b = convert_to_index_number(int(input("Input upper limit:")),n_nodes)
    n_cover = int(input("N-cover: "))
    overcover_nodes = calc_n_cover(a,b,n_cover,n_nodes)
    color_dict = {}
    depth = math.ceil(math.log(n_nodes, 2))
    x_node_min = depth - math.floor(math.log(overcover_nodes[0], 2)) - 1  # depth to leaf layer/ height
    x_node_max = depth - math.floor(math.log(overcover_nodes[-1], 2)) - 1
    min = overcover_nodes[0] * (2 ** (x_node_min))
    max = (overcover_nodes[-1] + 1) * (2 ** x_node_max) - 1
    for node in range(min,max+1):
        if a <= node <= b:
            color_dict[node] = "covered_node"
        else:
            color_dict[node] = "overhead_node"
    for node in overcover_nodes:
        color_dict[node] = "overcover_node"
    visualize(n_nodes,color_dict)
