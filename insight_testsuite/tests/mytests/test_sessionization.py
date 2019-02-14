# tests function which determines the number of seconds between two dates and times

import unittest
import os
import sys
from datetime import datetime
import csv

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, '../../../src/')

from sessionization import time_diff
from sessionization import get_inactivity
from sessionization import line_to_dic
from sessionization import update_dic
from sessionization import current_time

class TestGetSessions(unittest.TestCase):
    """Test functions from the sessionization.py script"""

    def test_time_diff1(self):
        """Is difference between two times (seconds) correctly calculated?"""
        str1 = '2017-06-17 00:00:00'
        str2 = '2017-06-17 00:00:02'
        self.assertEqual(time_diff(str1, str2), 3)

    def test_time_diff2(self):
        """Is difference between two times (minutes) correctly calculated?"""
        str1 = '2017-06-17 00:00:00'
        str2 = '2017-06-17 00:01:00'
        self.assertEqual(time_diff(str1, str2), 61)

    def test_time_diff3(self):
        """Is difference between two times (hours) correctly calculated?"""
        str1 = '2017-06-17 00:00:00'
        str2 = '2017-06-17 01:00:00'
        self.assertEqual(time_diff(str1, str2), 3601)


    def test_get_inactivity(self):
        """Is inactivity threshold correctly read from text file?"""
        self.assertEqual(get_inactivity('./input/inactivity_period.txt'), 2)

    def test_line_to_dic(self):
        """Is a line from the log correctly generated?"""
        reference = {'ip':'101.81.133.jja', 'first':'2017-06-30 00:00:00',\
                'last':'2017-06-30 00:00:00', 'duration':1, 'count':1}
        with open('./input/log.csv', newline='') as logfile:
            reader = csv.DictReader(logfile)
            line = next(reader)
        self.assertEqual(line_to_dic(line), reference)

    def test_update_dic(self):
        """Is a session correctly updated?"""
        dic = {'ip':'101.81.133.jja', 'first':'2017-06-29 23:59:58',\
                'last':'2017-06-30 00:00:00', 'duration':1, 'count':1}
        reference = {'ip':'101.81.133.jja', 'first':'2017-06-29 23:59:58',\
                'last':'2017-06-30 00:00:00', 'duration':3, 'count':2}
        with open('./input/log.csv', newline='') as logfile:
            reader = csv.DictReader(logfile)
            line = next(reader)
        self.assertEqual(update_dic(dic, line), reference)

    def test_current_time(self):
        """Is the time of the current log line correctly identified?"""
        reference = '2017-06-30 00:00:00'
        with open('./input/log.csv', newline='') as logfile:
            reader = csv.DictReader(logfile)
            line = next(reader)
        curr_time = current_time(line)
        self.assertEqual(reference, curr_time)

if __name__ == '__main__':
    unittest.main()
