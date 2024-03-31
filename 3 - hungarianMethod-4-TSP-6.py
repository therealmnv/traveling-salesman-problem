import time
from collections import defaultdict

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    
    data['distance_matrix'] = [                 #-------TA           
        [float('inf'), 2451, 713, 1018, 1631],
        [2451, float('inf'), 1745, 1524, 831],
        [713, 1745, float('inf'), 355, 920],
        [1018, 1524, 355, float('inf'), 700],
        [1631, 831, 920, 700, float('inf')]
    ]  

    # data['distance_matrix'] = [                 #-------TA, stuck in loop
    #     [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875],
    #     [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589],
    #     [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262],
    #     [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466],
    #     [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796],
    #     [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547],
    #     [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724],
    #     [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038],
    #     [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744],
    #     [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0]
    # ]  

    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def rowAndColTransform(matrix):
    for i in range(n):
        row_min = min(matrix[i])
        if row_min == 0:
            continue
        for j in range(n):
            matrix[i][j]-=row_min

    col_mins = []
    for i in range(n):
        col_min = float('inf')
        for j in range(n):
            if matrix[j][i]<col_min:
                col_min = matrix[j][i]
        col_mins.append(col_min)

    for i in range(n):
        for j in range(n):
            matrix[j][i]-=col_mins[i]

def countZeros(matrix,cannedRow=[],cannedCol=[]):
    rowZeros = [0 for _ in range(n)]
    colZeros = rowZeros[:]

    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 0:
                if i not in cannedRow and j not in cannedCol:
                    rowZeros[i]+=1
                    colZeros[j]+=1

    return rowZeros,colZeros

def findNonZeroMinimum(matrix):
    min = float('inf')
    for i in range(n):
        for j in range(n):
            if matrix[i][j]<min and matrix[i][j]!=0:
                min = matrix[i][j]

def findNonZeroMinimum(matrix):
    min = float('inf')
    for i in range(n):
        for j in range(n):
            if matrix[i][j]<min and matrix[i][j]!=0:
                min = matrix[i][j]
    # print(min)
    if min==float('inf'):
        return None

    newLocations = []

    for i in range(n):
        for j in range(n):
            if matrix[i][j]==min:
                matrix[i][j]=0
                newLocations.append((i,j))

    return newLocations

def inspect(matrix):
    newLocs = findNonZeroMinimum(matrix)

    if not newLocs:
        return 

    for i in newLocs:
        tempMatrix = [x[:] for x in matrix]
        coverZeros(tempMatrix,modified=False,cannedRow=[i[0]],cannedCol=[i[1]],assignedPoints=[(i[0],i[1])])

def checkTSPoptimality(matrix,assignedPoints):
    global minCost,minPath

    cycle = [assignedPoints[0]]
    visited = [assignedPoints[0]]
    cycles = []
    for i in range(n):
        if assignedPoints[cycle[-1][1]] in visited:
            for j in assignedPoints:
                if j not in visited:
                    cycles.append(cycle)
                    cycle = [j]
                    visited.append(j)
                    break
        else:
            visited.append(assignedPoints[cycle[-1][1]])
            cycle.append(assignedPoints[cycle[-1][1]])

    cycles.append(cycle) 

    if len(cycles)==1:
        out = [0]
        cost = 0

        for i in cycles[0]:
            out.append(i[1])
            cost+=data['distance_matrix'][out[-2]][out[-1]]
        if cost<minCost:
            minCost = cost
            minPath = out[:]
        # print_path_with_cost(out,cost)

    else:
        inspect(matrix)

def makeOptimal(matrix,cannedRow,cannedCol):
    min = float('inf')
    for i in range(n):
        for j in range(n):
            if i not in cannedRow and j not in cannedCol:
                if matrix[i][j]<min:
                    min = matrix[i][j]

    for i in range(n):
        for j in range(n):
            if i not in cannedRow and j not in cannedCol:
                matrix[i][j]-=min
            elif i in cannedRow and j in cannedCol:
                matrix[i][j]+=min

