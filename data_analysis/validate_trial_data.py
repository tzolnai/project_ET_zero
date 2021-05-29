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
import sys
import pandas
import math

def convertToFloat(data):
    return float(str(data).replace(",", "."))

def checkRTOutput(trial_file_name, RT_upper_limits):
    trial_data = pandas.read_csv(trial_file_name, sep='\t')

    assert(len(trial_data.index) == len(RT_upper_limits))

    for index, row in trial_data.iterrows():
        actual_RT = convertToFloat(row["RT (ms)"])
        assert(actual_RT < (RT_upper_limits[index] - 350.0))

def calcRTUpperLimits(raw_file_name):
    input_data = pandas.read_csv(raw_file_name, sep='\t')

    last_trial = "1"
    start_time = 0
    start_time_set = False
    RT_data = []
    previous_row = -1

    for index, row in input_data.iterrows():
        if not start_time_set and str(row['trial']) == "1" and str(row['block']) == "1":
            start_time_set = True
            start_time = int(row['gaze_data_time_stamp'])

        # we are at the end of the trial (actually at the first row of the next trial)
        if last_trial != str(row['trial']) or index == len(input_data.index) - 1:
            if isinstance(previous_row, pandas.Series) and str(previous_row['block']) != "0": # validation blocks
                end_time = int(previous_row['gaze_data_time_stamp'])
                RT_data.append((end_time - start_time) / 1000.0)

                last_trial = str(row['trial'])
                start_time = int(row['gaze_data_time_stamp'])

        previous_row = row

    assert(len(RT_data) == 3280)
    return RT_data

def getAOI(row):
    left_gaze_validity = bool(row['left_gaze_validity'])
    right_gaze_validity = bool(row['right_gaze_validity'])

    left_gaze_X = convertToFloat(row['left_gaze_data_X_ADCS'])
    left_gaze_Y = convertToFloat(row['left_gaze_data_Y_ADCS'])
    right_gaze_X = convertToFloat(row['right_gaze_data_X_ADCS'])
    right_gaze_Y = convertToFloat(row['right_gaze_data_Y_ADCS'])

    if left_gaze_validity and right_gaze_validity:
        X = (left_gaze_X + right_gaze_X) / 2.0
        Y = (left_gaze_Y + right_gaze_Y) / 2.0
    elif left_gaze_validity:
        X = left_gaze_X
        Y = left_gaze_Y
    elif right_gaze_validity:
        X = right_gaze_X
        Y = right_gaze_Y
    else:
        return [-1, -1, -1]

    if X <= 0.5 and Y <= 0.5:
        return [1, X, Y]
    elif X >= 0.5 and Y <= 0.5:
        return [2, X, Y]
    elif X <= 0.5 and Y >= 0.5:
        return [3, X, Y]
    else:
        return [4, X, Y]

def calcLastAOIGuess(raw_file_name):
    input_data = pandas.read_csv(raw_file_name, sep='\t')

    last_trial = "1"
    last_ROI_data = []
    last_ROI_trio = [-1, -1, -1]
    previous_row = -1
    last_ROI_found = False

    for index, row in input_data.iterrows():
        if str(row['block']) == "0": # validation blocks
            previous_row = row
            continue

        if not last_ROI_found:
            if row['trial_phase'] != 'before_stimulus':
                if str(row['trial']) in ["1", "2"]:
                    last_ROI_found = True
                    last_ROI_trio = [-1, -1, -1]
                else:
                    last_ROI_found = True
                    prev_AOI = getAOI(previous_row)
                    current_AOI = getAOI(row)
                    last_ROI_trio = [prev_AOI[0], current_AOI[1], current_AOI[2]]

        # we are at the end of the trial (actually at the first row of the next trial)
        if last_trial != str(row['trial']) or index == len(input_data.index) - 1:
            if isinstance(previous_row, pandas.Series):
                if last_ROI_found:
                    last_ROI_data.append(last_ROI_trio)
                else:
                    last_ROI_data.append([-1, -1, -1])
                last_trial = str(row['trial'])
                last_ROI_found = False

        previous_row = row

    assert(len(last_ROI_data) == 3280)
    return last_ROI_data

def checkAOIOutput(trial_file_name, last_AOIs):
    trial_data = pandas.read_csv(trial_file_name, sep='\t')

    assert(len(trial_data.index) == len(last_AOIs))

    checked_items = 0
    failed_items = 0
    for index, row in trial_data.iterrows():
        actual_last_AOI = row["last_AOI_before_stimulus"]
        if str(row["trial"]) in ["1", "2"]:
            assert(actual_last_AOI == "none")
            checked_items += 1
        elif last_AOIs[index][0] != -1:
            if actual_last_AOI != str(last_AOIs[index][0]):
                assert(abs(last_AOIs[index][1] - 0.5) < 0.05 or
                       abs(last_AOIs[index][2] - 0.5) < 0.05 ) # close to AOI boundaries
            checked_items += 1

    print("Last AOI validation. Validated items: " + str(checked_items))

def checkAOIForNullRTs(trial_file_name):
    trial_data = pandas.read_csv(trial_file_name, sep='\t')

    checked_items = 0
    for index, row in trial_data.iterrows():
        actual_last_AOI = row["last_AOI_before_stimulus"]
        if str(row["trial"]) in ["1", "2"]:
            assert(actual_last_AOI == "none")
            checked_items += 1
        elif str(row["RT (ms)"]) == "0":
            checked_items += 1
            assert(str(row["stimulus"]) == actual_last_AOI)

    print("Last AOI validation for 0 RTs. Validated items: " + str(checked_items))

def validateTrialData(raw_file_name, trial_file_name):
    RT_upper_limits = calcRTUpperLimits(raw_file_name)
    checkRTOutput(trial_file_name, RT_upper_limits)

    last_AOIs = calcLastAOIGuess(raw_file_name)
    checkAOIOutput(trial_file_name, last_AOIs)
    checkAOIForNullRTs(trial_file_name)