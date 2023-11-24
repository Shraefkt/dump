'''
    Calculate n_cover-cover of ranged query [a, b].

    Input:
        a, b: ints
    Output:
        list of ints for n_cover cover or smaller
'''
import math
from minimal_cover import calc_min_cover
from hello import visualize
def calc_n_cover(a :int, b: int, n: int,debug=False):
    # get minimal cover with unlimited nodes
    minimized_range = calc_min_cover(a,b)

    #base cases
    if len(minimized_range) <= n:
        return minimized_range
    # recursive case
    minimized_range = minimize_nodes(minimized_range,n)
    if debug:
        print(f"#1 Minimized range: {minimized_range}")
    return minimized_range

def calc_1_cover(a: int, b: int, n:int):
    if a > n or b > n or a > b or a < 0:
        return None
    depth = math.ceil(math.log(n,2))+1
    a = a + 2 ** (depth - 1) - 1
    b = b + 2 ** (depth - 1) - 1
    return [a >> (len("{:b}".format(a^b)) if a!=b else 0)]
def minimize_nodes(minimized_range: list, n: int):
    if len(minimized_range) <= n: # or n_cover
        return minimized_range
    left_merge_result = get_merge_result(minimized_range[0], minimized_range[1])
    right_merge_result = get_merge_result(minimized_range[-1], minimized_range[-2])
    if get_node_depth(right_merge_result) >= get_node_depth(left_merge_result):
        minimized_range.pop()
        minimized_range.pop()
        minimized_range.append(right_merge_result)
        if len(minimized_range) <= n:  # or n_cover
            return minimized_range
    elif get_node_depth(left_merge_result) >= get_node_depth(right_merge_result):
        minimized_range.pop(0)
        minimized_range.pop(0)
        minimized_range.insert(0, left_merge_result)
    return minimize_nodes(minimized_range,n)
def get_merge_result(a,b): # need not be the same layer
    bin_len_a, bin_len_b = len("{:b}".format(a)) , len("{:b}".format(b))
    if bin_len_b > bin_len_a:
        b = b >> (bin_len_b - bin_len_a)
    elif bin_len_a > bin_len_b:
        a = a >> (bin_len_a-bin_len_b)
    return a >> (len("{:b}".format(a^b)) if a!=b else 0)
def get_node_depth(i):
    return math.floor(math.log(i,2))+1
if __name__ == '__main__':
    a = 38#int(input("Input lower limit:"))
    b = 58#int(input("Input upper limit:"))
    n_cover = 2#int(input("N: "))
    n_nodes = 63
    assert 0 < a <= b and len(bin(a)) == len(bin(b)), 'a and b are not on the same layer of a binary tree!'
    cover_nodes = calc_min_cover(a, b)
    color_dict = {}
    depth = math.ceil(math.log(n_nodes, 2))
    x_node_min = depth - math.floor(math.log(cover_nodes[0], 2)) - 1  # depth to leaf layer/ height
    x_node_max = depth - math.floor(math.log(cover_nodes[-1], 2)) - 1
    min = cover_nodes[0] * (2 ** (x_node_min))
    max = (cover_nodes[-1] + 1) * (2 ** x_node_max) - 1
    for node in cover_nodes:
        color_dict[node] = "overcover_node"
    for node in range(min,max+1):
        if a <= node <= b:
            color_dict[node] = "covered_node"
        else:
            color_dict[node] = "overhead_node"
    visualize(n_nodes,color_dict)
