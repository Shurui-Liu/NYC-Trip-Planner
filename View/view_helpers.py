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
            return "Not Found"
    else:
        return f"Error: {response.status_code}"