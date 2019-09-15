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
import psychopy_gui_mock as pgm


class allSettingsDefTest(unittest.TestCase):

    def tearDown(self):
        tempdir = os.path.abspath(__file__)
        (tempdir, trail) = os.path.split(tempdir)
        tempdir = os.path.join(tempdir, "data", "all_settings_def")

        # remove all temp files
        for file in os.listdir(tempdir):
            file_path = os.path.join(tempdir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def setUp(self):
        tempdir = os.path.abspath(__file__)
        (tempdir, trail) = os.path.split(tempdir)
        tempdir = os.path.join(tempdir, "data", "all_settings_def")
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)

    def constructFilePath(self, file_name):
        filepath = os.path.abspath(__file__)
        (inst_and_feedback_path, trail) = os.path.split(filepath)
        inst_and_feedback_path = os.path.join(inst_and_feedback_path, "data")
        inst_and_feedback_path = os.path.join(
            inst_and_feedback_path, "all_settings_def")
        inst_and_feedback_path = os.path.join(
            inst_and_feedback_path, file_name)
        return inst_and_feedback_path

    def testLoadExistingSettings(self):
        output_file = self.constructFilePath("testLoadExistingSettings")
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings(output_file, "")

        experiment.settings.experiment_type = 'reaction-time'
        experiment.settings.numsessions = 1
        experiment.settings.groups = ["kontrol"]
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.block_in_epochN = 5
        experiment.settings.epochN = 5
        experiment.settings.epochs = [5]
        experiment.settings.asrt_types = ["implicit"]
        experiment.settings.monitor_width = 29
        experiment.settings.computer_name = "Laposka"
        experiment.settings.asrt_distance = 4.5
        experiment.settings.asrt_size = 1.8
        experiment.settings.asrt_rcolor = "Orange"
        experiment.settings.asrt_pcolor = "Green"
        experiment.settings.asrt_background = "Ivory"
        experiment.settings.RSI_time = 0.12
        experiment.settings.key1 = 'z'
        experiment.settings.key2 = 'c'
        experiment.settings.key3 = 'b'
        experiment.settings.key4 = 'm'
        experiment.settings.key_quit = 'q'
        experiment.settings.whether_warning = True
        experiment.settings.speed_warning = 93
        experiment.settings.acc_warning = 91

        experiment.settings.write_to_file()

        experiment.settings = asrt.ExperimentSettings(output_file, "")
        experiment.all_settings_def()

        self.assertEqual(experiment.settings.experiment_type, 'reaction-time')
        self.assertEqual(experiment.settings.groups, ["kontrol"])
        self.assertEqual(experiment.settings.blockprepN, 5)
        self.assertEqual(experiment.settings.blocklengthN, 80)
        self.assertEqual(experiment.settings.block_in_epochN, 5)
        self.assertEqual(experiment.settings.epochN, 5)
        self.assertEqual(experiment.settings.epochs, [5])
        self.assertEqual(experiment.settings.asrt_types, ["implicit"])
        self.assertEqual(experiment.settings.monitor_width, 29)
        self.assertEqual(experiment.settings.computer_name, "Laposka")
        self.assertEqual(experiment.settings.asrt_distance, 4.5)
        self.assertEqual(experiment.settings.asrt_size, 1.8)
        self.assertEqual(experiment.settings.asrt_rcolor, "Orange")
        self.assertEqual(experiment.settings.asrt_pcolor, "Green")
        self.assertEqual(experiment.settings.asrt_background, "Ivory")
        self.assertEqual(experiment.settings.RSI_time, 0.12)
        self.assertEqual(experiment.settings.key1, 'z')
        self.assertEqual(experiment.settings.key2, 'c')
        self.assertEqual(experiment.settings.key3, 'b')
        self.assertEqual(experiment.settings.key4, 'm')
        self.assertEqual(experiment.settings.key_quit, 'q')
        self.assertEqual(experiment.settings.whether_warning, True)
        self.assertEqual(experiment.settings.speed_warning, 93)
        self.assertEqual(experiment.settings.acc_warning, 91)
        self.assertEqual(experiment.settings.get_maxtrial(), 2125)
        self.assertEqual(experiment.settings.get_session_starts(), [1, 2126])
        self.assertEqual(experiment.settings.get_block_starts(), [
                         1, 86, 171, 256, 341, 426, 511, 596, 681, 766, 851, 936, 1021, 1106, 1191, 1276, 1361, 1446, 1531, 1616, 1701, 1786, 1871, 1956, 2041, 2126, 2211])

    def testSettingsDialogsDefaultValues(self):
        output_file = self.constructFilePath(
            "testSettingsDialogsDefaultValues")
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings(
            output_file, output_file + "_reminder.txt")

        gui_mock = pgm.PsychoPyGuiMock()
        experiment.all_settings_def()

        self.assertEqual(experiment.settings.experiment_type, 'reaction-time')
        self.assertEqual(experiment.settings.groups, ["", ""])
        self.assertEqual(experiment.settings.blockprepN, 5)
        self.assertEqual(experiment.settings.blocklengthN, 80)
        self.assertEqual(experiment.settings.block_in_epochN, 5)
        self.assertEqual(experiment.settings.epochN, 10)
        self.assertEqual(experiment.settings.epochs, [5, 5])
        self.assertEqual(experiment.settings.asrt_types, {1: 'implicit', 2: 'implicit'})
        self.assertEqual(experiment.settings.monitor_width, 34.2)
        self.assertEqual(experiment.settings.computer_name, "Laposka")
        self.assertEqual(experiment.settings.asrt_distance, 3)
        self.assertEqual(experiment.settings.asrt_size, 1)
        self.assertEqual(experiment.settings.asrt_rcolor, "Orange")
        self.assertEqual(experiment.settings.asrt_pcolor, "Green")
        self.assertEqual(experiment.settings.asrt_background, "Ivory")
        self.assertEqual(experiment.settings.RSI_time, 0.12)
        self.assertEqual(experiment.settings.key1, 'y')
        self.assertEqual(experiment.settings.key2, 'c')
        self.assertEqual(experiment.settings.key3, 'b')
        self.assertEqual(experiment.settings.key4, 'm')
        self.assertEqual(experiment.settings.key_quit, 'q')
        self.assertEqual(experiment.settings.whether_warning, True)
        self.assertEqual(experiment.settings.speed_warning, 93)
        self.assertEqual(experiment.settings.acc_warning, 91)
        self.assertEqual(experiment.settings.get_maxtrial(), 4250)
        self.assertEqual(
            experiment.settings.get_session_starts(), [1, 2126, 4251])
        self.assertEqual(experiment.settings.get_block_starts(), [1, 86, 171, 256, 341, 426, 511, 596, 681, 766, 851, 936, 1021, 1106, 1191,
                                                                  1276, 1361, 1446, 1531, 1616, 1701, 1786, 1871, 1956, 2041, 2126, 2211, 2296,
                                                                  2381, 2466, 2551, 2636, 2721, 2806, 2891, 2976, 3061, 3146, 3231, 3316, 3401,
                                                                  3486, 3571, 3656, 3741, 3826, 3911, 3996, 4081, 4166, 4251, 4336])
        # output file exists
        self.assertTrue(os.path.exists(output_file + ".dat") or os.path.exists(output_file))
        self.assertTrue(os.path.exists(output_file + "_reminder.txt"))

        # reload saved data
        experiment.settings = asrt.ExperimentSettings(output_file, "")
        experiment.all_settings_def()

        self.assertEqual(experiment.settings.experiment_type, 'reaction-time')
        self.assertEqual(experiment.settings.groups, ["", ""])
        self.assertEqual(experiment.settings.blockprepN, 5)
        self.assertEqual(experiment.settings.blocklengthN, 80)
        self.assertEqual(experiment.settings.block_in_epochN, 5)
        self.assertEqual(experiment.settings.epochN, 10)
        self.assertEqual(experiment.settings.epochs, [5, 5])
        self.assertEqual(experiment.settings.asrt_types, {1: 'implicit', 2: 'implicit'})
        self.assertEqual(experiment.settings.monitor_width, 34.2)
        self.assertEqual(experiment.settings.computer_name, "Laposka")
        self.assertEqual(experiment.settings.asrt_distance, 3)
        self.assertEqual(experiment.settings.asrt_size, 1)
        self.assertEqual(experiment.settings.asrt_rcolor, "Orange")
        self.assertEqual(experiment.settings.asrt_pcolor, "Green")
        self.assertEqual(experiment.settings.asrt_background, "Ivory")
        self.assertEqual(experiment.settings.RSI_time, 0.12)
        self.assertEqual(experiment.settings.key1, 'y')
        self.assertEqual(experiment.settings.key2, 'c')
        self.assertEqual(experiment.settings.key3, 'b')
        self.assertEqual(experiment.settings.key4, 'm')
        self.assertEqual(experiment.settings.key_quit, 'q')
        self.assertEqual(experiment.settings.whether_warning, True)
        self.assertEqual(experiment.settings.speed_warning, 93)
        self.assertEqual(experiment.settings.acc_warning, 91)
        self.assertEqual(experiment.settings.get_maxtrial(), 4250)
        self.assertEqual(
            experiment.settings.get_session_starts(), [1, 2126, 4251])
        self.assertEqual(experiment.settings.get_block_starts(), [1, 86, 171, 256, 341, 426, 511, 596, 681, 766, 851, 936, 1021, 1106, 1191,
                                                                  1276, 1361, 1446, 1531, 1616, 1701, 1786, 1871, 1956, 2041, 2126, 2211, 2296,
                                                                  2381, 2466, 2551, 2636, 2721, 2806, 2891, 2976, 3061, 3146, 3231, 3316, 3401,
                                                                  3486, 3571, 3656, 3741, 3826, 3911, 3996, 4081, 4166, 4251, 4336])

    def testSettingsDialogsCustomValues(self):
        output_file = self.constructFilePath("testSettingsDialogsCustomValues")
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings(
            output_file, output_file + "_reminder.txt")

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['reakció idő', 1, 1, 10, 75, 7, 12, 'implicit', 29.1, "Alma", 4, 2, "Blue", "Red",
                                 "Yellow", 300, 'a', 's', 'd', 'f', 'g', False, 89, 78])
        experiment.all_settings_def()

        self.assertEqual(experiment.settings.experiment_type, 'reaction-time')
        self.assertEqual(experiment.settings.groups, ['nincsenek csoportok'])
        self.assertEqual(experiment.settings.blockprepN, 10)
        self.assertEqual(experiment.settings.blocklengthN, 75)
        self.assertEqual(experiment.settings.block_in_epochN, 7)
        self.assertEqual(experiment.settings.epochN, 12)
        self.assertEqual(experiment.settings.epochs, [12])
        self.assertEqual(experiment.settings.asrt_types, {1: 'implicit'})
        self.assertEqual(experiment.settings.monitor_width, 29.1)
        self.assertEqual(experiment.settings.computer_name, "Alma")
        self.assertEqual(experiment.settings.asrt_distance, 4)
        self.assertEqual(experiment.settings.asrt_size, 2)
        self.assertEqual(experiment.settings.asrt_rcolor, "Blue")
        self.assertEqual(experiment.settings.asrt_pcolor, "Red")
        self.assertEqual(experiment.settings.asrt_background, "Yellow")
        self.assertEqual(experiment.settings.RSI_time, 0.3)
        self.assertEqual(experiment.settings.key1, 'a')
        self.assertEqual(experiment.settings.key2, 's')
        self.assertEqual(experiment.settings.key3, 'd')
        self.assertEqual(experiment.settings.key4, 'f')
        self.assertEqual(experiment.settings.key_quit, 'g')
        self.assertEqual(experiment.settings.whether_warning, False)
        self.assertEqual(experiment.settings.speed_warning, 89)
        self.assertEqual(experiment.settings.acc_warning, 78)
        self.assertEqual(experiment.settings.get_maxtrial(), 7140)
        self.assertEqual(experiment.settings.get_session_starts(), [1, 7141])
        self.assertEqual(experiment.settings.get_block_starts(), [1, 86, 171, 256, 341, 426, 511, 596, 681, 766, 851, 936, 1021, 1106, 1191,
                                                                  1276, 1361, 1446, 1531, 1616, 1701, 1786, 1871, 1956, 2041, 2126, 2211, 2296,
                                                                  2381, 2466, 2551, 2636, 2721, 2806, 2891, 2976, 3061, 3146, 3231, 3316, 3401,
                                                                  3486, 3571, 3656, 3741, 3826, 3911, 3996, 4081, 4166, 4251, 4336, 4421, 4506,
                                                                  4591, 4676, 4761, 4846, 4931, 5016, 5101, 5186, 5271, 5356, 5441, 5526, 5611,
                                                                  5696, 5781, 5866, 5951, 6036, 6121, 6206, 6291, 6376, 6461, 6546, 6631, 6716,
                                                                  6801, 6886, 6971, 7056, 7141, 7226])
        # output file exists
        self.assertTrue(os.path.exists(output_file + ".dat") or os.path.exists(output_file))
        self.assertTrue(os.path.exists(output_file + "_reminder.txt"))

        # reload saved data
        experiment.settings = asrt.ExperimentSettings(output_file, "")
        experiment.all_settings_def()

        self.assertEqual(experiment.settings.experiment_type, 'reaction-time')
        self.assertEqual(experiment.settings.groups, ['nincsenek csoportok'])
        self.assertEqual(experiment.settings.blockprepN, 10)
        self.assertEqual(experiment.settings.blocklengthN, 75)
        self.assertEqual(experiment.settings.block_in_epochN, 7)
        self.assertEqual(experiment.settings.epochN, 12)
        self.assertEqual(experiment.settings.epochs, [12])
        self.assertEqual(experiment.settings.asrt_types, {1: 'implicit'})
        self.assertEqual(experiment.settings.monitor_width, 29.1)
        self.assertEqual(experiment.settings.computer_name, "Alma")
        self.assertEqual(experiment.settings.asrt_distance, 4)
        self.assertEqual(experiment.settings.asrt_size, 2)
        self.assertEqual(experiment.settings.asrt_rcolor, "Blue")
        self.assertEqual(experiment.settings.asrt_pcolor, "Red")
        self.assertEqual(experiment.settings.asrt_background, "Yellow")
        self.assertEqual(experiment.settings.RSI_time, 0.3)
        self.assertEqual(experiment.settings.key1, 'a')
        self.assertEqual(experiment.settings.key2, 's')
        self.assertEqual(experiment.settings.key3, 'd')
        self.assertEqual(experiment.settings.key4, 'f')
        self.assertEqual(experiment.settings.key_quit, 'g')
        self.assertEqual(experiment.settings.whether_warning, False)
        self.assertEqual(experiment.settings.speed_warning, 89)
        self.assertEqual(experiment.settings.acc_warning, 78)
        self.assertEqual(experiment.settings.get_maxtrial(), 7140)
        self.assertEqual(experiment.settings.get_session_starts(), [1, 7141])
        self.assertEqual(experiment.settings.get_block_starts(), [1, 86, 171, 256, 341, 426, 511, 596, 681, 766, 851, 936, 1021, 1106, 1191,
                                                                  1276, 1361, 1446, 1531, 1616, 1701, 1786, 1871, 1956, 2041, 2126, 2211, 2296,
                                                                  2381, 2466, 2551, 2636, 2721, 2806, 2891, 2976, 3061, 3146, 3231, 3316, 3401,
                                                                  3486, 3571, 3656, 3741, 3826, 3911, 3996, 4081, 4166, 4251, 4336, 4421, 4506,
                                                                  4591, 4676, 4761, 4846, 4931, 5016, 5101, 5186, 5271, 5356, 5441, 5526, 5611,
                                                                  5696, 5781, 5866, 5951, 6036, 6121, 6206, 6291, 6376, 6461, 6546, 6631, 6716,
                                                                  6801, 6886, 6971, 7056, 7141, 7226])


if __name__ == "__main__":
    unittest.main()  # run all tests
