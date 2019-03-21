"""
Wraps the set of waypoints we have and allows tham to be queried
"""

import json

class Waypoints():
    def __init__(self, file_name = "waypoints.json"):
        with open(file_name, "rt") as waypoints_file:
            self._waypoints = json.load(waypoints_file)
            for k in self._waypoints:
                if 'lat' in k:
                    k['lat'] = float(k['lat'])
                if 'lon' in k:
                    k['lon'] = float(k['lon'])

    def names(self):
        """
        Returns the names of the waypoints in order
        """
        return [ ' '.join( (x['id'], x['name'])) for x in self._waypoints ]

    def update_crash_location(self, loc):
        """
        Waypoints can contain a location where an SRV crash happened, so 
        you can navigate back to it. This method updates that - the 
        loc is a (lat, long) tuple.
        """
        SRV_CRASH_NAME = "Last SRV Crash"
        existing = self.info(SRV_CRASH_NAME)
        if existing: 
            existing['lat'] = loc[0]
            existing['lon'] = loc[1]
        else:
            self._waypoints.append( { 'id': 'XSRV', 'name': SRV_CRASH_NAME, 'lat': loc[0], 'lon': loc[1] } )
        

    def info(self, name):
        """
        Returns all the info we have about a waypoint - specified
        by name. Will return None if not found.
        """
        for wp in self._waypoints:
            if ' '.join(( wp['id'], wp['name'])) == name:
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

        

