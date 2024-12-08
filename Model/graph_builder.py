"""
This file builds a graph of the places user wants to visit in a day, together with
starting and ending points.

Representation: Adjacency Matrix
"""

from functions import calculate_distance


def create_graph(places: list) -> list:
    """
    Creates a graph with starting point, ending point and attractions
    Args: 
        - places (list): a list of Starting point, Ending point, Attractions to visit
    Returns:
        - Adjacency Matrix representing the graph
    """
    # initialize an empty adjacency matrix. where distances are 0.
    adj_matrix = [[0 for _ in range(len(places))] for _ in range(len(places))]

    # fill in the distance from each point to every other point
    # time complexity: O(n^2)
    for i in range(len(places)):
        for j in range(i+1, len(places)):
            adj_matrix[i][j] = calculate_distance(places[i], places[j])
            adj_matrix[j][i] = adj_matrix[i][j]
    return adj_matrix
