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

import pandas

def computeRepetitionColumn(data_table):
    repetition_column = []
    stimulus_column = data_table["stimulus"]
    trial_column = data_table["trial"]

    for i in range(len(stimulus_column)):
        if trial_column[i] > 1 and stimulus_column[i] == stimulus_column[i - 1]:
            repetition_column.append(True)
        else:
            repetition_column.append(False)

    return repetition_column

def computeTrillColumn(data_table):
    trill_column = []
    stimulus_column = data_table["stimulus"]
    trial_column = data_table["trial"]

    for i in range(len(stimulus_column)):
        if trial_column[i] > 2 and stimulus_column[i] == stimulus_column[i - 2]:
            trill_column.append(True)
        else:
            trill_column.append(False)

    return trill_column

def computeHighLowBasedOnLearningSequence(data_table):
    high_low_column = []
    stimulus_column = data_table["stimulus"]
    trial_column = data_table["trial"]

    # get the learning sequence
    learning_sequence = data_table["PCode"][5 * 82]
    learning_sequence += learning_sequence[0]

    for i in range(len(stimulus_column)):
        if trial_column[i] > 2:
            if (str(stimulus_column[i - 2]) + str(stimulus_column[i])) in learning_sequence:
                high_low_column.append('high')
            else:
                high_low_column.append('low')
        else:
            high_low_column.append('none')

    return high_low_column

def computeAnticipationColumn(data_table):
    anticipation_column = []
    stimulus_column = data_table["stimulus"]
    last_AOI_column = data_table["last_AOI_before_stimulus"]

    for i in range(len(stimulus_column)):
        if last_AOI_column[i] == 'none':
            anticipation_column.append(False)
        elif int(last_AOI_column[i]) != int(stimulus_column[i - 1]):
            anticipation_column.append(True)
        else:
            anticipation_column.append(False)

    return anticipation_column

def computeCorrectAnticipationColumn(data_table):
    correct_anticipation_data = []
    stimulus_column = data_table["stimulus"]
    last_AOI_column = data_table["last_AOI_before_stimulus"]

    # get the learning sequence
    learning_sequence = data_table["PCode"][5 * 82]
    learning_sequence += learning_sequence[0]

    for i in range(len(stimulus_column)):
        if last_AOI_column[i] == 'none' or i < 2:
            correct_anticipation_data.append(False)
        elif int(last_AOI_column[i]) == int(stimulus_column[i - 1]):
            correct_anticipation_data.append(False)
        elif str(stimulus_column[i - 2]) + str(last_AOI_column[i]) in learning_sequence:
            correct_anticipation_data.append(True)
        else:
            correct_anticipation_data.append(False)

    return correct_anticipation_data

def extendTrialData(input_file, output_file):
    data_table = pandas.read_csv(input_file, sep='\t')

    # previous trial has the stimulus at the same position -> repetition.
    repetition_data = computeRepetitionColumn(data_table)
    assert(len(repetition_data) == len(data_table.index))
    data_table["repetition"] = repetition_data

    # trill: first item and third item of trial triplet is the same: e.g. 1x1, 2x2, etc.
    trill_data = computeTrillColumn(data_table)
    assert(len(trill_data) == len(data_table.index))
    data_table["trill"] = trill_data

    # calculate frequency based on learning sequence
    high_low_data = computeHighLowBasedOnLearningSequence(data_table)
    assert(len(high_low_data) == len(data_table.index))
    data_table["high_low_learning"] = high_low_data

    # calculate whether anticipatory eye-movement was happened
    anticipation_data = computeAnticipationColumn(data_table)
    assert(len(anticipation_data) == len(data_table.index))
    data_table["is_anticipation"] = anticipation_data

    # calculate whether correct anticipatory eye-movement was happened
    correct_anticipation_data = computeCorrectAnticipationColumn(data_table)
    assert(len(correct_anticipation_data) == len(data_table.index))
    data_table["correct_anticipation"] = correct_anticipation_data

    data_table.to_csv(output_file, sep='\t', index=False)
