# -*- coding: utf-8 -*-

"""
Class to wrap rate-of-progress code, Is given the remaining distance
and the time, and works out when we will get to the destination
"""

import time

class Rate():
    def __init__(self):
        self._start_timestamp = None
        self._end_timestamp = None
        self._start_distance = None
        self._end_distance = None
        self._last_report = None

    def progress(self, distance, timestamp = time.time()):
        """
        Sets the progress that we have made - the remaining distance
        and the current timestamp (like returned by time.time() - a float 
        second count)
        """
        if not self._start_timestamp:
            self._start_timestamp = timestamp
        if not self._start_distance:
            self._start_distance = distance
        self._end_timestamp = timestamp
        self._end_distance = distance

    def remaining_secs(self, asked_at=time.time()):
        """
        Number of seconds remaining. Can be None. asked_at allows
        for call time to be overridden for tests
        """
        self._last_report = asked_at
        if not self._start_timestamp:
            return None
        if self._end_distance >= self._start_distance:
            return None
        t = self._end_timestamp - self._start_timestamp
        d = self._start_distance - self._end_distance
        r = t / d
        return int((r * self._end_distance))

    def need_update(self, asked_at=time.time()):
        """
        Call this method to find out if the results need to be updated - 
        if we have had reports and either have not reported or not reported 
        recently, then we will report
        """
        if not self._start_timestamp:
            return False
        if not self._last_report:
            return True
        return asked_at - self._last_report > 20.0
        


