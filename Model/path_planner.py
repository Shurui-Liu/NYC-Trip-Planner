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
    if starting_point == ending_point:
        return path_planner_cycle(graph, attractions, starting_point)
    else:
        return path_planner_non_cycle(graph, starting_point, ending_point)


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

def path_planner_non_cycle(graph, starting_point, ending_point):
    """
    Plans a near-optimal path of minimum distance to travel to all attractions,
    from a starting point to ending point.

    Args:
        graph (list of list): The graph represented as an adjacency matrix.
        attractions (list): List of indices of places to visit in a day.
        starting_point (str): The place_id of the starting location.
        ending_point (str): The place_id of the ending location.
    
    Returns:
        list: The optimal path to visit all attractions.
    """
    number_of_places = len(graph)

    # Step 1: Nearest Neighbor Heuristic
    path = [starting_point]
    visited = set(path)
    
    # Find the nearest neighbor to the last visited city
    while len(path) < number_of_places and path[-1] != ending_point:
        last = path[-1]
        next_city = min((j for j in range(number_of_places) if j not in visited and j != last), 
                        key=lambda x: graph[last][x], default=ending_point)
        path.append(next_city)
        visited.add(next_city)
    
    if path[-1] != ending_point:
        path.append(ending_point)

    # Step 2: 2-opt Optimization
    def calculate_cost(path):
        return sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1))

    def two_opt(path):
        best = path
        improved = True
        while improved:
            improved = False
            for i in range(1, len(path) - 2):
                for j in range(i + 1, len(path) - 1):
                    if j - i == 1: continue  # Skip adjacent nodes
                    new_path = path[:i] + path[i:j + 1][::-1] + path[j + 1:]
                    if calculate_cost(new_path) < calculate_cost(best):
                        best = new_path
                        improved = True
            path = best
        return best

    optimized_path = two_opt(path)
    return optimized_path
