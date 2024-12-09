"""main function for the NYC Trip Planner"""
from Model import organize_attractions_to_days as oad
from Model import path_planner
from Model import graph_builder
from View import view_helpers as vh
from View import user_interaction_functions as uif
from attractions import ATTRACTIONS
import googlemaps

PLACES_API = 'AIzaSyDafDzPc6c8ODZ0LZMcOYJrlvw7jgZmDeo'


def main():
    """
    1. Take user input -> max_daily_time, attractions_info, starting_name, ending_name
    2. Get place_ids for starting_name and ending_name
    3. Build a graph of places (attractions + starting & ending points) using the place_ids
    4. Plan the trip using the graph -> optimized_path (a list of place_ids)
    5. Display the trip plan
    """

    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=PLACES_API)

    # Get user input: max_daily_time,
    # maximum time spent traveling in a day
    max_daily_time = uif.get_max_daily_time()

    # Get user input: attractions_info,
    # a dictionary of attractions in form of {attraction_id: time_to_spend}
    attractions_info = uif.get_attractions_dictionary(
        PLACES_API, max_daily_time)

    # Get user input: starting_name, ending_name
    starting_name, ending_name = uif.get_starting_and_ending_names(PLACES_API)

    # Get place_ids for starting and ending points
    starting_id = vh.place_name_to_id_through_api(starting_name, PLACES_API)
    ending_id = vh.place_name_to_id_through_api(ending_name, PLACES_API)

    # Combine all places (attractions + starting & ending points) to build a graph
    places = [starting_id] + list(attractions_info.keys()) + [ending_id]
    print("Places: ", places)

    # Organize the attractions to multiple days if needed

    # a dictionary of attractions to visit by place_id: {place_id: time_length}
    attractions_organized_to_days = oad.group_attractions_to_days(max_daily_time, attractions_info)

    # initialize the paths list for all days
    paths = []
    
    for day in attractions_organized_to_days:
        # Build a graph for each day
        places_for_day = [starting_id] + day + [ending_id]
        graph = graph_builder.create_graph(gmaps, places_for_day)
        print("Graph: ", graph, "\n")

        # Plan the trip for each day
        if starting_id == ending_id:
            optimized_path = path_planner.path_planner_cycle(
                graph, places, starting_id)
        else:
            optimized_path = path_planner.path_planner_non_cycle(
                graph, places, starting_id, ending_id)
        paths.append(optimized_path)

    # Display the trip plan
    ## Initiate day number from 1 
    day = 1
    for optimized_path in paths:
        print(f"Day {day}:")
        uif.display_trip_plan_for_day(optimized_path)
        day += 1


if __name__ == "__main__":
    main()
