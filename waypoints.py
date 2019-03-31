"""
Wraps the set of waypoints we have and allows tham to be queried
"""

import json
import heading

class Waypoints():
    def __init__(self, file_name = "waypoints.json", radius=605):
        self._radius = radius
        with open(file_name, "rt") as waypoints_file:
            self._waypoints = json.load(waypoints_file)
            for k in self._waypoints:
                if 'lat' in k:
                    k['lat'] = float(k['lat'])
                if 'lon' in k:
                    k['lon'] = float(k['lon'])
        self._total_distance = None


    def total_distance(self):
        """
        Total distance for the set of waypoints from the first to the 
        same point again (linked by the 'next' field and ignoring any
        without lat/lon information
        """
        if not self._total_distance:
            self._total_distance = self.remaining_distance(self._waypoints[0]['id'])
        return self._total_distance

    def remaining_distance(self, id_):
        """
        Distance from the given waypoint id back to the start of the 
        path
        """
        end_id = self._waypoints[0]['id']
        current = self.by_id(id_)
        more_to_do = True
        dist = 0
        while more_to_do:
            # Assumes there will be a path that loops back
            next_ = self.next_navigable(current['id'])
            dist = dist + heading.great_circle(self.latlon(current['id']), self.latlon(next_['id']), self._radius)
            current = next_
            more_to_do = next_['id'] != end_id
        return dist

    def next_navigable(self, id_):
        """
        Returns the next waypoint on the route that has lat and lon. 
        <name> is the name of a waypoint.
        """
        next_ = self.by_id(self.by_id(id_)['next'])
        if not next_:
            print("*** Failed to find next for {}".format(id_))
        while 'lat' not in next_:
            next_ = self.by_id(next_['next'])
        return next_

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

    def by_id(self, id_):
        """
        Returns all the info we have about a waypoint - specified
        by id. Will return None if not found.
        """
        for wp in self._waypoints:
            if wp['id'] == id_:
                return wp
        return None

    def latlon(self, id_):
        """
        Returns the latitude/longitude tuple of a given waypoint id, 
        or None if it has none
        """
        info = self.by_id(id_)
        if info and 'lat' in info:
            return ( info['lat'], info['lon'])
        return None

        

