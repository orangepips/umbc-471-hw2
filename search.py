#!/usr/bin/python3

from __future__ import print_function
# Importing some common modules
import os, sys
import queue


# ------ You could use any python data structure or create your own class to maintain nodes, edges, queues etc. ----
# ------ This is just a simple skeleton. You don't have to use it. You can create your own code from scratch if you wish ----


# Helper functions
# I/O functions to read the different input files
# NOTE: The input files can simply be the filename if it is in the same directory as the program.
# Otherwise you have to specify the full path
# You could use functions from the "os" module to navigate file paths

# This function should read a node file. You could return a list or use any other data structure of your choice
def read_node_file(node_file):
    # You should use open() to open the file and then use read() or readlines() to read it. Remove the "pass" statement and fill in your code
    pass


# This function should read an edge file. You could use a dictionary or use any other data structure of your choice
def read_edge_file(edge_file):
    # You should use open() to open the file and then use read() or readlines() to read it. Remove the "pass" statement and fill in your code
    pass


# This function should read an heuristics file. You could use a dictionary or use any other data structure of your choice
def read_heuristics_file(heuristics_file):
    # You should use open() to open the file and then use read() or readlines() to read it. Remove the "pass" statement and fill in your code
    heuristics = {}
    lines = open(heuristics_file, 'r').readlines()
    for line in lines:
        heuristics[line.split(' ')[0]] = int(line.split(' ')[1])
    return heuristics


# Search functions
def breadth_first_search(graph, start_node, end_node):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start_node])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end_node:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for key, value in sorted(graph[node].items(), reverse=True):
            new_path = list(path)
            new_path.append(key)
            queue.append(new_path)

    return None

def depth_first_search(graph, start_node, end_node):
    # print(graph)
    stack = [start_node]
    visited = []
    while stack:
        vertex = stack.pop()

        while vertex not in visited:
            # exclude terminal nodes if not the end node go to the next item in the stack
            if (vertex not in graph and vertex != end_node):
                vertex = stack.pop()
                if vertex == None:
                    break
                continue
            visited.append(vertex)

            if vertex in graph:
                for key, value in sorted(graph[vertex].items(), reverse=True):
                    stack.extend(key)
        if end_node in visited:
            return visited

    return None

def calc_path_cost(path):
    cost = 0
    for idx, val in enumerate(path):
        if (idx+1 > len(path) - 1 or val not in graph):
            break
        next = path[idx+1]
        cost = cost + graph[val].get(next)
    return cost

def uniform_cost_search(graph, start_node, end_node):
    q = queue.PriorityQueue()
    q.put( (0, [start_node]) )
    while q:
        (path_cost, path) = q.get()
        path_end = path[-1]
        if path_end == end_node:
            return path
        for neighbor, edge_weight in sorted(graph[path_end].items(), reverse=True):
            path_with_neighbor = list(path)
            path_with_neighbor.append(neighbor)
            q.put( ( path_cost + edge_weight, path_with_neighbor) )
    return None


def greedy_search(nodes, edges, start_node, end_node, heuristic_values):
    pass


