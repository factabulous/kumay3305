"""
Wraps the set of waypoints we have and allows tham to be queried
"""

import json

class Waypoints():
    def __init__(self):
        with open("waypoints.json", "rt") as waypoints_file:
            self._waypoints = json.load(waypoints_file)

    def names(self):
        """
        Returns the names of the waypoints in order
        """
        return [ x['name'] for x in self._waypoints ]

    def info(self, name):
        """
        Returns all the info we have about a waypoint - specified
        by name. Will return None if not found.
        """
        for wp in self._waypoints:
            if wp['name'] == name:
                return wp
        return None

    def latlon(self, name):
        """
        Returns the latitude/longitude tuple of a given named waypoint, 
        or None if it has none
        """
        info = self.info(name)
        if info and 'lat' in info:
            return ( float(info['lat']), float(info['lon']))
        return None

        

