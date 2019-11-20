# !/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) <2019>  <Tamás Zolnai>    <zolnaitamas2000@gmail.com>

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


class personDataHandlerTest(unittest.TestCase):

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

    def testRoundTripPersonSettings(self):
        all_settings_file_path = self.constructFilePath(
            "testRoundTripSettings")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", all_settings_file_path, "", "", "", "")

        experiment = asrt.Experiment("")

        experiment.PCodes = {1: '3rd - 1324'}
        experiment.subject_sex = 'male'
        experiment.subject_age = '31'
        experiment.stim_output_line = 1
        experiment.stim_sessionN = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1,
                                    7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        experiment.stimepoch = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1,
                                7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        experiment.stimblock = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1,
                                7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        experiment.stimtrial = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7,
                                8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15}
        experiment.stimlist = {1: 3, 2: 1, 3: 2, 4: 3, 5: 2, 6: 2,
                               7: 2, 8: 4, 9: 1, 10: 1, 11: 4, 12: 3, 13: 3, 14: 2, 15: 2}
        experiment.stimpr = {1: 'random', 2: 'random', 3: 'random', 4: 'random', 5: 'random', 6: 'pattern', 7: 'random',
                             8: 'pattern', 9: 'random', 10: 'pattern', 11: 'random', 12: 'pattern', 13: 'random', 14: 'pattern', 15: 'random'}
        experiment.last_N = 1
        experiment.end_at = {1: 16, 2: 16, 3: 16, 4: 16, 5: 16, 6: 16, 7: 16,
                             8: 16, 9: 16, 10: 16, 11: 16, 12: 16, 13: 16, 14: 16, 15: 16}

        person_data_handler.save_person_settings(experiment)

        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", all_settings_file_path, "", "", "", "")

        person_data_handler.load_person_settings(experiment)

        self.assertEqual(experiment.PCodes, {1: '3rd - 1324'})
        self.assertEqual(experiment.stim_output_line, 1)
        self.assertEqual(experiment.subject_sex, 'male')
        self.assertEqual(experiment.subject_age, '31')
        self.assertEqual(experiment.stim_sessionN, {
                         1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1})
        self.assertEqual(experiment.stimepoch, {
                         1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1})
        self.assertEqual(experiment.stimblock, {
                         1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1})
        self.assertEqual(experiment.stimtrial, {
                         1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15})
        self.assertEqual(experiment.stimlist, {
                         1: 3, 2: 1, 3: 2, 4: 3, 5: 2, 6: 2, 7: 2, 8: 4, 9: 1, 10: 1, 11: 4, 12: 3, 13: 3, 14: 2, 15: 2})
        self.assertEqual(experiment.stimpr, {1: 'random', 2: 'random', 3: 'random', 4: 'random', 5: 'random', 6: 'pattern',
                                             7: 'random', 8: 'pattern', 9: 'random', 10: 'pattern', 11: 'random', 12: 'pattern', 13: 'random', 14: 'pattern', 15: 'random'})
        self.assertEqual(experiment.last_N, 1)
        self.assertEqual(experiment.end_at, {1: 16, 2: 16, 3: 16, 4: 16, 5: 16, 6: 16,
                                             7: 16, 8: 16, 9: 16, 10: 16, 11: 16, 12: 16, 13: 16, 14: 16, 15: 16})

    def testReadMissingPersonSettings(self):
        all_settings_file_path = self.constructFilePath(
            "testReadMissingPersonSettings")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", all_settings_file_path, "", "", "", "")

        experiment = asrt.Experiment("")

        person_data_handler.load_person_settings(experiment)

        self.assertEqual(experiment.PCodes, {})
        self.assertEqual(experiment.subject_sex, None)
        self.assertEqual(experiment.subject_age, None)
        self.assertEqual(experiment.stim_output_line, 0)
        self.assertEqual(experiment.stim_sessionN, {})
        self.assertEqual(experiment.stimepoch, {})
        self.assertEqual(experiment.stimblock, {})
        self.assertEqual(experiment.stimtrial, {})
        self.assertEqual(experiment.stimlist, {})
        self.assertEqual(experiment.stimpr, {})
        self.assertEqual(experiment.last_N, 0)
        self.assertEqual(experiment.end_at, {})

    def testReadIncompletePersonSettings(self):
        all_settings_file_path = self.constructFilePath(
            "testReadIncompletePersonSettings")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", all_settings_file_path, "", "", "", "")

        experiment = asrt.Experiment("")

        # save something, but not all settings
        with shelve.open(all_settings_file_path, 'n') as all_settings_file:
            this_person_settings = {}
            this_person_settings['PCodes'] = {1: '3rd - 1324'}
            this_person_settings['stim_output_line'] = 12

            all_settings = {}
            all_settings["alattomos-aladar_333_group1"] = this_person_settings

            all_settings_file['all_settings'] = all_settings

        person_data_handler.load_person_settings(experiment)

        self.assertEqual(experiment.PCodes, {})
        self.assertEqual(experiment.subject_sex, None)
        self.assertEqual(experiment.subject_age, None)
        self.assertEqual(experiment.stim_output_line, 0)
        self.assertEqual(experiment.stim_sessionN, {})
        self.assertEqual(experiment.stimepoch, {})
        self.assertEqual(experiment.stimblock, {})
        self.assertEqual(experiment.stimtrial, {})
        self.assertEqual(experiment.stimlist, {})
        self.assertEqual(experiment.stimpr, {})
        self.assertEqual(experiment.last_N, 0)
        self.assertEqual(experiment.end_at, {})

    def testUpdateExistingPersonSettings(self):
        all_settings_file_path = self.constructFilePath(
            "testUpdateExistingPersonSettings")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", all_settings_file_path, "", "", "", "")

        experiment = asrt.Experiment("")

        experiment.PCodes = {1: '3rd - 1324'}
        experiment.subject_sex = 'male'
        experiment.subject_age = '31'
        experiment.stim_output_line = 1
        experiment.stim_sessionN = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1,
                                    7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        experiment.stimepoch = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1,
                                7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        experiment.stimblock = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1,
                                7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        experiment.stimtrial = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7,
                                8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15}
        experiment.stimlist = {1: 3, 2: 1, 3: 2, 4: 3, 5: 2, 6: 2,
                               7: 2, 8: 4, 9: 1, 10: 1, 11: 4, 12: 3, 13: 3, 14: 2, 15: 2}
        experiment.stimpr = {1: 'random', 2: 'random', 3: 'random', 4: 'random', 5: 'random', 6: 'pattern', 7: 'random',
                             8: 'pattern', 9: 'random', 10: 'pattern', 11: 'random', 12: 'pattern', 13: 'random', 14: 'pattern', 15: 'random'}
        experiment.last_N = 1
        experiment.end_at = {1: 16, 2: 16, 3: 16, 4: 16, 5: 16, 6: 16, 7: 16,
                             8: 16, 9: 16, 10: 16, 11: 16, 12: 16, 13: 16, 14: 16, 15: 16}

        person_data_handler.save_person_settings(experiment)

        experiment.stim_output_line = 41
        experiment.last_N = 32
        person_data_handler.save_person_settings(experiment)

        person_data_handler.load_person_settings(experiment)

        self.assertEqual(experiment.stim_output_line, 41)
        self.assertEqual(experiment.last_N, 32)

    def testCreateAllSubjectFiles(self):
        all_IDs_file_path = self.constructFilePath("testCreateAllSubjectFiles")
        subject_list_file_path = self.constructFilePath("testCreateIDsFiles.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", all_IDs_file_path, subject_list_file_path, "", "")

        person_data_handler.update_all_subject_attributes_files("male", "25", ['1th - 1234', '2nd - 1243'])

        # output files exist
        self.assertTrue(os.path.exists(all_IDs_file_path + ".dat")
                        or os.path.exists(all_IDs_file_path))
        self.assertTrue(os.path.exists(subject_list_file_path))

        with shelve.open(all_IDs_file_path) as all_subject_file:
            self.assertEqual(all_subject_file['ids'], ["alattomos-aladar_333_group1"])
            self.assertEqual(all_subject_file["alattomos-aladar_333_group1"], ['male', '25', ['1th - 1234', '2nd - 1243']])

        with codecs.open(subject_list_file_path, 'r', encoding='utf-8') as subject_list_txt:
            self.assertEqual(subject_list_txt.read(),
                             "subject_name\tsubject_id\tsubject_group\tsubject_sex\tsubject_age\tsubject_PCodes\n"
                             "alattomos-aladar\t333\tgroup1\tmale\t25\t['1th - 1234', '2nd - 1243']\n")

    def testAddSameSubjectToAllSubjectFiles(self):
        all_IDs_file_path = self.constructFilePath("testAddSameSubjectToAllSubjectFiles")
        subject_list_file_path = self.constructFilePath("testAddSameSubjectToAllSubjectFiles.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", all_IDs_file_path, subject_list_file_path, "", "")

        # call this twice simulating of running the experiment with the same subject more times
        person_data_handler.update_all_subject_attributes_files("male", "25", ['1th - 1234', '2nd - 1243'])
        person_data_handler.update_all_subject_attributes_files("female", "35", ['1th - 1243', '2nd - 1234'])

        # output files exist
        self.assertTrue(os.path.exists(all_IDs_file_path + ".dat")
                        or os.path.exists(all_IDs_file_path))
        self.assertTrue(os.path.exists(subject_list_file_path))

        with shelve.open(all_IDs_file_path) as all_subject_file:
            self.assertEqual(all_subject_file['ids'], ["alattomos-aladar_333_group1"])
            self.assertEqual(all_subject_file["alattomos-aladar_333_group1"], ['male', '25', ['1th - 1234', '2nd - 1243']])

        with codecs.open(subject_list_file_path, 'r', encoding='utf-8') as subject_list_txt:
            self.assertEqual(subject_list_txt.read(),
                             "subject_name\tsubject_id\tsubject_group\tsubject_sex\tsubject_age\tsubject_PCodes\n"
                             "alattomos-aladar\t333\tgroup1\tmale\t25\t['1th - 1234', '2nd - 1243']\n")

    def testAddMoreSubjectsToAllSubjectFile(self):
        all_IDs_file_path = self.constructFilePath("testAddMoreSubjectsToAllSubjectFile")
        subject_list_file_path = self.constructFilePath("testAddMoreSubjectsToAllSubjectFile.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", all_IDs_file_path, subject_list_file_path, "", "")
        person_data_handler.update_all_subject_attributes_files("male", "25", ['3rd - 1324', '2nd - 1243'])

        person_data_handler = asrt.PersonDataHandler(
            "toth-csaba_111_group2", "", all_IDs_file_path, subject_list_file_path, "", "")
        person_data_handler.update_all_subject_attributes_files("female", "32", ['1th - 1234', '2nd - 1243'])

        person_data_handler = asrt.PersonDataHandler(
            "kertesz-bela_222_group3", "", all_IDs_file_path, subject_list_file_path, "", "")
        person_data_handler.update_all_subject_attributes_files("male", "43", ['1th - 1234', '3rd - 1324'])

        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", all_IDs_file_path, subject_list_file_path, "", "")
        person_data_handler.update_all_subject_attributes_files("male", "25", ['3rd - 1324', '2nd - 1243'])

        # output files exist
        self.assertTrue(os.path.exists(all_IDs_file_path + ".dat")
                        or os.path.exists(all_IDs_file_path))
        self.assertTrue(os.path.exists(subject_list_file_path))

        with shelve.open(all_IDs_file_path) as all_subject_file:
            self.assertEqual(all_subject_file['ids'], ["alattomos-aladar_333_group1", 'toth-csaba_111_group2', 'kertesz-bela_222_group3'])
            self.assertEqual(all_subject_file["alattomos-aladar_333_group1"], ['male', '25', ['3rd - 1324', '2nd - 1243']])
            self.assertEqual(all_subject_file["toth-csaba_111_group2"], ['female', '32', ['1th - 1234', '2nd - 1243']])
            self.assertEqual(all_subject_file["kertesz-bela_222_group3"], ['male', '43', ['1th - 1234', '3rd - 1324']])

        with codecs.open(subject_list_file_path, 'r', encoding='utf-8') as subject_list_txt:
            self.assertEqual(subject_list_txt.read(),
                             "subject_name\tsubject_id\tsubject_group\tsubject_sex\tsubject_age\tsubject_PCodes\n"
                             "alattomos-aladar\t333\tgroup1\tmale\t25\t['3rd - 1324', '2nd - 1243']\n"
                             "toth-csaba\t111\tgroup2\tfemale\t32\t['1th - 1234', '2nd - 1243']\n"
                             "kertesz-bela\t222\tgroup3\tmale\t43\t['1th - 1234', '3rd - 1324']\n")

    def testSaveSpecialGroupNameToAllSubjectFile(self):
        all_IDs_file_path = self.constructFilePath("testSaveSpecialGroupNameToAllSubjectFile")
        subject_list_file_path = self.constructFilePath("testSaveSpecialGroupNameToAllSubjectFile.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group_1", "", all_IDs_file_path, subject_list_file_path, "", "")
        person_data_handler.update_all_subject_attributes_files("male", "25", ['1th - 1234', '2nd - 1243'])

        # output files exist
        self.assertTrue(os.path.exists(all_IDs_file_path + ".dat")
                        or os.path.exists(all_IDs_file_path))
        self.assertTrue(os.path.exists(subject_list_file_path))

        with shelve.open(all_IDs_file_path) as all_IDs_file:
            all_IDs = all_IDs_file['ids']
            self.assertEqual(all_IDs, ["alattomos-aladar_333_group_1"])

        with codecs.open(subject_list_file_path, 'r', encoding='utf-8') as subject_list_txt:
            self.assertEqual(subject_list_txt.read(),
                             "subject_name\tsubject_id\tsubject_group\tsubject_sex\tsubject_age\tsubject_PCodes\n"
                             "alattomos-aladar\t333\tgroup_1\tmale\t25\t['1th - 1234', '2nd - 1243']\n")

    def testAppendToEmptyOutput(self):
        output_file_path = self.constructFilePath("testAppendToEmptyOutput.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group_1", "", "", "", output_file_path, "reaction-time")

        person_data_handler.append_to_output_file("something")

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tsubject_group\tsubject_name\tsubject_number\tsubject_sex\tsubject_age\tasrt_type\tPCode\toutput_line\t"
                                                 "session\tepoch\tblock\ttrial\tRSI_time\tframe_rate\tframe_time\tframe_sd\t"
                                                 "date\ttime\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tRT\terror\tstimulus\tresponse\tquit_log\tsomething")

    def testAppendToEmptyOutputET(self):
        output_file_path = self.constructFilePath("testAppendToEmptyOutputET.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group_1", "", "", "", output_file_path, "eye-tracking")

        person_data_handler.append_to_output_file("something")

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group\tsubject_name\tsubject_number\t"
                                                 "subject_sex\tsubject_age\tasrt_type\tPCode\tsession\tepoch\tblock\ttrial\tRSI_time\tframe_rate\t"
                                                 "frame_time\tframe_sd\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tstimulus\ttrial_phase\t"
                                                 "left_gaze_data_X_ADCS\tleft_gaze_data_Y_ADCS\tright_gaze_data_X_ADCS\tright_gaze_data_Y_ADCS\tleft_gaze_data_X_PCMCS\t"
                                                 "left_gaze_data_Y_PCMCS\tright_gaze_data_X_PCMCS\tright_gaze_data_Y_PCMCS\tleft_gaze_validity\tright_gaze_validity\t"
                                                 "left_pupil_diameter\tright_pupil_diameter\tleft_pupil_validity\tright_pupil_validity\tgaze_data_time_stamp\tstimulus_1_position_X_PCMCS\t"
                                                 "stimulus_1_position_Y_PCMCS\tstimulus_2_position_X_PCMCS\tstimulus_2_position_Y_PCMCS\tstimulus_3_position_X_PCMCS\t"
                                                 "stimulus_3_position_Y_PCMCS\tstimulus_4_position_X_PCMCS\tstimulus_4_position_Y_PCMCS\tquit_log\tsomething")

    def testAppendMoreTimesToOutput(self):
        output_file_path = self.constructFilePath(
            "testAppendMoreTimesToOutput.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group_1", "", "", "", output_file_path, "reaction-time")

        person_data_handler.append_to_output_file("\nsomething")
        person_data_handler.append_to_output_file("\nsomething2")
        person_data_handler.append_to_output_file("\nsomething3")

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tsubject_group\tsubject_name\tsubject_number\tsubject_sex\tsubject_age\tasrt_type\tPCode\toutput_line\t"
                                                 "session\tepoch\tblock\ttrial\tRSI_time\tframe_rate\tframe_time\tframe_sd\t"
                                                 "date\ttime\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tRT\terror\tstimulus\tresponse\tquit_log\t\n"
                                                 "something\nsomething2\nsomething3")

    def testAppendMoreTimesToOutputET(self):
        output_file_path = self.constructFilePath("testAppendMoreTimesToOutputET.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group_1", "", "", "", output_file_path, "eye-tracking")

        person_data_handler.append_to_output_file("\nsomething")
        person_data_handler.append_to_output_file("\nsomething2")
        person_data_handler.append_to_output_file("\nsomething3")

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group\tsubject_name\tsubject_number\t"
                                                 "subject_sex\tsubject_age\tasrt_type\tPCode\tsession\tepoch\tblock\ttrial\tRSI_time\tframe_rate\t"
                                                 "frame_time\tframe_sd\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tstimulus\ttrial_phase\t"
                                                 "left_gaze_data_X_ADCS\tleft_gaze_data_Y_ADCS\tright_gaze_data_X_ADCS\tright_gaze_data_Y_ADCS\tleft_gaze_data_X_PCMCS\t"
                                                 "left_gaze_data_Y_PCMCS\tright_gaze_data_X_PCMCS\tright_gaze_data_Y_PCMCS\tleft_gaze_validity\tright_gaze_validity\t"
                                                 "left_pupil_diameter\tright_pupil_diameter\tleft_pupil_validity\tright_pupil_validity\tgaze_data_time_stamp\tstimulus_1_position_X_PCMCS\t"
                                                 "stimulus_1_position_Y_PCMCS\tstimulus_2_position_X_PCMCS\tstimulus_2_position_Y_PCMCS\tstimulus_3_position_X_PCMCS\t"
                                                 "stimulus_3_position_Y_PCMCS\tstimulus_4_position_X_PCMCS\tstimulus_4_position_Y_PCMCS\tquit_log\t\nsomething\nsomething2\nsomething3")

    def testWriteEmptyOutput(self):
        output_file_path = self.constructFilePath("testWriteEmptyOutput.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", "", "", output_file_path, "reaction-time")

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.computer_name = "Laposka"
        experiment.subject_group = "group1"
        experiment.subject_name = "alattomos-aladar"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.settings.asrt_types = {1: 'implicit'}
        experiment.PCodes = {1: '1st - 1234'}
        experiment.stim_output_line = 12
        experiment.stim_sessionN = {0: 1}
        experiment.stimepoch = {0: 2}
        experiment.stimblock = {0: 12}
        experiment.stimtrial = {0: 2}
        stim_RSI = 0.123
        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3
        stim_RT_time = time.strftime('%H:%M:%S')
        stim_RT_date = time.strftime('%d/%m/%Y')
        stimcolor = 'Orange'
        experiment.stimpr = {0: 'pattern'}
        stimRT = 321.2345
        stimACC = 0
        experiment.stimlist = {0: 1}
        response = 'z'
        N = 0

        person_data_handler.output_data_buffer.append([N, stim_RSI, stim_RT_time, stim_RT_date, stimRT,
                                                       stimACC, response, stimcolor, experiment.stim_output_line])
        person_data_handler.flush_RT_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tsubject_group\tsubject_name\tsubject_number\tsubject_sex\tsubject_age\tasrt_type\t"
                                                 "PCode\toutput_line\tsession\tepoch\tblock\ttrial\tRSI_time\tframe_rate\tframe_time\tframe_sd\t"
                                                 "date\ttime\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tRT\terror\tstimulus\tresponse\tquit_log\t\n"
                                                 "Laposka\tgroup1\talattomos-aladar\t333\tmale\t25\timplicit\t1234\t12\t1\t2\t"
                                                 "12\t2\t0,123\t59,1\t16,56\t1,3\t" +
                                                 str(stim_RT_time) + "\t" +
                                                 str(stim_RT_date) + "\t"
                                                 "Orange\tpattern\tnone\t321,2345\t0\t1\tz\t")

    def testWriteEmptyOutputET(self):
        output_file_path = self.constructFilePath("testWriteEmptyOutputET.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", "", "", output_file_path, "eye-tracking")

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.computer_name = "Laposka"
        experiment.settings.monitor_width = 47.6
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.epochN = 5
        experiment.settings.block_in_epochN = 5
        experiment.subject_group = "group1"
        experiment.subject_name = "alattomos-aladar"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.trial_phase = "stimulus_on_screen"
        experiment.last_N = 0
        experiment.last_RSI = "500.0"
        experiment.settings.asrt_types = {1: 'implicit'}
        experiment.PCodes = {1: '1st - 1234'}
        experiment.stim_sessionN = {1: 1}
        experiment.stimepoch = {1: 2}
        experiment.stimblock = {1: 12}
        experiment.stimtrial = {1: 1}
        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3
        experiment.stimpr = {1: 'pattern'}
        experiment.stimlist = {1: 1}
        experiment.colors = {'wincolor': 'black', 'linecolor': 'black', 'stimp': 'black', 'stimr': 'black'}
        experiment.mymonitor = self.my_monitor
        experiment.dict_pos = {1: (-0.5, -0.5), 2: (0.5, -0.5), 3: (-0.5, 0.5), 4: (0.5, 0.5)}

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = True
        gazeData['right_gaze_point_validity'] = True
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = True
        gazeData['right_pupil_validity'] = True

        time_stamp = 10000

        person_data_handler.output_data_buffer.append([experiment.last_N, experiment.last_RSI, experiment.trial_phase, gazeData, time_stamp])
        person_data_handler.flush_ET_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group\tsubject_name\tsubject_number\t"
                                                 "subject_sex\tsubject_age\tasrt_type\tPCode\tsession\tepoch\tblock\ttrial\tRSI_time\tframe_rate\t"
                                                 "frame_time\tframe_sd\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tstimulus\ttrial_phase\t"
                                                 "left_gaze_data_X_ADCS\tleft_gaze_data_Y_ADCS\tright_gaze_data_X_ADCS\tright_gaze_data_Y_ADCS\tleft_gaze_data_X_PCMCS\t"
                                                 "left_gaze_data_Y_PCMCS\tright_gaze_data_X_PCMCS\tright_gaze_data_Y_PCMCS\tleft_gaze_validity\tright_gaze_validity\t"
                                                 "left_pupil_diameter\tright_pupil_diameter\tleft_pupil_validity\tright_pupil_validity\tgaze_data_time_stamp\tstimulus_1_position_X_PCMCS\t"
                                                 "stimulus_1_position_Y_PCMCS\tstimulus_2_position_X_PCMCS\tstimulus_2_position_Y_PCMCS\tstimulus_3_position_X_PCMCS\t"
                                                 "stimulus_3_position_Y_PCMCS\tstimulus_4_position_X_PCMCS\tstimulus_4_position_Y_PCMCS\tquit_log\t\n"
                                                 "Laposka\t1366\t768\tgroup1\talattomos-aladar\t333\tmale\t25\timplicit\t1234\t1\t2\t12\t1\t500.0\t59,1\t16,56\t"
                                                 "1,3\tblack\tpattern\tnone\t1\tstimulus_on_screen\t0,5\t0,5\t0,5\t0,5\t0,0\t-0,0\t0,0\t-0,0\tTrue\tTrue\t3\t3\tTrue\tTrue\t10000\t"
                                                 "-0,5\t-0,5\t0,5\t-0,5\t-0,5\t0,5\t0,5\t0,5\t")

    def testWriteETDataWithBigLastN(self):
        output_file_path = self.constructFilePath("testWriteETDataWithBigLastN.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", "", "", output_file_path, "eye-tracking")

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.computer_name = "Laposka"
        experiment.settings.monitor_width = 47.6
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.epochN = 5
        experiment.settings.block_in_epochN = 5
        experiment.subject_group = "group1"
        experiment.subject_name = "alattomos-aladar"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.trial_phase = "stimulus_on_screen"
        experiment.last_N = experiment.settings.get_maxtrial()
        experiment.last_RSI = "500.0"
        experiment.settings.asrt_types = {1: 'implicit'}
        experiment.PCodes = {1: '1st - 1234'}
        experiment.stim_sessionN = {1: 1}
        experiment.stimepoch = {1: 2}
        experiment.stimblock = {1: 12}
        experiment.stimtrial = {1: 21}
        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3
        experiment.stimpr = {1: 'pattern'}
        experiment.stimlist = {1: 1}
        experiment.colors = {'wincolor': 'black', 'linecolor': 'black', 'stimp': 'black', 'stimr': 'black'}
        experiment.mymonitor = self.my_monitor
        experiment.dict_pos = {1: (-0.5, -0.5), 2: (0.5, -0.5), 3: (-0.5, 0.5), 4: (0.5, 0.5)}

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = True
        gazeData['right_gaze_point_validity'] = True
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = True
        gazeData['right_pupil_validity'] = True

        time_stamp = 10000

        person_data_handler.output_data_buffer.append([experiment.last_N, experiment.last_RSI, experiment.trial_phase, gazeData, time_stamp])
        person_data_handler.flush_ET_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group\tsubject_name\tsubject_number\t"
                                                 "subject_sex\tsubject_age\tasrt_type\tPCode\tsession\tepoch\tblock\ttrial\tRSI_time\tframe_rate\t"
                                                 "frame_time\tframe_sd\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tstimulus\ttrial_phase\t"
                                                 "left_gaze_data_X_ADCS\tleft_gaze_data_Y_ADCS\tright_gaze_data_X_ADCS\tright_gaze_data_Y_ADCS\tleft_gaze_data_X_PCMCS\t"
                                                 "left_gaze_data_Y_PCMCS\tright_gaze_data_X_PCMCS\tright_gaze_data_Y_PCMCS\tleft_gaze_validity\tright_gaze_validity\t"
                                                 "left_pupil_diameter\tright_pupil_diameter\tleft_pupil_validity\tright_pupil_validity\tgaze_data_time_stamp\tstimulus_1_position_X_PCMCS\t"
                                                 "stimulus_1_position_Y_PCMCS\tstimulus_2_position_X_PCMCS\tstimulus_2_position_Y_PCMCS\tstimulus_3_position_X_PCMCS\t"
                                                 "stimulus_3_position_Y_PCMCS\tstimulus_4_position_X_PCMCS\tstimulus_4_position_Y_PCMCS\tquit_log\t")

    def testWriteETDataExplicitASRT(self):
        output_file_path = self.constructFilePath("testWriteETDataExplicitASRT.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", "", "", output_file_path, "eye-tracking")

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.computer_name = "Laposka"
        experiment.settings.monitor_width = 47.6
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.epochN = 5
        experiment.settings.block_in_epochN = 5
        experiment.subject_group = "group1"
        experiment.subject_name = "alattomos-aladar"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.trial_phase = "stimulus_on_screen"
        experiment.last_N = 0
        experiment.last_RSI = "500.0"
        experiment.settings.asrt_types = {1: 'explicit'}
        experiment.PCodes = {1: '1st - 1234'}
        experiment.stim_sessionN = {1: 1}
        experiment.stimepoch = {1: 2}
        experiment.stimblock = {1: 12}
        experiment.stimtrial = {1: 1}
        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3
        experiment.stimpr = {1: 'pattern'}
        experiment.stimlist = {1: 1}
        experiment.colors = {'wincolor': 'black', 'linecolor': 'black', 'stimp': 'black', 'stimr': 'black'}
        experiment.mymonitor = self.my_monitor
        experiment.dict_pos = {1: (-0.5, -0.5), 2: (0.5, -0.5), 3: (-0.5, 0.5), 4: (0.5, 0.5)}

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = True
        gazeData['right_gaze_point_validity'] = True
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = True
        gazeData['right_pupil_validity'] = True

        time_stamp = 10000

        person_data_handler.output_data_buffer.append([experiment.last_N, experiment.last_RSI, experiment.trial_phase, gazeData, time_stamp])
        person_data_handler.flush_ET_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group\tsubject_name\tsubject_number\t"
                                                 "subject_sex\tsubject_age\tasrt_type\tPCode\tsession\tepoch\tblock\ttrial\tRSI_time\tframe_rate\t"
                                                 "frame_time\tframe_sd\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tstimulus\ttrial_phase\t"
                                                 "left_gaze_data_X_ADCS\tleft_gaze_data_Y_ADCS\tright_gaze_data_X_ADCS\tright_gaze_data_Y_ADCS\tleft_gaze_data_X_PCMCS\t"
                                                 "left_gaze_data_Y_PCMCS\tright_gaze_data_X_PCMCS\tright_gaze_data_Y_PCMCS\tleft_gaze_validity\tright_gaze_validity\t"
                                                 "left_pupil_diameter\tright_pupil_diameter\tleft_pupil_validity\tright_pupil_validity\tgaze_data_time_stamp\tstimulus_1_position_X_PCMCS\t"
                                                 "stimulus_1_position_Y_PCMCS\tstimulus_2_position_X_PCMCS\tstimulus_2_position_Y_PCMCS\tstimulus_3_position_X_PCMCS\t"
                                                 "stimulus_3_position_Y_PCMCS\tstimulus_4_position_X_PCMCS\tstimulus_4_position_Y_PCMCS\tquit_log\t\n"
                                                 "Laposka\t1366\t768\tgroup1\talattomos-aladar\t333\tmale\t25\texplicit\t1234\t1\t2\t12\t1\t500.0\t59,1\t16,56\t"
                                                 "1,3\tblack\tpattern\tnone\t1\tstimulus_on_screen\t0,5\t0,5\t0,5\t0,5\t0,0\t-0,0\t0,0\t-0,0\tTrue\tTrue\t3\t3\tTrue\tTrue\t10000\t"
                                                 "-0,5\t-0,5\t0,5\t-0,5\t-0,5\t0,5\t0,5\t0,5\t")

    def testWriteETDataNoPatternASRT(self):
        output_file_path = self.constructFilePath("testWriteETDataExplicitASRT.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", "", "", output_file_path, "eye-tracking")

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.computer_name = "Laposka"
        experiment.settings.monitor_width = 47.6
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.epochN = 5
        experiment.settings.block_in_epochN = 5
        experiment.subject_group = "group1"
        experiment.subject_name = "alattomos-aladar"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.trial_phase = "stimulus_on_screen"
        experiment.last_N = 0
        experiment.last_RSI = "500.0"
        experiment.settings.asrt_types = {1: 'noASRT'}
        experiment.PCodes = {1: 'noPattern'}
        experiment.stim_sessionN = {1: 1}
        experiment.stimepoch = {1: 2}
        experiment.stimblock = {1: 12}
        experiment.stimtrial = {1: 21}
        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3
        experiment.stimpr = {1: 'pattern'}
        experiment.stimlist = {1: 1}
        experiment.colors = {'wincolor': 'black', 'linecolor': 'black', 'stimp': 'black', 'stimr': 'black'}
        experiment.mymonitor = self.my_monitor
        experiment.dict_pos = {1: (-0.5, -0.5), 2: (0.5, -0.5), 3: (-0.5, 0.5), 4: (0.5, 0.5)}

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = True
        gazeData['right_gaze_point_validity'] = True
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = True
        gazeData['right_pupil_validity'] = True

        time_stamp = 10000

        person_data_handler.output_data_buffer.append([experiment.last_N, experiment.last_RSI, experiment.trial_phase, gazeData, time_stamp])
        person_data_handler.flush_ET_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group\tsubject_name\tsubject_number\t"
                                                 "subject_sex\tsubject_age\tasrt_type\tPCode\tsession\tepoch\tblock\ttrial\tRSI_time\tframe_rate\t"
                                                 "frame_time\tframe_sd\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tstimulus\ttrial_phase\t"
                                                 "left_gaze_data_X_ADCS\tleft_gaze_data_Y_ADCS\tright_gaze_data_X_ADCS\tright_gaze_data_Y_ADCS\tleft_gaze_data_X_PCMCS\t"
                                                 "left_gaze_data_Y_PCMCS\tright_gaze_data_X_PCMCS\tright_gaze_data_Y_PCMCS\tleft_gaze_validity\tright_gaze_validity\t"
                                                 "left_pupil_diameter\tright_pupil_diameter\tleft_pupil_validity\tright_pupil_validity\tgaze_data_time_stamp\tstimulus_1_position_X_PCMCS\t"
                                                 "stimulus_1_position_Y_PCMCS\tstimulus_2_position_X_PCMCS\tstimulus_2_position_Y_PCMCS\tstimulus_3_position_X_PCMCS\t"
                                                 "stimulus_3_position_Y_PCMCS\tstimulus_4_position_X_PCMCS\tstimulus_4_position_Y_PCMCS\tquit_log\t\n"
                                                 "Laposka\t1366\t768\tgroup1\talattomos-aladar\t333\tmale\t25\tnoASRT\tnoPattern\t1\t2\t12\t21\t500.0\t59,1\t16,56\t"
                                                 "1,3\tblack\tpattern\tnone\t1\tstimulus_on_screen\t0,5\t0,5\t0,5\t0,5\t0,0\t-0,0\t0,0\t-0,0\tTrue\tTrue\t3\t3\tTrue\tTrue\t10000\t"
                                                 "-0,5\t-0,5\t0,5\t-0,5\t-0,5\t0,5\t0,5\t0,5\t")

    def testWriteExistingOutput(self):
        output_file_path = self.constructFilePath("testWriteExistingOutput.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", "", "", output_file_path, "reaction-time")

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.computer_name = "Laposka"
        experiment.subject_group = "group1"
        experiment.subject_name = "alattomos-aladar"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.settings.asrt_types = {1: 'implicit'}
        experiment.PCodes = {1: '1st - 1234'}
        experiment.stim_output_line = 12
        experiment.stim_sessionN = {1: 1}
        experiment.stimepoch = {1: 2}
        experiment.stimblock = {1: 1}
        experiment.stimtrial = {1: 1}
        stim_RSI = 0.123
        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3
        stim_RT_time = time.strftime('%H:%M:%S')
        stim_RT_date = time.strftime('%d/%m/%Y')
        stimcolor = 'Orange'
        experiment.stimpr = {1: 'pattern'}
        stimRT = 321.2345
        stimACC = 0
        experiment.stimlist = {1: 1}
        response = 'z'
        N = 1

        person_data_handler.output_data_buffer.append([N, stim_RSI, stim_RT_time, stim_RT_date, stimRT,
                                                       stimACC, response, stimcolor, experiment.stim_output_line])
        person_data_handler.flush_RT_data_to_output(experiment)

        experiment.stim_output_line = 13
        experiment.stimtrial[1] = 2
        stim_RSI = 0.111
        stim_RT_time = time.strftime('%H:%M:%S')
        stim_RT_date = time.strftime('%d/%m/%Y')
        stimcolor = 'Green'
        experiment.stimpr[1] = 'random'
        stimRT = 523.2345
        stimACC = 1
        experiment.stimlist[1] = 2
        response = 'b'

        person_data_handler.output_data_buffer.append([N, stim_RSI, stim_RT_time, stim_RT_date, stimRT,
                                                       stimACC, response, stimcolor, experiment.stim_output_line])
        person_data_handler.flush_RT_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tsubject_group\tsubject_name\tsubject_number\tsubject_sex\tsubject_age\tasrt_type\t"
                                                 "PCode\toutput_line\tsession\tepoch\tblock\ttrial\tRSI_time\tframe_rate\tframe_time\tframe_sd\t"
                                                 "date\ttime\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tRT\terror\tstimulus\tresponse\tquit_log\t\n"
                                                 "Laposka\tgroup1\talattomos-aladar\t333\tmale\t25\timplicit\t1234\t12\t1\t2\t"
                                                 "1\t1\t0,123\t59,1\t16,56\t1,3\t" +
                                                 str(stim_RT_time) + "\t" +
                                                 str(stim_RT_date) + "\t"
                                                 "Orange\tpattern\tnone\t321,2345\t0\t1\tz\t\n"
                                                 "Laposka\tgroup1\talattomos-aladar\t333\tmale\t25\timplicit\t1234\t13\t1\t2\t"
                                                 "1\t2\t0,111\t59,1\t16,56\t1,3\t" +
                                                 str(stim_RT_time) + "\t" +
                                                 str(stim_RT_date) + "\t"
                                                 "Green\trandom\tnone\t523,2345\t1\t2\tb\t")

    def testWriteExistingOutputET(self):
        output_file_path = self.constructFilePath("testWriteExistingOutputET.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", "", "", output_file_path, "eye-tracking")

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.computer_name = "Laposka"
        experiment.settings.monitor_width = 47.6
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.epochN = 5
        experiment.settings.block_in_epochN = 5
        experiment.subject_group = "group1"
        experiment.subject_name = "alattomos-aladar"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.trial_phase = "stimulus_on_screen"
        experiment.last_N = 0
        experiment.last_RSI = "500.0"
        experiment.settings.asrt_types = {1: 'implicit'}
        experiment.PCodes = {1: '1st - 1234'}
        experiment.stim_sessionN = {1: 1}
        experiment.stimepoch = {1: 1}
        experiment.stimblock = {1: 12}
        experiment.stimtrial = {1: 2}
        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3
        experiment.stimpr = {1: 'pattern'}
        experiment.stimlist = {1: 1}
        experiment.colors = {'wincolor': 'black', 'linecolor': 'black', 'stimp': 'black', 'stimr': 'black'}
        experiment.mymonitor = self.my_monitor
        experiment.dict_pos = {1: (-0.5, -0.5), 2: (0.5, -0.5), 3: (-0.5, 0.5), 4: (0.5, 0.5)}

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = True
        gazeData['right_gaze_point_validity'] = True
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = True
        gazeData['right_pupil_validity'] = True

        time_stamp = 10000

        person_data_handler.output_data_buffer.append([experiment.last_N, experiment.last_RSI, experiment.trial_phase, gazeData, time_stamp])
        person_data_handler.flush_ET_data_to_output(experiment)

        experiment.stimtrial = {1: 2}
        experiment.colors = {'wincolor': 'Green', 'linecolor': 'Green', 'stimp': 'Green', 'stimr': 'Green'}
        experiment.stimpr[1] = 'random'
        experiment.stimlist[1] = 2
        experiment.last_RSI = "123.4"

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.75, 0.75)
        gazeData['right_gaze_point_on_display_area'] = (0.25, 0.25)
        gazeData['left_gaze_point_validity'] = True
        gazeData['right_gaze_point_validity'] = True
        gazeData['left_pupil_diameter'] = float('nan')
        gazeData['right_pupil_diameter'] = float('nan')
        gazeData['left_pupil_validity'] = False
        gazeData['right_pupil_validity'] = False

        time_stamp = 10000

        person_data_handler.output_data_buffer.append([experiment.last_N, experiment.last_RSI, experiment.trial_phase, gazeData, time_stamp])
        person_data_handler.flush_ET_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group\tsubject_name\tsubject_number\t"
                                                 "subject_sex\tsubject_age\tasrt_type\tPCode\tsession\tepoch\tblock\ttrial\tRSI_time\tframe_rate\t"
                                                 "frame_time\tframe_sd\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tstimulus\ttrial_phase\t"
                                                 "left_gaze_data_X_ADCS\tleft_gaze_data_Y_ADCS\tright_gaze_data_X_ADCS\tright_gaze_data_Y_ADCS\tleft_gaze_data_X_PCMCS\t"
                                                 "left_gaze_data_Y_PCMCS\tright_gaze_data_X_PCMCS\tright_gaze_data_Y_PCMCS\tleft_gaze_validity\tright_gaze_validity\t"
                                                 "left_pupil_diameter\tright_pupil_diameter\tleft_pupil_validity\tright_pupil_validity\tgaze_data_time_stamp\tstimulus_1_position_X_PCMCS\t"
                                                 "stimulus_1_position_Y_PCMCS\tstimulus_2_position_X_PCMCS\tstimulus_2_position_Y_PCMCS\tstimulus_3_position_X_PCMCS\t"
                                                 "stimulus_3_position_Y_PCMCS\tstimulus_4_position_X_PCMCS\tstimulus_4_position_Y_PCMCS\tquit_log\t\n"
                                                 "Laposka\t1366\t768\tgroup1\talattomos-aladar\t333\tmale\t25\timplicit\t1234\t1\t1\t12\t2\t500.0\t59,1\t16,56\t"
                                                 "1,3\tblack\tpattern\tnone\t1\tstimulus_on_screen\t0,5\t0,5\t0,5\t0,5\t0,0\t-0,0\t0,0\t-0,0\tTrue\tTrue\t3\t3\tTrue\tTrue\t10000\t"
                                                 "-0,5\t-0,5\t0,5\t-0,5\t-0,5\t0,5\t0,5\t0,5\t\n"
                                                 "Laposka\t1366\t768\tgroup1\talattomos-aladar\t333\tmale\t25\timplicit\t1234\t1\t1\t12\t2\t123.4\t59,1\t16,56\t"
                                                 "1,3\tGreen\trandom\tnone\t2\tstimulus_on_screen\t0,75\t0,75\t0,25\t0,25\t11,900000000000002\t-6,690483162518303\t-11,9\t6,690483162518302\t"
                                                 "True\tTrue\tnan\tnan\tFalse\tFalse\t10000\t-0,5\t-0,5\t0,5\t-0,5\t-0,5\t0,5\t0,5\t0,5\t")

    def testPointInComputerNameOrDate(self):
        output_file_path = self.constructFilePath(
            "testPointInComputerName.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", "", "", output_file_path, "reaction-time")

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.computer_name = "I. Richárd"
        experiment.subject_group = "group1"
        experiment.subject_name = "alattomos-aladar"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.settings.asrt_types = {1: 'implicit'}
        experiment.PCodes = {1: '1st - 1234'}
        experiment.stim_output_line = 12
        experiment.stim_sessionN = {0: 1}
        experiment.stimepoch = {0: 2}
        experiment.stimblock = {0: 12}
        experiment.stimtrial = {0: 1}
        stim_RSI = 0.123
        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3
        stim_RT_time = time.strftime('%H:%M:%S')
        stim_RT_date = time.strftime('%Y.%m.%d')
        stimcolor = 'Orange'
        experiment.stimpr = {0: 'pattern'}
        stimRT = 321.2345
        stimACC = 0
        experiment.stimlist = {0: 1}
        response = 'z'
        N = 0

        person_data_handler.output_data_buffer.append([N, stim_RSI, stim_RT_time, stim_RT_date, stimRT,
                                                       stimACC, response, stimcolor, experiment.stim_output_line])
        person_data_handler.flush_RT_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tsubject_group\tsubject_name\tsubject_number\tsubject_sex\tsubject_age\tasrt_type\t"
                                                 "PCode\toutput_line\tsession\tepoch\tblock\ttrial\tRSI_time\tframe_rate\tframe_time\tframe_sd\t"
                                                 "date\ttime\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tRT\terror\tstimulus\tresponse\tquit_log\t\n"
                                                 "I. Richárd\tgroup1\talattomos-aladar\t333\tmale\t25\timplicit\t1234\t12\t1\t2\t"
                                                 "12\t1\t0,123\t59,1\t16,56\t1,3\t" +
                                                 str(stim_RT_time) + "\t" +
                                                 str(stim_RT_date) + "\t"
                                                 "Orange\tpattern\tnone\t321,2345\t0\t1\tz\t")

    def testWriteRandomTrialOutputET(self):
        output_file_path = self.constructFilePath("testWriteOutputET.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", "", "", output_file_path, "eye-tracking")

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.computer_name = "Laposka"
        experiment.settings.monitor_width = 47.6
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.epochN = 5
        experiment.settings.block_in_epochN = 5
        experiment.subject_group = "group1"
        experiment.subject_name = "alattomos-aladar"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.trial_phase = "stimulus_on_screen"
        experiment.last_N = 0
        experiment.last_RSI = "500.0"
        experiment.settings.asrt_types = {1: 'implicit'}
        experiment.PCodes = {1: '1st - 1234'}
        experiment.stim_sessionN = {1: 1}
        experiment.stimepoch = {1: 2}
        experiment.stimblock = {1: 12}
        experiment.stimtrial = {1: 1}
        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3
        experiment.stimpr = {1: 'random'}
        experiment.stimlist = {1: 1}
        experiment.colors = {'wincolor': 'black', 'linecolor': 'black', 'stimp': 'black', 'stimr': 'black'}
        experiment.mymonitor = self.my_monitor
        experiment.dict_pos = {1: (-0.5, -0.5), 2: (0.5, -0.5), 3: (-0.5, 0.5), 4: (0.5, 0.5)}

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 0
        gazeData['right_gaze_point_validity'] = 0
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = 0
        gazeData['right_pupil_validity'] = 0

        time_stamp = 10000

        person_data_handler.output_data_buffer.append([experiment.last_N, experiment.last_RSI, experiment.trial_phase, gazeData, time_stamp])
        person_data_handler.flush_ET_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group\tsubject_name\tsubject_number\t"
                                                 "subject_sex\tsubject_age\tasrt_type\tPCode\tsession\tepoch\tblock\ttrial\tRSI_time\tframe_rate\t"
                                                 "frame_time\tframe_sd\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tstimulus\ttrial_phase\t"
                                                 "left_gaze_data_X_ADCS\tleft_gaze_data_Y_ADCS\tright_gaze_data_X_ADCS\tright_gaze_data_Y_ADCS\tleft_gaze_data_X_PCMCS\t"
                                                 "left_gaze_data_Y_PCMCS\tright_gaze_data_X_PCMCS\tright_gaze_data_Y_PCMCS\tleft_gaze_validity\tright_gaze_validity\t"
                                                 "left_pupil_diameter\tright_pupil_diameter\tleft_pupil_validity\tright_pupil_validity\tgaze_data_time_stamp\tstimulus_1_position_X_PCMCS\t"
                                                 "stimulus_1_position_Y_PCMCS\tstimulus_2_position_X_PCMCS\tstimulus_2_position_Y_PCMCS\tstimulus_3_position_X_PCMCS\t"
                                                 "stimulus_3_position_Y_PCMCS\tstimulus_4_position_X_PCMCS\tstimulus_4_position_Y_PCMCS\tquit_log\t\n"
                                                 "Laposka\t1366\t768\tgroup1\talattomos-aladar\t333\tmale\t25\timplicit\t1234\t1\t2\t12\t1\t500.0\t59,1\t16,56\t"
                                                 "1,3\tblack\trandom\tnone\t1\tstimulus_on_screen\t0,5\t0,5\t0,5\t0,5\tnan\tnan\tnan\tnan\t0\t0\t3\t3\t0\t0\t10000\t"
                                                 "-0,5\t-0,5\t0,5\t-0,5\t-0,5\t0,5\t0,5\t0,5\t")

    def testWriteHighRandomTrialOutputET(self):
        output_file_path = self.constructFilePath("testWriteOutputET.txt")
        person_data_handler = asrt.PersonDataHandler(
            "alattomos-aladar_333_group1", "", "", "", output_file_path, "eye-tracking")

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.computer_name = "Laposka"
        experiment.settings.monitor_width = 47.6
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.epochN = 5
        experiment.settings.block_in_epochN = 5
        experiment.subject_group = "group1"
        experiment.subject_name = "alattomos-aladar"
        experiment.subject_number = 333
        experiment.subject_sex = "male"
        experiment.subject_age = "25"
        experiment.trial_phase = "stimulus_on_screen"
        experiment.last_N = 4
        experiment.last_RSI = "500.0"
        experiment.settings.asrt_types = {1: 'implicit'}
        experiment.PCodes = {1: '1st - 1234'}
        experiment.stim_sessionN = {3: 1, 4: 1, 5: 1}
        experiment.stimepoch = {3: 1, 4: 1, 5: 1}
        experiment.stimblock = {3: 1, 4: 1, 5: 1}
        experiment.stimtrial = {3: 3, 4: 4, 5: 5}
        experiment.stimlist = {3: 1, 4: 1, 5: 2}
        experiment.stimpr = {3: "random", 4: "pattern", 5: "random"}
        experiment.frame_rate = 59.1
        experiment.frame_time = 16.56
        experiment.frame_sd = 1.3
        experiment.colors = {'wincolor': 'black', 'linecolor': 'black', 'stimp': 'black', 'stimr': 'black'}
        experiment.mymonitor = self.my_monitor
        experiment.dict_pos = {1: (-0.5, -0.5), 2: (0.5, -0.5), 3: (-0.5, 0.5), 4: (0.5, 0.5)}

        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 0
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = 1
        gazeData['right_pupil_validity'] = 1

        time_stamp = 10000

        person_data_handler.output_data_buffer.append([experiment.last_N, experiment.last_RSI, experiment.trial_phase, gazeData, time_stamp])
        person_data_handler.flush_ET_data_to_output(experiment)

        with codecs.open(output_file_path, 'r', encoding='utf-8') as output_file:
            self.assertEqual(output_file.read(), "computer_name\tmonitor_width_pixel\tmonitor_height_pixel\tsubject_group\tsubject_name\tsubject_number\t"
                                                 "subject_sex\tsubject_age\tasrt_type\tPCode\tsession\tepoch\tblock\ttrial\tRSI_time\tframe_rate\t"
                                                 "frame_time\tframe_sd\tstimulus_color\ttrial_type_pr\ttriplet_type_hl\tstimulus\ttrial_phase\t"
                                                 "left_gaze_data_X_ADCS\tleft_gaze_data_Y_ADCS\tright_gaze_data_X_ADCS\tright_gaze_data_Y_ADCS\tleft_gaze_data_X_PCMCS\t"
                                                 "left_gaze_data_Y_PCMCS\tright_gaze_data_X_PCMCS\tright_gaze_data_Y_PCMCS\tleft_gaze_validity\tright_gaze_validity\t"
                                                 "left_pupil_diameter\tright_pupil_diameter\tleft_pupil_validity\tright_pupil_validity\tgaze_data_time_stamp\tstimulus_1_position_X_PCMCS\t"
                                                 "stimulus_1_position_Y_PCMCS\tstimulus_2_position_X_PCMCS\tstimulus_2_position_Y_PCMCS\tstimulus_3_position_X_PCMCS\t"
                                                 "stimulus_3_position_Y_PCMCS\tstimulus_4_position_X_PCMCS\tstimulus_4_position_Y_PCMCS\tquit_log\t\n"
                                                 "Laposka\t1366\t768\tgroup1\talattomos-aladar\t333\tmale\t25\timplicit\t1234\t1\t1\t1\t5\t500.0\t59,1\t16,56\t"
                                                 "1,3\tblack\trandom\thigh\t2\tstimulus_on_screen\t0,5\t0,5\t0,5\t0,5\t0,0\t-0,0\tnan\tnan\t1\t0\t3\t3\t1\t1\t10000\t"
                                                 "-0,5\t-0,5\t0,5\t-0,5\t-0,5\t0,5\t0,5\t0,5\t")


if __name__ == "__main__":
    unittest.main()  # run all tests
