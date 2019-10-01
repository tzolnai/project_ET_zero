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
import unittest


class OutputValidation(unittest.TestCase):

    def validate_computer_name(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[0], "computer_name")
        for line in output_lines[1:]:
            self.assertEqual(line.split('\t')[0], "Laposka")

    def validate_subject_group(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[1], "subject_group")
        for line in output_lines[1:]:
            self.assertEqual(line.split('\t')[1], "")

    def validate_subject_name(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[2], "subject_name")
        for line in output_lines[1:]:
            self.assertEqual(line.split('\t')[2], "sebi")

    def validate_subject_number(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[3], "subject_number")
        for line in output_lines[1:]:
            self.assertEqual(line.split('\t')[3], "1")

    def validate_subject_sex(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[4], "subject_sex")
        for line in output_lines[1:]:
            self.assertEqual(line.split('\t')[4], "male")

    def validate_subject_age(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[5], "subject_age")
        for line in output_lines[1:]:
            self.assertEqual(line.split('\t')[5], "29")

    def validate_asrt_type(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[6], "asrt_type")
        for line in output_lines[1:]:
            self.assertEqual(line.split('\t')[6], "implicit")

    def validate_PCode(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[7], "PCode")
        for line in output_lines[1:]:
            self.assertEqual(line.split('\t')[7], "1234")

    def validate_session(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[8], "session")
        for line in output_lines[1:]:
            self.assertEqual(line.split('\t')[8], "1")

    def validate_epoch(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[9], "epoch")
        for line in output_lines[1:]:
            block_num = int(line.split('\t')[10])
            self.assertEqual(line.split('\t')[9], str((block_num - 1) // 5 + 1))

    def validate_block(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[10], "block")
        block_num = 1
        last_trial = ""
        for line in output_lines[1:]:
            if last_trial == "85" and line.split('\t')[11] == "1":
                block_num += 1
            self.assertEqual(line.split('\t')[10], str(block_num))
            last_trial = line.split('\t')[11]

    def validate_trial_and_RSI(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[11], "trial")
        trial_num = 1
        last_RSI = "-1"
        for line in output_lines[1:]:
            if last_RSI != "-1" and line.split('\t')[12] == "-1":
                trial_num += 1
            self.assertEqual(line.split('\t')[11], str(trial_num))
            last_RSI = line.split('\t')[12]

    def validate_RSI(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[12], "RSI_time")
        for line in output_lines[1:]:
            if line.split('\t')[19] == "False":
                self.assertEqual(line.split('\t')[12], "-1")
            else:
                self.assertTrue(line.split('\t')[12] == "0,0" or abs(float(line.split('\t')[12].replace(',', '.')) - 0.500) < 0.02)

    def validate_frame_rate(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[13], "frame_rate")
        frame_rate = output_lines[1].split('\t')[13]
        for line in output_lines[2:]:
            self.assertEqual(line.split('\t')[13], frame_rate)

    def validate_frame_time(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[14], "frame_time")
        frame_time = output_lines[1].split('\t')[14]
        for line in output_lines[2:]:
            self.assertEqual(line.split('\t')[14], frame_time)

    def validate_frame_sd(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[15], "frame_sd")
        frame_sd = output_lines[1].split('\t')[15]
        for line in output_lines[2:]:
            self.assertEqual(line.split('\t')[15], frame_sd)

    def validate_stim_color(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[16], "stimulus_color")
        stimulus_color = output_lines[1].split('\t')[16]
        for line in output_lines[2:]:
            self.assertEqual(line.split('\t')[16], stimulus_color)

    def validate_pattern_random(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[17], "PR")
        for line in output_lines[1:]:
            current_trial = int(line.split('\t')[11])
            if current_trial <= 5 or (current_trial - 5) % 2 == 0:
                self.assertEqual(line.split('\t')[17], "R")
            else:
                self.assertEqual(line.split('\t')[17], "P")

    def validate_stimulus(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        self.assertEqual(output_lines[0].split('\t')[18], "stimulus")

        PCode = output_lines[1].split('\t')[7]

        dict_next_stimulus = {}
        dict_next_stimulus[PCode[0]] = PCode[1]
        dict_next_stimulus[PCode[1]] = PCode[2]
        dict_next_stimulus[PCode[2]] = PCode[3]
        dict_next_stimulus[PCode[3]] = PCode[0]
        last_trial = 0
        last_pattern_stimulus = 0

        for line in output_lines[1:]:
            current_trial = int(line.split('\t')[11])
            if current_trial <= 5:
                last_pattern_stimulus = 0

            if last_trial != current_trial and line.split('\t')[17] == "P":
                if last_pattern_stimulus != 0:
                    self.assertEqual(line.split('\t')[18], dict_next_stimulus[str(last_pattern_stimulus)])
                last_pattern_stimulus = int(line.split('\t')[18])

            self.assertTrue(int(line.split('\t')[18]) in [1, 2, 3, 4])

            last_trial = int(line.split('\t')[11])

    def validate_RSI_interval_sampling(self, file_name):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        self.assertTrue(len(output_lines) > 0)
        sampling_counter = 0
        last_trial = "1"
        for line in output_lines[1:]:
            if line.split('\t')[12] == "-1" and line.split('\t')[11] != "1" and last_trial == line.split('\t')[11]:
                sampling_counter += 1
            else:
                self.assertTrue(sampling_counter < 65)
                if sampling_counter > 0:
                    self.assertTrue(sampling_counter > 54)
                sampling_counter = 0
            last_trial = line.split('\t')[11]

    def validate(self, file_name):
        # self.validate_computer_name(file_name)
        # self.validate_subject_group(file_name)
        # self.validate_subject_name(file_name)
        # self.validate_subject_number(file_name)
        # self.validate_subject_sex(file_name)
        # self.validate_subject_age(file_name)
        # self.validate_asrt_type(file_name)
        # self.validate_PCode(file_name)
        # self.validate_session(file_name)
        # self.validate_epoch(file_name)
        # self.validate_block(file_name)
        #self.validate_trial_and_RSI(file_name) // error
        # self.validate_RSI(file_name)
        # self.validate_frame_rate(file_name)
        # self.validate_frame_time(file_name)
        # self.validate_frame_sd(file_name)
        # self.validate_stim_color(file_name)
        # self.validate_pattern_random(file_name)
        # self.validate_stimulus(file_name)
        self.validate_RSI_interval_sampling(file_name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You need to specify the path of an output txt file.")

    if not os.path.isfile(sys.argv[1]):
        print("The passed parameter should be a valid file's path: " + sys.argv[1])

    output_validation = OutputValidation()
    output_validation.validate(sys.argv[1])
