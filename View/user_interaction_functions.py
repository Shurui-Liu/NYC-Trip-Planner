"""Takes inputs from user"""
from view_helpers import attractions_name_to_id
from Model.functions import get_category_list, get_attractions_by_category
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
        max_daily_time = input("Enter the maximum time you can spend in a day (in hours): ")
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
    categories = get_category_list(ATTRACTIONS)
    print("Categories of attractions:")
    for category in categories:
        print(f"  - {category}")

def get_category() -> str:
    """
    Returns the category of attractions
    """
    while True:
        category = input("Enter the category of attractions you want to visit: ")
        if category not in get_category_list(ATTRACTIONS):
            print("Error: Please enter a valid category")
            continue
        return category

def display_attractions_in_category(category: str, ATTRACTIONS: dict) -> None:
    """
    Displays the attractions in the given category
    """
    attractions_by_category = get_attractions_by_category(ATTRACTIONS)
    attractions = attractions_by_category[category]
    print(f"Attractions in the category '{category}':")
    for attraction in attractions:
        print(f"  - {attraction}")


def get_attraction_id(api_key) -> str:
    """
    Returns the place_id of the attraction
    """
    while True:
        attraction_name = input("Enter the name of the attraction: ")
        if attraction_name not in ATTRACTIONS:
            print("Error: Please enter a valid attraction name")
            continue
        try:
            attraction_id = attractions_name_to_id(attraction_name, api_key)
        except ValueError as e:
            print(e)
            continue
        return attraction_id
    

def get_time_to_spend(max_daily_time) -> float:
    """
    Returns the time to spend at the attraction

    Args:
        max_daily_time (float): The maximum time a user can spend in a day, from input by user
    """
    while True:
        time_to_spend = input("Enter the time to spend at the attraction (in hours): ")
        try:
            time_to_spend_float = float(time_to_spend)
        except ValueError:
            print("Error: Please enter a valid number")
            continue
        time_to_spend = input("Enter the time to spend at the attraction (in hours): ")
        try:
            time_to_spend_float = float(time_to_spend)
        except ValueError:
            print("Error: Please enter a valid number")
            continue
        if time_to_spend_float > max_daily_time:
            print("Error: Time to spend at an attraction cannot be more than the maximum daily time")
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

def display_trip_plan(trip_plan: dict) -> None:
    """
    Displays the trip plan
    """