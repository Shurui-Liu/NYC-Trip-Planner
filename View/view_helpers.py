"""Helper functions for views."""
import requests

def attractions_name_to_id(attraction_name: str, api_key: str) -> str:
    """
    Fetches the Google Places ID for a given attraction name.

    Args:
        attraction_name (str): Name of the attraction.
        api_key (str): Your Google Places API key.
    
    Returns:
        str: Attraction ID (place_id) from Google Places API, or 'Not Found' if unavailable.
    """
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": attraction_name,
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
            raise ValueError(f"Error: Place does not exist: {attraction_name}")
    else:
        raise ValueError(f"Error: Unable to fetch data: {response.status_code}")
    
def attractions_id_to_name(place_id: str, attractions: dict) -> str:
    """
    Returns the name of the attraction given the place_id.

    Args:
        place_id (str): The place_id of the attraction.
        attractions (dict): Dictionary of attractions with place_id as key.

    Returns:
        str: Name of the attraction.
    """
    for place_id in attractions.keys():
        if attractions[place_id] == place_id:
            return attractions[place_id]["name"]
    raise ValueError(f"Error: Place ID not found: {place_id}")

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


def place_id_to_name_through_api(place_id: str, api_key: str) -> str:
    """
    Fetches the name of the place given the place_id. This is for 
    starting and ending points, because they are not in the ATTRACTIONS dictionary.

    Args:
        place_id (str): The place_id of the attraction.
        api_key (str): Google Places API key.

    Returns:
        str: Name of the place
    """
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name",
        "key": api_key
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("result"):
            return data["result"]["name"]
        else:
            raise ValueError(f"Error: Place ID not found: {place_id}")
    else:
        raise ValueError(f"Error: Unable to fetch data: {response.status_code}")
