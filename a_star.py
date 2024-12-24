import numpy as np
import heapq


def a_star(source, destination, adjacency_matrix, distance_matrix):

    num_nodes = len(adjacency_matrix)

    # Initialize open and closed sets
    open_set = []
    heapq.heappush(open_set, (0, source))  # (cost, node)

    came_from = {}
    g_score = {node: float('inf') for node in range(num_nodes)}
    g_score[source] = 0

    f_score = {node: float('inf') for node in range(num_nodes)}
    f_score[source] = heuristic(source, destination, distance_matrix)

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == destination:
            return reconstruct_path(came_from, current)

        for neighbor in range(num_nodes):
            if adjacency_matrix[current][neighbor] == 1:  # Check if neighbors
                tentative_g_score = g_score[current] + distance_matrix[current][neighbor]

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, destination, distance_matrix)

                    if (f_score[neighbor], neighbor) not in open_set:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # Return an empty path if no path found


def heuristic(node, destination, distance_matrix):
    """A simple heuristic function (using direct distance to destination)."""
    return distance_matrix[node][destination]


def reconstruct_path(came_from, current):
    """Reconstruct the path from source to destination."""
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]  # Return reversed path


# Example usage
adjacency_matrix = [
    [0, 1, 1],
    [1, 0, 0],
    [1, 0, 0]
]

distance_matrix = [
    [0, 20, 5],
    [20, 0, 10],
    [5, 10, 0]
]

source = 0
destination = 1
path = a_star(source, destination, adjacency_matrix, distance_matrix)
print("Shortest path:", path)  # Output should show the nodes in the path