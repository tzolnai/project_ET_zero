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
sys.path = [".."] + \
    [os.path.join("..", "externals", "psychopy_mock")] + sys.path

import unittest
import asrt
import pytest
from psychopy import core
import threading
import psychopy_visual_mock as pvm


def DummyConvert(pos):
    return pos


@pytest.mark.skipif(not asrt.g_tobii_available, reason="Can't run without tobii package")
class waitForEyeResponseTest(unittest.TestCase):

    def testWindowSize(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 12
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.2
        experiment.settings.dispersion_threshold = 0.1
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(100):
            experiment.eye_data_callback(gazeData)

        thread = threading.Thread(target=experiment.wait_for_eye_response, args=((0.45, 0.45), experiment.current_sampling_window, ))
        thread.start()
        thread.join(3.0)
        self.assertTrue(not thread.is_alive())

    def testWindowSize2(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 12
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.5
        experiment.settings.dispersion_threshold = 0.2
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.25, 0.4)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(100):
            experiment.eye_data_callback(gazeData)

        self.assertEqual(len(experiment.gaze_data_list), experiment.current_sampling_window)

        thread = threading.Thread(target=experiment.wait_for_eye_response, args=((0.4, 0.4), experiment.current_sampling_window, ))
        thread.start()
        thread.join(3.0)
        self.assertTrue(not thread.is_alive())

    def testInvalidEyeData(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 12
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.5
        experiment.settings.dispersion_threshold = 0.2
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.25, 0.4)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1
        for i in range(experiment.current_sampling_window):
            experiment.eye_data_callback(gazeData)

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.25, 0.4)
        gazeData['left_gaze_point_validity'] = 0
        gazeData['right_gaze_point_validity'] = 0

        for i in range(experiment.current_sampling_window):
            experiment.eye_data_callback(gazeData)

        self.assertEqual(len(experiment.gaze_data_list), experiment.current_sampling_window)

        thread = threading.Thread(target=experiment.wait_for_eye_response, args=((0.4, 0.4), experiment.current_sampling_window, ))
        thread.start()
        thread.join(3.0)
        self.assertTrue(thread.is_alive())
        
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.25, 0.4)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1
        for i in range(experiment.current_sampling_window):
            experiment.eye_data_callback(gazeData)
        thread.join(3.0)
        self.assertTrue(not thread.is_alive())

    def testDataListStructure(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 12
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.2
        experiment.settings.dispersion_threshold = 0.1
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(experiment.current_sampling_window):
            experiment.eye_data_callback(gazeData)

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.2, 0.2)
        gazeData['right_gaze_point_on_display_area'] = (0.2, 0.2)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(experiment.current_sampling_window):
            experiment.eye_data_callback(gazeData)

        self.assertEqual(len(experiment.gaze_data_list), experiment.current_sampling_window)

        thread = threading.Thread(target=experiment.wait_for_eye_response, args=((0.12, 0.12), experiment.current_sampling_window, ))
        thread.start()
        thread.join(3.0)
        self.assertTrue(not thread.is_alive())

    def testSharedDataLock(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 12
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.2
        experiment.settings.dispersion_threshold = 0.1
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(experiment.current_sampling_window):
            experiment.eye_data_callback(gazeData)

        with experiment.shared_data_lock:
            thread = threading.Thread(target=experiment.wait_for_eye_response, args=((0.45, 0.45), experiment.current_sampling_window, ))
            thread.start()

            thread.join(3.0)
            self.assertTrue(thread.is_alive())

        thread.join(3.0)
        self.assertTrue(not thread.is_alive())

    def testLotsOfInvalidData(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 12
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.2
        experiment.settings.dispersion_threshold = 0.1
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 0
        gazeData['right_gaze_point_validity'] = 0
        for i in range(100):
            experiment.eye_data_callback(gazeData)
        self.assertEqual(len(experiment.gaze_data_list), experiment.current_sampling_window)

        thread = threading.Thread(target=experiment.wait_for_eye_response, args=((0.25, 0.25), experiment.current_sampling_window, ))
        thread.start()
        thread.join(3.0)
        self.assertTrue(thread.is_alive())

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.2, 0.2)
        gazeData['right_gaze_point_on_display_area'] = (0.2, 0.2)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(experiment.current_sampling_window):
            experiment.eye_data_callback(gazeData)

        thread.join(3.0)
        self.assertTrue(not thread.is_alive())

    def testLockMainLoopLock(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 12
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.2
        experiment.settings.dispersion_threshold = 0.1
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.2, 0.2)
        gazeData['right_gaze_point_on_display_area'] = (0.2, 0.2)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(experiment.current_sampling_window):
            experiment.eye_data_callback(gazeData)

        thread = threading.Thread(target=experiment.wait_for_eye_response, args=((0.5, 0.5), experiment.current_sampling_window, ))
        thread.start()
        thread.join(3.0)
        self.assertTrue(thread.is_alive())
        self.assertTrue(experiment.main_loop_lock.locked())

        gazeData['left_gaze_point_on_display_area'] = (0.45, 0.45)
        gazeData['right_gaze_point_on_display_area'] = (0.45, 0.45)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(experiment.current_sampling_window):
            experiment.eye_data_callback(gazeData)

        thread.join(3.0)
        self.assertTrue(not thread.is_alive())
        self.assertTrue(not experiment.main_loop_lock.locked())

    def testNoData(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 12
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.1
        experiment.settings.dispersion_threshold = 0.1
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        thread = threading.Thread(target=experiment.wait_for_eye_response, args=((0.45, 0.45), experiment.current_sampling_window, ))
        thread.start()
        thread.join(3.0)
        self.assertTrue(thread.is_alive())
        self.assertTrue(experiment.main_loop_lock.locked())

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(100):
            experiment.eye_data_callback(gazeData)

        thread.join(3.0)
        self.assertTrue(not thread.is_alive())

    def testNotEnoughData(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 12
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.1
        experiment.settings.dispersion_threshold = 0.1
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(experiment.current_sampling_window - 1):
            experiment.eye_data_callback(gazeData)

        thread = threading.Thread(target=experiment.wait_for_eye_response, args=((0.45, 0.45), experiment.current_sampling_window, ))
        thread.start()
        thread.join(3.0)
        self.assertTrue(thread.is_alive())
        self.assertTrue(experiment.main_loop_lock.locked())

        experiment.eye_data_callback(gazeData)

        thread.join(3.0)
        self.assertTrue(not thread.is_alive())
        self.assertTrue(not experiment.main_loop_lock.locked())

    def testMoreData(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 12
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.1
        experiment.settings.dispersion_threshold = 0.1
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (200, 200)
        gazeData['right_gaze_point_on_display_area'] = (200, 200)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(experiment.current_sampling_window):
            experiment.eye_data_callback(gazeData)

        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(experiment.current_sampling_window):
            experiment.eye_data_callback(gazeData)

        thread = threading.Thread(target=experiment.wait_for_eye_response, args=((0.45, 0.45), experiment.current_sampling_window, ))
        thread.start()
        thread.join(3.0)
        self.assertTrue(not thread.is_alive())

    def testPosNotInAOI(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 12
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.1
        experiment.settings.dispersion_threshold = 0.1
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.6, 0.6)
        gazeData['right_gaze_point_on_display_area'] = (0.6, 0.6)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(experiment.current_sampling_window):
            experiment.eye_data_callback(gazeData)

        thread = threading.Thread(target=experiment.wait_for_eye_response, args=((0.45, 0.45), experiment.current_sampling_window, ))
        thread.start()
        thread.join(3.0)
        self.assertTrue(thread.is_alive())
        self.assertTrue(experiment.main_loop_lock.locked())

        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1

        for i in range(experiment.current_sampling_window):
            experiment.eye_data_callback(gazeData)

        thread.join(3.0)
        self.assertTrue(not thread.is_alive())
        self.assertTrue(not experiment.main_loop_lock.locked())

    def testAverageCalculator(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 4
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.2
        experiment.settings.dispersion_threshold = 0.15
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.45, 0.55)
        gazeData['right_gaze_point_on_display_area'] = (0.45, 0.55)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1
        experiment.eye_data_callback(gazeData)

        gazeData['left_gaze_point_on_display_area'] = (0.4, 0.6)
        gazeData['right_gaze_point_on_display_area'] = (0.4, 0.6)
        experiment.eye_data_callback(gazeData)

        gazeData['left_gaze_point_on_display_area'] = (0.41, 0.61)
        gazeData['right_gaze_point_on_display_area'] = (0.42, 0.63)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1
        experiment.eye_data_callback(gazeData)

        gazeData['left_gaze_point_on_display_area'] = (0.39, 0.57)
        gazeData['right_gaze_point_on_display_area'] = (0.38, 0.59)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1
        experiment.eye_data_callback(gazeData)

        thread = threading.Thread(target=experiment.wait_for_eye_response, args=((0.5, 0.5), experiment.current_sampling_window, ))
        thread.start()
        thread.join(3.0)
        self.assertTrue(not thread.is_alive())

    def testMainLoopLockIsReleasedByQuit(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 12
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.2
        experiment.settings.dispersion_threshold = 0.1
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        experiment.main_loop_lock.acquire()

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['q'])
        experiment.wait_for_eye_response((0.33, 0.64), experiment.current_sampling_window)

        self.assertTrue(not experiment.main_loop_lock.locked())

    def testMainLoopLockIsReleasedByQuit2(self):
        experiment = asrt.Experiment("")
        experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.current_sampling_window = 12
        experiment.last_N = 10
        experiment.last_RSI = 400.0
        experiment.trial_phase = "before_stimulus"
        experiment.settings.AOI_size = 0.2
        experiment.settings.dispersion_threshold = 0.1
        experiment.ADCS_to_PCMCS = DummyConvert
        experiment.distance_ADCS_to_PCMCS = DummyConvert

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['q'])
        experiment.wait_for_eye_response((0.33, 0.64), experiment.current_sampling_window)

        self.assertTrue(not experiment.main_loop_lock.locked())


if __name__ == "__main__":
    unittest.main()  # run all tests
