'''
    Calculate n-cover of ranged query [a, b].

    Input:
        a, b: ints
    Output:
        list of ints for n cover or smaller
'''
import math
from minimal_cover import calc_min_cover
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
    if len(minimized_range) <= n: # or n
        return minimized_range
    left_merge_result = get_merge_result(minimized_range[0], minimized_range[1])
    right_merge_result = get_merge_result(minimized_range[-1], minimized_range[-2])
    if get_node_depth(right_merge_result) >= get_node_depth(left_merge_result):
        minimized_range.pop()
        minimized_range.pop()
        minimized_range.append(right_merge_result)
        if len(minimized_range) <= n:  # or n
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
    return math.ceil(math.log(i,2))+1
if __name__ == '__main__':
    a = int(input("Input lower limit:"))
    b = int(input("Input upper limit:"))
    n = int(input("N: "))
    assert 0 < a <= b and len(bin(a)) == len(bin(b)), 'a and b are not on the same layer of a binary tree!'
    print(calc_n_cover(a,b,n))
