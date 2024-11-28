"""
This file builds a graph of the places user wants to visit in a day, together with
starting and ending points.

Representation: Adjacency Matrix
"""

from functions import calculate_distance

def create_graph(vertices: list) -> list:
    """
    Creates a graph with starting point, ending point and attractions
    Args: 
        - Vertices: Starting point, Ending point, Attractions to visit
    Returns:
        - Adjacency Matrix representing the graph
    """
    # initialize an empty adjacency matrix. where distances are 0.
    adj_matrix = [[0 for _ in range(len(vertices))] for _ in range(len(vertices))]

    # fill in the distance from each point to every other point
    # time complexity: O(n^2)
    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)):
            adj_matrix[i][j] = calculate_distance(vertices[i], vertices[j])
            adj_matrix[j][i] = adj_matrix[i][j]
    return adj_matrix