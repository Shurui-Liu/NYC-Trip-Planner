"""Takes inputs from user"""
from view_helpers import attractions_name_to_id


def get_attractions_dictionary(api_key) -> dict:
    """
    Returns a dictionary of attractions in form of {attraction_id: time_to_spend}
    """
    attractions_info = {}
    while True:
        attraction_name = input("Enter the name of the attraction: ")
        try:
            attraction_id = attractions_name_to_id(attraction_name, api_key)
        except ValueError as e:
            print(e)
            continue
        time_to_spend = input("Enter the time to spend at the attraction (in hours): ")
        try:
            time_to_spend_float = float(time_to_spend)
        except ValueError:
            print("Error: Please enter a valid number")
            continue
        attractions_info[attraction_id] = time_to_spend_float
        if input("Do you want to add more attractions? (y/n): ") == "n":
            break
    pass
