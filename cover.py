def calculate_nodes(a,b):
    results = []
    node = (a,a)
    while node[1] <= b:
        parent_node = get_parent_node(node,b)
        results.append(parent_node)
        node = (parent_node[1]+1,parent_node[1]+1)
    print(results)

def get_next_node(current_node):
    layer = current_node[1]-current_node[0] + 1
    return (current_node[1]+1, current_node[1] + layer)


def get_parent_node(current_node,b): #current_node [x,y]
    next_node = get_next_node(current_node)
    if next_node[1] > b : return current_node
    if current_node[1]/(current_node[1]-current_node[0]+1) %2 == 1: # is first_node in its set
        return get_parent_node((current_node[0],next_node[1]),b)
    return current_node

calculate_nodes(3,2043)