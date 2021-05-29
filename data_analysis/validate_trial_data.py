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

def validateTrialData(raw_file_name, trial_file_name):
    RT_upper_limits = calcRTUpperLimits(raw_file_name)
    checkRTOutput(trial_file_name, RT_upper_limits)