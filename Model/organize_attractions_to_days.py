"""
This file splits the visits into each day, 
to ensure the mimimum days required to visit all the attractions.
"""
def create_dictionary_by_time_length(attractions_by_place_id: dict) -> dict:
    """
    This function creates a dictionary with place_id as key and time_length as value.
    Args:
        - attractions_by_place_id (dict): List of attractions to visit, by place_id
    Returns:
        - attractions_by_time_spend (dict): Dictionary with place_id as key and time_length as value
    Examples:
    >>> create_dictionary_by_time_length({"num_1": {"name": "Statue of Liberty", "time_length": 2}})
    {"num_1": 2}
    >>> create_dictionary_by_time_length({"num_1": {"name": "Statue of Liberty", "time_length": 2}, "num_2": {"name": "Central Park", "time_length": 3}})
    {"num_1": 2, "num_2": 3}
    """
    attractions_by_time_length = {}
    for attraction_place_id in attractions_by_place_id.keys():
        time_length = attractions_by_place_id.get(attraction_place_id).get("time_length")
        attractions_by_time_length[attraction_place_id] = time_length
    return attractions_by_time_length

def create_new_day(day_attractions: list, day_time_left: list, max_day_time: float) -> None:
    """
    Helper function for group_attractions_to_days that creates a new day.
    Args:
        - day_attractions (list): 
          a list of lists, each list contains attractions for a day
        - day_time_left (list):
            a list of time left in each day
        - max_day_time (float):
            The maximum number of hours a user can spend in a day
    Returns:
        - None, modifies the day_attractions and day_time_left lists
    """
    day_attractions.append([])
    day_time_left.append(max_day_time)

def add_attraction_to_day(attraction_id: str, attractions_by_place_id: dict, 
                          day_index: int, day_attractions: list, day_time_left: list) -> None:
    """
    Helper function for group_attractions_to_days that adds an attraction to a day.
    It modifies the day_attractions and day_time_left lists.
    """
    day_attractions[day_index].append(attraction_id)
    day_time_left[day_index] -= attractions_by_place_id.get(attraction_id)
    
def group_attractions_to_days(max_day_time, attractions_by_place_id: dict):
    """
    This function groups the attractions into mimimum number of days.
    This function adopts the greedy approach. Otherwise, DP would require O(4^n) time complexity.
    Greedy heuristic: start with the longest one. 
    Args:
        - max_day_time (float): The maximum number of hours a user can spend in a day
        - attractions_by_place_id (dict): {place_id: time_length}
    """
    """
    1. Sort the attractions by time_length in descending order.
    2. Initialize: the day_attractions list with an empty list.
    3. 
    """
    attractions_by_place_sorted = sorted(attractions_by_place_id.items(), key=lambda x: x[1], reverse=True)
    day_attractions = [] # a list of lists, each list contains attractions for a day
    day_time_left = [] # a list of time left in each day
    current_day = 0 # the current day's index in day_attractions
    for attraction_id, time_length in attractions_by_place_sorted:
        if day_attractions == []:
            # updates the day_attractions and day_time_left lists, to add 1 day.
            create_new_day(day_attractions, day_time_left, max_day_time)
            day_attractions[-1].append(attraction_id)
            day_time_left[-1] -= time_length
        else:
            # if the new attraction can be added to an existing day:
            if time_length <= day_time_left[current_day]:
                day_attractions[current_day].append(attraction_id)
                day_time_left[current_day] -= time_length
            else:
                create_new_day(day_attractions, day_time_left, max_day_time)
                day_attractions[-1].append(attraction_id)
                day_time_left[-1] -= time_length
            
        


    attractions_by_place_id = {}
        for attraction in attractions:
            place_id = attraction.get_place_id()
            attractions_by_place_id[place_id] = attraction.get_name()
        return attractions_by_place_id
    for attraction in attractions_by_place_id.keys():
        if not isinstance(attraction, str):
            raise TypeError("Attraction should be a string.")
        
    return