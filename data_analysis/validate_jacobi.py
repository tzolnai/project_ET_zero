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
import analyizer
from utils import strToFloat, floatToStr

all_triplet_count = 88

def computeNonHighCounts(jacobi_output_path):
    data_table = pandas.read_csv(jacobi_output_path, sep='\t')

    response_column = data_table["response"]
    trial_column = data_table["trial"]
    test_type_column = data_table["test_type"]
    PCode_column = data_table["PCode"]

    learning_sequence = str(PCode_column[0])
    learning_sequence += learning_sequence[0]

    inclusion_non_high_count = 0
    exclusion_non_high_count = 0
    for i in range(len(trial_column)):
        if int(trial_column[i]) > 2:
            assert(i > 1)
            if (str(response_column[i - 2]) + str(response_column[i])) not in learning_sequence:
                if test_type_column[i] == 'inclusion':
                    inclusion_non_high_count += 1
                else:
                    assert(test_type_column[i] == 'exclusion')
                    exclusion_non_high_count += 1

    return inclusion_non_high_count, exclusion_non_high_count

def checkHighRatio(output_file, subject, inclusion_non_high_ratio, exclusion_non_high_ratio):
    print("Validate jacobi high ratio for subject: " + str(subject))

    input_data = pandas.read_csv(output_file, sep='\t')

    for index, row in input_data.iterrows():
        if row["subject"] == int(subject):
            subject_row = row

    inclusion_high_ratio = strToFloat(subject_row["inclusion_high_ratio"])
    assert(abs(100.0 - (inclusion_high_ratio + inclusion_non_high_ratio) < 0.001))

    exclusion_high_ratio = strToFloat(subject_row["exclusion_high_ratio"])
    assert(abs(100.0 - (exclusion_high_ratio + exclusion_non_high_ratio) < 0.001))

def validateJacobiTestData(input_dir, output_file):
    for root, dirs, files in os.walk(input_dir):
        for subject in dirs:
            if subject.startswith('.'):
                continue

            if analyizer.filter_subject(subject):
                continue

            jacobi_output_path = os.path.join(root, subject, 'subject_' + subject + '__jacobi_log.txt')
            inclusion_non_high_count, exclusion_non_high_count = computeNonHighCounts(jacobi_output_path)
            checkHighRatio(output_file, subject, inclusion_non_high_count / all_triplet_count * 100,
                                                 exclusion_non_high_count / all_triplet_count * 100)
        break
