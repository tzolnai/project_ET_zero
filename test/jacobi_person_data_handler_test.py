# !/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) <2019-2021>  <Tamás Zolnai>    <zolnaitamas2000@gmail.com>

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

import sys
import os
# Add the local path to the main script so we can import it.
sys.path = [".."] + sys.path

import unittest
import asrt
import time
import shelve
import dbm
import codecs
from psychopy import monitors


class jacobiPersonDataHandlerTest(unittest.TestCase):

    def tearDown(self):
        tempdir = os.path.abspath(__file__)
        (tempdir, trail) = os.path.split(tempdir)
        tempdir = os.path.join(tempdir, "data", "person_data_handler")

        # remove all temp files
        for file in os.listdir(tempdir):
            file_path = os.path.join(tempdir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def setUp(self):
        self.maxDiff = None
        self.my_monitor = monitors.Monitor('myMon')
        self.my_monitor.setSizePix([1366, 768])
        self.my_monitor.setWidth(29)
        self.my_monitor.saveMon()

        tempdir = os.path.abspath(__file__)
        (tempdir, trail) = os.path.split(tempdir)
        tempdir = os.path.join(tempdir, "data", "person_data_handler")
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)

    def constructFilePath(self, file_name):
        this_file_path = os.path.abspath(__file__)
        file_path = os.path.split(this_file_path)[0]
        file_path = os.path.join(file_path, "data")
        file_path = os.path.join(file_path, "person_data_handler")
        file_path = os.path.join(file_path, file_name)
        return file_path

    def testAddFileHeader(self):
        output_file_path = self.constructFilePath("testAddFileHeader.txt")
        person_data_handler = asrt.PersonDataHandler(
            "subject_333_group_1", "", "", "", "", "eye-tracking", output_file_path, "")

        with codecs.open(person_data_handler.jacobi_output_file_path, 'w', encoding='utf-8') as output_file:
            person_data_handler.add_jacobi_heading_to_output(output_file)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group"
                                                 "\tsubject_number\tsubject_sex\tsubject_age\tasrt_type\tPCode\ttest_type"
                                                 "\trun\ttrial\tframe_rate\tframe_time\tframe_sd\tresponse\t")

    def testAddFileHeaderET(self):
        output_file_path = self.constructFilePath("testAddFileHeaderET.txt")
        person_data_handler = asrt.PersonDataHandler(
            "subject_333_group_1", "", "", "", "", "eye-tracking", "", output_file_path)

        with codecs.open(person_data_handler.jacobi_ET_output_file_path, 'w', encoding='utf-8') as output_file:
            person_data_handler.add_jacobi_ET_heading_to_output(output_file)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group"
                                                 "\tsubject_number\tsubject_sex\tsubject_age\tasrt_type\tPCode\ttest_type"
                                                 "\trun\ttrial\tframe_rate\tframe_time\tframe_sd\ttrial_phase\tleft_gaze_data_X_ADCS"
                                                 "\tleft_gaze_data_Y_ADCS\tright_gaze_data_X_ADCS\tright_gaze_data_Y_ADCS"
                                                 "\tleft_gaze_data_X_PCMCS\tleft_gaze_data_Y_PCMCS\tright_gaze_data_X_PCMCS"
                                                 "\tright_gaze_data_Y_PCMCS\tleft_eye_distance\tright_eye_distance\tleft_gaze_validity"
                                                 "\tright_gaze_validity\tleft_pupil_diameter\tright_pupil_diameter\tleft_pupil_validity"
                                                 "\tright_pupil_validity\tgaze_data_time_stamp\tstimulus_1_position_X_PCMCS"
                                                 "\tstimulus_1_position_Y_PCMCS\tstimulus_2_position_X_PCMCS\tstimulus_2_position_Y_PCMCS"
                                                 "\tstimulus_3_position_X_PCMCS\tstimulus_3_position_Y_PCMCS\tstimulus_4_position_X_PCMCS"
                                                 "\tstimulus_4_position_Y_PCMCS\t")

    def testWriteEmptyOutput(self):
        output_file_path = self.constructFilePath("testWriteEmptyOutput.txt")
        person_data_handler = asrt.PersonDataHandler(
            "subject_333_group1", "", "", "", "", "eye-tracking", output_file_path, "")

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.computer_name = "Laposka"
        experiment.settings.epochN = 2
        experiment.subject_group = "group1"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit'}
        experiment.PCodes = {1: '1st - 1234', 2: '1st - 1234'}
        experiment.mymonitor = self.my_monitor

        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3

        jacobi_test_phase = 'inclusion'
        jacobi_run = 1
        jacobi_trial = 4
        response = 2

        person_data_handler.jacobi_output_data_buffer.append([jacobi_test_phase, jacobi_run, jacobi_trial, response])

        person_data_handler.flush_jacobi_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel"
                                                 "\tsubject_group\tsubject_number\tsubject_sex\tsubject_age"
                                                 "\tasrt_type\tPCode\ttest_type\trun\ttrial\tframe_rate\tframe_time"
                                                 "\tframe_sd\tresponse\t\n"
                                                 "Laposka\t1366\t768\tgroup1\t333\tmale\t25\timplicit\t1234\tinclusion"
                                                 "\t1\t4\t59,1\t16,56\t1,3\t2\t")

    def testWriteEmptyOutputET(self):
        output_file_path = self.constructFilePath("testWriteEmptyOutputET.txt")
        person_data_handler = asrt.PersonDataHandler(
            "subject_333_group1", "", "", "", "", "eye-tracking", "", output_file_path)

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.computer_name = "Laposka"
        experiment.settings.epochN = 2
        experiment.settings.monitor_width = 47.6
        experiment.subject_group = "group1"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit'}
        experiment.PCodes = {1: '1st - 1234', 2: '1st - 1234'}
        experiment.mymonitor = self.my_monitor

        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3

        jacobi_test_phase = 'inclusion'
        jacobi_run = 1
        jacobi_trial = 4
        jacobi_trial_phase = 'before_reaction'
        time_stamp = 10000
        experiment.dict_pos = {1: (-0.5, -0.5), 2: (0.5, -0.5), 3: (-0.5, 0.5), 4: (0.5, 0.5)}

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_origin_in_user_coordinate_system'] = (10, 10, 9)
        gazeData['right_gaze_origin_in_user_coordinate_system'] = (10, 10, 6)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = 1
        gazeData['right_pupil_validity'] = 1

        person_data_handler.output_data_buffer.append([jacobi_test_phase, jacobi_run, jacobi_trial, jacobi_trial_phase, gazeData, time_stamp])

        person_data_handler.flush_jacobi_ET_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group"
                                                 "\tsubject_number\tsubject_sex\tsubject_age\tasrt_type\tPCode"
                                                 "\ttest_type\trun\ttrial\tframe_rate\tframe_time\tframe_sd\ttrial_phase"
                                                 "\tleft_gaze_data_X_ADCS\tleft_gaze_data_Y_ADCS\tright_gaze_data_X_ADCS\tright_gaze_data_Y_ADCS"
                                                 "\tleft_gaze_data_X_PCMCS\tleft_gaze_data_Y_PCMCS\tright_gaze_data_X_PCMCS"
                                                 "\tright_gaze_data_Y_PCMCS\tleft_eye_distance\tright_eye_distance\tleft_gaze_validity"
                                                 "\tright_gaze_validity\tleft_pupil_diameter\tright_pupil_diameter\tleft_pupil_validity"
                                                 "\tright_pupil_validity\tgaze_data_time_stamp\tstimulus_1_position_X_PCMCS\tstimulus_1_position_Y_PCMCS"
                                                 "\tstimulus_2_position_X_PCMCS\tstimulus_2_position_Y_PCMCS\tstimulus_3_position_X_PCMCS"
                                                 "\tstimulus_3_position_Y_PCMCS\tstimulus_4_position_X_PCMCS\tstimulus_4_position_Y_PCMCS\t\n"
                                                 "Laposka\t1366\t768\tgroup1\t333\tmale\t25\timplicit\t1234\tinclusion\t1\t4\t59,1\t16,56"
                                                 "\t1,3\tbefore_reaction\t0,5\t0,5\t0,5\t0,5\t0,0\t-0,0\t0,0\t-0,0\t9\t6\tTrue\tTrue"
                                                 "\t3\t3\tTrue\tTrue\t10000\t-0,5\t-0,5\t0,5\t-0,5\t-0,5\t0,5\t0,5\t0,5\t")

    def testWriteDataWithZeroRun(self):
        output_file_path = self.constructFilePath("testWriteDataWithZeroRun.txt")
        person_data_handler = asrt.PersonDataHandler(
            "subject_333_group1", "", "", "", "", "eye-tracking", output_file_path, "")

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.computer_name = "Laposka"
        experiment.settings.epochN = 2
        experiment.subject_group = "group1"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit'}
        experiment.PCodes = {1: '1st - 1234', 2: '1st - 1234'}
        experiment.mymonitor = self.my_monitor

        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3

        jacobi_test_phase = 'inclusion'
        jacobi_run = 1
        jacobi_trial = 0
        response = 2

        person_data_handler.jacobi_output_data_buffer.append([jacobi_test_phase, jacobi_run, jacobi_trial, response])

        person_data_handler.flush_jacobi_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel"
                                                 "\tsubject_group\tsubject_number\tsubject_sex\tsubject_age"
                                                 "\tasrt_type\tPCode\ttest_type\trun\ttrial\tframe_rate\tframe_time"
                                                 "\tframe_sd\tresponse\t")

    def testWriteETDataWithZeroRun(self):
        output_file_path = self.constructFilePath("testWriteETDataWithZeroRun.txt")
        person_data_handler = asrt.PersonDataHandler(
            "subject_333_group1", "", "", "", "", "eye-tracking", "", output_file_path)

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.computer_name = "Laposka"
        experiment.settings.epochN = 2
        experiment.settings.monitor_width = 47.6
        experiment.subject_group = "group1"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit'}
        experiment.PCodes = {1: '1st - 1234', 2: '1st - 1234'}
        experiment.mymonitor = self.my_monitor

        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3

        jacobi_test_phase = 'inclusion'
        jacobi_run = 1
        jacobi_trial = 0
        jacobi_trial_phase = 'before_reaction'
        time_stamp = 10000
        experiment.dict_pos = {1: (-0.5, -0.5), 2: (0.5, -0.5), 3: (-0.5, 0.5), 4: (0.5, 0.5)}

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_origin_in_user_coordinate_system'] = (10, 10, 9)
        gazeData['right_gaze_origin_in_user_coordinate_system'] = (10, 10, 6)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = 1
        gazeData['right_pupil_validity'] = 1

        person_data_handler.output_data_buffer.append([jacobi_test_phase, jacobi_run, jacobi_trial, jacobi_trial_phase, gazeData, time_stamp])

        person_data_handler.flush_jacobi_ET_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group"
                                                 "\tsubject_number\tsubject_sex\tsubject_age\tasrt_type\tPCode"
                                                 "\ttest_type\trun\ttrial\tframe_rate\tframe_time\tframe_sd\ttrial_phase"
                                                 "\tleft_gaze_data_X_ADCS\tleft_gaze_data_Y_ADCS\tright_gaze_data_X_ADCS\tright_gaze_data_Y_ADCS"
                                                 "\tleft_gaze_data_X_PCMCS\tleft_gaze_data_Y_PCMCS\tright_gaze_data_X_PCMCS"
                                                 "\tright_gaze_data_Y_PCMCS\tleft_eye_distance\tright_eye_distance\tleft_gaze_validity"
                                                 "\tright_gaze_validity\tleft_pupil_diameter\tright_pupil_diameter\tleft_pupil_validity"
                                                 "\tright_pupil_validity\tgaze_data_time_stamp\tstimulus_1_position_X_PCMCS\tstimulus_1_position_Y_PCMCS"
                                                 "\tstimulus_2_position_X_PCMCS\tstimulus_2_position_Y_PCMCS\tstimulus_3_position_X_PCMCS"
                                                 "\tstimulus_3_position_Y_PCMCS\tstimulus_4_position_X_PCMCS\tstimulus_4_position_Y_PCMCS\t")

    def testInvalidETDataOutput(self):
        output_file_path = self.constructFilePath("testWriteEmptyOutputET.txt")
        person_data_handler = asrt.PersonDataHandler(
            "subject_333_group1", "", "", "", "", "eye-tracking", "", output_file_path)

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.computer_name = "Laposka"
        experiment.settings.epochN = 2
        experiment.settings.monitor_width = 47.6
        experiment.subject_group = "group1"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit'}
        experiment.PCodes = {1: '1st - 1234', 2: '1st - 1234'}
        experiment.mymonitor = self.my_monitor

        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3

        jacobi_test_phase = 'inclusion'
        jacobi_run = 1
        jacobi_trial = 4
        jacobi_trial_phase = 'before_reaction'
        time_stamp = 10000
        experiment.dict_pos = {1: (-0.5, -0.5), 2: (0.5, -0.5), 3: (-0.5, 0.5), 4: (0.5, 0.5)}

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_origin_in_user_coordinate_system'] = (10, 10, 9)
        gazeData['right_gaze_origin_in_user_coordinate_system'] = (10, 10, 6)
        gazeData['left_gaze_point_validity'] = 0
        gazeData['right_gaze_point_validity'] = 0
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = 1
        gazeData['right_pupil_validity'] = 1

        person_data_handler.output_data_buffer.append([jacobi_test_phase, jacobi_run, jacobi_trial, jacobi_trial_phase, gazeData, time_stamp])

        person_data_handler.flush_jacobi_ET_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group"
                                                 "\tsubject_number\tsubject_sex\tsubject_age\tasrt_type\tPCode"
                                                 "\ttest_type\trun\ttrial\tframe_rate\tframe_time\tframe_sd\ttrial_phase"
                                                 "\tleft_gaze_data_X_ADCS\tleft_gaze_data_Y_ADCS\tright_gaze_data_X_ADCS\tright_gaze_data_Y_ADCS"
                                                 "\tleft_gaze_data_X_PCMCS\tleft_gaze_data_Y_PCMCS\tright_gaze_data_X_PCMCS"
                                                 "\tright_gaze_data_Y_PCMCS\tleft_eye_distance\tright_eye_distance\tleft_gaze_validity"
                                                 "\tright_gaze_validity\tleft_pupil_diameter\tright_pupil_diameter\tleft_pupil_validity"
                                                 "\tright_pupil_validity\tgaze_data_time_stamp\tstimulus_1_position_X_PCMCS\tstimulus_1_position_Y_PCMCS"
                                                 "\tstimulus_2_position_X_PCMCS\tstimulus_2_position_Y_PCMCS\tstimulus_3_position_X_PCMCS"
                                                 "\tstimulus_3_position_Y_PCMCS\tstimulus_4_position_X_PCMCS\tstimulus_4_position_Y_PCMCS\t\n"
                                                 "Laposka\t1366\t768\tgroup1\t333\tmale\t25\timplicit\t1234\tinclusion\t1\t4\t59,1\t16,56"
                                                 "\t1,3\tbefore_reaction\t0,5\t0,5\t0,5\t0,5\tnan\tnan\tnan\tnan\t9\t6\tFalse\tFalse"
                                                 "\t3\t3\tTrue\tTrue\t10000\t-0,5\t-0,5\t0,5\t-0,5\t-0,5\t0,5\t0,5\t0,5\t")


if __name__ == "__main__":
    unittest.main()  # run all tests
