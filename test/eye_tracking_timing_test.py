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
from psychopy import core, monitors
import pytest


class eyeTrackingTimingTest(unittest.TestCase):

    @pytest.mark.skipif(not asrt.g_tobii_available, reason="Can't run without tobii package")
    def testGazeDataCallback(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 36

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = True
        gazeData['right_gaze_point_validity'] = True

        clock = core.Clock()
        for i in range(100):
            experiment.eye_data_callback(gazeData)
        run_time = clock.getTime()
        self.assertAlmostEqual(run_time, 0.0, delta=0.1)

    def testWaitForEyeResponse(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.monitor_width = 47.5
        experiment.settings.AOI_size = 1.0
        experiment.settings.dispersion_threshold = 2.0
        sampling_window = 36

        experiment.mymonitor = monitors.Monitor('myMon')
        experiment.mymonitor.setSizePix([1366, 768])
        experiment.mymonitor.setWidth(29)
        experiment.mymonitor.saveMon()

        for i in range(sampling_window):
            experiment.gaze_data_list.append([0.5, 0.5])

        clock = core.Clock()
        for i in range(100):
            experiment.wait_for_eye_response([0.5, 0.5], sampling_window // 2)
        run_time = clock.getTime()
        self.assertAlmostEqual(run_time, 0.0, delta=0.1)


if __name__ == "__main__":
    unittest.main()  # run all tests
