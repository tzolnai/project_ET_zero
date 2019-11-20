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
# Add the local path to the main script so we can import it.
sys.path = [".."] + \
    [os.path.join("..", "externals", "psychopy_mock")] + sys.path

import unittest
import asrt
import pytest
import psychopy_visual_mock as pvm
from psychopy import monitors, visual, core

try:
    import tobii_research as tobii
except:
    pass


def DummyFunction(*argv):
    pass


core.wait = DummyFunction


@pytest.mark.skipif(not asrt.g_tobii_available, reason="Can't run without tobii package")
class initEyeTrackerTest(unittest.TestCase):

    def setUp(self):
        self.mywindow = None

    def tearDown(self):
        if self.mywindow is not None:
            self.mywindow.close()

    def initWindow(self):
        my_monitor = monitors.Monitor('myMon')
        my_monitor.setSizePix([1366, 768])
        my_monitor.setWidth(29)
        my_monitor.saveMon()

        self.mywindow = visual.Window(size=[1366, 768],
                                      pos=[0, 0],
                                      units='cm',
                                      fullscr=False,
                                      allowGUI=True,
                                      monitor=my_monitor,
                                      color='White',
                                      gammaRamp=256,
                                      gammaErrorPolicy='ignore')

    def testIdealCase(self):
        experiment = asrt.Experiment("")
        self.assertTrue(experiment.eye_tracker is None)

        self.original_find_all_eyetrackers = tobii.find_all_eyetrackers

        def find_all_eyetrackers_mock():
            return ["I'm an eye-tracker"]
        tobii.find_all_eyetrackers = find_all_eyetrackers_mock

        experiment.init_eyetracker()
        self.assertTrue(experiment.eye_tracker == "I'm an eye-tracker")

        tobii.find_all_eyetrackers = self.original_find_all_eyetrackers

    def testNoDevice(self):
        experiment = asrt.Experiment("")
        self.assertTrue(experiment.eye_tracker is None)

        self.original_find_all_eyetrackers = tobii.find_all_eyetrackers

        def find_all_eyetrackers_mock():
            return []
        tobii.find_all_eyetrackers = find_all_eyetrackers_mock

        visual_mock = pvm.PsychoPyVisualMock()
        self.initWindow()
        experiment.mywindow = self.mywindow

        with self.assertRaises(SystemExit):
            experiment.init_eyetracker()

        self.assertTrue(experiment.eye_tracker is None)
        drawing_list = visual_mock.getListOfDrawings()
        self.assertEqual(len(drawing_list), 2)

        self.assertEqual(drawing_list[0].text, "Eye-tracker eszköz keresése...")
        self.assertEqual(drawing_list[1].text, "Nem találtam semmilyen eye-tracker eszközt!")

        tobii.find_all_eyetrackers = self.original_find_all_eyetrackers

    try_counter_g = 0

    def testDeviceFoundAfterSomeTry(self):
        experiment = asrt.Experiment("")
        self.assertTrue(experiment.eye_tracker is None)

        self.original_find_all_eyetrackers = tobii.find_all_eyetrackers

        global try_counter_g
        try_counter_g = 0

        def find_all_eyetrackers_mock():
            global try_counter_g
            try_counter_g += 1
            if try_counter_g < 100:
                return []
            else:
                return ["I'm an eye-tracker"]

        tobii.find_all_eyetrackers = find_all_eyetrackers_mock

        visual_mock = pvm.PsychoPyVisualMock()
        self.initWindow()
        experiment.mywindow = self.mywindow

        experiment.init_eyetracker()

        self.assertTrue(experiment.eye_tracker == "I'm an eye-tracker")
        drawing_list = visual_mock.getListOfDrawings()
        self.assertEqual(len(drawing_list), 1)

        self.assertEqual(drawing_list[0].text, "Eye-tracker eszköz keresése...")

        tobii.find_all_eyetrackers = self.original_find_all_eyetrackers

    def testDeviceNeedsToomanyTries(self):
        experiment = asrt.Experiment("")
        self.assertTrue(experiment.eye_tracker is None)

        self.original_find_all_eyetrackers = tobii.find_all_eyetrackers

        global try_counter_g
        try_counter_g = 0

        def find_all_eyetrackers_mock():
            global try_counter_g
            try_counter_g += 1
            if try_counter_g < 1000:
                return []
            else:
                return ["I'm an eye-tracker"]

        tobii.find_all_eyetrackers = find_all_eyetrackers_mock

        visual_mock = pvm.PsychoPyVisualMock()
        self.initWindow()
        experiment.mywindow = self.mywindow

        with self.assertRaises(SystemExit):
            experiment.init_eyetracker()

        self.assertTrue(experiment.eye_tracker is None)
        drawing_list = visual_mock.getListOfDrawings()
        self.assertEqual(len(drawing_list), 2)

        self.assertEqual(drawing_list[0].text, "Eye-tracker eszköz keresése...")
        self.assertEqual(drawing_list[1].text, "Nem találtam semmilyen eye-tracker eszközt!")

        tobii.find_all_eyetrackers = self.original_find_all_eyetrackers


if __name__ == "__main__":
    unittest.main()  # run all tests
