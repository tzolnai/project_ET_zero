# !/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) <2019>  <Tamás Zolnai>    <zolnaitamas2000@gmail.com>

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
from psychopy import monitors, visual, core, logging
import asrt
import psychopy_visual_mock as pvm
import platform
import pytest


def DummyFunction(*argv):
    pass


core.wait = DummyFunction

# ignore warnings comming from psychopy
logging.console.setLevel(logging.ERROR)


class drawJacobiScreenTest(unittest.TestCase):

    def setUp(self):
        self.mywindow = None

    def tearDown(self):
        if self.mywindow is not None:
            self.mywindow.close()

    def assertEqualWithEOL(self, string1, string2):
        string1 = string1.replace("\r", "")
        string2 = string2.replace("\r", "")
        self.assertEqual(string1, string2)

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

    def constructFilePath(self, file_name):
        filepath = os.path.abspath(__file__)
        (inst_and_feedback_path, trail) = os.path.split(filepath)
        inst_and_feedback_path = os.path.join(
            inst_and_feedback_path, "data", "instr_and_feedback", file_name)
        return inst_and_feedback_path

    def testDefaultScreen(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.asrt_distance = 15
        experiment.settings.asrt_size = 3.0
        experiment.colors = {'linecolor': 'black'}

        experiment.dict_pos = {1: (-0.5, 0.5), 2: (0.5, 0.5), 3: (-0.5, -0.5), 4: (0.5, -0.5)}

        visual_mock = pvm.PsychoPyVisualMock()
        self.initWindow()
        experiment.mywindow = self.mywindow
        experiment.draw_jacobi_screen()

        drawing_list = visual_mock.getListOfDrawings()
        self.assertEqual(len(drawing_list), 4)

        for i in range(len(drawing_list)):
            stim_background_circle = drawing_list[i]
            self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
            self.assertEqual(stim_background_circle.lineColor, 'black')
            self.assertEqual(stim_background_circle.fillColor, None)

    def testScreenWithInstruction(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.asrt_distance = 15
        experiment.settings.asrt_size = 3.0
        experiment.colors = {'linecolor': 'black'}

        experiment.dict_pos = {1: (-0.5, 0.5), 2: (0.5, 0.5), 3: (-0.5, -0.5), 4: (0.5, -0.5)}

        visual_mock = pvm.PsychoPyVisualMock()
        self.initWindow()
        experiment.mywindow = self.mywindow
        experiment.draw_jacobi_screen("Some text!")

        drawing_list = visual_mock.getListOfDrawings()
        self.assertEqual(len(drawing_list), 5)

        instruction_text = drawing_list[0]
        self.assertTrue(isinstance(instruction_text, pvm.TextStim))
        # size
        self.assertAlmostEqual(instruction_text.height, 0.8, delta=0.001)
        # pos
        self.assertAlmostEqual(instruction_text.pos[0], 0.0, delta=0.001)
        self.assertAlmostEqual(instruction_text.pos[1], 10.5, delta=0.001)
        # color
        self.assertEqual(instruction_text.color, "black")
        # text
        self.assertEqual(instruction_text.text, str("Some text!"))

        for i in range(len(drawing_list) - 1):
            stim_background_circle = drawing_list[i + 1]
            self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
            self.assertEqual(stim_background_circle.lineColor, 'black')
            self.assertEqual(stim_background_circle.fillColor, None)

    def testScreenWithInstructionAndActiveStim(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.asrt_distance = 15
        experiment.settings.asrt_size = 3.0
        experiment.colors = {'wincolor': 'white', 'linecolor': 'black',
                             'stimp': 'blue', 'stimr': 'blue'}

        experiment.dict_pos = {1: (-0.5, 0.5), 2: (0.5, 0.5), 3: (-0.5, -0.5), 4: (0.5, -0.5)}

        visual_mock = pvm.PsychoPyVisualMock()
        self.initWindow()
        experiment.mywindow = self.mywindow
        experiment.draw_jacobi_screen("Some text!", 2)

        drawing_list = visual_mock.getListOfDrawings()
        self.assertEqual(len(drawing_list), 6)

        instruction_text = drawing_list[0]
        self.assertTrue(isinstance(instruction_text, pvm.TextStim))
        # size
        self.assertAlmostEqual(instruction_text.height, 0.8, delta=0.001)
        # pos
        self.assertAlmostEqual(instruction_text.pos[0], 0.0, delta=0.001)
        self.assertAlmostEqual(instruction_text.pos[1], 10.5, delta=0.001)
        # color
        self.assertEqual(instruction_text.color, "black")
        # text
        self.assertEqual(instruction_text.text, str("Some text!"))

        for i in range(1, 4):
            stim_background_circle = drawing_list[i]
            self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
            self.assertEqual(stim_background_circle.lineColor, 'black')
            self.assertEqual(stim_background_circle.fillColor, None)

        active_stim = drawing_list[5]
        self.assertTrue(isinstance(active_stim, pvm.Circle))
        self.assertEqual(active_stim.lineColor, 'black')
        self.assertEqual(active_stim.fillColor, 'blue')
        self.assertEqual(active_stim.radius, experiment.settings.asrt_size)
        self.assertAlmostEqual(active_stim.pos[0], 0.5, delta=0.001)
        self.assertAlmostEqual(active_stim.pos[1], 0.5, delta=0.001)

    def testScreenWithActiveStim(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.asrt_distance = 15
        experiment.settings.asrt_size = 3.0
        experiment.colors = {'wincolor': 'white', 'linecolor': 'black',
                             'stimp': 'blue', 'stimr': 'blue'}

        experiment.dict_pos = {1: (-0.5, 0.5), 2: (0.5, 0.5), 3: (-0.5, -0.5), 4: (0.5, -0.5)}

        visual_mock = pvm.PsychoPyVisualMock()
        self.initWindow()
        experiment.mywindow = self.mywindow
        experiment.draw_jacobi_screen("", 3)

        drawing_list = visual_mock.getListOfDrawings()
        self.assertEqual(len(drawing_list), 5)

        for i in range(0, 3):
            stim_background_circle = drawing_list[i]
            self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
            self.assertEqual(stim_background_circle.lineColor, 'black')
            self.assertEqual(stim_background_circle.fillColor, None)

        active_stim = drawing_list[4]
        self.assertTrue(isinstance(active_stim, pvm.Circle))
        self.assertEqual(active_stim.lineColor, 'black')
        self.assertEqual(active_stim.fillColor, 'blue')
        self.assertEqual(active_stim.radius, experiment.settings.asrt_size)
        self.assertAlmostEqual(active_stim.pos[0], -0.5, delta=0.001)
        self.assertAlmostEqual(active_stim.pos[1], -0.5, delta=0.001)


if __name__ == "__main__":
    unittest.main()  # run all tests
