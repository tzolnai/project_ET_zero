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

import sys
import os
# Add the local path to the main script and external scripts so we can import them.
sys.path = [".."] + \
    [os.path.join("..", "externals", "psychopy_mock")] + sys.path

import unittest
import asrt
import shutil
import pytest
import psychopy_visual_mock as pvm
import psychopy_gui_mock as pgm
from psychopy import visual, logging, core, monitors
import random
from datetime import datetime
import codecs

try:
    import tobii_research as tobii
except:
    pass


# ignore warnings comming from psychopy
logging.console.setLevel(logging.ERROR)


random_generator_g = 1


def choice_mock(list):
    global random_generator_g
    if random_generator_g == 1:
        random_generator_g = 2
    elif random_generator_g == 2:
        random_generator_g = 3
    elif random_generator_g == 3:
        random_generator_g = 4
    else:
        random_generator_g = 1
    return random_generator_g


def DummyFunction(*argv):
    pass


core.wait = DummyFunction


class EyeTrackerMock:
    def subscribe_to(self, subscription_type, callback, as_dictionary=False):
        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = 1
        gazeData['right_pupil_validity'] = 1
        callback(gazeData)
        global gaze_data_callback
        gaze_data_callback = callback

    def unsubscribe_from(self, subscription_type, callback=None):
        global gaze_data_callback
        gaze_data_callback = None


def find_all_eyetrackers_mock():
    return [EyeTrackerMock()]


def get_system_time_stamp_mock():
    return 1000000


