"""
This file builds a graph of the places user wants to visit in a day, together with
starting and ending points.

Representation: Adjacency Matrix
"""

import functions


def create_graph(gmaps, places: list) -> list:
    """
    Creates a graph with starting point, ending point and attractions
    Args: 
        - places (list): a list of place_ids of Starting point, Ending point, Attractions to visit
    Returns:
        - Adjacency Matrix representing the graph
    
    Example:
        >>> import googlemaps
        >>> gmaps = googlemaps.Client(key="AIzaSyDafDzPc6c8ODZ0LZMcOYJrlvw7jgZmDeo")
        >>> places = ['ChIJ4zGFAZpYwokRGUGph3Mf37k', 'ChIJaXQRs6lZwokRY6EFpJnhNNE']
        >>> create_graph(gmaps, places)
        [[0, 2.238], [2.238, 0]]
    """
    # initialize an empty adjacency matrix. where distances are 0.
    adj_matrix = [[0 for _ in range(len(places))] for _ in range(len(places))]

    # fill in the distance from each point to every other point
    # time complexity: O(n^2)
    for i in range(len(places)):
        for j in range(i+1, len(places)):
            adj_matrix[i][j] = functions.calculate_distance(gmaps, places[i], places[j])
            adj_matrix[j][i] = adj_matrix[i][j]
    return adj_matrix


if __name__ == "__main__":
    import doctest
    doctest.testmod()