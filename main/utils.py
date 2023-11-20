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
    x_overcover_node_min = get_height(overcover_nodes[0],n)
    x_overcover_node_max = get_height(overcover_nodes[-1],n)
    min_descendant = overcover_nodes[0] * (2 ** (x_overcover_node_min))
    max_descendant = (overcover_nodes[-1] + 1) * (2 ** x_overcover_node_max) - 1
    if max_descendant > n:
        max_descendant = n
    overhead_number = max_descendant - b + a - min_descendant
    if debug:
        print(f"Actual a:{a}, Actual b:{b}")
        print(f"Overcover Nodes: {overcover_nodes}")
        print(f"depth: {depth}, x_min: {x_overcover_node_min}, x_max :{x_overcover_node_max}")
        print(f"Min descendant:{min_descendant}, max descendant: {max_descendant}")
        print(f"Overhead: {overhead_number}")
    return overhead_number
