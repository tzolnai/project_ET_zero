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

def computeInterferenceOneSubject(input_file):
    input_data_table = pandas.read_csv(input_file, sep='\t')

    RT_column = input_data_table["RT (ms)"]
    repetition_column = input_data_table["repetition"]
    trill_column = input_data_table["trill"]
    epoch_column = input_data_table["epoch"]
    block_column = input_data_table["block"]
    trial_column = input_data_table["trial"]
    trial_type_column = input_data_table["high_low_learning"]
    trial_type_interfer_column = input_data_table["triplet_type_hl"]

    high_low_list = []
    low_low_list = []
    low_high_list = []
    for i in range(len(RT_column)):

        # we ignore the first two trials, repetitions and trills
        if (epoch_column[i] == 7 and trial_column[i] > 2
           and repetition_column[i] == False and trill_column[i] == False):
            if trial_type_column[i] == 'high' and trial_type_interfer_column[i] == 'low':
                high_low_list.append(strToFloat(RT_column[i]))
            elif trial_type_column[i] == 'low' and trial_type_interfer_column[i] == 'low':
                low_low_list.append(strToFloat(RT_column[i]))
            elif trial_type_column[i] == 'low' and trial_type_interfer_column[i] == 'high':
                low_high_list.append(strToFloat(RT_column[i]))

    return numpy.median(high_low_list), numpy.median(low_low_list), numpy.median(low_high_list)

def computeInterferenceData(input_dir, output_file):
    learning_data = pandas.DataFrame(columns=['subject', 'epoch_7_high_low', 'epoch_7_low_low', 'epoch_7_low_high'])

    for root, dirs, files in os.walk(input_dir):
        for file in files:

            input_file = os.path.join(input_dir, file)
            subject = int(file.split('_')[1])

            print("Compute interference measures for subject: " + str(subject))

            high_low_median, low_low_median, low_high_median = computeInterferenceOneSubject(input_file)
            learning_data.loc[len(learning_data)] = [subject, floatToStr(high_low_median), floatToStr(low_low_median), floatToStr(low_high_median)]
        break

    learning_data.to_csv(output_file, sep='\t', index=False)
