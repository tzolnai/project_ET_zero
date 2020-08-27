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
        for cell in column:
            self.assertEqual(cell, "ET-PC")

        print("OK")

    def validate_monitor_width(self, data_table):
        print("Validate monitor width...")

        column = data_table["monitor_width_pixel"]
        self.assertTrue(len(column) > 0)
        for cell in column:
            self.assertEqual(cell, 1920)

        print("OK")

    def validate_monitor_height(self, data_table):
        print("Validate monitor height...")

        column = data_table["monitor_height_pixel"]
        self.assertTrue(len(column) > 0)
        for cell in column:
            self.assertEqual(cell, 1080)

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

        asrt_type_column = data_table["asrt_type"]
        epoch_column = data_table["epoch"]
        self.assertTrue(len(asrt_type_column) > 0)

        for row in range(len(asrt_type_column)):
            if epoch_column[row] == 1:
                self.assertEqual(asrt_type_column[row], "noASRT")
            else:
                self.assertEqual(asrt_type_column[row], "implicit")

        print("OK")

    def validate_PCode(self, data_table):
        print("Validate PCode...")

        PCode_column = data_table["PCode"]
        epoch_column = data_table["epoch"]
        self.assertTrue(len(PCode_column) > 0)

        first_row_of_8th_epoch = -1
        first_row_of_2nd_epoch = -1
        for row in range(len(PCode_column)):
            self.assertTrue(str(PCode_column[row]) in ["1234", "1243", "1324", "1342", "1423", "1432", "noPattern"])
            if epoch_column[row] == 1:
                self.assertEqual(PCode_column[row], "noPattern")
            elif epoch_column[row] in [2, 3, 4, 5, 6, 8]:
                if first_row_of_2nd_epoch == -1:
                    first_row_of_2nd_epoch = row
                self.assertEqual(str(PCode_column[row]), str(PCode_column[first_row_of_2nd_epoch]))
            elif epoch_column[row] == 8:
                if first_row_of_8th_epoch == -1:
                    first_row_of_8th_epoch = row
                self.assertEqual(str(PCode_column[row]), str(PCode_column[first_row_of_8th_epoch]))

        print("OK")

    def validate_session(self, data_table):
        print("Validate session...")

        session_column = data_table["session"]
        epoch_column = data_table["epoch"]
        self.assertTrue(len(session_column) > 0)


        for row in range(len(session_column)):
            if epoch_column[row] in [1, 2, 3, 4, 5]:
                self.assertEqual(session_column[row], 1)
            else:
                self.assertEqual(session_column[row], 2)

            if row != 0:
                self.assertTrue(session_column[row] == session_column[row - 1] or
                                session_column[row] == session_column[row - 1] + 1)

        print("OK")

    def validate_epoch_block_relation(self, data_table):
        print("Validate epoch...")

        epoch_column = data_table["epoch"]
        block_column = data_table["block"]
        self.assertTrue(len(epoch_column) > 0)
        self.assertEqual(len(epoch_column), len(block_column))

        for row in range(len(epoch_column)):
            block_number = block_column[row]
            epoch_number = epoch_column[row]
            if block_number == 0:
                self.assertTrue(epoch_number == 1 or epoch_number == 6)
            else:                
                self.assertEqual(epoch_number, (block_number - 1) // 5 + 1)
            self.assertTrue(epoch_number >= 1 and epoch_number <= 8)
            
            if row != 0:
                self.assertTrue(epoch_number == epoch_column[row - 1] or
                                epoch_number == epoch_column[row - 1] + 1)

        print("OK")

    def validate_block_trial_relation(self, data_table):
        print("Validate block...")

        block_column = data_table["block"]
        trial_column = data_table["trial"]
        self.assertTrue(len(block_column) > 0)
        self.assertEqual(len(block_column), len(trial_column))

        expected_block_number = 0
        for row in range(len(block_column)):
            block_number = block_column[row]
            if row > 0 and trial_column[row] == 1 and trial_column[row - 1] != 1 and block_number != 0:
                expected_block_number += 1
            
            if block_number != 0:
                self.assertEqual(block_number, expected_block_number)
            else:
                self.assertTrue(trial_column[row] <= 20)
            self.assertTrue(block_number >= 0 and block_number <= 40)

            if row != 0 and block_number != 0 and block_column[row - 1] != 0:
                self.assertTrue(block_number == block_column[row - 1] or
                                block_number == block_column[row - 1] + 1)

        print("OK")

    def validate_trial_RSI_relation(self, data_table):
        print("Validate trial...")

        trial_column = data_table["trial"]
        block_column = data_table["block"]
        RSI_column = data_table["RSI_time"]
        self.assertTrue(len(trial_column) > 0)
        self.assertEqual(len(trial_column), len(RSI_column))

        expected_trial_number = 1
        trial_displayed = False
        for row in range(len(trial_column)):
            trial_num = trial_column[row]
            if row > 0 and RSI_column[row] == "-1" and RSI_column[row - 1] != "-1":
                expected_trial_number += 1
                trial_displayed = False

            if RSI_column[row] != "-1":
                trial_displayed = True

            if trial_num != expected_trial_number and not trial_displayed:
                expected_trial_number += 1

            if (row != 0 and block_column[row - 1] == 0 and expected_trial_number > 20) or expected_trial_number > 82:
                expected_trial_number = 1

            self.assertEqual(trial_num, expected_trial_number)

            if block_column[row] == 0:
                self.assertTrue(trial_num >= 1 and trial_num <= 20)
            else:
                self.assertTrue(trial_num >= 1 and trial_num <= 82)
                
            if row != 0:
                self.assertTrue(trial_num == trial_column[row - 1] or
                                trial_num == trial_column[row - 1] + 1 or
                                trial_num == 1)

        print("OK")

    def validate_RSI_trial_phase_relation(self, data_table):
        print("Validate RSI time...")

        RSI_column = data_table["RSI_time"]
        trial_phase_column = data_table["trial_phase"]
        trial_column = data_table["trial"]
        self.assertTrue(len(RSI_column) > 0)
        self.assertEqual(len(RSI_column), len(trial_phase_column))

        expected_block_number = 1
        for row in range(len(RSI_column)):
            if trial_phase_column[row] == "before_stimulus":
                self.assertEqual(RSI_column[row], "-1")
            elif trial_column[row] == 1:
                self.assertEqual(RSI_column[row], "0,0")
            else:
                self.assertTrue(abs(float(RSI_column[row].replace(',', '.')) - 0.500) < 0.03)

        print("OK")

    def validate_frame_rate(self, data_table):
        print("Validate frame rate...")

        column = data_table["frame_rate"]
        self.assertTrue(len(column) > 0)

        for cell in column:
            self.assertTrue(abs(float(cell.replace(',', '.')) - 60.0) < 0.5)

        print("OK")

    def validate_frame_time(self, data_table):
        print("Validate frame time...")

        column = data_table["frame_time"]
        self.assertTrue(len(column) > 0)

        for row in range(len(column)):
            frame_rate = float(data_table["frame_rate"][row].replace(',', '.'))
            self.assertTrue(abs(float(column[row].replace(',', '.')) - (1000.0 / 60.0)) < 0.05)
            self.assertTrue(abs(float(column[row].replace(',', '.')) - (1000.0 / frame_rate)) < 0.08)

        print("OK")

    def validate_frame_sd(self, data_table):
        print("Validate frame standard deviation...")

        column = data_table["frame_sd"]
        self.assertTrue(len(column) > 0)

        for cell in column:
            print(cell)
            self.assertTrue(abs(float(cell.replace(',', '.'))) < 0.5)

        print("OK")

    def validate_stimulus_color(self, data_table):
        print("Validate stimulus color...")

        column = data_table["stimulus_color"]
        self.assertTrue(len(column) > 0)

        for cell in column:
            self.assertEqual(cell, "DarkBlue")

        print("OK")

    def validate_trial_type_pr(self, data_table):
        print("Validate pattern/random...")

        pr_column = data_table["trial_type_pr"]
        trial_column = data_table["trial"]
        block_column = data_table["block"]
        epoch_column = data_table["epoch"]
        self.assertTrue(len(pr_column) > 0)
        self.assertEqual(len(pr_column), len(trial_column))

        for row in range(len(pr_column)):
            if str(block_column[row]) == "0" or epoch_column[row] == 1 or trial_column[row] <= 2:
                self.assertEqual(pr_column[row], "random")
            elif trial_column[row] % 2 == 1:
                self.assertEqual(pr_column[row], "pattern")
            else:
                self.assertEqual(pr_column[row], "random")

        print("OK")

    def validate_triplet_type_hl(self, data_table):
        print("Validate triplet frequency...")

        high_low_column = data_table["triplet_type_hl"]
        trial_column = data_table["trial"]
        pr_column = data_table["trial_type_pr"]
        stimulus_column = data_table["stimulus"]
        block_column = data_table["block"]
        self.assertTrue(len(high_low_column) > 0)
        self.assertEqual(len(high_low_column), len(trial_column))

        last_random_stimulus = 0
        for row in range(len(high_low_column)):
            if str(block_column[row]) == "0":
                pass
            elif trial_column[row] <= 2:
                self.assertEqual(high_low_column[row], "none")
            elif pr_column[row] == "pattern":
                self.assertEqual(high_low_column[row], "high")
            else:
                PCode = str(data_table["PCode"][row])
                dict_next_stimulus = {}
                dict_next_stimulus[PCode[0]] = PCode[1]
                dict_next_stimulus[PCode[1]] = PCode[2]
                dict_next_stimulus[PCode[2]] = PCode[3]
                dict_next_stimulus[PCode[3]] = PCode[0]

                if PCode == "noPattern":
                    self.assertEqual(high_low_column[row], "none")
                elif trial_column[row] != trial_column[row - 1]:
                    if str(stimulus_column[row]) == dict_next_stimulus[str(last_random_stimulus)]:
                        self.assertEqual(high_low_column[row], "high")
                    else:
                        self.assertEqual(high_low_column[row], "low")
                else:
                    self.assertEqual(high_low_column[row], high_low_column[row - 1])

            if pr_column[row] == "random":
                last_random_stimulus = stimulus_column[row]

        print("OK")

    def validate_stimulus(self, data_table):
        print("Validate stimulus...")

        pr_column = data_table["pattern_or_random"]
        stimulus_column = data_table["stimulus"]
        trial_column = data_table["trial"]
        self.assertTrue(len(stimulus_column) > 0)
        self.assertEqual(len(stimulus_column), len(pr_column))
        self.assertEqual(len(stimulus_column), len(trial_column))

        PCode = str(data_table["PCode"][0])
        dict_next_stimulus = {}
        dict_next_stimulus[PCode[0]] = PCode[1]
        dict_next_stimulus[PCode[1]] = PCode[2]
        dict_next_stimulus[PCode[2]] = PCode[3]
        dict_next_stimulus[PCode[3]] = PCode[0]

        last_pattern_stimulus = 0
        for row in range(len(stimulus_column)):
            self.assertTrue(stimulus_column[row] in [1, 2, 3, 4])
            if pr_column[row] == "pattern":
                if trial_column[row] > 1 and stimulus_column[row] != last_pattern_stimulus:
                    self.assertEqual(str(stimulus_column[row]), dict_next_stimulus[str(last_pattern_stimulus)])
                last_pattern_stimulus = stimulus_column[row]

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

    def validate_trial_phase_local(self, data_table):
        print("Validate trial phase local...")

        trial_phase_column = data_table["trial_phase"]
        self.assertTrue(len(trial_phase_column) > 0)

        for i in range(len(trial_phase_column)):
            self.assertTrue(trial_phase_column[i] in ["before_stimulus", "stimulus_on_screen", "after_reaction"])
            if i > 0 and trial_phase_column[i] != trial_phase_column[i - 1]:
                if trial_phase_column[i] == "before_stimulus":
                    self.assertTrue(trial_phase_column[i - 1] == "after_reaction" or trial_phase_column[i - 1] == "stimulus_on_screen")
                elif trial_phase_column[i] == "stimulus_on_screen":
                    self.assertEqual(trial_phase_column[i - 1], "before_stimulus")
                elif trial_phase_column[i] == "after_reaction":
                    self.assertTrue(trial_phase_column[i - 1] == "before_stimulus" or trial_phase_column[i - 1] == "stimulus_on_screen")

        print("OK")

    def validate_trial_phase_global(self, data_table):
        print("Validate trial phase global...")

        trial_phase_column = data_table["trial_phase"]
        RSI_column = data_table["RSI_time"]
        self.assertTrue(len(trial_phase_column) > 0)
        self.assertEqual(len(trial_phase_column), len(RSI_column))

        for i in range(len(trial_phase_column)):
            self.assertTrue(trial_phase_column[i] in ["before_stimulus", "stimulus_on_screen", "after_reaction"])
            # in the begining of the trial we have before stimulus state
            if RSI_column[i] == "-1":
                self.assertEqual(trial_phase_column[i], "before_stimulus")
            else:
                self.assertTrue(trial_phase_column[i] in ["stimulus_on_screen", "after_reaction"])

        print("OK")

    def validate_gaze_data_ADCS_local(self, data_table):
        print("Validate gaze data in ADCS (local)...")

        for gaze_data_string in ["left_gaze_data_X_ADCS", "left_gaze_data_Y_ADCS", "right_gaze_data_X_ADCS", "right_gaze_data_Y_ADCS"]:
            gaze_data_column = data_table[gaze_data_string]
            self.assertEqual(len(data_table["left_gaze_data_X_ADCS"]), len(gaze_data_column))

            for i in range(len(gaze_data_column)):
                gaze_data = gaze_data_column[i]
                if isinstance(gaze_data, str):
                    self.assertTrue(float(gaze_data.replace(",", ".")) > -0.2)
                    self.assertTrue(float(gaze_data.replace(",", ".")) < 2.2)
                elif isinstance(gaze_data, float):
                    self.assertTrue(math.isnan(gaze_data))

        print("OK")

    def validate_gaze_data_ADCS_global(self, data_table):
        print("Validate gaze data in ADCS (global)...")

        left_gaze_X_column = data_table["left_gaze_data_X_ADCS"]
        left_gaze_Y_column = data_table["left_gaze_data_Y_ADCS"]
        right_gaze_X_column = data_table["right_gaze_data_X_ADCS"]
        right_gaze_Y_column = data_table["right_gaze_data_Y_ADCS"]

        for i in range(len(left_gaze_X_column)):
            left_gaze_X = left_gaze_X_column[i]
            left_gaze_Y = left_gaze_Y_column[i]
            right_gaze_X = right_gaze_X_column[i]
            right_gaze_Y = right_gaze_Y_column[i]

            self.assertEqual(isinstance(left_gaze_X, str), isinstance(left_gaze_Y, str))
            self.assertEqual(isinstance(left_gaze_X, float), isinstance(left_gaze_Y, float))

            self.assertEqual(isinstance(right_gaze_X, str), isinstance(right_gaze_Y, str))
            self.assertEqual(isinstance(right_gaze_X, float), isinstance(right_gaze_Y, float))

            if data_table["left_gaze_validity"][i]:
                self.assertTrue(isinstance(left_gaze_X, str))
                self.assertTrue(isinstance(left_gaze_Y, str))
            else:
                self.assertTrue(isinstance(left_gaze_X, float))
                self.assertTrue(isinstance(left_gaze_Y, float))

            if data_table["right_gaze_validity"][i]:
                self.assertTrue(isinstance(right_gaze_X, str))
                self.assertTrue(isinstance(right_gaze_Y, str))
            else:
                self.assertTrue(isinstance(right_gaze_X, float))
                self.assertTrue(isinstance(right_gaze_Y, float))

        print("OK")

    def validate_gaze_data_PCMCS_local(self, data_table):
        print("Validate gaze data in PCMCS (local)...")

        monitor_width = 53.7

        for gaze_data_string in ["left_gaze_data_X_PCMCS", "left_gaze_data_Y_PCMCS", "right_gaze_data_X_PCMCS", "right_gaze_data_Y_PCMCS"]:
            gaze_data_column = data_table[gaze_data_string]
            self.assertEqual(len(data_table["left_gaze_data_X_PCMCS"]), len(gaze_data_column))

            for i in range(len(gaze_data_column)):
                gaze_data = gaze_data_column[i]
                if isinstance(gaze_data, str):
                    self.assertTrue(float(gaze_data.replace(",", ".")) > -monitor_width)
                    self.assertTrue(float(gaze_data.replace(",", ".")) < monitor_width)
                elif isinstance(gaze_data, float):
                    self.assertTrue(math.isnan(gaze_data))

        print("OK")

    def validate_gaze_data_PCMCS_global(self, data_table):
        print("Validate gaze data in PCMCS (global)...")

        left_gaze_X_column = data_table["left_gaze_data_X_PCMCS"]
        left_gaze_Y_column = data_table["left_gaze_data_Y_PCMCS"]
        right_gaze_X_column = data_table["right_gaze_data_X_PCMCS"]
        right_gaze_Y_column = data_table["right_gaze_data_Y_PCMCS"]

        for i in range(len(left_gaze_X_column)):
            left_gaze_X = left_gaze_X_column[i]
            left_gaze_Y = left_gaze_Y_column[i]
            right_gaze_X = right_gaze_X_column[i]
            right_gaze_Y = right_gaze_Y_column[i]

            self.assertEqual(isinstance(left_gaze_X, str), isinstance(left_gaze_Y, str))
            self.assertEqual(isinstance(left_gaze_X, float), isinstance(left_gaze_Y, float))

            self.assertEqual(isinstance(right_gaze_X, str), isinstance(right_gaze_Y, str))
            self.assertEqual(isinstance(right_gaze_X, float), isinstance(right_gaze_Y, float))

            if data_table["left_gaze_validity"][i]:
                self.assertTrue(isinstance(left_gaze_X, str))
                self.assertTrue(isinstance(left_gaze_Y, str))
            else:
                self.assertTrue(isinstance(left_gaze_X, float))
                self.assertTrue(isinstance(left_gaze_Y, float))

            if data_table["right_gaze_validity"][i]:
                self.assertTrue(isinstance(right_gaze_X, str))
                self.assertTrue(isinstance(right_gaze_Y, str))
            else:
                self.assertTrue(isinstance(right_gaze_X, float))
                self.assertTrue(isinstance(right_gaze_Y, float))

        print("OK")

    def validate_pupil_data_local(self, data_table):
        print("Validate pupil data (local)...")

        for pupil_data_string in ["left_pupil_diameter", "right_pupil_diameter"]:
            pupil_data_column = data_table[pupil_data_string]
            self.assertEqual(len(data_table["left_pupil_diameter"]), len(data_table["right_pupil_diameter"]))

            minus_pupil_counter = 0
            for i in range(len(pupil_data_column)):
                if i > 0 and data_table["trial"][i - 1] != data_table["trial"][i]:
                    minus_pupil_counter = 0

                pupil_data = pupil_data_column[i]
                if isinstance(pupil_data, str):
                    if pupil_data == "-1,0":
                        minus_pupil_counter += 1
                        self.assertTrue(minus_pupil_counter <= 2)
                    else:
                        self.assertTrue(float(pupil_data.replace(",", ".")) > 0.0)
                        self.assertTrue(float(pupil_data.replace(",", ".")) < 5.0)
                        minus_pupil_counter = 0
                elif isinstance(pupil_data, float):
                    self.assertTrue(math.isnan(pupil_data))
                    minus_pupil_counter = 0

        print("OK")

    def validate_pupil_data_global(self, data_table):
        print("Validate pupil data (global)...")

        left_pupil_column = data_table["left_pupil_diameter"]
        right_pupil_column = data_table["right_pupil_diameter"]

        for i in range(len(left_pupil_column)):

            if data_table["left_pupil_validity"][i]:
                self.assertTrue(isinstance(left_pupil_column[i], str))
            else:
                self.assertTrue(isinstance(left_pupil_column[i], float))

            if data_table["right_pupil_validity"][i]:
                self.assertTrue(isinstance(right_pupil_column[i], str))
            else:
                self.assertTrue(isinstance(right_pupil_column[i], float))

        print("OK")

    def validate_validity_flag(self, data_table):
        print("Validate validity flag...")

        left_gaze_validity = data_table["left_gaze_validity"]
        right_gaze_validity = data_table["right_gaze_validity"]
        left_pupil_validity = data_table["left_pupil_validity"]
        right_pupil_validity = data_table["right_pupil_validity"]

        for i in range(len(left_gaze_validity)):
            self.assertTrue(left_gaze_validity[i] in [0, 1])
            self.assertTrue(right_gaze_validity[i] in [0, 1])
            self.assertTrue(left_pupil_validity[i] in [0, 1])
            self.assertTrue(right_pupil_validity[i] in [0, 1])

            self.assertEqual(left_gaze_validity[i], left_pupil_validity[i])
            self.assertEqual(right_gaze_validity[i], right_pupil_validity[i])

        print("OK")

    def validate_gaze_timestamp(self, data_table):
        print("Validate gaze timesstamp...")

        for timestamp in data_table["gaze_data_time_stamp"]:
            self.assertTrue(timestamp > 0)
            self.assertTrue(timestamp < 10000000000)

        for i in range(1, len(data_table["gaze_data_time_stamp"])):
            self.assertTrue(data_table["gaze_data_time_stamp"][i] > data_table["gaze_data_time_stamp"][i - 1])
            if data_table["trial"][i] == data_table["trial"][i - 1]:
                self.assertTrue(data_table["gaze_data_time_stamp"][i] - data_table["gaze_data_time_stamp"][i - 1] < 50000)

        print("OK")

    def validate_stim_pos_PCMCS(self, data_table):
        print("Validate stim pos in PCMCS...")

        stim_distance = 15
        for data in data_table["stimulus_1_position_X_PCMCS"]:
            self.assertEqual(data, str(-stim_distance / 2).replace(".", ","))

        for data in data_table["stimulus_1_position_Y_PCMCS"]:
            self.assertEqual(data, str(-stim_distance / 2).replace(".", ","))

        for data in data_table["stimulus_2_position_X_PCMCS"]:
            self.assertEqual(data, str(stim_distance / 2).replace(".", ","))

        for data in data_table["stimulus_2_position_Y_PCMCS"]:
            self.assertEqual(data, str(-stim_distance / 2).replace(".", ","))

        for data in data_table["stimulus_3_position_X_PCMCS"]:
            self.assertEqual(data, str(-stim_distance / 2).replace(".", ","))

        for data in data_table["stimulus_3_position_Y_PCMCS"]:
            self.assertEqual(data, str(stim_distance / 2).replace(".", ","))

        for data in data_table["stimulus_4_position_X_PCMCS"]:
            self.assertEqual(data, str(stim_distance / 2).replace(".", ","))

        for data in data_table["stimulus_4_position_Y_PCMCS"]:
            self.assertEqual(data, str(stim_distance / 2).replace(".", ","))

        print("OK")

    def validate_quit_log(self, data_table):
        print("Validate quit log...")

        for data in data_table["quit_log"]:
            if isinstance(data, float):
                self.assertTrue(math.isnan(data))
            else:
                self.assertTrue(data in ["sessionend_planned_quit", "user_quit"])

        print("OK")

    def validate(self, file_name):
        data_table = pandas.read_csv(file_name, sep='\t')

        #self.validate_computer_name(data_table)
        #self.validate_monitor_width(data_table)
        #self.validate_monitor_height(data_table)
        #self.validate_subject_group(data_table)
        #self.validate_subject_number(data_table)
        #self.validate_subject_sex(data_table)
        #self.validate_subject_age(data_table)
        #self.validate_asrt_type(data_table)
        #self.validate_PCode(data_table)
        #self.validate_session(data_table)
        #self.validate_epoch_block_relation(data_table)
        #self.validate_block_trial_relation(data_table)
        #self.validate_trial_RSI_relation(data_table)
        #self.validate_RSI_trial_phase_relation(data_table)
        #self.validate_frame_rate(data_table)
        #self.validate_frame_time(data_table)
        #self.validate_frame_sd(data_table)
        #self.validate_stimulus_color(data_table)
        #self.validate_trial_type_pr(data_table)
        self.validate_triplet_type_hl(data_table)
        self.validate_stimulus(data_table)
        # self.validate_RSI_interval_sampling(data_table)
        self.validate_trial_phase_local(data_table)
        self.validate_trial_phase_global(data_table)
        self.validate_gaze_data_ADCS_local(data_table)
        self.validate_gaze_data_ADCS_global(data_table)
        self.validate_gaze_data_PCMCS_local(data_table)
        self.validate_gaze_data_PCMCS_global(data_table)
        self.validate_pupil_data_local(data_table)
        self.validate_pupil_data_global(data_table)
        self.validate_validity_flag(data_table)
        # self.validate_gaze_timestamp(data_table)
        self.validate_stim_pos_PCMCS(data_table)
        self.validate_quit_log(data_table)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You need to specify the path of an output txt file.")

    if not os.path.isfile(sys.argv[1]):
        print("The passed parameter should be a valid file's path: " + sys.argv[1])

    output_validation = OutputValidation()
    output_validation.validate(sys.argv[1])
