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
import shelve
import dbm
import codecs


class experimentSettingsFileHandlingTest(unittest.TestCase):

    def tearDown(self):
        tempdir = os.path.abspath(__file__)
        (tempdir, trail) = os.path.split(tempdir)
        tempdir = os.path.join(tempdir, "data", "experiment_settings")

        # remove all temp files
        for file in os.listdir(tempdir):
            file_path = os.path.join(tempdir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def setUp(self):
        tempdir = os.path.abspath(__file__)
        (tempdir, trail) = os.path.split(tempdir)
        tempdir = os.path.join(tempdir, "data", "experiment_settings")
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)

    def constructFilePath(self, file_name):
        filepath = os.path.abspath(__file__)
        (inst_and_feedback_path, trail) = os.path.split(filepath)
        inst_and_feedback_path = os.path.join(inst_and_feedback_path, "data")
        inst_and_feedback_path = os.path.join(
            inst_and_feedback_path, "experiment_settings")
        inst_and_feedback_path = os.path.join(
            inst_and_feedback_path, file_name)
        return inst_and_feedback_path

    def testRoundTripInitialState(self):
        output_file = self.constructFilePath("testRoundTripInitialState")
        exp_settings = asrt.ExperimentSettings(output_file, "")
        exp_settings.write_to_file()

        exp_settings = asrt.ExperimentSettings(output_file, "")
        exp_settings.read_from_file()

        self.assertEqual(exp_settings.experiment_type, None)
        self.assertEqual(exp_settings.groups, None)
        self.assertEqual(exp_settings.blockprepN, None)
        self.assertEqual(exp_settings.blocklengthN, None)
        self.assertEqual(exp_settings.block_in_epochN, None)
        self.assertEqual(exp_settings.epochN, None)
        self.assertEqual(exp_settings.epochs, None)
        self.assertEqual(exp_settings.asrt_types, None)
        self.assertEqual(exp_settings.monitor_width, None)
        self.assertEqual(exp_settings.computer_name, None)
        self.assertEqual(exp_settings.asrt_distance, None)
        self.assertEqual(exp_settings.asrt_size, None)
        self.assertEqual(exp_settings.asrt_rcolor, None)
        self.assertEqual(exp_settings.asrt_pcolor, None)
        self.assertEqual(exp_settings.asrt_background, None)
        self.assertEqual(exp_settings.RSI_time, None)
        self.assertEqual(exp_settings.AOI_size, None)
        self.assertEqual(exp_settings.stim_fixation_threshold, None)
        self.assertEqual(exp_settings.instruction_fixation_threshold, None)
        self.assertEqual(exp_settings.key1, None)
        self.assertEqual(exp_settings.key2, None)
        self.assertEqual(exp_settings.key3, None)
        self.assertEqual(exp_settings.key4, None)
        self.assertEqual(exp_settings.key_quit, None)
        self.assertEqual(exp_settings.whether_warning, None)
        self.assertEqual(exp_settings.speed_warning, None)
        self.assertEqual(exp_settings.acc_warning, None)

        with self.assertRaises(TypeError):
            exp_settings.get_maxtrial()

        with self.assertRaises(TypeError):
            exp_settings.get_session_starts()

        with self.assertRaises(TypeError):
            exp_settings.get_block_starts()

        self.assertEqual(exp_settings.get_key_list(), None)

    def testRoundTripCustomValues(self):
        output_file = self.constructFilePath("testRoundTripCustomValues")
        exp_settings = asrt.ExperimentSettings(output_file, "")

        exp_settings.experiment_type = 'reaction-time'
        exp_settings.numsessions = 1
        exp_settings.groups = ["kontrol"]
        exp_settings.blockprepN = 5
        exp_settings.blocklengthN = 80
        exp_settings.block_in_epochN = 5
        exp_settings.epochN = 5
        exp_settings.epochs = [5]
        exp_settings.asrt_types = ["implicit"]
        exp_settings.monitor_width = 29
        exp_settings.computer_name = "Laposka"
        exp_settings.asrt_distance = 4.5
        exp_settings.asrt_size = 1.8
        exp_settings.asrt_rcolor = "Orange"
        exp_settings.asrt_pcolor = "Green"
        exp_settings.asrt_background = "Ivory"
        exp_settings.RSI_time = 0.12
        exp_settings.key1 = 'z'
        exp_settings.key2 = 'c'
        exp_settings.key3 = 'b'
        exp_settings.key4 = 'm'
        exp_settings.key_quit = 'q'
        exp_settings.whether_warning = True
        exp_settings.speed_warning = 93
        exp_settings.acc_warning = 91

        exp_settings.write_to_file()

        exp_settings = asrt.ExperimentSettings(output_file, "")
        exp_settings.read_from_file()

        self.assertEqual(exp_settings.experiment_type, "reaction-time")
        self.assertEqual(exp_settings.groups, ["kontrol"])
        self.assertEqual(exp_settings.blockprepN, 5)
        self.assertEqual(exp_settings.blocklengthN, 80)
        self.assertEqual(exp_settings.block_in_epochN, 5)
        self.assertEqual(exp_settings.epochN, 5)
        self.assertEqual(exp_settings.epochs, [5])
        self.assertEqual(exp_settings.asrt_types, ["implicit"])
        self.assertEqual(exp_settings.monitor_width, 29)
        self.assertEqual(exp_settings.computer_name, "Laposka")
        self.assertEqual(exp_settings.asrt_distance, 4.5)
        self.assertEqual(exp_settings.asrt_size, 1.8)
        self.assertEqual(exp_settings.asrt_rcolor, "Orange")
        self.assertEqual(exp_settings.asrt_pcolor, "Green")
        self.assertEqual(exp_settings.asrt_background, "Ivory")
        self.assertEqual(exp_settings.RSI_time, 0.12)
        self.assertEqual(exp_settings.AOI_size, None)
        self.assertEqual(exp_settings.stim_fixation_threshold, None)
        self.assertEqual(exp_settings.instruction_fixation_threshold, None)
        self.assertEqual(exp_settings.key1, 'z')
        self.assertEqual(exp_settings.key2, 'c')
        self.assertEqual(exp_settings.key3, 'b')
        self.assertEqual(exp_settings.key4, 'm')
        self.assertEqual(exp_settings.key_quit, 'q')
        self.assertEqual(exp_settings.whether_warning, True)
        self.assertEqual(exp_settings.speed_warning, 93)
        self.assertEqual(exp_settings.acc_warning, 91)
        self.assertEqual(exp_settings.get_maxtrial(), 2125)
        self.assertEqual(exp_settings.get_session_starts(), [1, 2126])
        self.assertEqual(exp_settings.get_block_starts(), [1, 86, 171, 256, 341, 426, 511, 596, 681, 766, 851,
                                                           936, 1021, 1106, 1191, 1276, 1361, 1446, 1531, 1616, 1701, 1786, 1871, 1956, 2041, 2126, 2211])
        self.assertEqual(exp_settings.get_key_list(), ['z', 'c', 'b', 'm', 'q'])

    def testRoundTripCustomValuesET(self):
        output_file = self.constructFilePath("testRoundTripCustomValuesET")
        exp_settings = asrt.ExperimentSettings(output_file, "")

        exp_settings.experiment_type = 'eye-tracking'
        exp_settings.numsessions = 1
        exp_settings.groups = ["kontrol"]
        exp_settings.blockprepN = 5
        exp_settings.blocklengthN = 80
        exp_settings.block_in_epochN = 5
        exp_settings.epochN = 5
        exp_settings.epochs = [5]
        exp_settings.asrt_types = ["implicit"]
        exp_settings.monitor_width = 29
        exp_settings.computer_name = "Laposka"
        exp_settings.asrt_distance = 4.5
        exp_settings.asrt_size = 1.8
        exp_settings.asrt_rcolor = "Orange"
        exp_settings.asrt_pcolor = "Green"
        exp_settings.asrt_background = "Ivory"
        exp_settings.RSI_time = 0.12
        exp_settings.AOI_size = 1.5
        exp_settings.stim_fixation_threshold = 12
        exp_settings.instruction_fixation_threshold = 36
        exp_settings.key1 = 'z'
        exp_settings.key2 = 'c'
        exp_settings.key3 = 'b'
        exp_settings.key4 = 'm'
        exp_settings.key_quit = 'q'
        exp_settings.whether_warning = True
        exp_settings.speed_warning = 93
        exp_settings.acc_warning = 91

        exp_settings.write_to_file()

        exp_settings = asrt.ExperimentSettings(output_file, "")
        exp_settings.read_from_file()

        self.assertEqual(exp_settings.experiment_type, "eye-tracking")
        self.assertEqual(exp_settings.groups, ["kontrol"])
        self.assertEqual(exp_settings.blockprepN, 5)
        self.assertEqual(exp_settings.blocklengthN, 80)
        self.assertEqual(exp_settings.block_in_epochN, 5)
        self.assertEqual(exp_settings.epochN, 5)
        self.assertEqual(exp_settings.epochs, [5])
        self.assertEqual(exp_settings.asrt_types, ["implicit"])
        self.assertEqual(exp_settings.monitor_width, 29)
        self.assertEqual(exp_settings.computer_name, "Laposka")
        self.assertEqual(exp_settings.asrt_distance, 4.5)
        self.assertEqual(exp_settings.asrt_size, 1.8)
        self.assertEqual(exp_settings.asrt_rcolor, "Orange")
        self.assertEqual(exp_settings.asrt_pcolor, "Green")
        self.assertEqual(exp_settings.asrt_background, "Ivory")
        self.assertEqual(exp_settings.RSI_time, 0.12)
        self.assertEqual(exp_settings.AOI_size, 1.5)
        self.assertEqual(exp_settings.stim_fixation_threshold, 12)
        self.assertEqual(exp_settings.instruction_fixation_threshold, 36)
        self.assertEqual(exp_settings.key1, None)
        self.assertEqual(exp_settings.key2, None)
        self.assertEqual(exp_settings.key3, None)
        self.assertEqual(exp_settings.key4, None)
        self.assertEqual(exp_settings.key_quit, 'q')
        self.assertEqual(exp_settings.whether_warning, None)
        self.assertEqual(exp_settings.speed_warning, None)
        self.assertEqual(exp_settings.acc_warning, None)
        self.assertEqual(exp_settings.get_maxtrial(), 2125)
        self.assertEqual(exp_settings.get_session_starts(), [1, 2126])
        self.assertEqual(exp_settings.get_block_starts(), [1, 86, 171, 256, 341, 426, 511, 596, 681, 766, 851,
                                                           936, 1021, 1106, 1191, 1276, 1361, 1446, 1531, 1616, 1701, 1786, 1871, 1956, 2041, 2126, 2211])
        self.assertEqual(exp_settings.get_key_list(), ['q'])

    def testReadEmptyFile(self):
        output_file = self.constructFilePath("testReadEmptyFile")
        exp_settings = asrt.ExperimentSettings(output_file, "")

        with self.assertRaises(dbm.error):
            exp_settings.read_from_file()

    def testReadCorruptedFile(self):
        output_file = self.constructFilePath("testReadCorruptedFile")
        exp_settings = asrt.ExperimentSettings(output_file, "")

        # not all data is written out
        with shelve.open(output_file) as settings_file:
            settings_file['numsessions'] = 10
            settings_file['groups'] = ["kontrol"]

        with self.assertRaises(KeyError):
            exp_settings.read_from_file()

        # exp_settings has the initial state
        self.assertEqual(exp_settings.experiment_type, None)
        self.assertEqual(exp_settings.groups, None)
        self.assertEqual(exp_settings.blockprepN, None)
        self.assertEqual(exp_settings.blocklengthN, None)
        self.assertEqual(exp_settings.block_in_epochN, None)
        self.assertEqual(exp_settings.epochN, None)
        self.assertEqual(exp_settings.epochs, None)
        self.assertEqual(exp_settings.asrt_types, None)
        self.assertEqual(exp_settings.monitor_width, None)
        self.assertEqual(exp_settings.computer_name, None)
        self.assertEqual(exp_settings.asrt_distance, None)
        self.assertEqual(exp_settings.asrt_size, None)
        self.assertEqual(exp_settings.asrt_rcolor, None)
        self.assertEqual(exp_settings.asrt_pcolor, None)
        self.assertEqual(exp_settings.asrt_background, None)
        self.assertEqual(exp_settings.RSI_time, None)
        self.assertEqual(exp_settings.AOI_size, None)
        self.assertEqual(exp_settings.stim_fixation_threshold, None)
        self.assertEqual(exp_settings.instruction_fixation_threshold, None)
        self.assertEqual(exp_settings.key1, None)
        self.assertEqual(exp_settings.key2, None)
        self.assertEqual(exp_settings.key3, None)
        self.assertEqual(exp_settings.key4, None)
        self.assertEqual(exp_settings.key_quit, None)
        self.assertEqual(exp_settings.whether_warning, None)
        self.assertEqual(exp_settings.speed_warning, None)
        self.assertEqual(exp_settings.acc_warning, None)

    def testReminderTxtCustomValues(self):
        output_file = self.constructFilePath("testReminderTxtCustomValues")
        exp_settings = asrt.ExperimentSettings("", output_file)

        exp_settings.experiment_type = "reaction-time"
        exp_settings.numsessions = 1
        exp_settings.groups = ["kontrol"]
        exp_settings.blockprepN = 5
        exp_settings.blocklengthN = 80
        exp_settings.block_in_epochN = 5
        exp_settings.epochN = 5
        exp_settings.epochs = [5]
        exp_settings.monitor_width = 29
        exp_settings.computer_name = "Laposka"
        exp_settings.asrt_distance = 4.5
        exp_settings.asrt_size = 1.8
        exp_settings.asrt_rcolor = "Orange"
        exp_settings.asrt_pcolor = "Green"
        exp_settings.asrt_background = "Ivory"
        exp_settings.RSI_time = 0.12
        exp_settings.key1 = 'z'
        exp_settings.key2 = 'c'
        exp_settings.key3 = 'b'
        exp_settings.key4 = 'm'
        exp_settings.key_quit = 'q'
        exp_settings.whether_warning = True
        exp_settings.speed_warning = 93
        exp_settings.acc_warning = 91
        exp_settings.sessionstarts = [1, 2, 3]

        exp_settings.write_out_reminder()

        with codecs.open(output_file, 'r', encoding='utf-8') as reminder_file:
            self.assertEqual(reminder_file.read(),
                             u'Beállítások\n' +
                             '\n' +
                             'Monitor Width: ' + '\t' + str(exp_settings.monitor_width).replace('.', ',') + '\n' +
                             'Computer Name: ' + '\t' + exp_settings.computer_name + '\n' +
                             'Experiment type:' + '\t' + exp_settings.experiment_type + '\n' +
                             'Response keys: ' + '\t' + exp_settings.key1 + ', ' + exp_settings.key2 + ', ' + exp_settings.key3 + ', ' + exp_settings.key4 + '.' + '\n' +
                             'Quit key: ' + '\t' + exp_settings.key_quit + '\n' +
                             'Warning (speed, accuracy): ' + '\t' + str(exp_settings.whether_warning) + '\n' +
                             'Speed warning at:' + '\t' + str(exp_settings.speed_warning) + '\n' +
                             'Acc warning at:' + '\t' + str(exp_settings.acc_warning) + '\n' +
                             'Groups:' + '\t' + str(exp_settings.groups)[1:-1].replace("u'", '').replace("'", '') + '\n' +
                             'Sessions:' + '\t' + str(exp_settings.numsessions) + '\n' +
                             'Epochs in sessions:' + '\t' + str(exp_settings.epochs)[1:-1].replace("u'", '').replace("'", '') + '\n' +
                             'Blocks in epochs:' + '\t' + str(exp_settings.block_in_epochN) + '\n' +
                             'Preparatory Trials\\Block:' + '\t' + str(exp_settings.blockprepN) + '\n' +
                             'Trials\\Block:' + '\t' + str(exp_settings.blocklengthN) + '\n' +
                             'RSI:' + '\t' + str(exp_settings.RSI_time).replace('.', ',') + '\n' +
                             'Asrt stim distance:' + '\t' + str(exp_settings.asrt_distance).replace('.', ',') + '\n' +
                             'Asrt stim size:' + '\t' + str(exp_settings.asrt_size).replace('.', ',') + '\n' +
                             'Asrt stim color (implicit):' + '\t' + exp_settings.asrt_rcolor + '\n' +
                             'Asrt stim color (explicit, cued):' + '\t' + exp_settings.asrt_pcolor + '\n' +
                             'Background color:' + '\t' + exp_settings.asrt_background + '\n' +
                             '\n' +
                             'Az alábbi beállítások minden személyre érvényesek és irányadóak\n\n' +

                             'A beállítások azokra a kísérletekre vonatkoznak, amelyeket ebből a mappából,\n' +
                             'az itt található scripttel indítottak. Ha más beállításokat (is) szeretnél alkalmazni,\n' +
                             'úgy az asrt.py és az instrukciókat tartalmazó inst_and_feedback.txt fájlt másold át egy,\n' +
                             'másik könyvtárba is, és annak a scriptnek az indításakor megadhatod a kívánt másmilyen beállításokat.\n\n' +

                             'Figyelj rá, hogy mindig abból a könyvtárból indítsd a scriptet, ahol a számodra megfelelő\n' +
                             'beállítások vannak elmentve.\n\n' +

                             'A settings/settings fájl kitörlésével a beállítások megváltoztathatóak; ugyanakkor a fájl\n' +
                             'törlése a későbbi átláthatóság miatt nem javasolt. Ha mégis a törlés mellett döntenél,\n' +
                             'jelen .txt fájlt előtte másold le, hogy a korábbi beállításokra is emlékezhess, ha szükséges lesz.\n')

    def testReminderTxtCustomValuesET(self):
        output_file = self.constructFilePath("testReminderTxtCustomValuesET")
        exp_settings = asrt.ExperimentSettings("", output_file)

        exp_settings.experiment_type = 'eye-tracking'
        exp_settings.numsessions = 1
        exp_settings.groups = ["kontrol"]
        exp_settings.blockprepN = 5
        exp_settings.blocklengthN = 80
        exp_settings.block_in_epochN = 5
        exp_settings.epochN = 5
        exp_settings.epochs = [5]
        exp_settings.monitor_width = 29
        exp_settings.computer_name = "Laposka"
        exp_settings.asrt_distance = 4.5
        exp_settings.asrt_size = 1.8
        exp_settings.asrt_rcolor = "Orange"
        exp_settings.asrt_pcolor = "Green"
        exp_settings.asrt_background = "Ivory"
        exp_settings.RSI_time = 0.12
        exp_settings.AOI_size = 1.5
        exp_settings.stim_fixation_threshold = 12
        exp_settings.instruction_fixation_threshold = 36
        exp_settings.key_quit = 'q'
        exp_settings.sessionstarts = [1, 2, 3]

        exp_settings.write_out_reminder()

        with codecs.open(output_file, 'r', encoding='utf-8') as reminder_file:
            self.assertEqual(reminder_file.read(),
                             u'Beállítások\n' +
                             '\n' +
                             'Monitor Width: ' + '\t' + str(exp_settings.monitor_width).replace('.', ',') + '\n' +
                             'Computer Name: ' + '\t' + exp_settings.computer_name + '\n' +
                             'Experiment type:' + '\t' + exp_settings.experiment_type + '\n' +
                             'Groups:' + '\t' + str(exp_settings.groups)[1:-1].replace("u'", '').replace("'", '') + '\n' +
                             'Sessions:' + '\t' + str(exp_settings.numsessions) + '\n' +
                             'Epochs in sessions:' + '\t' + str(exp_settings.epochs)[1:-1].replace("u'", '').replace("'", '') + '\n' +
                             'Blocks in epochs:' + '\t' + str(exp_settings.block_in_epochN) + '\n' +
                             'Preparatory Trials\\Block:' + '\t' + str(exp_settings.blockprepN) + '\n' +
                             'Trials\\Block:' + '\t' + str(exp_settings.blocklengthN) + '\n' +
                             'RSI:' + '\t' + str(exp_settings.RSI_time).replace('.', ',') + '\n' +
                             'Asrt stim distance:' + '\t' + str(exp_settings.asrt_distance).replace('.', ',') + '\n' +
                             'Asrt stim size:' + '\t' + str(exp_settings.asrt_size).replace('.', ',') + '\n' +
                             'Asrt stim color (implicit):' + '\t' + exp_settings.asrt_rcolor + '\n' +
                             'Asrt stim color (explicit, cued):' + '\t' + exp_settings.asrt_pcolor + '\n' +
                             'Background color:' + '\t' + exp_settings.asrt_background + '\n' +
                             'AOI size:' + '\t' + str(exp_settings.AOI_size).replace('.', ',') + '\n' +
                             'Fixation threshold for stimulus:' + '\t' + str(exp_settings.stim_fixation_threshold) + '\n' +
                             'Fixation threshold for instructions:' + '\t' + str(exp_settings.instruction_fixation_threshold) + '\n'
                             '\n' +
                             'Az alábbi beállítások minden személyre érvényesek és irányadóak\n\n' +

                             'A beállítások azokra a kísérletekre vonatkoznak, amelyeket ebből a mappából,\n' +
                             'az itt található scripttel indítottak. Ha más beállításokat (is) szeretnél alkalmazni,\n' +
                             'úgy az asrt.py és az instrukciókat tartalmazó inst_and_feedback.txt fájlt másold át egy,\n' +
                             'másik könyvtárba is, és annak a scriptnek az indításakor megadhatod a kívánt másmilyen beállításokat.\n\n' +

                             'Figyelj rá, hogy mindig abból a könyvtárból indítsd a scriptet, ahol a számodra megfelelő\n' +
                             'beállítások vannak elmentve.\n\n' +

                             'A settings/settings fájl kitörlésével a beállítások megváltoztathatóak; ugyanakkor a fájl\n' +
                             'törlése a későbbi átláthatóság miatt nem javasolt. Ha mégis a törlés mellett döntenél,\n' +
                             'jelen .txt fájlt előtte másold le, hogy a korábbi beállításokra is emlékezhess, ha szükséges lesz.\n')

    def testProjectETZero(self):
        output_file = self.constructFilePath("testRoundTripCustomValuesET")
        exp_settings = asrt.ExperimentSettings(output_file, "", True)

        exp_settings.experiment_type = 'eye-tracking'
        exp_settings.numsessions = 2
        exp_settings.groups = []
        exp_settings.blockprepN = 2
        exp_settings.blocklengthN = 80
        exp_settings.block_in_epochN = 5
        exp_settings.epochN = 8
        exp_settings.epochs = [5, 3]
        exp_settings.asrt_types = ["noASRT", "implicit", "implicit", "implicit", "implicit", "implicit", "implicit", "implicit", "implicit"]
        exp_settings.monitor_width = 53.7
        exp_settings.computer_name = "Laposka"
        exp_settings.asrt_distance = 15.0
        exp_settings.asrt_size = 1.5
        exp_settings.asrt_rcolor = "DarkBlue"
        exp_settings.asrt_pcolor = "Green"
        exp_settings.asrt_background = "Ivory"
        exp_settings.RSI_time = 0.5
        exp_settings.AOI_size = 5.0
        exp_settings.stim_fixation_threshold = 12
        exp_settings.instruction_fixation_threshold = 36

        exp_settings.write_to_file()

        exp_settings = asrt.ExperimentSettings(output_file, "", True)
        exp_settings.read_from_file()

        self.assertEqual(exp_settings.experiment_type, "eye-tracking")
        self.assertEqual(exp_settings.groups, [])
        self.assertEqual(exp_settings.blockprepN, 2)
        self.assertEqual(exp_settings.blocklengthN, 80)
        self.assertEqual(exp_settings.block_in_epochN, 5)
        self.assertEqual(exp_settings.epochN, 8)
        self.assertEqual(exp_settings.epochs, [5, 3])
        self.assertEqual(exp_settings.asrt_types, ["noASRT", "implicit", "implicit", "implicit",
                                                   "implicit", "implicit", "implicit", "implicit", "implicit"])
        self.assertEqual(exp_settings.monitor_width, 53.7)
        self.assertEqual(exp_settings.computer_name, "Laposka")
        self.assertEqual(exp_settings.asrt_distance, 15.0)
        self.assertEqual(exp_settings.asrt_size, 1.5)
        self.assertEqual(exp_settings.asrt_rcolor, "DarkBlue")
        self.assertEqual(exp_settings.asrt_pcolor, "Green")
        self.assertEqual(exp_settings.asrt_background, "Ivory")
        self.assertEqual(exp_settings.RSI_time, 0.5)
        self.assertEqual(exp_settings.AOI_size, 5.0)
        self.assertEqual(exp_settings.stim_fixation_threshold, 12)
        self.assertEqual(exp_settings.instruction_fixation_threshold, 36)
        self.assertEqual(exp_settings.key1, None)
        self.assertEqual(exp_settings.key2, None)
        self.assertEqual(exp_settings.key3, None)
        self.assertEqual(exp_settings.key4, None)
        self.assertEqual(exp_settings.key_quit, 'q')
        self.assertEqual(exp_settings.whether_warning, None)
        self.assertEqual(exp_settings.speed_warning, None)
        self.assertEqual(exp_settings.acc_warning, None)
        self.assertEqual(exp_settings.get_maxtrial(), 3320)
        self.assertEqual(exp_settings.get_session_starts(), [1, 2071, 3321])
        self.assertEqual(exp_settings.get_block_starts(), [1, 21, 103, 185, 267, 349, 431, 513, 595, 677, 759, 841, 923, 1005, 1087, 1169,
                                                           1251, 1333, 1415, 1497, 1579, 1661, 1743, 1825, 1907, 1989, 2071,
                                                           2091, 2173, 2255, 2337, 2419, 2501, 2583, 2665, 2747, 2829, 2911,
                                                           2993, 3075, 3157, 3239, 3321, 3403])
        self.assertEqual(exp_settings.get_key_list(), ['q'])


if __name__ == "__main__":
    unittest.main()  # run all tests
