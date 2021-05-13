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

def computeMissingDataRatioImpl(input):
    data_table = pandas.read_csv(input, sep='\t')

    trial_column = data_table["trial"]
    left_gaze_validity = data_table["left_gaze_validity"]
    right_gaze_validity = data_table["right_gaze_validity"]

    all_data_count = 0
    missing_data_count = 0
    for i in range(len(trial_column)):
        if int(trial_column[i]) > 2:
            all_data_count += 1
            if not bool(left_gaze_validity[i]) and not bool(right_gaze_validity[i]):
                missing_data_count += 1

    return missing_data_count / all_data_count * 100.0

def computeMissingDataRatio(input_dir, output_file):

    missing_data_ratios = []
    subjects = []
    for root, dirs, files in os.walk(input_dir):
        for subject in dirs:
            if subject.startswith('.'):
                continue

            subjects.append(subject)
            input_file = os.path.join(root, subject, 'subject_' + subject + '__log.txt')
            result = computeMissingDataRatioImpl(input_file)
            missing_data_ratios.append(result)

        break

    missing_data = pandas.DataFrame({'subject' : subjects, 'missing_data_ratio' : missing_data_ratios})
    missing_data.to_csv(output_file, sep='\t', index=False)