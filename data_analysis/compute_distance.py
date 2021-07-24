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
    epoch_column = data_table["epoch"]
    left_gaze_validity = data_table["left_gaze_validity"]
    right_gaze_validity = data_table["right_gaze_validity"]
    left_eye_distance = data_table["left_eye_distance"]
    right_eye_distance = data_table["right_eye_distance"]
    block_column = data_table["block"]

    epoch_distances = {}
    for i in range(len(trial_column)):
        if int(trial_column[i]) <= 2:
            continue

        if int(block_column[i]) == 0: # calibration validation
            continue

        distance = -1.0
        if bool(left_gaze_validity[i]) and bool(right_gaze_validity[i]):
            distance = (strToFloat(left_eye_distance[i]) + strToFloat(right_eye_distance[i])) / 2.0
        elif bool(left_gaze_validity[i]):
            distance = strToFloat(left_eye_distance[i])
        elif bool(right_gaze_validity[i]):
            distance = strToFloat(right_eye_distance[i])

        if distance > 0.0:
            current_epoch = int(epoch_column[i])
            if current_epoch in epoch_distances.keys():
                epoch_distances[current_epoch].append(distance)
            else:
                epoch_distances[current_epoch] = [distance]

    epoch_summary = numpy.zeros(8).tolist()
    for epoch in epoch_distances.keys():
        epoch_summary[epoch - 1] = floatToStr(numpy.median(epoch_distances[epoch]))

    return epoch_summary

def computeDistanceImplJacobi(input):
    data_table = pandas.read_csv(input, sep='\t')

    trial_column = data_table["trial"]
    left_gaze_validity = data_table["left_gaze_validity"]
    right_gaze_validity = data_table["right_gaze_validity"]
    left_eye_distance = data_table["left_eye_distance"]
    right_eye_distance = data_table["right_eye_distance"]
    test_type_column = data_table["test_type"]

    phase_distances = {}
    for i in range(len(trial_column)):
        if int(trial_column[i]) <= 2:
            continue

        distance = -1.0
        if bool(left_gaze_validity[i]) and bool(right_gaze_validity[i]):
            distance = (strToFloat(left_eye_distance[i]) + strToFloat(right_eye_distance[i])) / 2.0
        elif bool(left_gaze_validity[i]):
            distance = strToFloat(left_eye_distance[i])
        elif bool(right_gaze_validity[i]):
            distance = strToFloat(right_eye_distance[i])

        if distance > 0.0:
            test_type = test_type_column[i]
            if test_type in phase_distances.keys():
                phase_distances[test_type].append(distance)
            else:
                phase_distances[test_type] = [distance]

    return floatToStr(numpy.median(phase_distances["inclusion"])), floatToStr(numpy.median(phase_distances["exclusion"]))

def computeDistance(input_dir, output_file, jacobi = False):
    median_ditances = []
    epochs_phases = []
    for root, dirs, files in os.walk(input_dir):
        for subject in dirs:
            if subject.startswith('.'):
                continue

            if not jacobi:
                print("Compute eye-screen distance data for subject (ASRT): " + subject)
                input_file = os.path.join(root, subject, 'subject_' + subject + '__log.txt')

                for i in range(1,9):
                    epochs_phases.append("subject_" + subject + "_" + str(i))

                epoch_medians = computeDistanceImpl(input_file)
                median_ditances += epoch_medians
            else:
                print("Compute eye-screen distance data for subject (jacobi): " + subject)
                input_file = os.path.join(root, subject, 'subject_' + subject + '__jacobi_ET_log.txt')

                epochs_phases.append("subject_" + subject + "_inclusion")
                epochs_phases.append("subject_" + subject + "_exclusion")

                inclusion_median, exclusion_median = computeDistanceImplJacobi(input_file)
                median_ditances.append(inclusion_median)
                median_ditances.append(exclusion_median)
        break

    if not jacobi:
        distance_data = pandas.DataFrame({'epoch' : epochs_phases, 'median_distance_mm' : median_ditances})
    else:
        distance_data = pandas.DataFrame({'phase' : epochs_phases, 'median_distance_mm' : median_ditances})
    distance_data.to_csv(output_file, sep='\t', index=False)