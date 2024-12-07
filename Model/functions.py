"""This module contains functions that are used in data processing."""
import googlemaps

# Google Maps API key
api_key = "YOUR_API_KEY"
 
# Initialize the Google Maps client
gmaps = googlemaps.Client(key=api_key)

def calculate_distance(gmaps, origin, destination, mode="driving", unit="km"):
    """
    Calculate the distance between two locations using the Google Maps Distance Matrix API.

    Args:
        gmaps (googlemaps.Client): Pre-initialized Google Maps client.
        origin (str/tuple): The starting location, by place_id
        destination (str/tuple): The destination location, by place_id
        mode (str): Travel mode where possible options are "driving", "walking", "bicycling", "transit" (default: "driving").
        unit (str): Unit of distance where options are "km" (default) or "meters".

    Returns:
        float: The distance between the two locations in the specified unit.
        str: Error message if the calculation fails.
    """
    # Validate mode input
    valid_modes = ["driving", "walking", "bicycling", "transit"]
    if mode not in valid_modes:
        return f"Error: Invalid mode '{mode}'. Choose from {valid_modes}."

    # Call the Distance Matrix API
    try:
        result = gmaps.distance_matrix(origins=origin,
                                       destinations=destination,
                                       mode=mode,
                                       units='metric')
    except Exception as e:
        return f"Error: Unable to fetch data from Google Maps API. Details: {e}"

    # Handle API-level errors
    if result.get("status") != "OK":
        return f"Error: API returned a status of {result.get('status')}."

    # Extract the distance
    try:
        element = result["rows"][0]["elements"][0]
        if element["status"] == "OK":
            distance = element["distance"]["value"]  # Distance in km
            if unit == "km":
                return distance  
            elif unit == "meters":      # Return as meters
                return distance * 1000  # Convert to meters
            else:
                return f"Error: Invalid unit '{unit}'. Choose 'km' or 'meters'."
        else:
            return f"Error: Element status is {element['status']}."
    except (IndexError, KeyError) as e:
        return f"Error: Issue with API response. Details: {e}"
