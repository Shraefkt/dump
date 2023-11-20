import numpy as np
import matplotlib.pyplot as plt
from cover_calc import calc_n_cover
from utils import *
def get_average_overhead(n_nodes,n_cover):
    counter = 0
    overhead_total = 0
    actual_n_nodes = 2 ** get_depth(n_nodes) + n_nodes # index number
    for b in range(1,n_nodes+1):
        for a in range(1,b):
            overcover_nodes = calc_n_cover(convert_to_index_number(a,actual_n_nodes),convert_to_index_number(b,actual_n_nodes),n_cover,actual_n_nodes)
            over_number = get_number_overhead_nodes(convert_to_index_number(a,actual_n_nodes),
                                                        convert_to_index_number(b,actual_n_nodes),
                                                        actual_n_nodes,
                                                        overcover_nodes=overcover_nodes,
                                                        debug=False)
            overhead_total += over_number / (b-a)
            counter += 1
    return overhead_total/counter
def plot(n_cover,n_times):
    Number_of_nodes_array = []
    Ave_overhead_array = []
    for i in range(2, n_times):
        Number_of_nodes_array.append(i)
        Ave_overhead_array.append(get_average_overhead(i, n_cover) * 100)
    Number_of_nodes_array = np.array(Number_of_nodes_array)
    Ave_overhead_array = np.array(Ave_overhead_array)
    plt.plot(Number_of_nodes_array, Ave_overhead_array, label=f"{int(n_cover)}-cover")

plt.xlabel("Number of nodes")
plt.ylabel("Average overhead percentage")
times = 100
plot(1,times)
plot(2,times)
plot(3,times)
plot(4,times)
plot(5,times)

leg = plt.legend(loc='upper center')
plt.show()
