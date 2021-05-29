# !/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) <2021>  <Tamás Zolnai>  <zolnaitamas2000@gmail.com>

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
import statistics

def calcEpochMinMaxRTsImplicit(input_file):
    input_data_table = pandas.read_csv(input_file, sep='\t')

    RT_column = input_data_table["RT (ms)"]
    repetition_column = input_data_table["repetition"]
    trill_column = input_data_table["trill"]
    epoch_column = input_data_table["epoch"]
    trial_column = input_data_table["trial"]
    trial_type_column = input_data_table["high_low_learning"]

    current_epoch = epoch_column[0]
    high_max = -100000000
    high_min = 100000000
    low_max = -100000000
    low_min = 100000000
    high_max_array = []
    high_min_array = []
    low_max_array = []
    low_min_array = []
    for i in range(len(RT_column) + 1):
        # end of the epoch -> calc median for low and high trials
        if i == len(RT_column) or current_epoch != epoch_column[i]:
            high_max_array.append(high_max)
            high_min_array.append(high_min)
            low_max_array.append(low_max)
            low_min_array.append(low_min)
            high_max = -100000000
            high_min = 100000000
            low_max = -100000000
            low_min = 100000000

            if i == len(RT_column):
                break

            current_epoch = epoch_column[i]

        # we ignore the first two trials, repetitions and trills
        if trial_column[i] > 2 and repetition_column[i] == False and trill_column[i] == False:
            RT = float(RT_column[i].replace(",", "."))
            if trial_type_column[i] == 'high':
                if high_max < RT:
                    high_max = RT
                if high_min > RT:
                    high_min = RT
            elif trial_type_column[i] == 'low':
                if low_max < RT:
                    low_max = RT
                if low_min > RT:
                    low_min = RT

    # 8 epochs
    assert(len(high_max_array) == 8)
    assert(len(high_min_array) == 8)
    assert(len(low_max_array) == 8)
    assert(len(low_min_array) == 8)
    return high_max_array, high_min_array, low_max_array, low_min_array

def checkEpochMedianImplicit(input_file, subject, high_max_array, high_min_array, low_max_array, low_min_array):
    print("Validate implicit learning data for subject: " + str(subject))

    input_data = pandas.read_csv(input_file, sep='\t')

    for index, row in input_data.iterrows():
        if row["subject"] == subject:
            subject_row = row

    for i in range(0,8):
        high_column_label = "epoch_" + str(i + 1) + "_high";
        high_value = subject_row[high_column_label]
        assert(high_value < high_max_array[i])
        assert(high_value > high_min_array[i])

        low_column_label = "epoch_" + str(i + 1) + "_low";
        low_value = subject_row[low_column_label]
        assert(low_value < low_max_array[i])
        assert(low_value > low_min_array[i])

def calcEpochMinMaxRTsSequence(input_file):
    input_data_table = pandas.read_csv(input_file, sep='\t')

    RT_column = input_data_table["RT (ms)"]
    repetition_column = input_data_table["repetition"]
    trill_column = input_data_table["trill"]
    epoch_column = input_data_table["epoch"]
    trial_column = input_data_table["trial"]
    trial_type_hl_column = input_data_table["high_low_learning"]
    trial_type_pr_column = input_data_table["trial_type_pr"]

    current_epoch = epoch_column[0]
    pattern_high_max = -100000000
    pattern_high_min = 100000000
    random_high_max = -100000000
    random_high_min = 100000000
    pattern_high_max_array = []
    pattern_high_min_array = []
    random_high_max_array = []
    random_high_min_array = []
    for i in range(len(RT_column) + 1):
        # end of the epoch -> calc median for low and high trials
        if i == len(RT_column) or current_epoch != epoch_column[i]:
            pattern_high_max_array.append(pattern_high_max)
            pattern_high_min_array.append(pattern_high_min)
            random_high_max_array.append(random_high_max)
            random_high_min_array.append(random_high_min)
            pattern_high_max = -100000000
            pattern_high_min = 100000000
            random_high_max = -100000000
            random_high_min = 100000000

            if i == len(RT_column):
                break

            current_epoch = epoch_column[i]

        if trial_column[i] > 2 and repetition_column[i] == False and trill_column[i] == False and trial_type_hl_column[i] == 'high':
            RT = float(RT_column[i].replace(",", "."))
            if trial_type_pr_column[i] == 'pattern':
                if pattern_high_max < RT:
                    pattern_high_max = RT
                if pattern_high_min > RT:
                    pattern_high_min = RT
            elif trial_type_pr_column[i] == 'random':
                if random_high_max < RT:
                    random_high_max = RT
                if random_high_min > RT:
                    random_high_min = RT

    # 8 epochs
    assert(len(pattern_high_max_array) == 8)
    assert(len(pattern_high_min_array) == 8)
    assert(len(random_high_max_array) == 8)
    assert(len(random_high_min_array) == 8)
    return pattern_high_max_array, pattern_high_min_array, random_high_max_array, random_high_min_array

