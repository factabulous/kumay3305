# -*- coding: utf-8 -*-

"""
Class to wrap rate-of-progress code, Is given the remaining distance
and the time, and works out when we will get to the destination
"""

import time
import collections

class Rate():
    def __init__(self):
        self._WINDOW_SECS = 60 # How long we consider data for rate calc
        self._REPORT_INTERVAL_SECS = 5 # How often we record the data
        self._reports = collections.deque([], self._WINDOW_SECS // self._REPORT_INTERVAL_SECS)
        self._last_report = None

    def progress(self, distance, timestamp = None):
        """
        Sets the progress that we have made - the remaining distance
        and the current timestamp (like returned by time.time() - a float 
        second count)
        """
        timestamp = self._init_time(timestamp)
        if not self._reports or self._reports[-1][0] < timestamp - self._REPORT_INTERVAL_SECS:
            self._reports.append( ( timestamp, distance) )
        if self._reports:
            while self._reports[0][0] < timestamp - self._WINDOW_SECS:
                self._reports.popleft()

    def _init_time(self, at):
        if at:
            return at
        return time.time()

    def remaining_secs(self, asked_at=None):
        """
        Number of seconds remaining. Can be None. asked_at allows
        for call time to be overridden for tests
        """
        asked_at = self._init_time(asked_at)
        self._last_report = asked_at
        if not len(self._reports) > 1: 
            return None
        if self._reports[0][1] <= self._reports[-1][1]:
            return None
        t = self._reports[-1][0] - self._reports[0][0]
        d = self._reports[0][1] - self._reports[-1][1]
        r = t / d
        return int((r * self._reports[-1][1]))

    def need_update(self, asked_at=None):
        """
        Call this method to find out if the results need to be updated - 
        if we have had reports and either have not reported or not reported 
        recently, then we will report
        """
        asked_at = self._init_time(asked_at)
        if not len(self._reports) > 1:
            return False
        if not self._last_report:
            return True
        return asked_at - self._last_report > 5.0
        


