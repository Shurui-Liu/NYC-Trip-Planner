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


def path_planner_cycle(graph, places, starting_point):
    """
    Plans the path that costs the minimum distance to travel to all given attractions, 
    from a starting point and back to the starting point.

    Uses the Held-Karp Algorithm for medium dataset. Time complexity: O(n^2 * 2^n)
    Balances time complexity and optimality. 

    Args:
        graph (list of list): The graph represented as an adjacency matrix, 
        vertices are place_ids and edges are distances.
        places (list): List of places (place_ids) to visit in a day and the starting point.
        starting_point (str): The place_id of the starting location.

    Returns:
        list: The optimal path to visit all attractions and return to the start,
                represented as a list of place_ids.

    Examples:
        >>> graph = [[0, 2, 3, 4], [2, 0, 5, 6], [3, 5, 0, 7], [4, 6, 7, 0]]
        >>> places = ['A', 'B', 'C', 'D']
        >>> starting_point = 'B'
        >>> path_planner_cycle(graph, places, starting_point)
        ['B', 'D', 'C', 'A', 'B']

        >>> graph = [[0, 4786.447, 4786.987, 4786.411, 0.0], [4786.447, 0, 1.609, 10.95, 4810.501], [4786.987, 1.609, 0, 12.018, 4811.311], [4786.411, 10.95, 12.018, 0, 4808.963], [0.0, 4810.501, 4811.311, 4808.963, 0]]
        >>> places = ['ChIJ0fci9hNawokRJVR9hdTAt80', 'ChIJaXQRs6lZwokRY6EFpJnhNNE', 'ChIJUW4vEPxYwokRW6o24DU0YIg', 'ChIJ-7A-bzFawokRw8mvHCzZsc4']
        >>> starting_point = 'ChIJ0fci9hNawokRJVR9hdTAt80'
        >>> path_planner_cycle(graph, places, starting_point)
        ['ChIJ0fci9hNawokRJVR9hdTAt80', 'ChIJ-7A-bzFawokRw8mvHCzZsc4', 'ChIJaXQRs6lZwokRY6EFpJnhNNE', 'ChIJUW4vEPxYwokRW6o24DU0YIg', 'ChIJ0fci9hNawokRJVR9hdTAt80']
    """
    if len(places) == 1:
        return [starting_point]

    # Map attractions to indices
    attraction_to_index = {node: i for i, node in enumerate(places)}
    index_to_attraction = {i: node for node, i in attraction_to_index.items()}
    num_attractions = len(places)

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
                            dp[mask][u] + graph[attraction_to_index[places[u]]][attraction_to_index[places[v]]]
                        )

    # Find the minimum cost path that returns to the starting point
    end_mask = (1 << num_attractions) - 1
    min_cost = float('inf')
    last_node = -1

    for i in range(num_attractions):
        cost = dp[end_mask][i] + graph[attraction_to_index[places[i]]][attraction_to_index[starting_point]]
        if cost < min_cost:
            min_cost = cost
            last_node = i

    # Reconstruct the optimal path
    path = []
    mask = end_mask
    current = last_node

    while current != -1:
        path.append(index_to_attraction[current])
        prev = -1
        for i in range(num_attractions):
            if mask & (1 << i) and dp[mask][current] == dp[mask ^ (1 << current)][i] + graph[attraction_to_index[places[i]]][attraction_to_index[places[current]]]:
                prev = i
                break
        mask ^= (1 << current)
        current = prev

    path.reverse()
    path.append(starting_point)

    return path


def path_planner_non_cycle(graph, places, starting_point, ending_point):
    """
    Plans an optimal path of minimum distance to travel to all attractions,
    from a starting point to ending point.

    Args:
        graph (list of list): The graph represented as an adjacency matrix.
        places (list): List of places to visit in a day, including the starting and ending points.
        starting_point (str): The place_id of the starting location.
        ending_point (str): The place_id of the ending location.

    Returns:
        list: The optimal path to visit all attractions.

    Examples:
        >>> graph = [[0, 2, 3, 4], [2, 0, 5, 6], [3, 5, 0, 7], [4, 6, 7, 0]]
        >>> places = ['A', 'B', 'C', 'D']
        >>> starting_point = 'A'
        >>> ending_point = 'D'
        >>> path_planner_non_cycle(graph, places, starting_point, ending_point)
        ['A', 'B', 'C', 'D']
    """
    number_of_places = len(places)
    if number_of_places <= 2:
        return [starting_point, ending_point]

    starting_index = places.index(starting_point)
    ending_index = places.index(ending_point)
    # Start with the greedy approach, using Nearest Neighbor Heuristic
    # a list of the indices of visited places in places
    path = [starting_index]
    visited = set(path)

    # Find a path in greedy approach
    while len(path) < number_of_places and path[-1] != ending_index:
        last_index = path[-1]
        # Find the nearest neighbor to the last visited place
        next_city = min((j for j in range(number_of_places) if j not in visited and j != last_index),
                        key=lambda x: graph[last_index][x], default=ending_point)
        path.append(next_city)
        visited.add(next_city)

    if path[-1] != ending_index:
        path.append(ending_index)

    # 2-opt Optimization to improve the path produced by the greedy solution
    # calculate the cost of the path
    def calculate_cost(path):
        return sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1))

    # 2-opt algorithm
    # by choosing two non-adjacent vertices and reversing the path between them
    # 2-opt is not globally optimal either.
    # I combined 2-opt with the nearest neighbor heuristic to balance optimality and time complexity
    def two_opt(path):
        best = path
        improved = True
        while improved:
            improved = False
            for i in range(1, len(path) - 2):
                for j in range(i + 1, len(path) - 1):
                    if j - i == 1:
                        continue  # Skip adjacent nodes
                    new_path = path[:i] + path[i:j + 1][::-1] + path[j + 1:]
                    if calculate_cost(new_path) < calculate_cost(best):
                        best = new_path
                        improved = True
            path = best
        return best

    optimized_path = two_opt(path)
    optimized_path = [places[i] for i in optimized_path]
    # returns a list of place_ids
    return optimized_path


if __name__ == "__main__":
    import doctest
    doctest.testmod()
