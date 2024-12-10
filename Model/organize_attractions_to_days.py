"""
This file splits the visits into each day, 
to ensure the mimimum days required to visit all the attractions.
"""


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

    Examples:
        >>> day_attractions = [['Attraction1'], ['Attraction2']]
        >>> day_time_left = [5.0, 3.0]
        >>> max_day_time = 8.0
        >>> create_new_day(day_attractions, day_time_left, max_day_time)
        >>> day_attractions
        [['Attraction1'], ['Attraction2'], []]
        >>> day_time_left
        [5.0, 3.0, 8.0]

        >>> day_attractions = []
        >>> day_time_left = []
        >>> max_day_time = 10.0
        >>> create_new_day(day_attractions, day_time_left, max_day_time)
        >>> day_attractions
        [[]]
        >>> day_time_left
        [10.0]
    """
    day_attractions.append([])
    day_time_left.append(max_day_time)


def add_attraction_to_day(attraction_id: str, attractions_by_place_id: dict,
                          day_index: int, day_attractions: list, day_time_left: list) -> None:
    """
    Helper function for group_attractions_to_days that adds an attraction to a day.
    It modifies the day_attractions and day_time_left lists.
    Args:
        - attraction_id (str): The place_id of the attraction
        - attractions_by_place_id (dict): {place_id: time_length}
        - day_index (int): The index of the day to add the attraction to
        - day_attractions (list): 
          a list of lists, each list contains attractions for a day
        - day_time_left (list):
            a list of time left in each day
    Returns:
        - None, modifies the day_attractions and day_time_left lists
    """
    if day_index < 0 or day_index >= len(day_attractions):
        raise ValueError("Invalid day index.")
    day_attractions[day_index].append(attraction_id)
    day_time_left[day_index] -= attractions_by_place_id.get(attraction_id)


def find_day_to_add_attraction(attraction_id: str, days_time_left: float,
                               attractions_by_time_length: dict):
    """
    This function finds the day to add the attraction to.
    Args:
        - attraction_id (str): The place_id of the attraction
        - attractions_by_time_length (dict): {place_id: time_length}
    Returns:
        - int: The index of the day to add the attraction to
          - -1: If the attraction cannot be added to any day
    Examples:
        >>> days_time_left = [3.0, 2.0, 1.5]
        >>> attractions_by_time_length = {'A1': 2.0, 'A2': 1.0, 'A3': 4.0}
        >>> find_day_to_add_attraction('A1', days_time_left, attractions_by_time_length)
        0
        >>> find_day_to_add_attraction('A2', days_time_left, attractions_by_time_length)
        0
        >>> find_day_to_add_attraction('A3', days_time_left, attractions_by_time_length)
        -1
    """
    # iterate through the days time left list to
    # find the first available day to add the attraction to
    day_index = 0
    while day_index < len(days_time_left):
        if days_time_left[day_index] >= attractions_by_time_length.get(attraction_id):
            return day_index
        day_index += 1
    return -1


def group_attractions_to_days(max_day_time, attractions_by_time_length: dict) -> list:
    """
    Groups attractions into a minimum number of days based on available time.

    Args:
        - max_day_time (float): The maximum time a user can spend in a day
        - attractions_by_time_length (dict): {place_id: time_length}
    Returns:
        - list: A list of lists, each list contains attractions for a day
    
    Example:
        >>> max_day_time = 6.0
        >>> attractions_by_time_length = {'A': 2.0, 'B': 4.0, 'C': 0.5}
        >>> group_attractions_to_days(max_day_time, attractions_by_time_length)
        [['B', 'C'], ['A']]

        >>> max_day_time = 4.0
        >>> attractions_by_time_length = {'A': 2.0, 'B': 2.4}
        >>> group_attractions_to_days(max_day_time, attractions_by_time_length)
        [['B'], ['A']]
    """
    if not attractions_by_time_length:
        return []

    # Sort attractions by time_length in descending order
    attractions_by_time_length_sorted = dict(sorted(
        attractions_by_time_length.items(), key=lambda x: x[1], reverse=True
    ))

    print("type of attractions_by_time_length_sorted: ", type(attractions_by_time_length_sorted))
    print("attractions_by_time_length_sorted: ", attractions_by_time_length_sorted)

    # Initialize days
    day_attractions = []  # List of lists, each representing attractions in a day
    day_time_left = []    # Remaining time for each day

    for attraction_id, time_length in attractions_by_time_length_sorted.items():
        # Raise an error if any attraction's time exceeds max_day_time
        if time_length > max_day_time:
            raise ValueError("The time length of an attraction cannot exceed the maximum day time.")

        # Try to fit the attraction into an existing day
        day_added = False
        for i in range(len(day_time_left)):
            if day_time_left[i] >= time_length:
                day_attractions[i].append(attraction_id)
                day_time_left[i] -= time_length
                day_added = True
                break

        # If it doesn't fit in any existing day, create a new day
        if not day_added:
            day_attractions.append([attraction_id])
            day_time_left.append(max_day_time - time_length)

    return day_attractions
