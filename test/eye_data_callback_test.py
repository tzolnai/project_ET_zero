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
import asrt
import pytest
from psychopy import core
import threading


@pytest.mark.skipif(not asrt.g_tobii_available, reason="Can't run without tobii package")
class eyeDataCallBackTest(unittest.TestCase):

    def testWindowSize(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 8
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        clock = core.Clock()
        for i in range(100):
            experiment.eye_data_callback(gazeData)

        self.assertEqual(len(experiment.gaze_data_list), experiment.current_sampling_window * 2)

    def testWindowSize2(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 8
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.25, 0.4)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        clock = core.Clock()
        for i in range(100):
            experiment.eye_data_callback(gazeData)

        self.assertEqual(len(experiment.gaze_data_list), experiment.current_sampling_window * 2)
        for gaze_data in experiment.gaze_data_list:
            self.assertEqual(gaze_data[0], 0.375)
            self.assertEqual(gaze_data[1], 0.45)

    def testInvalidEyeData(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 8
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (1.0, 1.0)
        gazeData['left_gaze_point_validity'] = 0
        gazeData['right_gaze_point_validity'] = 0

        experiment.eye_data_callback(gazeData)
        self.assertEqual(len(experiment.gaze_data_list), 1)
        self.assertEqual(experiment.gaze_data_list[0][0], None)
        self.assertEqual(experiment.gaze_data_list[0][1], None)

        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (1.0, 1.0)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        experiment.eye_data_callback(gazeData)
        self.assertEqual(len(experiment.gaze_data_list), 2)
        self.assertEqual(experiment.gaze_data_list[1][0], 0.75)
        self.assertEqual(experiment.gaze_data_list[1][1], 0.75)

        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (1.0, 1.0)
        gazeData['left_gaze_point_validity'] = 0
        gazeData['right_gaze_point_validity'] = 1

        experiment.eye_data_callback(gazeData)
        self.assertEqual(len(experiment.gaze_data_list), 3)
        self.assertEqual(experiment.gaze_data_list[2][0], 1.0)
        self.assertEqual(experiment.gaze_data_list[2][1], 1.0)

        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (1.0, 1.0)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 0

        experiment.eye_data_callback(gazeData)
        self.assertEqual(len(experiment.gaze_data_list), 4)
        self.assertEqual(experiment.gaze_data_list[3][0], 0.5)
        self.assertEqual(experiment.gaze_data_list[3][1], 0.5)

        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (1.0, 1.0)
        gazeData['left_gaze_point_validity'] = 0
        gazeData['right_gaze_point_validity'] = 0

        experiment.eye_data_callback(gazeData)
        self.assertEqual(len(experiment.gaze_data_list), 5)
        self.assertEqual(experiment.gaze_data_list[4][0], None)
        self.assertEqual(experiment.gaze_data_list[4][1], None)

    def testDataListAppend(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 8
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"

        gazeData = {}
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(0, experiment.current_sampling_window):
            gazeData['right_gaze_point_on_display_area'] = (0.02 * i, 0.02 * i)
            gazeData['left_gaze_point_on_display_area'] = (0.03 * i, 0.03 * i)
            experiment.eye_data_callback(gazeData)

        self.assertEqual(len(experiment.gaze_data_list), experiment.current_sampling_window)
        for i in range(0, experiment.current_sampling_window):
            self.assertAlmostEqual(experiment.gaze_data_list[i][0], 0.05 * i / 2.0, delta=0.0001)
            self.assertAlmostEqual(experiment.gaze_data_list[i][1], 0.05 * i / 2.0, delta=0.0001)

    def testUnlockMainLoopLock(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 8
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"

        experiment.main_loop_lock.acquire()
        self.assertTrue(experiment.main_loop_lock.locked())

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1
        experiment.eye_data_callback(gazeData)
        self.assertTrue(not experiment.main_loop_lock.locked())

    def testSharedDataLock(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 8
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"

        with experiment.shared_data_lock:
            gazeData = {}
            gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
            gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
            gazeData['left_gaze_point_validity'] = 1
            gazeData['right_gaze_point_validity'] = 1

            thread = threading.Thread(target=experiment.eye_data_callback, args=(gazeData, ))
            thread.start()

            thread.join(3.0)
            self.assertTrue(thread.is_alive())

        thread.join()
        self.assertTrue(not thread.is_alive())

    def testLotsOfInvalidData(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 8
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        clock = core.Clock()
        for i in range(100):
            experiment.eye_data_callback(gazeData)

        self.assertEqual(len(experiment.gaze_data_list), experiment.current_sampling_window * 2)

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 0
        gazeData['right_gaze_point_validity'] = 0
        for i in range(100):
            experiment.eye_data_callback(gazeData)
        self.assertEqual(len(experiment.gaze_data_list), experiment.current_sampling_window * 2)


if __name__ == "__main__":
    unittest.main()  # run all tests
