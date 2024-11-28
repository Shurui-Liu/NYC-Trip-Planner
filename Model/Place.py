"""
Defines a class for place.
Attributes:
    - name: str, name of the place
    - place_id: str, unique identifier of the place
    - location: tuple, (longitude, latitude) location of the place

Methods:
    - __init__: initializes the place object
    - __str__: returns the name of the place
"""

class Place:
    name = None
    location = None
    def __init__(self, name: str, location: tuple):
        """
        Initializes the place object.
        Input:
            - name: str, name of the place
            - location: tuple, (longitude, latitude) location of the place
        """
        self.name = name
        self.location = location

    def __str__(self) -> str:
        """
        Returns the textual representation of the place.
        """
        return self.name