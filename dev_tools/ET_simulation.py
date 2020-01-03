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
# Add the local path to the asrt script
sys.path = [".."] + sys.path

import asrt
import tobii_research as tobii
import os

import time
from pynput import mouse

gaze_data_callback = None

g_counter = 0


class EyeTrackerMock:
    def subscribe_to(self, subscription_type, callback, as_dictionary=False):
        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = 1
        gazeData['right_pupil_validity'] = 1
        callback(gazeData)
        global gaze_data_callback
        gaze_data_callback = callback

    def unsubscribe_from(self, subscription_type, callback=None):
        global gaze_data_callback
        gaze_data_callback = None


def find_all_eyetrackers_mock():
    return [EyeTrackerMock()]


def get_system_time_stamp_mock():
    return 1000000


tobii.find_all_eyetrackers = find_all_eyetrackers_mock
tobii.get_system_time_stamp = get_system_time_stamp_mock


def on_move(x, y):
    global g_counter
    for i in range(0, 4):
        if gaze_data_callback is not None:
            g_counter += 1
            xCoord = (x / 1366)
            yCoord = (y / 768)
            gazeData = {}
            if g_counter % 10 != 0:
                gazeData['left_gaze_point_on_display_area'] = (xCoord + 0.02, yCoord)
                gazeData['right_gaze_point_on_display_area'] = (xCoord - 0.02, yCoord)
                gazeData['left_gaze_point_validity'] = 1
                gazeData['right_gaze_point_validity'] = 1
            elif g_counter / 10 == 1:
                gazeData['left_gaze_point_on_display_area'] = (xCoord + 0.02, yCoord)
                gazeData['right_gaze_point_on_display_area'] = (float('nan'), float('nan'))
                gazeData['left_gaze_point_validity'] = 1
                gazeData['right_gaze_point_validity'] = 0
            else:
                gazeData['left_gaze_point_on_display_area'] = (float('nan'), float('nan'))
                gazeData['right_gaze_point_on_display_area'] = (xCoord - 0.02, yCoord)
                gazeData['left_gaze_point_validity'] = 0
                gazeData['right_gaze_point_validity'] = 1

            gazeData['left_pupil_diameter'] = 3
            gazeData['right_pupil_diameter'] = 3
            gazeData['left_pupil_validity'] = 1
            gazeData['right_pupil_validity'] = 1
            gaze_data_callback(gazeData)


if __name__ == "__main__":
    with mouse.Listener(on_move=on_move) as listener:
        thispath = os.path.split(os.path.abspath(__file__))[0]
        thispath = os.path.split(thispath)[0]
        experiment = asrt.Experiment(thispath)
        experiment.run(False, True)