def minLinesMaxZeros(matrix,assignedPoints):
    maxSet = set(range(n))
    assignedRows = set()
    tickedCols = set()

    for i in assignedPoints:
        assignedRows.add(i[0])

    tickedRows = maxSet.difference(assignedRows)

    for i in tickedRows:
        for j in range(n):
            if matrix[i][j]==0:
                tickedCols.add(j)

    newlyMarkedRows = set()
    for i,j in assignedPoints:
        if j in tickedCols:
            newlyMarkedRows.add(i)
            tickedRows.add(i)

    for i in newlyMarkedRows:
        for j in range(n):
            if matrix[i][j]==0:
                tickedCols.add(j)

    return maxSet.difference(tickedRows),tickedCols

def coverZeros(matrix,modified=True,cannedRow=[],cannedCol=[],assignedPoints=[]):
    if modified:
        rowZeros,colZeros = countZeros(matrix,[],[])
        if sum(rowZeros) == (n*n-n):
            # print("-----ZERO ANOMALY-----")
            return 
    else:
        rowZeros,colZeros = countZeros(matrix,cannedRow,cannedCol)
        if sum(rowZeros) == (n*n-n):
            # print("-----ZERO ANOMALY-----")
            return 

        if len(assignedPoints)!=n:
            if sum(rowZeros)+sum(colZeros) == 0: # cover zeros with minimum number of lines and perform operations
                untickedRow,tickedCol = minLinesMaxZeros(matrix,assignedPoints)

                if len(untickedRow)==n or len(tickedCol)==n:
                    # print("-----TICK ANOMALY-----")
                    return

                makeOptimal(matrix,untickedRow,tickedCol)
                coverZeros(matrix,True,[],[],[])
                return 
                
            flag = True

            for i in range(n):
                if rowZeros[i]==1 or colZeros[i]==1:
                    flag = False
                    break

            if flag: # force assign zeros  
                unassignedZeros = []
                for i in range(n):
                    for j in range(n):
                        if i not in cannedRow and j not in cannedCol and matrix[i][j]==0 and (i,j) not in assignedPoints:
                            unassignedZeros.append((i,j))
                            

                for i in unassignedZeros:
                    tempAssignedPoints = assignedPoints[:]
                    tempCannedRow = cannedRow[:]
                    tempCannedCol = cannedCol[:]
                    
                    tempAssignedPoints.append(i)
                    tempCannedRow.append(i[0])
                    tempCannedCol.append(i[1])

                    coverZeros(matrix,False,tempCannedRow,tempCannedCol,tempAssignedPoints)
                return
            
                  
    for i in range(n):
        for j in range(n):
            if rowZeros[i]==1 and matrix[i][j]==0 and j not in cannedCol and i not in cannedRow:
                assignedPoints.append((i,j))
                cannedCol.append(j)

    for i in range(n):
        for j in range(n):
            if colZeros[i]==1 and matrix[j][i]==0 and i not in cannedCol and j not in cannedRow:
                assignedPoints.append((j,i))
                cannedRow.append(j)

    if len(assignedPoints)==n:
        assignedPoints.sort(key = lambda x: x[0])
        ap = tuple(assignedPoints)
        if ap in d:
            for mat in d[ap]:
                if mat==matrix:
                    return 

        d[ap].append(matrix)
        checkTSPoptimality(matrix,assignedPoints)
    else:
        coverZeros(matrix,False,cannedRow,cannedCol,assignedPoints)
        

def print_path_with_cost(path,cost):
    output = ""

    for node in path[:-1]:
        output += str(node+1) + " --> "
    output += str(path[-1]+1) + "   ==>  "

    print(output,cost)
    
def main():
    matrix = [x[:] for x in data['distance_matrix']]
    rowAndColTransform(matrix)
    coverZeros(matrix)

if __name__ == '__main__':
    start_time = time.process_time()
    data = create_data_model()
    n = len(data['distance_matrix'])
    for i in range(n):
        data['distance_matrix'][i][i]=float('inf')
    minCost = float('inf')
    minPath = None
    d = defaultdict(list)
    main()
    print_path_with_cost(minPath,minCost)
    print(time.process_time() - start_time)