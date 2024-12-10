"""Takes inputs from user"""
from . import view_helpers
from attractions import ATTRACTIONS


def display_welcome_message() -> None:
    """
    Displays the welcome message
    """
    print("Welcome to the Trip Planner!")
    print("This program will help you plan your trip in New York City.")
    print("Let's get started!")


def display_attractions_by_category(attractions_by_category: dict) -> None:
    """
    Displays the attractions by category
    """
    for category, attractions in attractions_by_category.items():
        print(f"Category: {category}")
        for attraction in attractions:
            print(f"  - {attraction}")


def get_max_daily_time() -> float:
    """
    Returns the maximum time a user want to spend in a day
    """
    while True:
        max_daily_time = input(
            "Enter the maximum time you can spend in a day (in hours): ")
        try:
            max_daily_time_float = float(max_daily_time)
        except ValueError:
            print("Error: Please enter a valid number")
            continue
        if max_daily_time_float <= 0 or max_daily_time_float > 24:
            print("Error: Please enter a valid number between 0 and 24")
            continue
        return max_daily_time_float


def display_categories(ATTRACTIONS: dict) -> None:
    """
    Displays the categories of attractions
    """
    categories = view_helpers.get_category_list(ATTRACTIONS)
    print("Categories of attractions:")
    for category in categories:
        print(f"  - {category}")


def get_category() -> str:
    """
    Returns the category of attractions
    """
    while True:
        category = input(
            "Enter the category of attractions you want to visit: ")
        if category not in view_helpers.get_category_list(ATTRACTIONS):
            print("Error: Please enter a valid category")
            continue
        return category


def display_attractions_in_category(category: str, ATTRACTIONS: dict) -> None:
    """
    Displays the attractions in the given category
    """
    # list of attractions by each category
    attractions_in_category = view_helpers.get_attractions_by_category(category, ATTRACTIONS)
    print(f"Attractions in the category '{category}':")
    for attraction in attractions_in_category:
        print(f"  - {attraction}")


def get_attraction_id(api_key) -> str:
    """
    Returns the place_id of the attraction
    """
    while True:
        attraction_name = input("Enter the name of the attraction: ")
        attractions_list = view_helpers.get_attractions_name_list(ATTRACTIONS)
        if attraction_name not in attractions_list:
            print("Error: Please enter a valid attraction name")
            continue
        try:
            attraction_id = view_helpers.attractions_name_to_id(
                attraction_name, ATTRACTIONS)
        except ValueError as e:
            print(e)
            continue
        return attraction_id


def get_time_to_spend(max_daily_time) -> float:
    """
    Returns the time to spend at the attraction

    Args:
        max_daily_time (float): The maximum time a user can spend in a day, from input by user
    
    Returns:
        float: The time to spend at the attraction
    """
    while True:
        time_to_spend = input(
            "Enter the time to spend at the attraction (in hours): ")
        print("Successfully entered time to spend at the attraction ")
        try:
            time_to_spend_float = float(time_to_spend)
            print("Successfully converted time to spend at the attraction to float")
        except ValueError:
            print("Error: Please enter a valid number")
            continue
        if time_to_spend_float > max_daily_time:
            print(
                "Error: Time to spend at an attraction cannot be more than the maximum daily time")
            continue
        return time_to_spend_float


def get_attractions_dictionary(api_key: str, max_daily_time: float) -> dict:
    """
    Returns a dictionary of attractions in form of {attraction_id: time_to_spend}

    Enter category:
    Display attractions in the category
    Enter attraction name

    Enter time to spend at the attraction

    """
    attractions_info = {}
    while True:
        display_categories(ATTRACTIONS)
        category = get_category()
        display_attractions_in_category(category, ATTRACTIONS)
        attraction_id = get_attraction_id(api_key)
        time_to_spend = get_time_to_spend(max_daily_time)
        attractions_info[attraction_id] = time_to_spend
        add_more = input("Do you want to add more attractions? (yes/no): ")
        if add_more.lower() != "yes":
            break
    return attractions_info


