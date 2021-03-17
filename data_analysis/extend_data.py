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

    for i in range(len(stimulus_column)):
        if i > 0 and stimulus_column[i] == stimulus_column[i - 1]:
            repetition_column.append(True)
        else:
            repetition_column.append(False)

    return repetition_column

def extendRTData(input_file, output_file):
    data_table = pandas.read_csv(input_file, sep='\t')

    # previous trial has the stimulus at the same position -> repetition.
    repetition_data = computeRepetitionColumn(data_table)
    assert(len(repetition_data) == len(data_table.index))
    data_table["repetition"] = repetition_data

    data_table.to_csv(output_file, sep='\t', index=False)
