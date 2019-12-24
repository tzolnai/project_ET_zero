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
from psychopy import visual, monitors, core
import pyglet
import asrt
import psychopy_visual_mock as pvm


class frameCheckTest(unittest.TestCase):

    def testFrameRate(self):
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        my_monitor = monitors.Monitor('myMon')
        my_monitor.setSizePix([screen.width, screen.height])
        my_monitor.setWidth(30)
        my_monitor.saveMon()
        experiment = asrt.Experiment("")

        with visual.Window(size=(screen.width, screen.height), color='white', monitor=my_monitor, fullscr=False,
                           units="cm", gammaRamp=256, gammaErrorPolicy='ignore') as experiment.mywindow:
            experiment.mywindow.getMsPerFrame = lambda nFrames: (16.67, 1.0)
            experiment.mywindow.getActualFrameRate = lambda: 60.0

            visual_mock = pvm.PsychoPyVisualMock()
            experiment.frame_check()

            self.assertAlmostEqual(experiment.frame_rate, 60.0, delta=0.0001)
            self.assertAlmostEqual(experiment.frame_sd, 1.0, delta=0.0001)
            self.assertAlmostEqual(experiment.frame_time, 16.67, delta=0.0001)

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 1)

            self.assertEqual(
                drawing_list[0].text, "Adatok előkészítése folyamatban.\n\nEz eltarthat pár másodpercig.\n\nAddig semmit sem fogsz látni a képernyőn...")


if __name__ == "__main__":
    unittest.main()  # run all tests
