#!/usr/bin/env python3

from waypoints import Waypoints
import unittest

class WaypointsTest(unittest.TestCase):

    def test_find_by_name(self):
        waypoints = Waypoints()
        self.assertEqual("Knievel's Jump", waypoints.info("KNJ Knievel's Jump")['name'])
        self.assertIsNone(waypoints.info("No such POI"))

    def test_find_by_id(self):
        waypoints = Waypoints()
        self.assertEqual("Knievel's Jump", waypoints.by_id("KNJ")['name'])
        self.assertIsNone(waypoints.by_id("No such POI"))

    def test_latlon(self):
        waypoints = Waypoints("waypoints_test.json")
        self.assertEqual((-50.1221, -70.0577), waypoints.latlon("KNJ"))
        self.assertIsNone(waypoints.latlon("Not an id"))

    def test_lists_waypoints(self):
        waypoints = Waypoints()
        self.assertTrue( len(waypoints.names()) > 5)

    def test_adding_srv_crash(self):
        waypoints = Waypoints()
        num_waypoints = len(waypoints.names())
        waypoints.update_crash_location( ( 12, 56) )
        self.assertEqual( num_waypoints + 1, len(waypoints.names()))

    def test_remaining_distance(self):
        waypoints = Waypoints("waypoints_test.json")
        self.assertEqual(4619.22936857578, waypoints.total_distance())

    def test_remaining_distance(self):
        waypoints = Waypoints("waypoints_test.json")
        self.assertEqual(4619.22936857578, waypoints.remaining_distance('BT'))
        self.assertEqual(856.5790562622092, waypoints.remaining_distance('KNJ'))

if __name__ == "__main__":
    unittest.main()
