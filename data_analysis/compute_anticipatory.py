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
from utils import strToFloat, floatToStr, filter_epoch

def computeAnticipDataForOneSubject(input_file, subject):
    input_data_table = pandas.read_csv(input_file, sep='\t')

    anticip_column = input_data_table["has_anticipation"]
    correct_anticip_column = input_data_table["has_learnt_anticipation"]
    epoch_column = input_data_table["epoch"]
    repetition_column = input_data_table["repetition"]
    trill_column = input_data_table["trill"]

    learnt_anticip_ratios = []
    all_aniticip = 0.0
    learnt_aniticip = 0.0
    current_epoch = epoch_column[0]
    for i in range(len(anticip_column) + 1):
        # end of the epoch -> calc summary data
        if i == len(anticip_column) or current_epoch != epoch_column[i]:
            assert(learnt_aniticip <= all_aniticip)

            learnt_ratio = learnt_aniticip / all_aniticip * 100.0

            if filter_epoch((subject, int(current_epoch))):
                learnt_ratio = float('nan')
                all_aniticip = float('nan')

            learnt_anticip_ratios.append(floatToStr(learnt_ratio))
            all_aniticip = 0.0
            learnt_aniticip = 0.0

        if i == len(anticip_column):
            break

        current_epoch = epoch_column[i]

        if repetition_column[i] == True or trill_column[i] == True:
            continue

        if str(anticip_column[i]) == 'True':
            all_aniticip += 1

        if str(correct_anticip_column[i]) == 'True':
            learnt_aniticip += 1

    return learnt_anticip_ratios

def computeAnticipatoryData(input_dir, output_file):
    anticip_data = pandas.DataFrame(columns=['subject',
                                              'epoch_1_learnt_anticip_ratio', 'epoch_2_learnt_anticip_ratio', 'epoch_3_learnt_anticip_ratio', 'epoch_4_learnt_anticip_ratio',
                                              'epoch_5_learnt_anticip_ratio', 'epoch_6_learnt_anticip_ratio', 'epoch_7_learnt_anticip_ratio', 'epoch_8_learnt_anticip_ratio'])

    for root, dirs, files in os.walk(input_dir):
        for file in files:

            input_file = os.path.join(input_dir, file)
            subject = int(file.split('_')[1])

            print("Compute anticipatory data for subject: " + str(subject))

            learnt_anticip_ratios = computeAnticipDataForOneSubject(input_file, subject)
            anticip_data.loc[len(anticip_data)] = [subject] + learnt_anticip_ratios
        break

    anticip_data.to_csv(output_file, sep='\t', index=False)
