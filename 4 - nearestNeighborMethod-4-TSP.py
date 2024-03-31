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

def solve(matrix):
    path,cost = [data['depot']],0

    cannedCol = set()
    cannedCol.add(data['depot'])
    
    rowMinIndex,colMinIndex = 0,None

    for _ in range(n-1):
        rowMin = float('inf')
        for j in range(n):
            if j not in cannedCol and matrix[rowMinIndex][j]<rowMin:
                rowMin = matrix[rowMinIndex][j]
                colMinIndex = j

        cannedCol.add(colMinIndex)
        rowMinIndex = colMinIndex
        path.append(rowMinIndex)
        cost += rowMin

    cost += matrix[path[-1]][data['depot']]
    path.append(data['depot'])
    
    print_path_with_cost(path,cost)
    
def print_path_with_cost(path,cost):
    output = ""

    for node in path[:-1]:
        output += str(node) + " --> "
    output += str(path[-1]) + "   ==>  "

    print(output,cost)

def main():
    solve(data['distance_matrix'])

if __name__ == '__main__':
    start_time = time.process_time()
    data = create_data_model()
    n = len(data['distance_matrix'])
    for i in range(n):
        data['distance_matrix'][i][i]=float('inf')
    main()
    print(time.process_time() - start_time)