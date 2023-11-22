import math

def get_depth(i):
    return math.floor(math.log(i, 2)) + 1

def get_height(i,n):
    return get_depth(n) - math.floor(math.log(i, 2)) - 1

def convert_to_index_number(i,n):
    #converts document number to index number
    return 2 ** (get_depth(n) - 1) + i - 1

def check_same_layer(a,b):
    assert 0 < a <= b and len(bin(a)) == len(bin(b)), 'a and b are not on the same layer of a binary tree!'
def get_merge_result(a,b):
    # need not be the same layer
    # returns 1_cover too
    bin_len_a, bin_len_b = len("{:b}".format(a)) , len("{:b}".format(b))
    if bin_len_b > bin_len_a:
        b = b >> (bin_len_b - bin_len_a)
    elif bin_len_a > bin_len_b:
        a = a >> (bin_len_a-bin_len_b)
    return a >> (len("{:b}".format(a^b)) if a!=b else 0)

def get_number_overhead_nodes(a,b,n,overcover_nodes: list,debug=False) -> int:
    if a == b:
        return 0
    check_same_layer(a,b)
    depth = get_depth(n)
    overall_min_descendant = get_min_descendant(overcover_nodes[0], n)
    overall_max_descendant = get_max_descendant(overcover_nodes[-1], n)
    for node in overcover_nodes:
        min_descendant = get_min_descendant(node,n)
        max_descendant = get_max_descendant(node,n)
        if min_descendant < overall_min_descendant:
            overall_min_descendant = min_descendant
        if max_descendant > overall_max_descendant:
            overall_max_descendant = max_descendant
    if overall_max_descendant > n:
        overall_max_descendant = n
    overhead_number = overall_max_descendant - b + a - overall_min_descendant
    if debug:
        print(f"Actual a:{a}, Actual b:{b}")
        print(f"Overcover Nodes: {overcover_nodes}")
        print(f"Min descendant:{overall_min_descendant}, max descendant: {overall_max_descendant}")
        print(f"Overhead: {overhead_number}")
    return overhead_number

def get_min_descendant(i,total_nodes):
    x_overcover_node_min = get_height(i, total_nodes)
    min_descendant = i * (2 ** (x_overcover_node_min))
    return min_descendant

def get_max_descendant(i,total_nodes):
    x_overcover_node_max = get_height(i, total_nodes)
    max_descendant = (i + 1) * (2 ** x_overcover_node_max) - 1
    return max_descendant
