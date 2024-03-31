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

class states_based_tree:
    leaf_nodes = []

    def __init__(self,data_matrix,cost,parent,level,city):
        self.data_matrix = data_matrix
        self.cost = cost
        self.parent = parent
        self.level = level
        self.city = city
        self.children = []
        self.ancestors = []

    def add_child(self,node):
        if node not in self.children:
            self.children.append(node)

    def add_ancestor(self,parent_node):
        if parent_node.ancestors:
            self.ancestors+=parent_node.ancestors+[parent_node]
        else:
            self.ancestors.append(parent_node)

    def show_node(self):
        print("\nData Matrix: ")
        for row in self.data_matrix:
            for val in row:
                print(val,end="\t")
            print("")
        print("Cost: ", self.cost)
        print("Parent: ", self.parent)
        print("Level: ", self.level)
        print("City: ",self.city)
        print("Children: ",self.children)
        print("Ancestors: ",self.ancestors)

    def add_leaf_node(self):
        if self not in states_based_tree.leaf_nodes:
            states_based_tree.leaf_nodes.append(self)
    
    def remove_leaf_node(self):
        states_based_tree.leaf_nodes.remove(self)

    @classmethod
    def show_leaves(cls):
        for node in states_based_tree.leaf_nodes:
            node.show_node()

def data_matrix_value(from_node,to_city):
    data_matrix = [i[:] for i in from_node.data_matrix]

    for i in range(n):
        data_matrix[from_node.city][i] = float('inf')
        data_matrix[i][to_city] = float('inf')
    data_matrix[to_city][0] = float('inf')

    return data_matrix, from_node.cost + from_node.data_matrix[from_node.city][to_city] + matrix_lower_bound(data_matrix)

def update_upper_bound():
    global states_based_tree_root,upper_bound

    from_node = states_based_tree(data['distance_matrix'],matrix_lower_bound(data['distance_matrix']),None,0,data['depot'])
    states_based_tree_root = from_node
    
    visited,min_path,cities = [0],[from_node],list(range(n))
    
    for i in range(n-1):
        for to_city in cities:
            if to_city not in visited:
                # creating states based tree node and connect it to the tree in the right place
                data_matrix,cost = data_matrix_value(from_node,to_city)
                states_based_tree_node = states_based_tree(data_matrix,cost,from_node.city,i+1,to_city)
                states_based_tree_node.add_ancestor(from_node)
                from_node.add_child(states_based_tree_node)

        # find the minimum cost node and minimum cost 
        min_cost_node_value = float('inf')
        min_cost_node = None
        for states_based_tree_node in from_node.children:
            if states_based_tree_node.cost < min_cost_node_value:
                min_cost_node_value = states_based_tree_node.cost
                min_cost_node = states_based_tree_node

        # if the children nodes are not minimum nodes, they are leaf nodes
        for node in from_node.children:
            if node!=min_cost_node:
                node.add_leaf_node()

        min_path.append(min_cost_node)
        visited.append(min_cost_node.city)
        
        from_node = min_cost_node

    # if from_node.cost < upper_bound
    upper_bound = from_node.cost

    return min_path

# the following recursive function uses DFS to explore all possible paths from a given node 
# a branch is explored only if the cost<=upper_bound else, the branch is killed
# current_node = leaf node to be futher discovered, visited_leaves = explored leaf nodes (not leaf anymore)
def explore(current_node,unvisited_node_set,paths,costs,visited_leaves): 
    global upper_bound,min_cost

    for to_city in unvisited_node_set:
        # creating states based tree node and connect it to the tree in the right place
        data_matrix,cost = data_matrix_value(current_node,to_city)
        states_based_tree_node = states_based_tree(data_matrix,cost,current_node.city,current_node.level+1,to_city)
        states_based_tree_node.add_ancestor(current_node)
        current_node.add_child(states_based_tree_node)

        # if cost>upper_bound, kill branch else, explore further
        if cost<=upper_bound:
            visited_leaves.append(current_node)
            unvisited_node_set_temp = unvisited_node_set[:]
            unvisited_node_set_temp.remove(states_based_tree_node.city)
            if unvisited_node_set_temp:
                explore(states_based_tree_node,unvisited_node_set_temp,paths,costs,visited_leaves)
            else:
                upper_bound = cost
                min_cost = cost
                paths.append(states_based_tree_node.ancestors + [states_based_tree_node])
                costs.append(cost)
        else:
            states_based_tree_node.add_leaf_node()

def print_path_with_cost(path,cost):
    output = ""

    for node in path:
        output+=str(node.city) + " --> "
    output+=str(data['depot']) + "   ==>  "

    print(output,cost)

def matrix_lower_bound(matrix):
    row_mins = []
    for i in range(n):
        row_min = min(matrix[i])
        if row_min == float('inf'):
            continue
        else:
            row_mins.append(row_min)
        for j in range(n):
            matrix[i][j]-=row_min
    
    col_mins = []
    for i in range(n):
        col_min = float('inf')
        for j in range(n):
            if matrix[j][i]<col_min:
                col_min = matrix[j][i]
        if col_min == float('inf'):
            col_mins.append(0)
        else:
            col_mins.append(col_min)

    for i in range(n):
        for j in range(n):
            matrix[j][i]-=col_mins[i]
    
    return sum(row_mins) + sum(col_mins)

def main():
    for i in range(n):
        data['distance_matrix'][i][i] = float('inf')
    
    path = update_upper_bound()

    min_paths = [path]
    min_costs = [path[-1].cost]

    print("INITIAL LEAST COST PATH IS: ")
    print_path_with_cost(path,path[-1].cost)
    visited_leaves = []

    for leaf_node in states_based_tree.leaf_nodes:
        if leaf_node.cost<=upper_bound:
            remaining_nodes = list(range(n))
            for visited_node in leaf_node.ancestors:
                remaining_nodes.remove(visited_node.city)
                
            remaining_nodes.remove(leaf_node.city)
            explore(leaf_node,remaining_nodes,min_paths,min_costs,visited_leaves)

    print("LEAST COST PATHS USING BnB ARE: ")
    for i in range(len(min_paths)):
        if min_costs[i] == min_cost:
            print_path_with_cost(min_paths[i],min_cost)

    for visited_leaf in visited_leaves:
        if visited_leaf in states_based_tree.leaf_nodes:
            visited_leaf.remove_leaf_node()

if __name__ == '__main__':
    start_time = time.process_time()

    # set data matrix and declare global variables
    data = create_data_model() 
    n = len(data['distance_matrix'])
    states_based_tree_root = None
    upper_bound = float('inf')
    min_cost = float('inf')
    
    main()

    print(time.process_time() - start_time)