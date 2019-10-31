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

import os
import shelve
import sys
import codecs
import numpy
import matplotlib.pyplot as pyplot


def convert(raw_file_name):

    with codecs.open(raw_file_name, 'r', encoding='utf-8') as raw_output_file:
        raw_lines = raw_output_file.readlines()

    if len(raw_lines) == 0:
        print("There is no data in the given output txt file.")

    heatmap_global = numpy.zeros((100, 100))
    heatmap_epoch = numpy.zeros((100, 100))

    trial_pos = raw_lines[0].split('\t').index("trial")
    stim_on_screen_pos = raw_lines[0].split('\t').index("stimulus_on_screen")
    epoch_pos = raw_lines[0].split('\t').index("epoch")

    try:
        left_gazeX_pos = raw_lines[0].split('\t').index("left_gaze_data_X_ADCS")
        left_gazeY_pos = raw_lines[0].split('\t').index("left_gaze_data_Y_ADCS")
        right_gazeX_pos = raw_lines[0].split('\t').index("right_gaze_data_X_ADCS")
        right_gazeY_pos = raw_lines[0].split('\t').index("right_gaze_data_Y_ADCS")
    except ValueError:  # backward compatibility
        left_gazeX_pos = raw_lines[0].split('\t').index("left_gaze_data_X")
        left_gazeY_pos = raw_lines[0].split('\t').index("left_gaze_data_Y")
        right_gazeX_pos = raw_lines[0].split('\t').index("right_gaze_data_X")
        right_gazeY_pos = raw_lines[0].split('\t').index("right_gaze_data_Y")

    left_gaze_valid_pos = raw_lines[0].split('\t').index("left_gaze_validity")
    right_gaze_valid_pos = raw_lines[0].split('\t').index("right_gaze_validity")

    last_epoch = "1"
    for line in raw_lines[1:]:
        current_trial = line.split('\t')[trial_pos]
        stimulus_on_screen = line.split('\t')[stim_on_screen_pos]
        epoch_number = line.split('\t')[epoch_pos]

        if current_trial == '1':
            continue

        if epoch_number != last_epoch:
            pyplot.figure("epoch " + last_epoch)
            pyplot.imshow(heatmap_epoch, cmap='hot')
            heatmap_epoch = numpy.zeros((100, 100))
            last_epoch = epoch_number

        left_gaze_XY = (float(line.split('\t')[left_gazeX_pos].replace(',', '.')), float(line.split('\t')[left_gazeY_pos].replace(',', '.')))
        left_gaze_valid = line.split('\t')[left_gaze_valid_pos]
        right_gaze_XY = (float(line.split('\t')[right_gazeX_pos].replace(',', '.')), float(line.split('\t')[right_gazeY_pos].replace(',', '.')))
        right_gaze_valid = line.split('\t')[right_gaze_valid_pos]
        x_coord = None
        y_coord = None
        if left_gaze_valid == "1" and right_gaze_valid == "1":
            x_coord = (left_gaze_XY[0] + right_gaze_XY[0]) / 2
            y_coord = (left_gaze_XY[1] + right_gaze_XY[1]) / 2
        elif left_gaze_valid == "1":
            x_coord = left_gaze_XY[0]
            y_coord = left_gaze_XY[1]
        elif right_gaze_valid == "1":
            x_coord = right_gaze_XY[0]
            y_coord = right_gaze_XY[1]

        if x_coord is not None and y_coord is not None and x_coord < 1.0 and y_coord < 1.0:
            heatmap_global[int(x_coord * 100)][int(y_coord * 100)] -= 1
            heatmap_epoch[int(x_coord * 100)][int(y_coord * 100)] -= 1

    pyplot.figure("epoch " + last_epoch)
    pyplot.imshow(heatmap_epoch, cmap='hot')

    data_count = abs(heatmap_global.sum(axis=0).sum())
    pyplot.figure("global")
    pyplot.imshow(heatmap_global, cmap='hot')
    pyplot.figure("global_limited")
    pyplot.imshow(heatmap_global, cmap='hot', vmin=-(data_count / 200.0))
    pyplot.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You need to specify the path of an output txt file.")

    if not os.path.isfile(sys.argv[1]):
        print("The passed parameter should be a valid file's path: " + sys.argv[1])

    convert(sys.argv[1])