def checkEpochMedianSequence(input_file, subject, pattern_high_max_array, pattern_high_min_array, random_high_max_array, random_high_min_array):
    print("Validate sequence learning data for subject: " + str(subject))

    input_data = pandas.read_csv(input_file, sep='\t')

    for index, row in input_data.iterrows():
        if row["subject"] == subject:
            subject_row = row

    for i in [1, 2, 3, 4, 5, 7]:
        pattern_high_column_label = "epoch_" + str(i + 1) + "_pattern_high";
        pattern_high_value = subject_row[pattern_high_column_label]
        assert(pattern_high_value < pattern_high_max_array[i])
        assert(pattern_high_value > pattern_high_min_array[i])

        random_high_column_label = "epoch_" + str(i + 1) + "_random_high";
        random_high_value = subject_row[random_high_column_label]
        assert(random_high_value < random_high_max_array[i])
        assert(random_high_value > random_high_min_array[i])

def calcEpochMinMaxRTsStatistical(input_file):
    input_data_table = pandas.read_csv(input_file, sep='\t')

    RT_column = input_data_table["RT (ms)"]
    repetition_column = input_data_table["repetition"]
    trill_column = input_data_table["trill"]
    epoch_column = input_data_table["epoch"]
    trial_column = input_data_table["trial"]
    trial_type_hl_column = input_data_table["high_low_learning"]
    trial_type_pr_column = input_data_table["trial_type_pr"]

    current_epoch = epoch_column[0]
    random_high_max = -100000000
    random_high_min = 100000000
    random_low_max = -100000000
    random_low_min = 100000000
    random_high_max_array = []
    random_high_min_array = []
    random_low_max_array = []
    random_low_min_array = []
    for i in range(len(RT_column) + 1):
        # end of the epoch -> calc median for low and high trials
        if i == len(RT_column) or current_epoch != epoch_column[i]:
            random_high_max_array.append(random_high_max)
            random_high_min_array.append(random_high_min)
            random_low_max_array.append(random_low_max)
            random_low_min_array.append(random_low_min)
            random_high_max = -100000000
            random_high_min = 100000000
            random_low_max = -100000000
            random_low_min = 100000000

            if i == len(RT_column):
                break

            current_epoch = epoch_column[i]

        if trial_column[i] > 2 and repetition_column[i] == False and trill_column[i] == False and trial_type_pr_column[i] == 'random':
            RT = float(RT_column[i].replace(",", "."))
            if trial_type_hl_column[i] == 'high':
                if random_high_max < RT:
                    random_high_max = RT
                if random_high_min > RT:
                    random_high_min = RT
            elif trial_type_hl_column[i] == 'low':
                if random_low_max < RT:
                    random_low_max = RT
                if random_low_min > RT:
                    random_low_min = RT

    # 8 epochs
    assert(len(random_high_max_array) == 8)
    assert(len(random_high_min_array) == 8)
    assert(len(random_low_max_array) == 8)
    assert(len(random_low_min_array) == 8)
    return random_high_max_array, random_high_min_array, random_low_max_array, random_low_min_array

def checkEpochMedianStatistical(input_file, subject, random_high_max_array, random_high_min_array, random_low_max_array, random_low_min_array):
    print("Validate statistical learning data for subject: " + str(subject))

    input_data = pandas.read_csv(input_file, sep='\t')

    for index, row in input_data.iterrows():
        if row["subject"] == subject:
            subject_row = row

    for i in [1, 2, 3, 4, 5, 7]:
        random_high_column_label = "epoch_" + str(i + 1) + "_random_high";
        random_high_value = subject_row[random_high_column_label]
        assert(random_high_value < random_high_max_array[i])
        assert(random_high_value > random_high_min_array[i])

        random_low_column_label = "epoch_" + str(i + 1) + "_random_low";
        random_low_value = subject_row[random_low_column_label]
        assert(random_low_value < random_low_max_array[i])
        assert(random_low_value > random_low_min_array[i])

def validateLearning(input_dir, output_file, type):
    for root, dirs, files in os.walk(input_dir):
        for file in files:

            input_file = os.path.join(input_dir, file)
            subject = int(file.split('_')[1])

            if type == 'implicit':
                high_max_array, high_min_array, low_max_array, low_min_array = calcEpochMinMaxRTsImplicit(input_file)
                checkEpochMedianImplicit(output_file, subject, high_max_array, high_min_array, low_max_array, low_min_array)
            elif type == 'sequence':
                pattern_high_max_array, pattern_high_min_array, random_high_max_array, random_high_min_array = calcEpochMinMaxRTsSequence(input_file)
                checkEpochMedianSequence(output_file, subject, pattern_high_max_array, pattern_high_min_array, random_high_max_array, random_high_min_array)
            elif type == 'statistical':
                random_high_max_array, random_high_min_array, random_low_max_array, random_low_min_array = calcEpochMinMaxRTsStatistical(input_file)
                checkEpochMedianStatistical(output_file, subject, random_high_max_array, random_high_min_array, random_low_max_array, random_low_min_array)
        break

def validateImplicitLearning(input_dir, output_file):
    validateLearning(input_dir, output_file, 'implicit')

def validateSequenceLearning(input_dir, output_file):
    validateLearning(input_dir, output_file, 'sequence')

def validateStatisticalLearning(input_dir, output_file):
    validateLearning(input_dir, output_file, 'statistical')
