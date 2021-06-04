# !/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) <2019-2021>  <Tamás Zolnai>  <zolnaitamas2000@gmail.com>

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
import pandas
import numpy
import math
from utils import strToFloat, floatToStr

def computeBinocularDistanceImpl(input):
    data_table = pandas.read_csv(input, sep='\t')

    trial_column = data_table["trial"]
    block_column = data_table["block"]
    left_gaze_validity = data_table["left_gaze_validity"]
    right_gaze_validity = data_table["right_gaze_validity"]
    left_gaze_data_X_PCMCS = data_table["left_gaze_data_X_PCMCS"]
    left_gaze_data_Y_PCMCS = data_table["left_gaze_data_Y_PCMCS"]
    right_gaze_data_X_PCMCS = data_table["right_gaze_data_X_PCMCS"]
    right_gaze_data_Y_PCMCS = data_table["right_gaze_data_Y_PCMCS"]

    all_binocular_distances = []
    for i in range(len(trial_column)):
        if int(block_column[i]) > 0 and int(trial_column[i]) > 2:
            binocular_distance = -1.0
            if bool(left_gaze_validity[i]) and bool(right_gaze_validity[i]):
                left_X = strToFloat(left_gaze_data_X_PCMCS[i])
                left_Y = strToFloat(left_gaze_data_Y_PCMCS[i])
                right_X = strToFloat(right_gaze_data_X_PCMCS[i])
                right_Y = strToFloat(right_gaze_data_Y_PCMCS[i])
                X_distance = abs(left_X - right_X)
                Y_distance = abs(left_Y - right_Y)
                binocular_distance = math.sqrt(pow(X_distance, 2) + pow(Y_distance, 2))
            
            if binocular_distance > 0.0:
                all_binocular_distances.append(binocular_distance)

    return numpy.median(all_binocular_distances)

def computeBinocularDistance(input_dir, output_file):

    median_distances = []
    subjects = []
    for root, dirs, files in os.walk(input_dir):
        for subject in dirs:
            if subject.startswith('.'):
                continue

            print("Compute eye-eye distance data for subject: " + subject)

            subjects.append(subject)
            input_file = os.path.join(root, subject, 'subject_' + subject + '__log.txt')
            result = computeBinocularDistanceImpl(input_file)
            median_distances.append(floatToStr(result))

        break

    binocular_distance_data = pandas.DataFrame({'subject' : subjects, 'median_binocular_distance_mm' : median_distances})
    binocular_distance_data.to_csv(output_file, sep='\t', index=False)