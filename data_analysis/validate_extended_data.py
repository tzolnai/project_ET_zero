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

def validateRepetition(data_table):
    print("Validate repetition column")

    repetition_column = []
    stimulus_column = data_table["stimulus"]
    trial_column = data_table["trial"]
    repetition_column = data_table["repetition"]

    for i in range(len(stimulus_column)):
        if trial_column[i] == 1:
            assert(repetition_column[i] == False)
        elif repetition_column[i]:
            assert(stimulus_column[i - 1] == stimulus_column[i])
        else:
            assert(repetition_column[i] == False)
            assert(stimulus_column[i - 1] != stimulus_column[i])

def validateTrill(data_table):
    print("Validate trill column")

    stimulus_column = data_table["stimulus"]
    trial_column = data_table["trial"]
    trill_column = data_table["trill"]

    for i in range(len(stimulus_column)):
        if trial_column[i] <= 2:
            assert(trill_column[i] == False)
        elif trill_column[i]:
            assert(stimulus_column[i - 2] == stimulus_column[i])
        else:
            assert(trill_column[i] == False)
            assert(stimulus_column[i - 2] != stimulus_column[i])

def validateHighLowBasedOnLearningSequence(data_table):
    print("Validate high_low_learning column")

    high_low_column = []
    stimulus_column = data_table["stimulus"]
    trial_column = data_table["trial"]
    high_low_column = data_table["high_low_learning"]

    # get the learning sequence
    learning_sequence = data_table["PCode"][5 * 82]
    learning_sequence += learning_sequence[0]

    for i in range(len(stimulus_column)):
        if trial_column[i] <= 2:
            assert(high_low_column[i] == "none")
        elif high_low_column[i] == "high":
            assert(str(stimulus_column[i - 2]) + str(stimulus_column[i]) in learning_sequence)
        else:
            assert(high_low_column[i] == "low")
            assert(str(stimulus_column[i - 2]) + str(stimulus_column[i]) not in learning_sequence)         

def validateAnticipationColumn(data_table):
    print("Validate anticipation column")

    anticipation_column = data_table["is_anticipation"]
    stimulus_column = data_table["stimulus"]
    last_AOI_column = data_table["last_AOI_before_stimulus"]
    trial_column = data_table["trial"]

    for i in range(len(stimulus_column)):
        if last_AOI_column[i] == 'none':
            assert(anticipation_column[i] == False)
        elif anticipation_column[i]:
            assert(trial_column[i] >= 1)
            assert(int(last_AOI_column[i]) != int(stimulus_column[i - 1]))
        else:
            assert(anticipation_column[i] == False)
            assert(trial_column[i] >= 1)
            assert(int(last_AOI_column[i]) == int(stimulus_column[i - 1]))

def validateCorrectAnticipationColumn(data_table):
    print("Validate correct anticipation column")

    correct_anticipation_column = data_table["correct_anticipation"]
    stimulus_column = data_table["stimulus"]
    last_AOI_column = data_table["last_AOI_before_stimulus"]
    anticipation_column = data_table["is_anticipation"]
    trial_column = data_table["trial"]

    # get the learning sequence
    learning_sequence = data_table["PCode"][5 * 82]
    learning_sequence += learning_sequence[0]

    for i in range(len(stimulus_column)):
        if last_AOI_column[i] == 'none':
            assert(correct_anticipation_column[i] == False)
        elif correct_anticipation_column[i]:
            assert(trial_column[i] >= 2)
            assert(anticipation_column[i] == True)
            assert(str(stimulus_column[i - 2]) + str(last_AOI_column[i]) in learning_sequence)
        else:
            assert(correct_anticipation_column[i] == False)
            assert(anticipation_column[i] == False or
                   str(stimulus_column[i - 2]) + str(last_AOI_column[i]) not in learning_sequence)

def validateExtendedTrialData(input_file):
    print("Validate trial data extension for file: " + input_file)
    data_table = pandas.read_csv(input_file, sep='\t')

    validateRepetition(data_table)
    validateTrill(data_table)
    validateHighLowBasedOnLearningSequence(data_table)
    validateAnticipationColumn(data_table)
    validateCorrectAnticipationColumn(data_table)
