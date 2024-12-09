"""main function for the NYC Trip Planner"""

PLACES_API = "AIzaSyDafDzPc6c8ODZ0LZMcOYJrlvw7jgZmDeo"

from attractions import ATTRACTIONS
from View import user_interaction_functions as uif
from View import view_helpers as vh
from Model import graph_builder
from Model import path_planner

def main():
    """
    1. Take user input -> max_daily_time, attractions_info, starting_name, ending_name
    2. Get place_ids for starting_name and ending_name
    3. Build a graph of places (attractions + starting & ending points) using the place_ids
    4. Plan the trip using the graph -> optimized_path (a list of place_ids)
    5. Display the trip plan
    """
    # Get user input: max_daily_time, 
    # maximum time spent traveling in a day
    max_daily_time = uif.get_max_daily_time()

    # Get user input: attractions_info, 
    # a dictionary of attractions in form of {attraction_id: time_to_spend}
    attractions_info = uif.get_attractions_dictionary(PLACES_API, max_daily_time)

    # Get user input: starting_name, ending_name
    starting_name, ending_name = uif.get_starting_and_ending_names()

    # Get place_ids for starting and ending points
    starting_id = vh.place_name_to_id_through_api(starting_name, PLACES_API)
    ending_id = vh.place_name_to_id_through_api(ending_name, PLACES_API)

    # Combine all places (attractions + starting & ending points) to build a graph
    places = [starting_id] + list(attractions_info.keys()) + [ending_id]

    # Build a graph 
    graph = graph_builder.create_graph(places)

    # Plan the trip
    if starting_id == ending_id:
        optimized_path = path_planner.path_planner_cycle(graph, places, starting_id)
    else:
        optimized_path = path_planner.path_planner_non_cycle(graph, places, starting_id, ending_id)

    # Display the trip plan
    uif.display_trip_plan(optimized_path)
