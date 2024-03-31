import time

def create_data_model():
    """Stores the data for the problem."""
    data = {}

    data['distance_matrix'] = [
        [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875],
        [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589],
        [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262],
        [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466],
        [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796],
        [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547],
        [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724],
        [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038],
        [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744],
        [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0]
    ]  
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def get_unique_paths(node_set,start_node,previous_node,current_node,path,paths,cost,costs):
    path.append(current_node)
    
    if previous_node != current_node: # False only for first iteration
        cost += data['distance_matrix'][previous_node][current_node]
        previous_node = current_node
    
    node_set.remove(current_node)

    if not node_set: # base case
        path.append(start_node)
        cost += data['distance_matrix'][previous_node][start_node]
        paths.append(path)
        costs.append(cost)
        return

    for node in node_set:
        temp_node_set = node_set[:]
        temp_path = path[:]
        get_unique_paths(temp_node_set,start_node,previous_node,node,temp_path,paths,cost,costs)


def print_path_with_cost(path,cost):
    output = ""

    for node in path[:-1]:
        output += str(node+1) + " --> "
    output += str(path[-1]+1) + "   ==>  "

    print(output,cost)

def least_cost_path(paths,costs):
    index = costs.index(min(costs))
    least_cost = costs[index]

    print("\nLEAST COST PATHS: ")

    while index<len(paths):
        if costs[index] == least_cost:
            print_path_with_cost(paths[index],costs[index])
        index += 1
    
def main():
    """FIND ALL POSSIBLE PATHS: VISITING EVERY NODE ONCE, AND BACK TO THE START"""
    paths,costs = [],[] # initialize containers for the output paths and their corresponding costs
    number_of_nodes = len(data['distance_matrix']) 
    cost = 0

    path = []
    start_node = previous_node = current_node = data['depot']
    
    get_unique_paths(list(range(number_of_nodes)),start_node,previous_node,current_node,path,paths,cost,costs)

    """PRINT ALL PATHS AND THEIR CORRESPONDING COSTS"""
    # for i,path in enumerate(paths):
    #     print_path_with_cost(path,costs[i])

    """FINDING ALL PATHS WITH MINIMUM COST"""
    least_cost_path(paths,costs)

if __name__ == '__main__':
    start_time = time.process_time()
    data = create_data_model() # set data matrix
    main()
    print(time.process_time() - start_time)