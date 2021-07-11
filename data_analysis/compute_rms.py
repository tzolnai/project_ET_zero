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
from utils import strToFloat, floatToStr, calcRMS, convertToAngle

def getPos(data_table, i):
    left_gaze_validity = data_table["left_gaze_validity"][i]
    right_gaze_validity = data_table["right_gaze_validity"][i]
    left_gaze_data_X_PCMCS = data_table["left_gaze_data_X_PCMCS"][i]
    left_gaze_data_Y_PCMCS = data_table["left_gaze_data_Y_PCMCS"][i]
    right_gaze_data_X_PCMCS = data_table["right_gaze_data_X_PCMCS"][i]
    right_gaze_data_Y_PCMCS = data_table["right_gaze_data_Y_PCMCS"][i]

    if bool(left_gaze_validity) and bool(right_gaze_validity):
        pos_X = (strToFloat(left_gaze_data_X_PCMCS) + strToFloat(right_gaze_data_X_PCMCS)) / 2.0
        pos_Y = (strToFloat(left_gaze_data_Y_PCMCS) + strToFloat(right_gaze_data_Y_PCMCS)) / 2.0
    elif bool(left_gaze_validity):
        pos_X = strToFloat(left_gaze_data_X_PCMCS)
        pos_Y = strToFloat(left_gaze_data_Y_PCMCS)
    elif bool(right_gaze_validity):
        pos_X = strToFloat(right_gaze_data_X_PCMCS)
        pos_Y = strToFloat(right_gaze_data_Y_PCMCS)
    else:
        return 0

    return (pos_X, pos_Y)

def clacDistancesForFixation(j, k, data_table):

    all_distances = []
    for i in range(j, k):
        prev_pos = getPos(data_table, i)
        next_pos = getPos(data_table, i + 1)
        if prev_pos != 0 and next_pos != 0:
            distance = math.sqrt(pow(prev_pos[0] - next_pos[0], 2) + pow(prev_pos[1] - next_pos[1], 2))
            all_distances.append(convertToAngle(distance))
    
    return all_distances

def computeRMSImpl(input):
    data_table = pandas.read_csv(input, sep='\t')

    trial_column = data_table["trial"]
    block_column = data_table["block"]
    epoch_column = data_table["epoch"]

    epoch_rmss = {}
    for i in range(len(trial_column) - 1):
        if int(block_column[i]) > 0 and int(trial_column[i]) > 2:

            if trial_column[i] != trial_column[i + 1]: # end of trial -> 100 ms fixation
                all_distances = clacDistancesForFixation(i - 11, i, data_table)
                if len(all_distances) > 0:
                    current_epoch = int(epoch_column[i])
                    new_RMS = calcRMS(all_distances)
                    if current_epoch in epoch_rmss.keys():
                        epoch_rmss[current_epoch].append(new_RMS)
                    else:
                        epoch_rmss[current_epoch] = [new_RMS]

    epoch_summary = numpy.zeros(8).tolist()
    for epoch in epoch_rmss.keys():
        epoch_summary[epoch - 1] = floatToStr(numpy.median(epoch_rmss[epoch]))

    return epoch_summary

def computeRMSJacobiImpl(input):
    data_table = pandas.read_csv(input, sep='\t')

    trial_column = data_table["trial"]
    trial_phase_column = data_table["trial_phase"]
    test_type_column = data_table["test_type"]
    run_column = data_table["run"]

    run_rmss = {}
    for i in range(len(trial_column) - 1):
        if int(trial_column[i]) > 2:

            if (trial_phase_column[i] == "before_reaction" and
                trial_phase_column[i + 1] == "after_reaction"): # end of fixation (100ms)
                all_distances = clacDistancesForFixation(i - 11, i, data_table)
                if len(all_distances) > 0:
                    current_run = int(run_column[i])
                    if test_type_column[i] == "exclusion":
                        current_run += 4
                    new_RMS = calcRMS(all_distances)
                    if current_run in run_rmss.keys():
                        run_rmss[current_run].append(new_RMS)
                    else:
                        run_rmss[current_run] = [new_RMS]

    run_summary = numpy.zeros(8).tolist()
    for run in run_rmss.keys():
        run_summary[run - 1] = floatToStr(numpy.median(run_rmss[run]))

    return run_summary

def computeRMS(input_dir, output_file, jacobi = False):

    rmss = []
    epochs_runs = []
    for root, dirs, files in os.walk(input_dir):
        for subject in dirs:
            if subject.startswith('.'):
                continue

            if not jacobi:
                print("Compute RMS for subject(ASRT): " + subject)
                input_file = os.path.join(root, subject, 'subject_' + subject + '__log.txt')
            else:
                print("Compute RMS for subject(jacobi): " + subject)
                input_file = os.path.join(root, subject, 'subject_' + subject + '__jacobi_ET_log.txt')

            for i in range(1,9):
                epochs_runs.append("subject_" + subject + "_" + str(i))

            if not jacobi:
                RMS = computeRMSImpl(input_file)
            else:
                RMS = computeRMSJacobiImpl(input_file)
            rmss += RMS

        break

    if not jacobi:
        distance_data = pandas.DataFrame({'epoch' : epochs_runs, 'RMS(S2S)_median' : rmss})
    else:
        distance_data = pandas.DataFrame({'run' : epochs_runs, 'RMS(S2S)_median' : rmss})
    distance_data.to_csv(output_file, sep='\t', index=False)