def astar_search(graph, start_node, end_node, heuristic_values):
    #  https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

    def heuristic_cost_estimate(start, goal):
        return abs(heuristic_values[start] - heuristic_values[goal])

    # the node in openSet having the lowest fScore[] value
    def get_current():
        pq = queue.PriorityQueue()
        for node in openSet:
            pq.put( (fScore[node], node) )

        return pq.get()[1]

    def reconstruct_path(cameFrom, current):
        total_path = [current]
        # for key, value in cameFrom.items():
        #     total_path.append(value)
        while current in cameFrom:
            current = cameFrom[current]
            total_path.append(current)
        total_path.reverse()
        return total_path

    # the set of nodes already evaluated.
    closedSet = set()

    # The set of currently discovered nodes still to be evaluated.
    # Initially, only the start node is known.
    openSet = set()
    openSet.add(start_node)

    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, cameFrom will eventually contain the
    # most efficient previous step.
    cameFrom = {}

    # For each node, the cost of getting from the start node to that node.
    gScore = {}
    gScore.setdefault(lambda: sys.maxint) # map with default value of Infinity

    # The cost of going from start to start is zero.
    gScore[start_node] = 0

    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    fScore = {}
    fScore.setdefault(lambda: sys.maxint) # map with default value of Infinity

    # For the first node, that value is completely heuristic.
    fScore[start_node] = heuristic_cost_estimate(start_node, end_node)

    while openSet:
        # print("openSet:\t" + str(openSet))
        # print("closedSet:\t" + str(closedSet))
        # print("cameFrom:\t" + str(cameFrom))

        current = get_current()
        if current == end_node:
            return reconstruct_path(cameFrom, current)

        openSet.remove(current)
        closedSet.add(current)

        # iterate neighbors of current node
        for neighbor, edge_weight in sorted(graph[current].items(), reverse=True):
            if neighbor in closedSet:
                continue # Ignore the neighbor which is already evaluated.
            # The distance from start to a neighbor
            tentative_gScore = gScore[current] + edge_weight
            if neighbor not in openSet: # Discover a new node
                openSet.add(neighbor)
            elif tentative_gScore >= gScore[neighbor]:
                continue # this is not a better path

            cameFrom[neighbor] = current
            gScore[neighbor] = tentative_gScore
            fScore[neighbor] = gScore[neighbor] + heuristic_cost_estimate(neighbor, end_node)

    return None


def createGraph(fileName):
    graph = dict()
    with open(fileName, "r") as f:
        for line in f:
            data = line.split(" ")
            if data[0] in graph:
                temp = graph[data[0]]
                temp.update({str(data[1]): int(data[2])})
                graph[data[0]] = temp
            else:
                graph[str(data[0])] = {str(data[1]): int(data[2])}
    return graph


# This is the main function that acts as an entry point to your program
if __name__ == "__main__":
    # Simple welcome message
    print("Welcome to this uber cool search program..")

    # Check to see if there are the right number of arguments
    if len(sys.argv) != 8:
        print(
            "Oops! Incorrect syntax..Lets try it again\npython search.py <algorithm_name> <node_file> <edge_file> <heuristics_file> <start_node> <end_node> <output_file>")
        exit(0)

    # Just for convenience, put all the values into variables
    algorithm = sys.argv[1]
    node_file = sys.argv[2]
    edge_file = sys.argv[3]
    heuristics_file = sys.argv[4]
    start_node = sys.argv[5]
    end_node = sys.argv[6]
    output_file = sys.argv[7]

    # Read the graph
    nodes = read_node_file(node_file)
    edges = read_edge_file(edge_file)
    heuristic_values = read_heuristics_file(heuristics_file)

    graph = createGraph(edge_file)

    # print (graph)
    # Open a file to write the output contents. Use the write() function to write strings into it
    output = open(output_file, 'w')

    # Depending on the algorithm specified, call the corresponding function
    # Note that the heuristics file isn't used for uninformed search algorithms like BFS, DFS and UCS

    # Replace the "pass" statements with the corresponding function calls
    if algorithm == "breadth":
        path = breadth_first_search(graph, start_node, end_node)

    elif algorithm == "depth":
        path = depth_first_search(graph, start_node, end_node)

    elif algorithm == "uniform":
        path = uniform_cost_search(graph, start_node, end_node)

    elif algorithm == "greedy":
        path = greedy_search(nodes, edges, start_node, end_node, heuristic_values)

    elif algorithm == "astar":
        path = astar_search(graph, start_node, end_node, heuristic_values)

    else:
        print("Invalid algorithm identifier '%s'" % algorithm)
        exit(0)

    cost = calc_path_cost(path)
    new_line_path = "\n".join(path)
    print(new_line_path)
    print(cost)

    output.write(new_line_path)
    output.write("\n" + str(cost))



    # Check if a valid path was returned. If it was, write the path contents and compute the cost of the path
    if not path:
        output.write("false")
    else:
        # Write the path to file.
        # If the path is a list of nodes, you can use the "join" operator.
        # The output file must have a node each line and have the path cost in the last line
        pass









