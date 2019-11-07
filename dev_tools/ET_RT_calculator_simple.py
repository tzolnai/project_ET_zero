# !/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) <2019>  <Tamás Zolnai>  <zolnaitamas2000@gmail.com>

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
import shelve
import sys
import codecs
from io import StringIO


def convert(raw_file_name, new_file_name):

    with codecs.open(raw_file_name, 'r', encoding='utf-8') as raw_output_file:
        raw_lines = raw_output_file.readlines()

    new_file_data = StringIO()
    end_pos = raw_lines[0].find("trial_phase")
    new_file_data.write(raw_lines[0][:end_pos])
    new_file_data.write('RT (samples)')
    new_file_data.write('\n')

    trial_pos = raw_lines[0].split('\t').index("trial")
    trial_phase_pos = raw_lines[0].split('\t').index("trial_phase")

    last_trial = "1"
    RT_counter = 0
    current_line = 1
    for line in raw_lines[1:]:
        if last_trial != line.split('\t')[trial_pos] or line == raw_lines[len(raw_lines) - 1]:
            line_to_write = raw_lines[current_line - 1]
            end_pos = find_variable_str_index(line_to_write, trial_phase_pos)
            new_file_data.write(line_to_write[:end_pos])
            new_file_data.write('\t')

            if line == raw_lines[len(raw_lines) - 1]:
                new_file_data.write(str(RT_counter + 1))
            else:
                new_file_data.write(str(RT_counter))
            new_file_data.write('\n')

            last_trial = line.split('\t')[trial_pos]
            RT_counter = 0
        current_line += 1
        if line.split('\t')[trial_phase_pos] == "stimulus_on_screen":
            RT_counter += 1

    with codecs.open(new_file_name, 'w', encoding='utf-8') as new_output_file:
        new_output_file.write(new_file_data.getvalue())
    new_file_data.close()


def find_variable_str_index(string, variable_pos):
    begin_index = 0
    for i in range(variable_pos - 1):
        begin_index = string.find("\t", begin_index) + 1
    return string.find("\t", begin_index)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("You need to specify the path of an output txt file.")

    if not os.path.isfile(sys.argv[1]):
        print("The passed parameter should be a valid file's path: " + sys.argv[1])

    convert(sys.argv[1], sys.argv[2])
