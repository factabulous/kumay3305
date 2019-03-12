#!/usr/bin/env python3

from waypoints import Waypoints
import unittest

class WaypointsTest(unittest.TestCase):

    def test_find_by_name(self):
        waypoints = Waypoints()
        self.assertEqual("Knievel's Jump", waypoints.info("Knievel's Jump")['name'])
        self.assertIsNone(waypoints.info("No such POI"))

    def test_latlon(self):
        waypoints = Waypoints()
        self.assertEqual((-50.3293, -70.2017), waypoints.latlon("Knievel's Jump"))
        self.assertIsNone(waypoints.latlon("No such POI"))

    def test_lists_waypoints(self):
        waypoints = Waypoints()
        self.assertTrue( len(waypoints.names()) > 5)

if __name__ == "__main__":
    unittest.main()
