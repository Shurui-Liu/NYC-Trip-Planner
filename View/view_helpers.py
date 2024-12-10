"""Helper functions for views."""
import requests


def get_category_list(ATTRACTIONS: dict) -> list:
    """
    Returns a list of unique categories from the ATTRACTIONS dictionary.

    Args:
        ATTRACTIONS (dict): Dictionary of attractions with category as key.

    Returns:
        list: List of unique categories.
    """
    category_list = []
    for place_info in ATTRACTIONS.values():
        if place_info.get("category") not in category_list:
            category_list.append(place_info.get("category"))
    return category_list


def get_attractions_by_category(category: str, ATTRACTIONS: dict) -> list:
    """
    Returns attractions in a given category from the ATTRACTIONS dictionary.

    Args:
        category (str): Category of attractions.
        ATTRACTIONS (dict): Dictionary of attractions with category as key.

    Returns:
        list: Attractions in the given category.
    """
    attractions_in_category = []
    for place_id, place_info in ATTRACTIONS.items():
        if place_info.get("category") == category:
            attractions_in_category.append(place_info.get("name"))
    return attractions_in_category


def attractions_name_to_id(attraction_name: str, ATTRACTIONS: dict) -> str:
    """
    Fetches the place_id of the attraction given the name.

    Args:
        attraction_name (str): Name of the attraction.
        ATTRACTION (dict): Dictionary of attractions with place_id as key.

    Returns:
        str: Attraction ID (place_id).
    """
    # Iterate through the ATTRACTIONS dictionary
    for place_id, details in ATTRACTIONS.items():
        # Check if the attraction name matches the input name (case-insensitive)
        if details['name'].lower() == attraction_name.lower():
            return place_id

    # If the attraction name is not found, return a message or None
    return None


def attractions_id_to_name(place_id: str, attractions: dict) -> str:
    """
    Returns the name of the attraction given the place_id.

    Args:
        place_id (str): The place_id of the attraction.
        attractions (dict): Dictionary of attractions with place_id as key.

    Returns:
        str: Name of the attraction.
    
    Examples:
        >>> ATTRACTIONS = {'ChIJ8-JRXoxZwokRGPiQ9Ek0L84': {'name': 'SoHo', 'category': 'shopping','recommeded_time_length': 2, 'location': [40.723301, -74.002988]}, 'ChIJy3Wdl0hEwokReRGPPNxadFQ': {'name': 'Coney Island', 'category': 'park', 'recommeded_time_length': 3, 'location': [40.575545, -73.970701]}}
        >>> attractions_id_to_name("ChIJ8-JRXoxZwokRGPiQ9Ek0L84", ATTRACTIONS)
        'SoHo'
    """
    # Check if the place_id is in the attractions dictionary
    if place_id in attractions:
        return attractions[place_id]["name"]
    
    # If the place_id is not found, raise an error
    raise ValueError(f"Error: Place ID not found: ", place_id)


def place_name_to_id_through_api(name: str, api_key: str) -> str:
    """
    Fetches the place_id of the place given the name. This is for 
    starting and ending points, because they are not in the ATTRACTIONS dictionary.

    Args:
        place_id (str): The place_id of the attraction.
        api_key (str): Google Places API key.

    Returns:
        str: place_id
    """
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": name,
        "inputtype": "textquery",
        "fields": "place_id",
        "key": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("candidates"):
            return data["candidates"][0]["place_id"]
        else:
            raise ValueError(f"Error: Place does not exist: {name}")
    else:
        raise ValueError(f"Error: Unable to fetch data: {response.status_code}")

def get_attractions_name_list(attractions: dict) -> list:
    """
    Returns a list of attraction names from the ATTRACTIONS dictionary.

    Args:
        attractions (dict): Dictionary of attractions with place_id as key.

    Returns:
        list: List of attraction names.
    """
    return [place_info.get("name") for place_info in attractions.values()]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
