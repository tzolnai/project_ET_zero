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
from utils import strToFloat, floatToStr

def computeDistanceImpl(input):
    data_table = pandas.read_csv(input, sep='\t')

    trial_column = data_table["trial"]
    block_column = data_table["block"]
    left_gaze_validity = data_table["left_gaze_validity"]
    right_gaze_validity = data_table["right_gaze_validity"]
    left_eye_distance = data_table["left_eye_distance"]
    right_eye_distance = data_table["right_eye_distance"]

    all_distances = []
    for i in range(len(trial_column)):
        if int(block_column[i]) > 0 and int(trial_column[i]) > 2:
            distance = -1.0
            if bool(left_gaze_validity[i]) and bool(right_gaze_validity[i]):
                distance = (strToFloat(left_eye_distance[i]) + strToFloat(right_eye_distance[i])) / 2.0
            elif bool(left_gaze_validity[i]):
                distance = strToFloat(left_eye_distance[i])
            elif bool(right_gaze_validity[i]):
                distance = strToFloat(right_eye_distance[i])
            
            if distance > 0.0:
                all_distances.append(distance)

    return numpy.median(all_distances)

def computeDistance(input_dir, output_file):

    median_ditances = []
    subjects = []
    for root, dirs, files in os.walk(input_dir):
        for subject in dirs:
            if subject.startswith('.'):
                continue

            print("Compute eye-screen distance data for subject: " + subject)

            subjects.append(subject)
            input_file = os.path.join(root, subject, 'subject_' + subject + '__log.txt')
            result = computeDistanceImpl(input_file)
            median_ditances.append(floatToStr(result))

        break

    distance_data = pandas.DataFrame({'subject' : subjects, 'median_distance_mm' : median_ditances})
    distance_data.to_csv(output_file, sep='\t', index=False)