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
from utils import strToFloat, floatToStr

def computeMinMaxOneSubject(input_file):
    input_data_table = pandas.read_csv(input_file, sep='\t')

    RT_column = input_data_table["RT (ms)"]
    repetition_column = input_data_table["repetition"]
    trill_column = input_data_table["trill"]
    epoch_column = input_data_table["epoch"]
    block_column = input_data_table["block"]
    trial_column = input_data_table["trial"]
    trial_type_column = input_data_table["high_low_learning"]
    trial_type_interfer_column = input_data_table["triplet_type_hl"]

    high_low_max = -100000000
    high_low_min = 100000000
    low_low_max = -100000000
    low_low_min = 100000000
    low_high_max = -100000000
    low_high_min = 100000000
    for i in range(len(RT_column)):

        # we ignore the first two trials, repetitions and trills
        if (epoch_column[i] == 7 and trial_column[i] > 2
           and repetition_column[i] == False and trill_column[i] == False):
            RT = strToFloat(RT_column[i])
            if trial_type_column[i] == 'high' and trial_type_interfer_column[i] == 'low':
                if high_low_max < RT:
                    high_low_max = RT
                if high_low_min > RT:
                    high_low_min = RT
            elif trial_type_column[i] == 'low' and trial_type_interfer_column[i] == 'low':
                if low_low_max < RT:
                    low_low_max = RT
                if low_low_min > RT:
                    low_low_min = RT
            elif trial_type_column[i] == 'low' and trial_type_interfer_column[i] == 'high':
                if low_high_max < RT:
                    low_high_max = RT
                if low_high_min > RT:
                    low_high_min = RT

    return high_low_max, high_low_min, low_low_max, low_low_min, low_high_max, low_high_min

def checkEpochMedian(input_file, subject, high_low_max, high_low_min, low_low_max, low_low_min, low_high_max, low_high_min):
    print("Validate interference RTs for subject: " + str(subject))

    input_data = pandas.read_csv(input_file, sep='\t')

    for index, row in input_data.iterrows():
        if row["subject"] == subject:
            subject_row = row

    high_low_value = strToFloat(subject_row["epoch_7_high_low"])
    assert(high_low_value < high_low_max)
    assert(high_low_value > high_low_min)

    low_low_value = strToFloat(subject_row['epoch_7_low_low'])
    assert(low_low_value < low_low_max)
    assert(low_low_value > low_low_min)

    low_high_value = strToFloat(subject_row['epoch_7_low_high'])
    assert(low_high_value < low_high_max)
    assert(low_high_value > low_high_min)

def validateInterferenceData(input_dir, output_file):
    for root, dirs, files in os.walk(input_dir):
        for file in files:

            input_file = os.path.join(input_dir, file)
            subject = int(file.split('_')[1])

            high_low_max, high_low_min, low_low_max, low_low_min, low_high_max, low_high_min = computeMinMaxOneSubject(input_file)
            checkEpochMedian(output_file, subject, high_low_max, high_low_min, low_low_max, low_low_min, low_high_max, low_high_min)
        break
