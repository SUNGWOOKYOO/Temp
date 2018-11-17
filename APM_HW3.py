# coding: utf-8
import numpy as np
import pandas as pd
import queue

GRAPH_SIZE = 200
INPUT_FILE = "graph.txt"

class Node:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity

        
# Problem 2.A. Breadth First Search
def BFS(adj_list, source, target):
    source = source - 1
    target = target -1
    Q = queue.Queue()
    distance = [None] * GRAPH_SIZE
    previous = [None] * GRAPH_SIZE
    distance[source] = 0
    visited = [source]
    Q.put(source)
    
    while Q.empty() == False:
        node = Q.get()
        for neighbor in adj_list[node]:
            if neighbor.id not in visited:
                distance[neighbor.id] = distance[node] + 1
                previous[neighbor.id] = node
                Q.put(neighbor.id)
                visited.append(neighbor.id)
    
    if distance[target] == None:
        print ("Path do not exist")
    else:
        print ('Length: ' + str(distance[target]))
        prev_node = previous[target]
        traverse_order = [target]
        while prev_node != None:
            traverse_order.append(prev_node)
            prev_node = previous[prev_node]

        for index, node in reversed(list(enumerate(traverse_order))):
            if index > 0:
                print ("(%d, %d)" % (node + 1, traverse_order[index-1] + 1), end=' ')


# Problem 2.B. Edmond-Karf Algorithm
def EdmondKarf(adj_list, adj_mat, source, target):
    flow = 0
    source = source - 1
    target = target - 1
    flow_mat = np.zeros((GRAPH_SIZE, GRAPH_SIZE), dtype=np.float64)
    
    while True:
        Q = queue.Queue()
        Q.put(source)
        visited = [source]
        previous = [None] * GRAPH_SIZE

        while Q.empty() == False:
            node = Q.get()
            for neighbor in adj_list[node]:
                if previous[neighbor.id] == None and neighbor.id not in visited and adj_mat[node][neighbor.id] > flow_mat[node][neighbor.id]:
                    previous[neighbor.id] = node
                    Q.put(neighbor.id)
                    visited.append(neighbor.id)
                    if neighbor.id == target:
                        break
        
        if previous[target] != None:
            min_cap = float("inf")
            prev_node = previous[target]
            next_node = target
            while prev_node != None:
                min_cap = min(min_cap, adj_mat[prev_node][next_node] - flow_mat[prev_node][next_node])
                next_node = prev_node
                prev_node = previous[prev_node]
            
            prev_node = previous[target]
            next_node = target
            while prev_node != None:
                flow_mat[prev_node][next_node] = flow_mat[prev_node][next_node] + min_cap
                flow_mat[next_node][prev_node] = flow_mat[next_node][prev_node] - min_cap
                next_node = prev_node
                prev_node = previous[prev_node]
            flow = flow + min_cap
        else:
            break
        
    print ("Total: " + str(flow))
    sum_of_edges = 0
    for neighbor in adj_list[source]:
        print ("(%d, %d)Flow: %f" % (source + 1, neighbor.id + 1, flow_mat[source][neighbor.id]))
    return flow_mat


# Problem 2.C Minimum ST-Cut
def BFS2(adj_list, adj_mat, residual_mat, reachable, source):
    source = source - 1
    Q = queue.Queue()
    reachable = [source]
    Q.put(source)
    
    while Q.empty() == False:
        node = Q.get()
        for neighbor in adj_list[node]:
            if residual_mat[node][neighbor.id] != 0 and neighbor.id not in reachable:
                Q.put(neighbor.id)
                reachable.append(neighbor.id)


def minCut(adj_list, adj_mat, residual_mat, source):
    source = source - 1
    total_cap = 0
    reachable = [source]
    BFS2(adj_list, adj_mat, residual_mat, reachable, source)
    
    total = 0
    visited = [source]
    for node in reachable:
        for neighbor in adj_list[node]:
            if neighbor.id not in visited:
                visited.append(neighbor.id)
                if neighbor.id not in reachable:
                    print (str(node + 1) + " - " + str(neighbor.id + 1) + ":" + str(adj_mat[node][neighbor.id]))
                    total = total + adj_mat[node][neighbor.id]
    print (total)

if __name__ == "__main__":
    # Graph Parsing from '.txt' file to a numpy 2D array
    file = pd.read_csv(INPUT_FILE, sep=' ', header=None)
    adj_mat = np.array(file)
    adj_mat = adj_mat[:, :GRAPH_SIZE]

    # Make Adjacency List from Adjacency Matrix
    adj_list = []
    for i in range(GRAPH_SIZE):
        adj_list.append([])
        adj_list[i] = []

    for row in range(GRAPH_SIZE):
        for col in range(GRAPH_SIZE):
            if adj_mat[row][col] != -1:
                new_node = Node(col, adj_mat[row][col])
                adj_list[row].append(new_node)


    BFS(adj_list, 1, 150)

    flow_mat = EdmondKarf(adj_list, adj_mat, 1, 150)

    residual_mat = adj_mat - abs(flow_mat)
    minCut(adj_list, adj_mat, residual_mat, 1)
else:
    print("This part can be showed when only being imported ")