@pytest.mark.skipif(not asrt.g_tobii_available, reason="Can't run without tobii package")
class integrationTest(unittest.TestCase):

    def setUp(self):
        # Init work directories
        filepath = os.path.abspath(__file__)
        (filepath, trail) = os.path.split(filepath)
        test_name = self.id().split(".")[2]
        self.current_dir = os.path.join(filepath, "data", "integration_ET", test_name)
        self.work_dir = os.path.join(self.current_dir, "workdir")
        asrt.ensure_dir(self.work_dir)
        self.clearDir(self.work_dir)
        self.copyFilesToWorkdir()

        # override this method to get the stimlist to be able to generate the keylist
        self.experiment = asrt.Experiment(self.work_dir)
        self.frame_check = self.experiment.frame_check
        self.experiment.frame_check = self.frame_check_override
        self.experiment.wait_for_eye_response_original = self.experiment.wait_for_eye_response
        self.experiment.wait_for_eye_response = self.wait_for_eye_response_override
        self.experiment.monitor_settings = self.monitor_settings_override

        global random_generator_g
        random_generator_g = 1
        random.choice = choice_mock

        # override static period to avoid waiting time
        class DummyStaticPeriod:
            def __init__(self, screenHz=None, win=None, name='StaticPeriod'):
                pass

            def start(self, duration):
                pass

            def complete(self):
                pass
        self.StaticPeriod = core.StaticPeriod
        core.StaticPeriod = DummyStaticPeriod

        tobii.find_all_eyetrackers = find_all_eyetrackers_mock
        tobii.get_system_time_stamp = get_system_time_stamp_mock

        # Change this variable to update all reference file
        self.update_references = False
        self.update_RSI_reference = False

    def tearDown(self):
        if self.update_references:
            reference_file_path = os.path.join(
                self.current_dir, "reference", "toth-bela_10__log.txt")
            workdir_output = os.path.join(
                self.work_dir, "logs", "toth-bela_10__log.txt")

            with codecs.open(workdir_output, 'r', encoding='utf-8') as workdir_output_file:
                output_lines = workdir_output_file.readlines()

            if not self.update_RSI_reference:
                with codecs.open(reference_file_path, 'r', encoding='utf-8') as reference_file:
                    ref_lines = reference_file.readlines()

                for i in range(1, len(output_lines)):
                    output_lines[i] = output_lines[i].replace(output_lines[i].split('\t')[14], ref_lines[i].split('\t')[14])

            with codecs.open(reference_file_path, 'w', encoding='utf-8') as reference_file:
                for line in output_lines:
                    reference_file.write(line)

        self.clearDir(self.work_dir)

        self.experiment.frame_check = self.frame_check
        self.experiment.wait_for_eye_response = self.experiment.wait_for_eye_response_original
        core.StaticPeriod = self.StaticPeriod

    def copyFilesToWorkdir(self):
        this_path = self.current_dir

        asrt.ensure_dir(os.path.join(self.work_dir, "settings"))
        asrt.ensure_dir(os.path.join(self.work_dir, "logs"))

        for file in os.listdir(self.current_dir):
            file_path = os.path.join(self.current_dir, file)
            if os.path.isfile(file_path):
                shutil.copyfile(file_path, os.path.join(self.work_dir, file))
            elif "workdir" in file_path or "reference" in file_path:
                continue
            elif os.path.isdir(file_path):
                for sub_file in os.listdir(file_path):
                    sub_file_path = os.path.join(file_path, sub_file)
                    if "settings" in sub_file_path:
                        shutil.copyfile(sub_file_path, os.path.join(
                            self.work_dir, "settings", sub_file))
                    else:
                        shutil.copyfile(sub_file_path, os.path.join(
                            self.work_dir, "logs", sub_file))

    def clearDir(self, dir_path):
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def frame_check_override(self):
        self.experiment.frame_time = 0.0
        self.experiment.frame_sd = 0.0
        self.experiment.frame_rate = 60.0

    def monitor_settings_override(self):
        self.experiment.mymonitor = monitors.Monitor('myMon')
        self.experiment.mymonitor.setSizePix([1366, 768])
        self.experiment.mymonitor.setWidth(29)

    def PCMCS_to_ADCS(self, pos_PCMCS):
        aspect_ratio = self.experiment.mymonitor.getSizePix()[1] / self.experiment.mymonitor.getSizePix()[0]
        monitor_width_cm = self.experiment.settings.monitor_width
        monitor_height_cm = monitor_width_cm * aspect_ratio

        # shift origin
        shift_x = monitor_width_cm / 2
        shift_y = monitor_height_cm / 2

        # scale coordinates and mirror the y coordinates
        pos_ADCS = ((pos_PCMCS[0] + shift_x) / monitor_width_cm,
                    ((pos_PCMCS[1] * -1) + shift_y) / monitor_height_cm)

        return pos_ADCS

    def wait_for_eye_response_override(self, expected_eye_pos, sampling_window):
        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = self.PCMCS_to_ADCS(expected_eye_pos)
        gazeData['right_gaze_point_on_display_area'] = self.PCMCS_to_ADCS(expected_eye_pos)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = 1
        gazeData['right_pupil_validity'] = 1

        for i in range(sampling_window):
            self.experiment.eye_data_callback(gazeData)

        return self.experiment.wait_for_eye_response_original(expected_eye_pos, sampling_window)

    def checkOutputFile(self, timing_small_delta=False):
        if self.update_references:
            return

        reference_file_path = os.path.join(
            self.current_dir, "reference", "toth-bela_10__log.txt")
        workdir_output = os.path.join(
            self.work_dir, "logs", "toth-bela_10__log.txt")

        with open(reference_file_path, "r") as ref_file:
            with open(workdir_output, "r") as output_file:
                while True:
                    ref_line = ref_file.readline()
                    output_line = output_file.readline()

                    # make sure both files have the same number of lines
                    self.assertEqual(bool(ref_line), bool(output_line))

                    if not ref_line or not output_line:
                        break

                    ref_values = ref_line.split("\t")
                    act_values = output_line.split("\t")

                    if ref_values[0] == "computer_name":
                        # first line is equal (headers)
                        self.assertEqual(ref_line, output_line)
                        continue

                    self.assertEqual(ref_values[0], act_values[0])  # computer name
                    self.assertEqual(ref_values[1], act_values[1])  # monitor_width_pixel
                    self.assertEqual(ref_values[2], act_values[2])  # monitor_height_pixel
                    self.assertEqual(ref_values[3], act_values[3])  # subject_group
                    self.assertEqual(ref_values[4], act_values[4])  # subject_name
                    self.assertEqual(ref_values[5], act_values[5])  # subject_number
                    self.assertEqual(ref_values[6], act_values[6])  # subject_sex
                    self.assertEqual(ref_values[7], act_values[7])  # subject_age
                    self.assertEqual(ref_values[8], act_values[8])  # asrt_type
                    self.assertEqual(ref_values[9], act_values[9])  # PCode
                    self.assertEqual(ref_values[10], act_values[10])  # session
                    self.assertEqual(ref_values[11], act_values[11])  # epoch
                    self.assertEqual(ref_values[12], act_values[12])  # block
                    self.assertEqual(ref_values[13], act_values[13])  # trial
                    # RSI
                    self.assertAlmostEqual(
                        float(ref_values[14].replace(",", ".")),
                        float(act_values[14].replace(",", ".")), delta=(0.002 if timing_small_delta else 0.1))
                    self.assertEqual(ref_values[15], act_values[15])  # frame_rate
                    self.assertEqual(ref_values[16], act_values[16])  # frame_time
                    self.assertEqual(ref_values[17], act_values[17])  # frame_sd
                    self.assertEqual(ref_values[18], act_values[18])  # stimulus color
                    self.assertEqual(ref_values[19], act_values[19])  # trial_type_pr
                    self.assertEqual(ref_values[20], act_values[20])  # triplet_type_hl
                    self.assertEqual(ref_values[21], act_values[21])  # stimulus
                    self.assertEqual(ref_values[22], act_values[22])  # trial_phase
                    self.assertEqual(ref_values[23], act_values[23])  # left_gaze_data_X_ADCS
                    self.assertEqual(ref_values[24], act_values[24])  # left_gaze_data_Y_ADCS
                    self.assertEqual(ref_values[25], act_values[25])  # right_gaze_data_X_ADCS
                    self.assertEqual(ref_values[26], act_values[26])  # right_gaze_data_Y_ADCS
                    self.assertEqual(ref_values[27], act_values[27])  # left_gaze_data_X_PCMCS
                    self.assertEqual(ref_values[28], act_values[28])  # left_gaze_data_Y_PCMCS
                    self.assertEqual(ref_values[29], act_values[29])  # right_gaze_data_X_PCMCS
                    self.assertEqual(ref_values[30], act_values[30])  # right_gaze_data_Y_PCMCS
                    self.assertEqual(ref_values[31], act_values[31])  # left_gaze_validity
                    self.assertEqual(ref_values[32], act_values[32])  # right_gaze_validity
                    self.assertEqual(ref_values[33], act_values[33])  # left_pupil_diameter
                    self.assertEqual(ref_values[34], act_values[34])  # right_pupil_diameter
                    self.assertEqual(ref_values[35], act_values[35])  # left_pupil_validity
                    self.assertEqual(ref_values[36], act_values[36])  # right_pupil_validity
                    self.assertEqual(ref_values[37], act_values[37])  # gaze_data_time_stamp
                    self.assertEqual(ref_values[38], act_values[38])  # stimulus_1_position_X_PCMCS
                    self.assertEqual(ref_values[39], act_values[39])  # stimulus_1_position_Y_PCMCS
                    self.assertEqual(ref_values[40], act_values[40])  # stimulus_2_position_X_PCMCS
                    self.assertEqual(ref_values[41], act_values[41])  # stimulus_2_position_Y_PCMCS
                    self.assertEqual(ref_values[42], act_values[42])  # stimulus_3_position_X_PCMCS
                    self.assertEqual(ref_values[43], act_values[43])  # stimulus_3_position_Y_PCMCS
                    self.assertEqual(ref_values[44], act_values[44])  # stimulus_4_position_X_PCMCS
                    self.assertEqual(ref_values[45], act_values[45])  # stimulus_4_position_Y_PCMCS
                    self.assertEqual(ref_values[46], act_values[46])  # quit_log

    def testSimpleTestCase(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, 'férfi', 25, '3rd'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        self.experiment.run(window_gammaErrorPolicy='ignore')

        self.checkOutputFile(True)


if __name__ == "__main__":
    unittest.main()  # run all tests
