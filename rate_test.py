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
        r.progress(900, 2.0)
        self.assertEqual(9, r.remaining_secs())

    def test_rate_reports_no_progress(self):
        r = rate.Rate()
        r.progress(1000, 1000.0)
        r.progress(1000, 2000.0)
        self.assertIsNone(r.remaining_secs())

    def test_rate_reports_negative_progress(self):
        r = rate.Rate()
        r.progress(1000, 1000.0)
        r.progress(1100, 2000.0)
        self.assertIsNone(r.remaining_secs())

    def test_need_update(self):
        r = rate.Rate()
        # No reports, so no need to update
        self.assertFalse(r.need_update(1000.0))
        r.progress(1000, 1000.0)
        # Now we have progress, so we need to report
        self.assertTrue(r.need_update(1001.0))
        # When we have made a report then we don't need another
        self.assertIsNone(r.remaining_secs(1001.0))
        self.assertFalse(r.need_update(1002.0))
        self.assertFalse(r.need_update(1021.0))
        # But we should report again after 20 seconds
        self.assertTrue(r.need_update(1022.0))

if __name__ == "__main__":
    unittest.main()
   