def get_starting_name(PLACE_API) -> str:
    """
    Returns the name of the starting point
    """
    while True:
        place_name = input("Enter the name of the starting point: ")
        try :
            # the place name can be converted to place_id
            place_id = view_helpers.place_name_to_id_through_api(
                place_name, PLACE_API)
            return place_name 
        except ValueError as e:
            print("Place not found. Please enter a valid place name.")
            continue


def get_ending_name(PLACE_API) -> str:
    """
    Returns the name of the ending point
    """
    while True:
        place_name = input("Enter the name of the ending point: ")
        try :
            # the place name can be converted to place_id
            place_id = view_helpers.place_name_to_id_through_api(
                place_name, PLACE_API)
            return place_name 
        except ValueError as e:
            print("Place not found. Please enter a valid place name.")
            continue

def get_starting_and_ending_names(PLACES_API) -> tuple:
    """
    Returns the name of the starting and ending points
    """
    starting_name = get_starting_name(PLACES_API) 
    def get_start_end_same():
        while True:
            start_end_same = input("Do you want to end at the same place? (yes/no): ")
            if start_end_same.lower() == "yes":
                return True
            elif start_end_same.lower() == "no":
                return False
            else:
                print("Please enter a valid input: yes/no.")
    
    if get_start_end_same():
        ending_name = starting_name
    else:  
        ending_name = get_ending_name(PLACES_API)
    return starting_name, ending_name


def display_trip_plan_for_day(trip_plan_for_day: list, starting_id, ending_id, starting_name, ending_name, ATTRACTIONS) -> None:
    """
    Displays the trip plan

    Args:
        trip_plan_for_day (list): List place_ids of attractions in the order to visit
        starting_id (str): The place_id of the starting location
        ending_id (str): The place_id of the ending location
        starting_name (str): The name of the starting location (input from user)
        ending_name (str): The name of the ending location (input from user)
        ATTRACTIONS (dict): Dictionary of attractions with place_id as key
    
    Examples:
        >>> trip_plan_for_day = ['ChIJ0fci9hNawokRJVR9hdTAt80', 'ChIJmQJIxlVYwokRLgeuocVOGVU', 'ChIJnxlg1U5YwokR8T90UrZiIwI', 'ChIJ0fci9hNawokRJVR9hdTAt80']
        >>> starting_id = 'ChIJ0fci9hNawokRJVR9hdTAt80'
        >>> ending_id = 'ChIJ0fci9hNawokRJVR9hdTAt80'
        >>> starting_name = 'Starting place'
        >>> ending_name = 'Ending place'
        >>> from attractions import ATTRACTIONS
        >>> display_trip_plan_for_day(trip_plan_for_day, starting_id, ending_id, starting_name, ending_name, ATTRACTIONS)
        Trip Plan for day:
          - McSorley’s Old Ale House
          - McSorley’s Old Ale House
    """
    print("trip_plan_for_day list: ", trip_plan_for_day) ##
    attractions_id_list = []
    for i in ATTRACTIONS.keys():
        attractions_id_list.append(i)
    print("attractions_id_list: ", attractions_id_list)
    print("Trip Plan for day:")
    for place_id in trip_plan_for_day:
        
        # if place_id represents an attraction:
        if place_id in attractions_id_list:#Should be a list!!!
            print(f"place_id: {place_id} in attractions_id_list")
            attraction_name = view_helpers.attractions_id_to_name(
                place_id, ATTRACTIONS)
            print("attraction id attempted to name.")
            print("attraction id to name: ", attraction_name)
            print(f"  - {attraction_name}")
        else:
        # if place_id represents a starting or ending point:
            print(f"place_id: {place_id} not in attractions_id_list")##shouldn't
            # run for ChIJ8-JRXoxZwokRGPiQ9Ek0L84
            if place_id == starting_id:
                print(f"  - Starting point: {starting_name}")
                return
            elif place_id == ending_id:
                print(f"  - Ending point: {ending_name}")
            else:
                print("place_id: ", place_id)
                raise ValueError("Error: Invalid place_id in trip plan: ", place_id)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
