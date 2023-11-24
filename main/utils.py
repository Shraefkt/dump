import math
from itertools import product

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

def return_volume_from_height_profile(height_profile):
    v = 0
    for h in height_profile:
        v += 2 ** h
    return v

def get_height_profile(s,depth,n_cover,debug=True):
    min_overcover_node = 1
    total_nodes = max_overcover_node = 2 ** depth - 1
    min_start_range_node = 2 ** (depth - 1)
    max_start_range_node = 2 ** (depth) - s # the starting node for iteration !!!
    range_dictionary = {} # {(a,b):[over_nodes_list]}
    height_dictionary = {} # {(a,b):[heights_list]}
    for x in range(min_start_range_node, max_start_range_node + 1):
        range_dictionary[(x,x+s-1)] = []
        height_dictionary[(x,x+s-1)] = []
    #gen
    numbers = list(range(min_overcover_node, max_overcover_node + 1))
    for overcover_nodes in product(numbers, repeat=n_cover):
        #check validity
        overcover_nodes = sorted(overcover_nodes)
        #1. overlap
        if len(set(overcover_nodes)) != n_cover:
            continue
        #2. continuity/overlap
        descendant_ranges = [(get_min_descendant(x,total_nodes),get_max_descendant(x,total_nodes)) for x in overcover_nodes]
        descendant_ranges = sorted(descendant_ranges,key=take_first)
        if return_continuity(descendant_ranges,n_cover) == False:
            continue
        #3. check covers volume; needed so less calculations
        if descendant_ranges[n_cover-1][1] - descendant_ranges[0][0] + 1 < s:
            continue
        #4. put in range/height dictionaries if it can cover range
        for z in range(min_start_range_node, max_start_range_node + 1):
            if descendant_ranges[n_cover-1][1] >= (z + s - 1) and descendant_ranges[0][0] <= z:
                if overcover_nodes not in range_dictionary[(z, z + s - 1)]:
                    range_dictionary[(z, z + s - 1)].append(overcover_nodes)
                heights = tuple(sorted([get_height(n,total_nodes) for n in overcover_nodes]))
                if heights not in height_dictionary[(z, z + s - 1)]:
                    height_dictionary[(z, z + s - 1)].append(heights)
        if debug:
            print(f"[over_covernodes]:{overcover_nodes}")
            print(f"Descendant ranges: {descendant_ranges}")
    # check if profile is universal profile by seeing if it covers all ranges
    validation_profile_dict = {}
    for z in range(min_start_range_node, max_start_range_node + 1):
        for prof in height_dictionary[(z, z + s - 1)]:
            if prof in validation_profile_dict.keys():
                validation_profile_dict[prof] += 1
            else:
                validation_profile_dict[prof] = 1
    range_dictionary.clear()
    height_dictionary.clear()
    universal_profiles = []
    for prof in validation_profile_dict.keys():
        if validation_profile_dict[prof] == (max_start_range_node - min_start_range_node + 1):
            universal_profiles.append(prof)
    #find best universal profile, by total height then volume
    validation_profile_dict.clear()
    actual_best_profile = universal_profiles[0]
    best_volume = return_volume_from_height_profile(universal_profiles[0])
    for prof in universal_profiles:
            volume = return_volume_from_height_profile(prof)
            if volume < best_volume:
                actual_best_profile = prof
    universal_profiles.clear()
    return actual_best_profile


def take_first(elem):
    return elem[0]


def return_continuity(descendant_ranges,n_cover):
    for i in range(n_cover- 1):
        if descendant_ranges[i][1] != descendant_ranges[i + 1][0] - 1:
            return False
    return True
