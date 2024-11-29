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
    """
    attractions_by_time_length = {}
    for attraction_place_id in attractions_by_place_id.keys():
        time_length = attractions_by_place_id.get(attraction_place_id).get("time_length")
        attractions_by_time_length[attraction_place_id] = time_length
    return attractions_by_time_length

def group_attractions_to_days(day_length, attractions_by_place_id: dict):
    """
    This function groups the attractions into mimimum number of days.
    Args:
        - day_length: The maximum number of hours a user can spend in a day
        - attractions_by_place_id (dict): List of attractions to visit, by place_id
    """

    attractions_by_place_id = {}
        for attraction in attractions:
            place_id = attraction.get_place_id()
            attractions_by_place_id[place_id] = attraction.get_name()
        return attractions_by_place_id
    for attraction in attractions_by_place_id.keys():
        if not isinstance(attraction, str):
            raise TypeError("Attraction should be a string.")
        
    return