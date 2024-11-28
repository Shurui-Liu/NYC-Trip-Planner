"""The algorithm for the path planner"""
import itertools

def path_planner(graph, attractions, starting_point, ending_point):
    """
    Plans the path that costs the minimum distance to travel to all given attractions, 
    from a starting point to ending point.

    Args:
        attractions (list): List of places to visit in a day
        starting_point (str): The place_id of starting location
        ending_point (str): The place_id of ending location
    Returns:
        list: The optimal path to visit all attractions
    """
    return

def path_planner_cycle(graph, attractions, starting_point):
    """
    Plans the path that costs the minimum distance to travel to all given attractions, 
    from a starting point and back to the starting point.

    Args:
        graph (list of list): The graph represented as an adjacency matrix.
        attractions (list): List of indices of places to visit in a day.
        starting_point (int): The index of the starting location.

    Returns:
        list: The optimal path to visit all attractions and return to the start.

    This is a brute-force solution for small graphs,
    because users cannot visit more than 10 places in a day.

    Time complexity: O(n!) where n is the number of attractions.
    """
    # Ensure the starting point is part of attractions
    places = [starting_point] + attractions
    
    # Generate all permutations of attractions except the starting point (fix start position)
    min_path = []
    min_distance = float('inf')
    
    # For each permutation of attractions
    for perm in itertools.permutations(places[1:]):
        current_path = [starting_point] + list(perm) + [starting_point]
        current_distance = sum(graph[current_path[i]][current_path[i + 1]] for i in range(len(current_path) - 1))
        
        if current_distance < min_distance:
            min_distance = current_distance
            min_path = current_path
    
    return min_path
