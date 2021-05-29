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

def computeAnticipDataForOneSubject(input_file):
    input_data_table = pandas.read_csv(input_file, sep='\t')

    anticip_column = input_data_table["is_anticipation"]
    correct_anticip_column = input_data_table["correct_anticipation"]
    epoch_column = input_data_table["epoch"]

    all_aniticip = 0.0
    correct_aniticip = 0.0
    for i in range(len(anticip_column)):
        if str(anticip_column[i]) == 'True':
            all_aniticip += 1

        if str(correct_anticip_column[i]) == 'True':
            correct_aniticip += 1

    correct_anticip_ratio = (correct_aniticip / all_aniticip) * 100.0
    return all_aniticip, correct_anticip_ratio

def checkAnticipData(output_file, subject, all_aniticip, correct_anticip_ratio_all):
    print("Validate anticip data for subject: " + str(subject))

    input_data = pandas.read_csv(output_file, sep='\t')

    for index, row in input_data.iterrows():
        if row["subject"] == int(subject):
            subject_row = row

    output_all_anticip = 0
    output_correct_anticip_ratios = []
    for i in range(0,8):
        anticip_count_label = "epoch_" + str(i + 1) + "_anticip_count";
        output_all_anticip += subject_row[anticip_count_label]

        correct_anticip_ratio_label = "epoch_" + str(i + 1) + "_correct_anticip_ratio";
        output_correct_anticip_ratios.append(subject_row[correct_anticip_ratio_label])

    assert(output_all_anticip == all_aniticip)
    assert(abs(correct_anticip_ratio_all - numpy.median(output_correct_anticip_ratios)) < 10.0)

def validateAnticipatoryData(input_dir, output_file):
    for root, dirs, files in os.walk(input_dir):
        for file in files:

            input_file = os.path.join(input_dir, file)
            subject = int(file.split('_')[1])

            all_aniticip, correct_anticip_ratio = computeAnticipDataForOneSubject(input_file)
            checkAnticipData(output_file, subject, all_aniticip, correct_anticip_ratio)
        break
