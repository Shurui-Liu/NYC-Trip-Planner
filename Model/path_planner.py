"""
The algorithms for the path planner

Part of the CS5800 final project
Date created: Dec 1, 2024
Author: Shurui Liu
"""

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

    Uses the Held-Karp Algorithm for medium dataset. Time complexity: O(n^2 * 2^n)
    Balances time complexity and optimality. 

    Args:
        graph (list of list): The graph represented as an adjacency matrix.
        attractions (list): List of places (place_ids) to visit in a day.
        starting_point (int): The index of the starting location.

    Returns:
        list: The optimal path to visit all attractions and return to the start.
    """
    if not attractions:
        return [starting_point]
    if len(attractions) == 1:
        return [starting_point] + attractions + [starting_point]
    from itertools import combinations

    # Number of attractions including the starting point
    number_of_places = len(graph)

    # Map attractions to a bitmask for DP
    attractions_set = set(attractions)
    all_places = [starting_point] + attractions
    attraction_to_index = {node: i for i, node in enumerate(all_places)}
    num_attractions = len(all_places)

    # DP table: dp[mask][i] = minimum cost to visit all nodes in `mask` ending at node `i`
    dp = [[float('inf')] * num_attractions for _ in range(1 << num_attractions)]
    dp[1 << attraction_to_index[starting_point]][attraction_to_index[starting_point]] = 0

    # Iterate over all subsets of attractions
    for mask in range(1 << num_attractions):
        for u in range(num_attractions):
            if mask & (1 << u):  # u is in the current subset
                for v in range(num_attractions):
                    if not (mask & (1 << v)):  # v is not in the subset yet
                        new_mask = mask | (1 << v)
                        dp[new_mask][v] = min(
                            dp[new_mask][v],
                            dp[mask][u] + graph[all_places[u]][all_places[v]]
                        )

    # Find the minimum cost path that returns to the starting point
    end_mask = (1 << num_attractions) - 1
    min_cost = float('inf')
    last_node = -1

    for i in range(num_attractions):
        cost = dp[end_mask][i] + graph[all_places[i]][starting_point]
        if cost < min_cost:
            min_cost = cost
            last_node = i

    # Reconstruct the optimal path
    path = []
    mask = end_mask
    current = last_node

    while mask:
        path.append(all_places[current])
        prev = -1
        for i in range(num_attractions):
            if mask & (1 << i) and dp[mask][current] == dp[mask ^ (1 << current)][i] + graph[all_places[i]][all_places[current]]:
                prev = i
                break
        mask ^= (1 << current)
        current = prev

    path.append(starting_point)
    return path[::-1]

def path_planner_non_cycle(graph, places, starting_point, ending_point):
    """
    Plans a near-optimal path of minimum distance to travel to all attractions,
    from a starting point to ending point.

    Args:
        graph (list of list): The graph represented as an adjacency matrix.
        starting_point (str): The place_id of the starting location.
        ending_point (str): The place_id of the ending location.
    
    Returns:
        list: The optimal path to visit all attractions.
    """  
    number_of_places = len(places)
    if number_of_places <= 2:
        return [starting_point, ending_point]

    # Start with the greedy approach, using Nearest Neighbor Heuristic
    path = [starting_point]
    visited = set(path)
    
    # Find a path in greedy approach
    while len(path) < number_of_places and path[-1] != ending_point:
        last = path[-1]
        # Find the nearest neighbor to the last visited place
        next_city = min((j for j in range(number_of_places) if j not in visited and j != last), 
                        key=lambda x: graph[last][x], default=ending_point)
        path.append(next_city)
        visited.add(next_city)
    
    if path[-1] != ending_point:
        path.append(ending_point)

    # 2-opt Optimization to improve the path produced by the greedy solution
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
