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
import sys
import shutil
import time

import RT_calc as rtc

def setupOutputDir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        time.sleep(.001)

    os.makedirs(dir_path)
    if not os.path.isdir(dir_path):
        print("Could not make the output folder: " + dir_path)
        exit(1)

def compute_RT_data(input_dir, output_dir):
    setupOutputDir(output_dir)

    for root, dirs, files in os.walk(input_dir):
        for subject_dir in dirs:
            if subject_dir.startswith('.'):
                continue

            raw_data_path = os.path.join(root, subject_dir, 'subject_' + subject_dir + '__log.txt')
            RT_data_path = os.path.join(output_dir, 'subject_' + subject_dir + '__RT_log.txt')
            rtc.generateRTData(raw_data_path, RT_data_path)

        break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You need to specify an input folder for raw data files.")
        exit(1)

    if not os.path.isdir(sys.argv[1]):
        print("The passed first parameter should be a valid directory path: " + sys.argv[1])
        exit(1)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    RT_data_dir = os.path.join(script_dir, 'data', 'RT_data')

    compute_RT_data(sys.argv[1], RT_data_dir)