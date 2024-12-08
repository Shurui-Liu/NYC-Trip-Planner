"""main function for the NYC Trip Planner"""

PLACES_API = "AIzaSyDafDzPc6c8ODZ0LZMcOYJrlvw7jgZmDeo"

from attractions import ATTRACTIONS
from View import user_interaction_functions as uif

def main():
    """
    1. Take user input -> max_daily_time, attractions_info, starting_name, ending_name
    2. Get place_ids for starting_name and ending_name
    3. Build a graph of places (attractions + starting & ending points) using the place_ids
    4. Plan the trip using the graph -> optimized_path (a list of place_ids)
    5. Display the trip plan
    """