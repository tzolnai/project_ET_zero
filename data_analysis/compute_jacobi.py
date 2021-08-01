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
import copy
import analyizer
from utils import strToFloat, floatToStr, calcRMS

all_triplet_count = 88

def computeHighFrequencies(jacobi_output_path, sequence):
    data_table = pandas.read_csv(jacobi_output_path, sep='\t')

    response_column = data_table["response"]
    trial_column = data_table["trial"]
    test_type_column = data_table["test_type"]

    tested_sequence = sequence
    tested_sequence += sequence[0]

    inclusion_high_count = 0
    exclusion_high_count = 0
    for i in range(len(trial_column)):
        if int(trial_column[i]) > 2:
            assert(i > 1)
            if (str(response_column[i - 2]) + str(response_column[i])) in tested_sequence:
                if test_type_column[i] == 'inclusion':
                    inclusion_high_count += 1
                else:
                    assert(test_type_column[i] == 'exclusion')
                    exclusion_high_count += 1
                
    
    return inclusion_high_count, exclusion_high_count

def computeOtherSeqsHighFrequencies(jacobi_output_path, sequence, subject):
    sequences = [ "1234", "1243", "1324", "1342", "1423", "1432" ]
    sequences.remove(sequence)

    inclusion_high_counts = []
    exclusion_high_counts = []
    for seq in sequences:
        inclusion_high_count, exclusion_high_count = computeHighFrequencies(jacobi_output_path, seq, subject)
        inclusion_high_counts.append(inclusion_high_count)
        exclusion_high_counts.append(exclusion_high_count)

    return numpy.mean(inclusion_high_counts), numpy.mean(exclusion_high_counts)

def computeTrillFrequencies(jacobi_output_path):
    data_table = pandas.read_csv(jacobi_output_path, sep='\t')

    response_column = data_table["response"]
    trial_column = data_table["trial"]
    test_type_column = data_table["test_type"]

    inclusion_trill_count = 0
    exclusion_trill_count = 0
    for i in range(len(trial_column)):
        if int(trial_column[i]) > 2:
            assert(i > 1)
            if str(response_column[i - 2]) == str(response_column[i]):
                if test_type_column[i] == 'inclusion':
                    inclusion_trill_count += 1
                else:
                    assert(test_type_column[i] == 'exclusion')
                    exclusion_trill_count += 1
                
    
    return inclusion_trill_count, exclusion_trill_count

def computeJacobiTestData(input_dir, output_file):
    jacobi_data = pandas.DataFrame(columns=['subject', 'inclusion_high_ratio', 'exclusion_high_ratio',
                                                       'inclusion_high_ratio_otherseqs', 'exclusion_high_ratio_otherseqs',
                                                       'inclusion_trill_ratio', 'exclusion_trill_ratio',
                                                       'inclusion_high_ratio_without_trills', 'exclusion_high_ratio_without_trills'])

    for root, dirs, files in os.walk(input_dir):
        for subject in dirs:
            if subject.startswith('.'):
                continue

            print("Compute jacobi data for subject: " + str(subject))

            jacobi_output_path = os.path.join(root, subject, 'subject_' + subject + '__jacobi_log.txt')

            data_table = pandas.read_csv(jacobi_output_path, sep='\t')
            learning_sequence = str(data_table["PCode"][0])
            inclusion_high_count, exclusion_high_count = computeHighFrequencies(jacobi_output_path, learning_sequence)

            inclusion_high_count_others, exclusion_high_count_others = computeOtherSeqsHighFrequencies(jacobi_output_path, learning_sequence)

            inclusion_trill_count, exclusion_trill_count = computeTrillFrequencies(jacobi_output_path)
            jacobi_data.loc[len(jacobi_data)] = [subject, floatToStr(inclusion_high_count / all_triplet_count * 100),
                                                          floatToStr(exclusion_high_count / all_triplet_count * 100),
                                                          floatToStr(inclusion_high_count_others / all_triplet_count * 100),
                                                          floatToStr(exclusion_high_count_others / all_triplet_count * 100),
                                                          floatToStr(inclusion_trill_count / all_triplet_count * 100),
                                                          floatToStr(exclusion_trill_count / all_triplet_count * 100),
                                                          floatToStr(inclusion_high_count / (all_triplet_count - inclusion_trill_count) * 100),
                                                          floatToStr(exclusion_high_count / (all_triplet_count - exclusion_trill_count) * 100)]

        break

    jacobi_data.to_csv(output_file, sep='\t', index=False)

def computeFilterCriteria(jacobi_output_path):
    data_table = pandas.read_csv(jacobi_output_path, sep='\t')

    stimulus_column = data_table["response"]
    test_type_column = data_table["test_type"]

    responses_8_inclusion = []
    responses_8_exclusion = []

    for i in range(0, len(stimulus_column), 8):
        count_1 = 0
        count_2 = 0
        count_3 = 0
        count_4 = 0
        ref_count = 2

        for j in range(i, i + 8):
            if str(stimulus_column[j]) == "1":
                count_1 += 1
            elif str(stimulus_column[j]) == "2":
                count_2 += 1
            elif str(stimulus_column[j]) == "3":
                count_3 += 1
            elif str(stimulus_column[j]) == "4":
                count_4 += 1

        diffs = [abs(ref_count - count_1)]
        diffs.append(abs(ref_count - count_2))
        diffs.append(abs(ref_count - count_3))
        diffs.append(abs(ref_count - count_4))
        rms = calcRMS(diffs)

        if test_type_column[i] == 'inclusion':
            responses_8_inclusion.append(rms)
        else:
            assert(test_type_column[i] == 'exclusion')
            responses_8_exclusion.append(rms)

    return floatToStr(sum(responses_8_inclusion)), floatToStr(sum(responses_8_exclusion))

def computeJacobiFilterCriteria(input_dir, output_file):
    jacobi_data = pandas.DataFrame(columns=['subject', 'filter_criteria_inclusion', 'filter_criteria_exclusion'])
    for root, dirs, files in os.walk(input_dir):
        for subject in dirs:
            if subject.startswith('.'):
                continue

            print("Compute jacobi filter data for subject: " + str(subject))

            jacobi_output_path = os.path.join(root, subject, 'subject_' + subject + '__jacobi_log.txt')
            filter_criteria_inclusion, filter_criteria_exclusion = computeFilterCriteria(jacobi_output_path)
            jacobi_data.loc[len(jacobi_data)] = [subject, filter_criteria_inclusion, filter_criteria_exclusion]

        break

    jacobi_data.to_csv(output_file, sep='\t', index=False)
