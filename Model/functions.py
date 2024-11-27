"""This module contains functions that are used in data processing."""
import googlemaps

# Google Maps API key
api_key = "YOUR_API_KEY"
 
# Initialize the Google Maps client
gmaps = googlemaps.Client(key=api_key)

def get_distance(origin: str, destination: str, gmaps) -> float:
    """
    gets the distance between two points (distance travelled from A to B).
    Input:
        - origin: str, address or place A
        - destination: str, address or place B
    Output:
        - distance: float
    """

    # Define the origin and destination
    origin = "Address or place A"
    destination = "Address or place B"

    # Request directions
    directions = gmaps.directions(
        origin,              # Start location
        destination,         # End location
        mode="driving"       # Mode of transport: driving, walking, bicycling, transit
    )

    # Extract the distance and duration from the response
    if directions:
        route = directions[0]['legs'][0]
        distance = route['distance']['text']   # E.g., "5.6 km"
        if not distance:
            return None
        if not " km" in distance:
            if " m" in distance:
                distance.replace(" m", "")
                distance = float(distance) / 1000
        else:
            distance.replace(" km", "")
        try:
            distance = float(distance)
        except:
            return None
        return distance 
    else:
        return None
    ###??? If None is returned, what should be done? what errors to catch?