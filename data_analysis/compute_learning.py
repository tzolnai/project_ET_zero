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
import statistics

def calcEpochMedianRTsImplicit(input_file):
    input_data_table = pandas.read_csv(input_file, sep='\t')

    RT_column = input_data_table["RT (ms)"]
    repetition_column = input_data_table["repetition"]
    trill_column = input_data_table["trill"]
    epoch_column = input_data_table["epoch"]
    trial_column = input_data_table["trial"]
    trial_type_column = input_data_table["high_low_learning"]

    current_epoch = epoch_column[0]
    high_RT_list = []
    low_RT_list = []
    high_median_array = []
    low_median_array = []
    for i in range(len(RT_column) + 1):
        # end of the epoch -> calc median for low and high trials
        if i == len(RT_column) or current_epoch != epoch_column[i]:
            assert(len(high_RT_list) > 0)
            high_median_array.append(statistics.median(high_RT_list))
            high_RT_list = []

            assert(len(low_RT_list) > 0)
            low_median_array.append(statistics.median(low_RT_list))
            low_RT_list = []

            if i == len(RT_column):
                break

            current_epoch = epoch_column[i]

        # we ignore the first two trials, repetitions and trills
        if trial_column[i] > 2 and repetition_column[i] == False and trill_column[i] == False:
            if trial_type_column[i] == 'high':
                high_RT_list.append(float(RT_column[i].replace(",", ".")))
            elif trial_type_column[i] == 'low':
                low_RT_list.append(float(RT_column[i].replace(",", ".")))

    # 8 epochs
    assert(len(low_median_array) == 8)
    assert(len(high_median_array) == 8)
    return low_median_array, high_median_array

def calcEpochMedianRTsSequence(input_file):
    input_data_table = pandas.read_csv(input_file, sep='\t')

    RT_column = input_data_table["RT (ms)"]
    repetition_column = input_data_table["repetition"]
    trill_column = input_data_table["trill"]
    epoch_column = input_data_table["epoch"]
    trial_column = input_data_table["trial"]
    trial_type_hl_column = input_data_table["high_low_learning"]
    trial_type_pr_column = input_data_table["trial_type_pr"]

    current_epoch = epoch_column[0]
    patter_high_RT_list = []
    random_high_RT_list = []
    pattern_high_median_array = []
    random_high_median_array = []
    for i in range(len(RT_column) + 1):
        # end of the epoch -> calc median for low and high trials
        if i == len(RT_column) or current_epoch != epoch_column[i]:
            if current_epoch == 1 or current_epoch == 7:
                patter_high_RT_list = []
                random_high_RT_list = []
                pattern_high_median_array.append(0)
                random_high_median_array.append(0)
            else:
                assert(len(patter_high_RT_list) > 0)
                pattern_high_median_array.append(statistics.median(patter_high_RT_list))
                patter_high_RT_list = []

                assert(len(random_high_RT_list) > 0)
                random_high_median_array.append(statistics.median(random_high_RT_list))
                random_high_RT_list = []

            if i == len(RT_column):
                break

            current_epoch = epoch_column[i]

        # we ignore the first two trials, repetitions and trills
        if trial_column[i] > 2 and repetition_column[i] == False and trill_column[i] == False and trial_type_hl_column[i] == 'high':
            if trial_type_pr_column[i] == 'pattern':
                patter_high_RT_list.append(float(RT_column[i].replace(",", ".")))
            elif trial_type_pr_column[i] == 'random':
                random_high_RT_list.append(float(RT_column[i].replace(",", ".")))

    # 8 epochs
    assert(len(pattern_high_median_array) == 8)
    assert(len(random_high_median_array) == 8)
    return pattern_high_median_array, random_high_median_array

