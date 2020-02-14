# !/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) <2019>  <Tamás Zolnai>  <zolnaitamas2000@gmail.com>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
# Add the local path to the main script and external scripts so we can import them.
sys.path = [".."] + sys.path

import unittest
from psychopy import visual, monitors, core
import asrt
import platform


class linearInterpolationTest(unittest.TestCase):

    def testOneMissingData(self):
        experiment = asrt.Experiment("")

        gaze_data_list = [(0.4, 0.5), (None, None), (0.6, 0.54)]

        result = experiment.linear_interpolation(gaze_data_list, 1)
        self.assertAlmostEqual(result[0], 0.5, delta=0.001)
        self.assertAlmostEqual(result[1], 0.52, delta=0.001)

    def testWrongFunctionCall(self):
        experiment = asrt.Experiment("")

        gaze_data_list = [(0.4, 0.5), (None, None), (0.6, 0.54)]

        with self.assertRaises(AssertionError):
            result = experiment.linear_interpolation(gaze_data_list, 0)

    def testNoValidPointBefore(self):
        experiment = asrt.Experiment("")

        gaze_data_list = [(None, None), (0.6, 0.54), (0.4, 0.5)]

        result = experiment.linear_interpolation(gaze_data_list, 0)
        self.assertEqual(result, None)

    def testNoValidPointBeforeTwoInvalidData(self):
        experiment = asrt.Experiment("")

        gaze_data_list = [(None, None), (None, None), (0.6, 0.54), (0.4, 0.5)]

        result = experiment.linear_interpolation(gaze_data_list, 1)
        self.assertEqual(result, None)

    def testNoValidPointAfter(self):
        experiment = asrt.Experiment("")

        gaze_data_list = [(0.6, 0.54), (0.4, 0.5), (None, None)]

        result = experiment.linear_interpolation(gaze_data_list, 2)
        self.assertEqual(result, None)

    def testNoValidPointAfterTwoInvalidData(self):
        experiment = asrt.Experiment("")

        gaze_data_list = [(0.6, 0.54), (0.4, 0.5), (None, None), (None, None)]

        result = experiment.linear_interpolation(gaze_data_list, 2)
        self.assertEqual(result, None)

    def testOneMissingDataAmongMoreData(self):
        experiment = asrt.Experiment("")

        gaze_data_list = [(0.8, 0.8), (0.4, 0.5), (None, None), (0.5, 0.6), (0.8, 0.8), (0.8, 0.8)]

        result = experiment.linear_interpolation(gaze_data_list, 2)
        self.assertAlmostEqual(result[0], 0.45, delta=0.001)
        self.assertAlmostEqual(result[1], 0.55, delta=0.001)

    def testMoreMissingData(self):
        experiment = asrt.Experiment("")

        gaze_data_list = [(0.8, 0.8), (0.4, 0.5), (None, None), (None, None), (0.7, 0.8), (0.8, 0.8), (0.8, 0.8)]

        result = experiment.linear_interpolation(gaze_data_list, 2)
        self.assertAlmostEqual(result[0], 0.5, delta=0.001)
        self.assertAlmostEqual(result[1], 0.6, delta=0.001)

    def testMoreMissingData2(self):
        experiment = asrt.Experiment("")

        gaze_data_list = [(0.8, 0.8), (0.4, 0.5), (None, None), (None, None), (0.7, 0.8), (0.8, 0.8), (0.8, 0.8)]

        result = experiment.linear_interpolation(gaze_data_list, 3)
        self.assertAlmostEqual(result[0], 0.6, delta=0.001)
        self.assertAlmostEqual(result[1], 0.7, delta=0.001)


if __name__ == "__main__":
    unittest.main()  # run all tests
