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

#!\\usr\\bin\\env python
# -*- coding: utf-8 -*-

import asrt
import pyglet
from psychopy import visual, monitors, core
import unittest

import os

import sys
# Add the local path to the main script so we can import it.
sys.path = [".."] + \
    [os.path.join("..", "externals", "psychopy_mock")] + sys.path


class frameRateTest(unittest.TestCase):

    def test60HZFrameRate(self):
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        my_monitor = monitors.Monitor('myMon')
        my_monitor.setSizePix([screen.width, screen.height])
        my_monitor.setWidth(30)
        my_monitor.saveMon()
        with visual.Window(size=(screen.width, screen.height), color='white', monitor=my_monitor, fullscr=False, units="cm") as mywindow:

            frame_time, frame_sd, frame_rate = asrt.frame_check(mywindow)

            self.assertAlmostEqual(
                frame_rate, 60.0, delta=2.0)  # not too stable

            self.assertAlmostEqual(frame_sd, 1.0, delta=1.0)  # in ms

            self.assertAlmostEqual(
                frame_time, 16.67, delta=1.0)  # not too stable

            self.assertAlmostEqual(1000.0 / frame_rate,
                                   frame_time, delta=1.0)  # not too stable

    def testFrameRatePyglet(self):
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        my_monitor = monitors.Monitor('myMon')
        my_monitor.setSizePix([screen.width, screen.height])
        my_monitor.setWidth(30)
        my_monitor.saveMon()
        with visual.Window(size=(screen.width, screen.height), winType="pyglet", color='white', monitor=my_monitor, fullscr=False, units="cm") as mywindow:
            timer = core.Clock()
            for i in range(0, 60):
                mywindow.flip()
            self.assertAlmostEqual(timer.getTime(), 1.0, delta=0.1)

    def testFrameRatePygame(self):
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        my_monitor = monitors.Monitor('myMon')
        my_monitor.setSizePix([screen.width, screen.height])
        my_monitor.setWidth(30)
        my_monitor.saveMon()
        with visual.Window(size=(screen.width, screen.height), winType="pygame", color='white', monitor=my_monitor, fullscr=False, units="cm") as mywindow:

            # does not actually work: MissingFunctionException: wglChoosePixelFormatARB is not exported by the available OpenGL driver
            timer = core.Clock()
            # for i in range(0,60):
            #    mywindow.flip()
            #self.assertAlmostEqual(timer.getTime(), 1.0, delta = 0.1)

    def testFrameRateFullScreen(self):
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        my_monitor = monitors.Monitor('myMon')
        my_monitor.setSizePix([screen.width, screen.height])
        my_monitor.setWidth(30)
        my_monitor.saveMon()
        with visual.Window(size=(screen.width, screen.height), winType="pyglet", color='white', monitor=my_monitor, fullscr=True, units="cm") as mywindow:
            timer = core.Clock()
            for i in range(0, 60):
                mywindow.flip()
            self.assertAlmostEqual(timer.getTime(), 1.0, delta=0.1)

    def testFrameRateNoMouse(self):
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        my_monitor = monitors.Monitor('myMon')
        my_monitor.setSizePix([screen.width, screen.height])
        my_monitor.setWidth(30)
        my_monitor.saveMon()
        with visual.Window(size=(screen.width, screen.height), winType="pyglet", color='white', monitor=my_monitor, fullscr=False, units="cm") as mywindow:
            mywindow.mouseVisible = False
            timer = core.Clock()
            for i in range(0, 60):
                mywindow.flip()
            self.assertAlmostEqual(timer.getTime(), 1.0, delta=0.1)

    def testFrameRatePixUnits(self):
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        my_monitor = monitors.Monitor('myMon')
        my_monitor.setSizePix([screen.width, screen.height])
        my_monitor.saveMon()
        with visual.Window(size=(screen.width, screen.height), winType="pyglet", color='white', monitor=my_monitor, fullscr=False, units="pix") as mywindow:
            mywindow.mouseVisible = False
            timer = core.Clock()
            for i in range(0, 60):
                mywindow.flip()
            self.assertAlmostEqual(timer.getTime(), 1.0, delta=0.1)

    def testFrameRateSmallWindow(self):
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        my_monitor = monitors.Monitor('myMon')
        my_monitor.setSizePix([screen.width / 2, screen.height / 2])
        my_monitor.saveMon()
        with visual.Window(size=(screen.width / 2, screen.height / 2), winType="pyglet", color='white', monitor=my_monitor, fullscr=False, units="pix") as mywindow:
            mywindow.mouseVisible = False
            timer = core.Clock()
            for i in range(0, 60):
                mywindow.flip()
            self.assertAlmostEqual(timer.getTime(), 1.0, delta=0.1)

    def testFrameRateBlackBackground(self):
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        my_monitor = monitors.Monitor('myMon')
        my_monitor.setSizePix([screen.width, screen.height])
        my_monitor.saveMon()
        with visual.Window(size=(screen.width, screen.height), winType="pyglet", color='black', monitor=my_monitor, fullscr=False, units="pix") as mywindow:
            timer = core.Clock()
            for i in range(0, 60):
                mywindow.flip()
            self.assertAlmostEqual(timer.getTime(), 1.0, delta=0.1)

    def testFrameRateNoClearBuffer(self):
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        my_monitor = monitors.Monitor('myMon')
        my_monitor.setSizePix([screen.width, screen.height])
        my_monitor.saveMon()
        with visual.Window(size=(screen.width, screen.height), winType="pyglet", color='white', monitor=my_monitor, fullscr=False, units="pix") as mywindow:
            timer = core.Clock()
            for i in range(0, 60):
                mywindow.flip(False)
            self.assertAlmostEqual(timer.getTime(), 1.0, delta=0.1)


if __name__ == "__main__":
    unittest.main()  # run all tests
