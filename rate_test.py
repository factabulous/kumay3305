#!/usr/bin/env python3

import rate
import unittest

class RatingTest(unittest.TestCase):

    def test_rate_no_reports(self):
        r = rate.Rate()
        self.assertIsNone(r.remaining_secs())

    def test_rate_reports(self):
        r = rate.Rate()
        r.progress(1000, 1.0)
        r.progress(900, 11.0)
        self.assertEqual(90, r.remaining_secs())

    def _test_rate_reports_recent_progress(self):
        """
        progress starts at 100km/s, but recent reports are 0.1km/s, so 
        we probably want to use that data, rather then the earlier data
        """
        r = rate.Rate()
        r.progress(1000, 1.0)
        r.progress(900, 6.0)
        r.progress(100, 800.0)
        r.progress(99, 810.0)
        self.assertEqual(990, r.remaining_secs())

    def test_rate_reports_no_progress(self):
        r = rate.Rate()
        r.progress(1000, 1000.0)
        r.progress(1000, 1030.0)
        self.assertIsNone(r.remaining_secs())

    def test_rate_reports_negative_progress(self):
        r = rate.Rate()
        r.progress(1000, 1000.0)
        r.progress(1100, 1020.0)
        self.assertIsNone(r.remaining_secs())

    def test_need_update(self):
        r = rate.Rate()
        # No reports, so no need to update
        self.assertFalse(r.need_update(1000.0))
        r.progress(1000, 1000.0)
        r.progress(1001, 1020.0)
        # Now we have progress, so we need to report
        self.assertTrue(r.need_update(1020.0))
        # When we have made a report then we don't need another
        self.assertIsNone(r.remaining_secs(1020.0))
        self.assertFalse(r.need_update(1021.0))
        self.assertTrue(r.need_update(1026.0))
        # But we should report again after 20 seconds
        self.assertTrue(r.need_update(1026.0))

if __name__ == "__main__":
    unittest.main()
   
