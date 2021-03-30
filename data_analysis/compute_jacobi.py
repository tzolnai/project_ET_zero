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
import copy

all_triplet_count = 88

def computeHighFrequencies(jacobi_output_path):
    data_table = pandas.read_csv(jacobi_output_path, sep='\t')

    response_column = data_table["response"]
    trial_column = data_table["trial"]
    test_type_column = data_table["test_type"]
    PCode_column = data_table["PCode"]

    learning_sequence = str(PCode_column[0])
    learning_sequence += learning_sequence[0]

    inclusion_high_count = 0
    exclusion_high_count = 0
    for i in range(len(trial_column)):
        if int(trial_column[i]) > 2:
            assert(i > 1)
            if (str(response_column[i - 2]) + str(response_column[i])) in learning_sequence:
                if test_type_column[i] == 'inclusion':
                    inclusion_high_count += 1
                else:
                    assert(test_type_column[i] == 'exclusion')
                    exclusion_high_count += 1
                
    
    return inclusion_high_count, exclusion_high_count

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
                                                       'inclusion_trill_ratio', 'exclusion_trill_ratio',
                                                       'inclusion_high_ratio_without_trills', 'exclusion_high_ratio_without_trills'])

    for root, dirs, files in os.walk(input_dir):
        for subject in dirs:
            if subject.startswith('.'):
                continue

            jacobi_output_path = os.path.join(root, subject, 'subject_' + subject + '__jacobi_log.txt')
            inclusion_high_count, exclusion_high_count = computeHighFrequencies(jacobi_output_path)
            inclusion_trill_count, exclusion_trill_count = computeTrillFrequencies(jacobi_output_path)
            jacobi_data.loc[len(jacobi_data)] = [subject, inclusion_high_count / all_triplet_count * 100,
                                                          exclusion_high_count / all_triplet_count * 100,
                                                          inclusion_trill_count / all_triplet_count * 100,
                                                          exclusion_trill_count / all_triplet_count * 100,
                                                          inclusion_high_count / (all_triplet_count - inclusion_trill_count) * 100,
                                                          exclusion_high_count / (all_triplet_count - exclusion_trill_count) * 100]

        break

    jacobi_data.to_csv(output_file, sep='\t', index=False)

def computeStimFrequencies(jacobi_output_path):
    data_table = pandas.read_csv(jacobi_output_path, sep='\t')

    stimulus_column = data_table["response"]
    test_type_column = data_table["test_type"]

    response_counts_inclusion = {}
    response_counts_inclusion[1] = 0
    response_counts_inclusion[2] = 0
    response_counts_inclusion[3] = 0
    response_counts_inclusion[4] = 0
    response_counts_exclusion = copy.deepcopy(response_counts_inclusion)
    for i in range(len(stimulus_column)):
        if test_type_column[i] == 'inclusion':
            response_counts_inclusion[stimulus_column[i]] += 1
        else:
            assert(test_type_column[i] == 'exclusion')
            response_counts_exclusion[stimulus_column[i]] += 1

    return response_counts_inclusion, response_counts_exclusion

def computeFilterCriteria(response_counts):
    filter_criteria = 0
    expected_count = 24
    for i in response_counts:
        filter_criteria += abs(expected_count - response_counts[i]) ** 2

    return filter_criteria

def computeJacobiFilterCriteria(input_dir, output_file):
    jacobi_data = pandas.DataFrame(columns=['subject', 'response_1_count_inclusion', 'response_2_count_inclusion',
                                            'response_3_count_inclusion', 'response_4_count_inclusion',
                                            'response_1_count_exclusion', 'response_2_count_exclusion',
                                            'response_3_count_exclusion', 'response_4_count_exclusion',
                                            'filter_criteria_inclusion', 'filter_criteria_exclusion'])

    for root, dirs, files in os.walk(input_dir):
        for subject in dirs:
            if subject.startswith('.'):
                continue

            jacobi_output_path = os.path.join(root, subject, 'subject_' + subject + '__jacobi_log.txt')
            response_counts_inclusion, response_counts_exclusion = computeStimFrequencies(jacobi_output_path)
            filter_criteria_inclusion = computeFilterCriteria(response_counts_inclusion)
            filter_criteria_exclusion = computeFilterCriteria(response_counts_exclusion)
            jacobi_data.loc[len(jacobi_data)] = [subject, response_counts_inclusion[1], response_counts_inclusion[2],
                                                          response_counts_inclusion[3], response_counts_inclusion[4],
                                                          response_counts_exclusion[1], response_counts_exclusion[2],
                                                          response_counts_exclusion[3], response_counts_exclusion[4],
                                                          filter_criteria_inclusion, filter_criteria_exclusion]

        break

    jacobi_data.to_csv(output_file, sep='\t', index=False)
