from flask import Flask, redirect, url_for, request, render_template
import json
import heapq
import webbrowser
from threading import Timer
app = Flask(__name__)
debug = True


def a_star(source, destination, adjacency_matrix, distance_matrix):
    """A* algorithm to find the shortest path in a graph."""
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


@app.route('/get-shortest-path/', methods=['POST'])
def getShortestPath():
    if request.method == 'POST':
        content = request.get_json()

        source = content['source_point']
        destination = content['destination_point']
        adjacency_matrix = content['adjacency_matrix']
        distance_matrix = content['distance_matrix']

        if debug:
            print(source)
            print(destination)
            for adj in adjacency_matrix:
                print(adj)
            print()
            for distance in distance_matrix:
                print(distance)

        # Call the A* algorithm
        solution = a_star(source, destination, adjacency_matrix, distance_matrix)

        return json.dumps(solution)


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('success', name=user))
    else:
        return render_template('index.html')


# if __name__ == '__main__':
#     app.debug = debug
#     app.run()
# if __name__ == '__main__':
#     app.debug = debug
#     app.run(use_reloader=True)  # Ensures the browser opens automatically
# app.run(host='0.0.0.0', port=5000, use_reloader=True)

import webbrowser
from threading import Timer

if __name__ == '__main__':
    app.debug = debug
    Timer(1, lambda: webbrowser.open('http://127.0.0.1:5000')).start()  # Open the browser after a slight delay
    app.run(use_reloader=True)

