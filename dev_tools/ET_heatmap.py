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
        
    heatmap = numpy.ones((100, 100))

    for line in raw_lines[1:]:
    
        current_trial = line.split('\t')[13]
        stimulus_on_screen = line.split('\t')[22]
        if current_trial == '1' and stimulus_on_screen == 'False':
            continue
    
        left_gaze_XY = (float(line.split('\t')[23].replace(',', '.')), float(line.split('\t')[24].replace(',', '.')))
        left_gaze_valid = line.split('\t')[31]
        right_gaze_XY = (float(line.split('\t')[25].replace(',', '.')), float(line.split('\t')[26].replace(',', '.')))
        right_gaze_valid = line.split('\t')[32]
        x_coord = None
        y_coord = None
        if left_gaze_valid == "1" and right_gaze_valid == "1":
            x_coord = (left_gaze_XY[0] + right_gaze_XY[0]) / 2
            y_coord = (left_gaze_XY[1] + right_gaze_XY[1]) / 2
        elif left_gaze_valid == "1":
            x_coord = left_gaze_XY[0]
            y_coord = left_gaze_XY[1]
        elif right_gaze_valid ==  "1":
            x_coord = right_gaze_XY[0]
            y_coord = right_gaze_XY[1]
        
        if x_coord is not None and y_coord is not None and x_coord < 1.0 and y_coord < 1.0:
            heatmap[int(x_coord * 100)][int(y_coord * 100)] -= 1

    pyplot.imshow(heatmap, cmap='hot')
    pyplot.show()
    pyplot.imshow(heatmap, cmap='hot', vmin=-1000)
    pyplot.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You need to specify the path of an output txt file.")

    if not os.path.isfile(sys.argv[1]):
        print("The passed parameter should be a valid file's path: " + sys.argv[1])

    convert(sys.argv[1])
