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
import pandas
import math


class OutputValidation(unittest.TestCase):

    def validate_computer_name(self, data_table):
        print("Validate computer name...")

        column = data_table["computer_name"]
        self.assertTrue(len(column) > 0)
        computer_name = column[0]
        self.assertEqual(computer_name, "Laposka")
        for cell in column:
            self.assertEqual(cell, computer_name)

        print("OK")

    def validate_subject_group(self, data_table):
        print("Validate subject group...")

        column = data_table["subject_group"]
        self.assertTrue(len(column) > 0)
        subject_group = column[0]
        self.assertTrue(math.isnan(subject_group))
        for cell in column:
            self.assertTrue(math.isnan(cell))

        print("OK")

    def validate_subject_name(self, data_table):
        print("Validate subject name...")

        column = data_table["subject_name"]
        self.assertTrue(len(column) > 0)
        subject_name = column[0]
        for cell in column:
            self.assertEqual(cell, subject_name)

        print("OK")

    def validate_subject_number(self, data_table):
        print("Validate subject number...")

        column = data_table["subject_number"]
        self.assertTrue(len(column) > 0)
        subject_number = column[0]

        # Check that subject namber is a natural number
        self.assertTrue(int(subject_number) >= 0)

        for cell in column:
            self.assertEqual(cell, subject_number)

        print("OK")

    def validate_subject_sex(self, data_table):
        print("Validate subject sex...")

        column = data_table["subject_sex"]
        self.assertTrue(len(column) > 0)

        subject_sex = column[0]
        self.assertTrue(subject_sex in ["male", "female", "other"])
        for cell in column:
            self.assertEqual(cell, subject_sex)

        print("OK")

    def validate_subject_age(self, data_table):
        print("Validate subject age...")

        column = data_table["subject_age"]
        self.assertTrue(len(column) > 0)

        subject_age = column[0]
        self.assertTrue(int(subject_age) >= 18 and int(subject_age) <= 50)

        for cell in column:
            self.assertEqual(cell, subject_age)

        print("OK")

    def validate_asrt_type(self, data_table):
        print("Validate asrt type...")

        column = data_table["asrt_type"]
        self.assertTrue(len(column) > 0)

        asrt_type = column[0]
        self.assertTrue(asrt_type in ["implicit", "explicit", "noASRT"])

        for cell in column:
            self.assertEqual(cell, asrt_type)

        print("OK")

    def validate_PCode(self, data_table):
        print("Validate PCode...")

        column = data_table["PCode"]
        self.assertTrue(len(column) > 0)

        PCode = column[0]
        self.assertTrue(str(PCode) in ["1234", "1243", "1324", "1342", "1423", "1432", "noPattern"])

        for cell in column:
            self.assertEqual(cell, PCode)

        print("OK")

    def validate_session(self, data_table):
        print("Validate session...")

        column = data_table["session"]
        self.assertTrue(len(column) > 0)

        session = column[0]
        self.assertTrue(int(session) >= 1)

        for cell in column:
            self.assertEqual(cell, session)

        print("OK")

    def validate_epoch_block_relation(self, data_table):
        print("Validate epoch...")

        epoch_column = data_table["epoch"]
        block_column = data_table["block"]
        self.assertTrue(len(epoch_column) > 0)
        self.assertEqual(len(epoch_column), len(block_column))

        for i in range(len(epoch_column)):
            block_number = block_column[i]
            self.assertEqual(epoch_column[i], (block_number - 1) // 5 + 1)
            self.assertTrue(epoch_column[i] >= 1 and epoch_column[i] <= 5)

        print("OK")

    def validate_block_trial_relation(self, data_table):
        print("Validate block...")

        block_column = data_table["block"]
        trial_column = data_table["trial"]
        self.assertTrue(len(block_column) > 0)
        self.assertEqual(len(block_column), len(trial_column))

        expected_block_number = 1
        for i in range(len(block_column)):
            if i > 0 and trial_column[i] == 1 and trial_column[i - 1] != 1:
                expected_block_number += 1
            self.assertEqual(block_column[i], expected_block_number)
            self.assertTrue(block_column[i] >= 1 and block_column[i] <= 25)

        print("OK")

    def validate_trial_RSI_relation(self, data_table):
        print("Validate trial...")

        trial_column = data_table["trial"]
        RSI_column = data_table["RSI_time"]
        self.assertTrue(len(trial_column) > 0)
        self.assertEqual(len(trial_column), len(RSI_column))

        expected_trial_number = 1
        trial_displayed = False
        for i in range(len(trial_column)):
            if i > 0 and RSI_column[i] == "-1" and RSI_column[i - 1] != "-1":
                expected_trial_number += 1
                trial_displayed = False

            if RSI_column[i] != "-1":
                trial_displayed = True

            if trial_column[i] != expected_trial_number and not trial_displayed:
                expected_trial_number += 1

            if expected_trial_number > 80:
                expected_trial_number = 1

            self.assertEqual(trial_column[i], expected_trial_number)
            self.assertTrue(trial_column[i] >= 1 and trial_column[i] <= 80)

        print("OK")

    def validate_RSI_trial_phase_relation(self, data_table):
        print("Validate RSI time...")

        RSI_column = data_table["RSI_time"]
        trial_phase_column = data_table["trial_phase"]
        trial_column = data_table["trial"]
        self.assertTrue(len(RSI_column) > 0)
        self.assertEqual(len(RSI_column), len(trial_phase_column))

        expected_block_number = 1
        for i in range(len(RSI_column)):
            if trial_phase_column[i] == "before_stimulus":
                self.assertEqual(RSI_column[i], "-1")
            elif trial_column[i] == 1:
                self.assertEqual(RSI_column[i], "0,0")
            else:
                self.assertTrue(abs(float(RSI_column[i].replace(',', '.')) - 0.500) < 0.03)

        print("OK")

    def validate_frame_rate(self, data_table):
        print("Validate frame rate...")

        column = data_table["frame_rate"]
        self.assertTrue(len(column) > 0)

        frame_rate = column[0]
        self.assertTrue(abs(float(frame_rate.replace(',', '.')) - 60.0) < 0.5)

        for cell in column:
            self.assertEqual(cell, frame_rate)

        print("OK")

    def validate_frame_time(self, data_table):
        print("Validate frame time...")

        column = data_table["frame_time"]
        self.assertTrue(len(column) > 0)

        frame_time = column[0]
        self.assertTrue(abs(float(frame_time.replace(',', '.')) - (1000.0 / 60.0)) < 0.05)

        frame_rate = float(data_table["frame_rate"][0].replace(',', '.'))
        self.assertTrue(abs(float(frame_time.replace(',', '.')) - (1000.0 / frame_rate)) < 0.06)

        for cell in column:
            self.assertEqual(cell, frame_time)

        print("OK")

    def validate_frame_sd(self, data_table):
        print("Validate frame standard deviation...")

        column = data_table["frame_sd"]
        self.assertTrue(len(column) > 0)

        frame_sd = column[0]
        self.assertTrue(abs(float(frame_sd.replace(',', '.'))) < 0.1)

        for cell in column:
            self.assertEqual(cell, frame_sd)

        print("OK")

    def validate_stimulus_color(self, data_table):
        print("Validate stimulus color...")

        column = data_table["stimulus_color"]
        self.assertTrue(len(column) > 0)

        stimulus_color = column[0]
        self.assertEqual(stimulus_color, "DarkBlue")

        for cell in column:
            self.assertEqual(cell, stimulus_color)

        print("OK")

    def validate_pattern_random_and_trial_relation(self, data_table):
        print("Validate pattern/random...")

        pr_column = data_table["triplet_type_pr"]
        trial_column = data_table["trial"]
        self.assertTrue(len(pr_column) > 0)
        self.assertEqual(len(pr_column), len(trial_column))

        for i in range(len(pr_column)):
            if trial_column[i] % 2 == 1:
                self.assertEqual(pr_column[i], "pattern")
            else:
                self.assertEqual(pr_column[i], "random")

        print("OK")

    def validate_triplet_frequency(self, data_table):
        print("Validate triplet frequency...")

        high_low_column = data_table["triplet_frequency"]
        trial_column = data_table["trial"]
        pr_column = data_table["triplet_type_pr"]
        stimulus_column = data_table["stimulus"]
        self.assertTrue(len(high_low_column) > 0)
        self.assertEqual(len(high_low_column), len(trial_column))

        PCode = str(data_table["PCode"][0])
        dict_next_stimulus = {}
        dict_next_stimulus[PCode[0]] = PCode[1]
        dict_next_stimulus[PCode[1]] = PCode[2]
        dict_next_stimulus[PCode[2]] = PCode[3]
        dict_next_stimulus[PCode[3]] = PCode[0]

        last_random_stimulus = 0
        for i in range(len(high_low_column)):
            if trial_column[i] <= 2:
                #self.assertEqual(high_low_column[i], "none")
                pass
            elif pr_column[i] == "pattern":
                self.assertEqual(high_low_column[i], "high")
            else:
                if trial_column[i] != trial_column[i - 1]:
                    if str(stimulus_column[i]) == dict_next_stimulus[str(last_random_stimulus)]:
                        self.assertEqual(high_low_column[i], "high")
                    else:
                        self.assertEqual(high_low_column[i], "low")
                else:
                    self.assertEqual(high_low_column[i], high_low_column[i - 1])

            if pr_column[i] == "random":
                last_random_stimulus = stimulus_column[i]

        print("OK")

    def validate_stimulus(self, data_table):
        print("Validate stimulus...")

        pr_column = data_table["triplet_type_pr"]
        stimulus_column = data_table["stimulus"]
        self.assertTrue(len(stimulus_column) > 0)
        self.assertEqual(len(stimulus_column), len(pr_column))

        PCode = str(data_table["PCode"][0])
        dict_next_stimulus = {}
        dict_next_stimulus[PCode[0]] = PCode[1]
        dict_next_stimulus[PCode[1]] = PCode[2]
        dict_next_stimulus[PCode[2]] = PCode[3]
        dict_next_stimulus[PCode[3]] = PCode[0]

        last_pattern_stimulus = 0
        for i in range(len(stimulus_column)):
            self.assertTrue(stimulus_column[i] in [1, 2, 3, 4])
            if pr_column[i] == "pattern":
                if i > 0 and stimulus_column[i] != last_pattern_stimulus:
                    self.assertEqual(str(stimulus_column[i]), dict_next_stimulus[str(last_pattern_stimulus)])
                last_pattern_stimulus = stimulus_column[i]

        print("OK")

    def validate_RSI_interval_sampling(self, data_table):
        print("Validate RSI interval sample count...")

        RSI_column = data_table["RSI_time"]
        trial_column = data_table["trial"]
        self.assertTrue(len(RSI_column) > 0)
        self.assertEqual(len(RSI_column), len(trial_column))

        sampling_counter = 1
        last_trial = 1
        for i in range(len(RSI_column)):
            if last_trial != 1:
                if last_trial != trial_column[i]:
                    self.assertTrue(abs(sampling_counter - 60) < 10)
                    sampling_counter = 1
                if RSI_column[i] == "-1" and last_trial == trial_column[i]:
                    sampling_counter += 1
            last_trial = trial_column[i]

        print("OK")

    def validate(self, file_name):
        data_table = pandas.read_csv(file_name, sep='\t')

        self.validate_computer_name(data_table)
        self.validate_subject_group(data_table)
        self.validate_subject_name(data_table)
        self.validate_subject_number(data_table)
        self.validate_subject_sex(data_table)
        self.validate_subject_age(data_table)
        self.validate_asrt_type(data_table)
        self.validate_PCode(data_table)
        self.validate_session(data_table)
        self.validate_epoch_block_relation(data_table)
        self.validate_block_trial_relation(data_table)
        self.validate_trial_RSI_relation(data_table)
        self.validate_RSI_trial_phase_relation(data_table)
        self.validate_frame_rate(data_table)
        self.validate_frame_time(data_table)
        self.validate_frame_sd(data_table)
        self.validate_pattern_random_and_trial_relation(data_table)
        self.validate_triplet_frequency(data_table)
        self.validate_stimulus(data_table)
        # self.validate_RSI_interval_sampling(data_table)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You need to specify the path of an output txt file.")

    if not os.path.isfile(sys.argv[1]):
        print("The passed parameter should be a valid file's path: " + sys.argv[1])

    output_validation = OutputValidation()
    output_validation.validate(sys.argv[1])
