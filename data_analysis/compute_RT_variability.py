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

def calcAverageRTDeviation(input_file):
    input_data_table = pandas.read_csv(input_file, sep='\t')

    RT_column = input_data_table["RT (ms)"]
    trial_column = input_data_table["trial"]
    block_column = input_data_table["block"]

    assert(len(RT_column) == len(trial_column))
    assert(len(RT_column) == len(block_column))

    block_RTs = []
    all_RT_deviations = []
    current_block = block_column[0]
    for i in range(len(RT_column) + 1):
        # end of the block
        if i == len(RT_column) or current_block != block_column[i]:
            all_RT_deviations.append(numpy.std(block_RTs))
            block_RTs = []

            if i == len(RT_column):
                break

            current_block = block_column[i]

        block_RTs.append(float(RT_column[i].replace(',','.')))

    print(input_file)
    print(all_RT_deviations)
    assert(len(all_RT_deviations) == 40) # 40 blocks
    return str(max(all_RT_deviations)).replace('.',',')

def computeRTVariability(input_dir, output_file):
    subjects = []
    deviations = []
    # Iterate through data files (one data file = one subject)
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            input_file = os.path.join(input_dir, file)

            # get subject ID
            subject = int(file.split('_')[1])
            subjects.append(subject)

            deviations.append(calcAverageRTDeviation(input_file))
        break

    average_data = pandas.DataFrame({'subject' : subjects, 'RT_deviaton': deviations})
    average_data.to_csv(output_file, sep='\t', index=False)