def calcEpochMedianRTsStatistical(input_file):
    input_data_table = pandas.read_csv(input_file, sep='\t')

    RT_column = input_data_table["RT (ms)"]
    repetition_column = input_data_table["repetition"]
    trill_column = input_data_table["trill"]
    epoch_column = input_data_table["epoch"]
    trial_column = input_data_table["trial"]
    trial_type_hl_column = input_data_table["high_low_learning"]
    trial_type_pr_column = input_data_table["trial_type_pr"]

    current_epoch = epoch_column[0]
    random_high_RT_list = []
    random_low_RT_list = []
    random_high_median_array = []
    random_low_median_array = []
    for i in range(len(RT_column) + 1):
        # end of the epoch -> calc median for low and high trials
        if i == len(RT_column) or current_epoch != epoch_column[i]:
            if current_epoch == 1 or current_epoch == 7:
                random_low_RT_list = []
                random_high_RT_list = []
                random_high_median_array.append(0)
                random_low_median_array.append(0)
            else:
                assert(len(random_high_RT_list) > 0)
                random_high_median_array.append(statistics.median(random_high_RT_list))
                random_high_RT_list = []

                assert(len(random_low_RT_list) > 0)
                random_low_median_array.append(statistics.median(random_low_RT_list))
                random_low_RT_list = []

            if i == len(RT_column):
                break

            current_epoch = epoch_column[i]

        # we ignore the first two trials, repetitions and trills
        if trial_column[i] > 2 and repetition_column[i] == False and trill_column[i] == False and trial_type_pr_column[i] == 'random':
            if trial_type_hl_column[i] == 'high':
                random_high_RT_list.append(float(RT_column[i].replace(",", ".")))
            elif trial_type_hl_column[i] == 'low':
                random_low_RT_list.append(float(RT_column[i].replace(",", ".")))

    # 8 epochs
    assert(len(random_high_median_array) == 8)
    assert(len(random_low_median_array) == 8)
    return random_high_median_array, random_low_median_array

def computeLearning(input_dir, output_file, type):
    if type == 'implicit':
        learning_data = pandas.DataFrame(columns=['subject', 'epoch_1_low', 'epoch_2_low', 'epoch_3_low', 'epoch_4_low',
                                         'epoch_5_low', 'epoch_6_low', 'epoch_7_low', 'epoch_8_low',
                                         'epoch_1_high', 'epoch_2_high', 'epoch_3_high', 'epoch_4_high',
                                         'epoch_5_high', 'epoch_6_high', 'epoch_7_high', 'epoch_8_high'])
    elif type == 'sequence':
        learning_data = pandas.DataFrame(columns=['subject', 'epoch_1_pattern_high', 'epoch_2_pattern_high', 'epoch_3_pattern_high', 'epoch_4_pattern_high',
                                         'epoch_5_pattern_high', 'epoch_6_pattern_high', 'epoch_7_pattern_high', 'epoch_8_pattern_high',
                                         'epoch_1_random_high', 'epoch_2_random_high', 'epoch_3_random_high', 'epoch_4_random_high',
                                         'epoch_5_random_high', 'epoch_6_random_high', 'epoch_7_random_high', 'epoch_8_random_high'])
    elif type == 'statistical':
        learning_data = pandas.DataFrame(columns=['subject', 'epoch_1_random_high', 'epoch_2_random_high', 'epoch_3_random_high', 'epoch_4_random_high',
                                         'epoch_5_random_high', 'epoch_6_random_high', 'epoch_7_random_high', 'epoch_8_random_high',
                                         'epoch_1_random_low', 'epoch_2_random_low', 'epoch_3_random_low', 'epoch_4_random_low',
                                         'epoch_5_random_low', 'epoch_6_random_low', 'epoch_7_random_low', 'epoch_8_random_low'])

    for root, dirs, files in os.walk(input_dir):
        for file in files:

            input_file = os.path.join(input_dir, file)
            subject = int(file.split('_')[1])

            if type == 'implicit':
                low_medians, high_medians = calcEpochMedianRTsImplicit(input_file)
                learning_data.loc[len(learning_data)] = [subject] + low_medians + high_medians
            elif type == 'sequence':
                pattern_high_medians, random_high_medians = calcEpochMedianRTsSequence(input_file)
                learning_data.loc[len(learning_data)] = [subject] + pattern_high_medians + random_high_medians
            elif type == 'statistical':
                random_high_medians, random_low_medians = calcEpochMedianRTsStatistical(input_file)
                learning_data.loc[len(learning_data)] = [subject] + random_high_medians + random_low_medians
        break

    learning_data.to_csv(output_file, sep='\t', index=False)

def computeImplicitLearning(input_dir, output_file):
    computeLearning(input_dir, output_file, 'implicit')

def computeSequenceLearning(input_dir, output_file):
    computeLearning(input_dir, output_file, 'sequence')

def computeStatisticalLearning(input_dir, output_file):
    computeLearning(input_dir, output_file, 'statistical')
