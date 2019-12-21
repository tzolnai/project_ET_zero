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
# Add the local path to the main script and external scripts so we can import them.
sys.path = [".."] + \
    [os.path.join("..", "externals", "psychopy_mock")] + sys.path

import unittest
from psychopy import monitors, visual, core, logging
import asrt
import psychopy_visual_mock as pvm
import platform
import pytest


# ignore warnings comming from psychopy
logging.console.setLevel(logging.ERROR)


def DummyFunction(*argv):
    pass


core.wait = DummyFunction


class showFeedbackTest(unittest.TestCase):

    def assertEqualWithEOL(self, string1, string2):
        if platform.system() == "Windows":
            self.assertEqual(string1, string2)
        else:
            string1 = string1.replace("\r", "")
            string2 = string2.replace("\r", "")
            self.assertEqual(string1, string2)

    def initWindow(self):
        my_monitor = monitors.Monitor('myMon')
        my_monitor.setSizePix([1366, 768])
        my_monitor.setWidth(29)
        my_monitor.saveMon()
        return visual.Window(size=[1366, 768],
                             pos=[0, 0],
                             units='cm',
                             fullscr=False,
                             allowGUI=True,
                             monitor=my_monitor,
                             color='White',
                             gammaErrorPolicy='ignore')

    def constructFilePath(self, file_name):
        filepath = os.path.abspath(__file__)
        (inst_and_feedback_path, trail) = os.path.split(filepath)
        inst_and_feedback_path = os.path.join(
            inst_and_feedback_path, "data", "instr_and_feedback", file_name)
        return inst_and_feedback_path

    def testShowImplicitFeedback(self):
        inst_and_feedback_path = self.constructFilePath("default.txt")
        experiment = asrt.Experiment("")
        experiment.instructions = asrt.InstructionHelper(
            inst_and_feedback_path)
        experiment.instructions.read_insts_from_file()

        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.experiment_type = 'reaction-time'
        experiment.settings.key1 = 'z'
        experiment.settings.key2 = 'c'
        experiment.settings.key3 = 'b'
        experiment.settings.key4 = 'm'
        experiment.settings.key_quit = 'q'
        experiment.settings.whether_warning = False
        experiment.settings.asrt_types = {1: "implicit"}

        number_of_patterns = 41
        patternERR = 1
        Npressed_in_block = 91
        accs_in_block = [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        RT_all_list = [0.65598639997188, 0.45464539993554354, 1.0849266999866813, 0.5534022999927402, 1.295695999986492, 0.5086965999798849, 0.5509545999811962, 0.49283529992680997, 1.306051000021398, 0.3599263000069186, 1.0645024999976158, 0.35126660007517785, 0.5442889999831095, 0.5597730999579653, 0.4632732999743894, 0.38760909996926785, 0.40207119996193796, 0.3861942000221461, 0.367133199935779, 0.3983248999575153, 0.3604499000357464, 0.34099430008791387, 0.35795259999576956, 0.3002517999848351, 0.40677210001740605, 0.36937460000626743, 0.5297788999741897, 0.30175390001386404, 0.3833951000124216, 0.32731279998552054, 0.32933780003804713, 0.3291419999441132, 0.35642329999245703, 0.42876619996968657, 0.07691950001753867, 0.6399777999613434, 0.6637531999731436, 0.38063269993290305, 0.3111947000725195, 0.4043739999178797, 0.3144469999242574, 0.33679540001321584, 0.34361800004262477, 0.25880250008776784, 0.5984262999845669,
                       0.36898319993633777, 0.4533040000824258, 0.5535239999881014, 0.38425100001040846, 0.31791740003973246, 0.3305279000196606, 0.32816859998274595, 0.5189762000227347, 0.3558485999237746, 0.3522320000920445, 0.36312330001965165, 0.37158000003546476, 0.2955864999676123, 0.4330413000425324, 0.3794643000001088, 0.45566460001282394, 0.3158706999383867, 0.34224989998620003, 0.3549642999423668, 0.3268801999511197, 0.36288769997190684, 0.40274560009129345, 0.2780501999659464, 0.3742851000279188, 0.3305659000761807, 0.3156298000831157, 0.36038500000722706, 0.3795830000890419, 0.6264467999571934, 0.41464949992951006, 0.41580979991704226, 0.31482500000856817, 0.38916250003967434, 0.2932135999435559, 0.4401645000325516, 0.3866993000265211, 0.5504634999670088, 0.38067620003130287, 0.33521519997157156, 0.40001529990695417, 0.3918521999148652, 0.43088040000293404, 0.3855049000121653, 0.3882131999125704, 0.3904447000240907, 0.36844549991656095]
        RT_pattern_list = [0.5509545999811962, 1.306051000021398, 0.3599263000069186, 0.5442889999831095, 0.4632732999743894, 0.40207119996193796, 0.367133199935779, 0.3604499000357464, 0.35795259999576956, 0.40677210001740605, 0.5297788999741897, 0.3833951000124216, 0.32933780003804713, 0.35642329999245703, 0.6399777999613434, 0.38063269993290305, 0.4043739999178797, 0.33679540001321584, 0.25880250008776784, 0.36898319993633777,
                           0.5535239999881014, 0.31791740003973246, 0.32816859998274595, 0.3558485999237746, 0.36312330001965165, 0.2955864999676123, 0.3794643000001088, 0.3158706999383867, 0.3549642999423668, 0.36288769997190684, 0.2780501999659464, 0.3156298000831157, 0.3795830000890419, 0.41464949992951006, 0.31482500000856817, 0.4401645000325516, 0.5504634999670088, 0.33521519997157156, 0.3918521999148652, 0.3855049000121653, 0.3904447000240907]
        N = 86
        experiment.stim_sessionN = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1, 37: 1, 38: 1, 39: 1, 40: 1, 41: 1,
                                    42: 1, 43: 1, 44: 1, 45: 1, 46: 1, 47: 1, 48: 1, 49: 1, 50: 1, 51: 1, 52: 1, 53: 1, 54: 1, 55: 1, 56: 1, 57: 1, 58: 1, 59: 1, 60: 1, 61: 1, 62: 1, 63: 1, 64: 1, 65: 1, 66: 1, 67: 1, 68: 1, 69: 1, 70: 1, 71: 1, 72: 1, 73: 1, 74: 1, 75: 1, 76: 1, 77: 1, 78: 1, 79: 1, 80: 1, 81: 1, 82: 1, 83: 1, 84: 1, 85: 1}

        visual_mock = pvm.PsychoPyVisualMock()
        with self.initWindow() as experiment.mywindow:
            return_value = experiment.show_feedback_RT(
                N, number_of_patterns, patternERR, Npressed_in_block, accs_in_block, RT_all_list, RT_pattern_list)
            self.assertEqual(return_value, "continue")

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 1)

            self.assertEqualWithEOL(drawing_list[0].text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                                          "Pontosságod: 93,40 %\r\n"
                                                          "Átlagos reakcióidőd: 0,432 másodperc\r\n\r\n\r\n")

    def testShowExplicitFeedback(self):
        inst_and_feedback_path = self.constructFilePath("default.txt")
        experiment = asrt.Experiment("")
        experiment.instructions = asrt.InstructionHelper(
            inst_and_feedback_path)
        experiment.instructions.read_insts_from_file()

        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.experiment_type = 'reaction-time'
        experiment.settings.key1 = 'z'
        experiment.settings.key2 = 'c'
        experiment.settings.key3 = 'b'
        experiment.settings.key4 = 'm'
        experiment.settings.key_quit = 'q'
        experiment.settings.whether_warning = False
        experiment.settings.asrt_types = {1: "explicit"}

        number_of_patterns = 41
        patternERR = 1
        Npressed_in_block = 91
        accs_in_block = [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        RT_all_list = [0.65598639997188, 0.45464539993554354, 1.0849266999866813, 0.5534022999927402, 1.295695999986492, 0.5086965999798849, 0.5509545999811962, 0.49283529992680997, 1.306051000021398, 0.3599263000069186, 1.0645024999976158, 0.35126660007517785, 0.5442889999831095, 0.5597730999579653, 0.4632732999743894, 0.38760909996926785, 0.40207119996193796, 0.3861942000221461, 0.367133199935779, 0.3983248999575153, 0.3604499000357464, 0.34099430008791387, 0.35795259999576956, 0.3002517999848351, 0.40677210001740605, 0.36937460000626743, 0.5297788999741897, 0.30175390001386404, 0.3833951000124216, 0.32731279998552054, 0.32933780003804713, 0.3291419999441132, 0.35642329999245703, 0.42876619996968657, 0.07691950001753867, 0.6399777999613434, 0.6637531999731436, 0.38063269993290305, 0.3111947000725195, 0.4043739999178797, 0.3144469999242574, 0.33679540001321584, 0.34361800004262477, 0.25880250008776784, 0.5984262999845669,
                       0.36898319993633777, 0.4533040000824258, 0.5535239999881014, 0.38425100001040846, 0.31791740003973246, 0.3305279000196606, 0.32816859998274595, 0.5189762000227347, 0.3558485999237746, 0.3522320000920445, 0.36312330001965165, 0.37158000003546476, 0.2955864999676123, 0.4330413000425324, 0.3794643000001088, 0.45566460001282394, 0.3158706999383867, 0.34224989998620003, 0.3549642999423668, 0.3268801999511197, 0.36288769997190684, 0.40274560009129345, 0.2780501999659464, 0.3742851000279188, 0.3305659000761807, 0.3156298000831157, 0.36038500000722706, 0.3795830000890419, 0.6264467999571934, 0.41464949992951006, 0.41580979991704226, 0.31482500000856817, 0.38916250003967434, 0.2932135999435559, 0.4401645000325516, 0.3866993000265211, 0.5504634999670088, 0.38067620003130287, 0.33521519997157156, 0.40001529990695417, 0.3918521999148652, 0.43088040000293404, 0.3855049000121653, 0.3882131999125704, 0.3904447000240907, 0.36844549991656095]
        RT_pattern_list = [0.5509545999811962, 1.306051000021398, 0.3599263000069186, 0.5442889999831095, 0.4632732999743894, 0.40207119996193796, 0.367133199935779, 0.3604499000357464, 0.35795259999576956, 0.40677210001740605, 0.5297788999741897, 0.3833951000124216, 0.32933780003804713, 0.35642329999245703, 0.6399777999613434, 0.38063269993290305, 0.4043739999178797, 0.33679540001321584, 0.25880250008776784, 0.36898319993633777,
                           0.5535239999881014, 0.31791740003973246, 0.32816859998274595, 0.3558485999237746, 0.36312330001965165, 0.2955864999676123, 0.3794643000001088, 0.3158706999383867, 0.3549642999423668, 0.36288769997190684, 0.2780501999659464, 0.3156298000831157, 0.3795830000890419, 0.41464949992951006, 0.31482500000856817, 0.4401645000325516, 0.5504634999670088, 0.33521519997157156, 0.3918521999148652, 0.3855049000121653, 0.3904447000240907]
        N = 86
        experiment.stim_sessionN = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1, 37: 1, 38: 1, 39: 1, 40: 1, 41: 1,
                                    42: 1, 43: 1, 44: 1, 45: 1, 46: 1, 47: 1, 48: 1, 49: 1, 50: 1, 51: 1, 52: 1, 53: 1, 54: 1, 55: 1, 56: 1, 57: 1, 58: 1, 59: 1, 60: 1, 61: 1, 62: 1, 63: 1, 64: 1, 65: 1, 66: 1, 67: 1, 68: 1, 69: 1, 70: 1, 71: 1, 72: 1, 73: 1, 74: 1, 75: 1, 76: 1, 77: 1, 78: 1, 79: 1, 80: 1, 81: 1, 82: 1, 83: 1, 84: 1, 85: 1}

        visual_mock = pvm.PsychoPyVisualMock()
        with self.initWindow() as experiment.mywindow:
            return_value = experiment.show_feedback_RT(
                N, number_of_patterns, patternERR, Npressed_in_block, accs_in_block, RT_all_list, RT_pattern_list)
            self.assertEqual(return_value, "continue")

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 1)

            self.assertEqualWithEOL(drawing_list[0].text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                                          "Pontosságod általában: 93,40 %\r\n"
                                                          "Átlagos reakcióidőd: 0,432 másodperc\r\n"
                                                          "Pontosságod a bejósolható elemeknél: 97,56 %\r\n"
                                                          "Átlagos reakcióidőd a bejósolható elemeknél: 0,412 másodperc\r\n\r\n\r\n")

    def testShowExplicitFeedbackQuit(self):
        inst_and_feedback_path = self.constructFilePath("default.txt")
        experiment = asrt.Experiment("")
        experiment.instructions = asrt.InstructionHelper(
            inst_and_feedback_path)
        experiment.instructions.read_insts_from_file()

        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.experiment_type = 'reaction-time'
        experiment.settings.key1 = 'z'
        experiment.settings.key2 = 'c'
        experiment.settings.key3 = 'b'
        experiment.settings.key4 = 'm'
        experiment.settings.key_quit = 'q'
        experiment.settings.whether_warning = False
        experiment.settings.asrt_types = {1: "explicit"}

        number_of_patterns = 41
        patternERR = 1
        Npressed_in_block = 91
        accs_in_block = [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        RT_all_list = [0.65598639997188, 0.45464539993554354, 1.0849266999866813, 0.5534022999927402, 1.295695999986492, 0.5086965999798849, 0.5509545999811962, 0.49283529992680997, 1.306051000021398, 0.3599263000069186, 1.0645024999976158, 0.35126660007517785, 0.5442889999831095, 0.5597730999579653, 0.4632732999743894, 0.38760909996926785, 0.40207119996193796, 0.3861942000221461, 0.367133199935779, 0.3983248999575153, 0.3604499000357464, 0.34099430008791387, 0.35795259999576956, 0.3002517999848351, 0.40677210001740605, 0.36937460000626743, 0.5297788999741897, 0.30175390001386404, 0.3833951000124216, 0.32731279998552054, 0.32933780003804713, 0.3291419999441132, 0.35642329999245703, 0.42876619996968657, 0.07691950001753867, 0.6399777999613434, 0.6637531999731436, 0.38063269993290305, 0.3111947000725195, 0.4043739999178797, 0.3144469999242574, 0.33679540001321584, 0.34361800004262477, 0.25880250008776784, 0.5984262999845669,
                       0.36898319993633777, 0.4533040000824258, 0.5535239999881014, 0.38425100001040846, 0.31791740003973246, 0.3305279000196606, 0.32816859998274595, 0.5189762000227347, 0.3558485999237746, 0.3522320000920445, 0.36312330001965165, 0.37158000003546476, 0.2955864999676123, 0.4330413000425324, 0.3794643000001088, 0.45566460001282394, 0.3158706999383867, 0.34224989998620003, 0.3549642999423668, 0.3268801999511197, 0.36288769997190684, 0.40274560009129345, 0.2780501999659464, 0.3742851000279188, 0.3305659000761807, 0.3156298000831157, 0.36038500000722706, 0.3795830000890419, 0.6264467999571934, 0.41464949992951006, 0.41580979991704226, 0.31482500000856817, 0.38916250003967434, 0.2932135999435559, 0.4401645000325516, 0.3866993000265211, 0.5504634999670088, 0.38067620003130287, 0.33521519997157156, 0.40001529990695417, 0.3918521999148652, 0.43088040000293404, 0.3855049000121653, 0.3882131999125704, 0.3904447000240907, 0.36844549991656095]
        RT_pattern_list = [0.5509545999811962, 1.306051000021398, 0.3599263000069186, 0.5442889999831095, 0.4632732999743894, 0.40207119996193796, 0.367133199935779, 0.3604499000357464, 0.35795259999576956, 0.40677210001740605, 0.5297788999741897, 0.3833951000124216, 0.32933780003804713, 0.35642329999245703, 0.6399777999613434, 0.38063269993290305, 0.4043739999178797, 0.33679540001321584, 0.25880250008776784, 0.36898319993633777,
                           0.5535239999881014, 0.31791740003973246, 0.32816859998274595, 0.3558485999237746, 0.36312330001965165, 0.2955864999676123, 0.3794643000001088, 0.3158706999383867, 0.3549642999423668, 0.36288769997190684, 0.2780501999659464, 0.3156298000831157, 0.3795830000890419, 0.41464949992951006, 0.31482500000856817, 0.4401645000325516, 0.5504634999670088, 0.33521519997157156, 0.3918521999148652, 0.3855049000121653, 0.3904447000240907]
        N = 86
        experiment.stim_sessionN = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1, 37: 1, 38: 1, 39: 1, 40: 1, 41: 1,
                                    42: 1, 43: 1, 44: 1, 45: 1, 46: 1, 47: 1, 48: 1, 49: 1, 50: 1, 51: 1, 52: 1, 53: 1, 54: 1, 55: 1, 56: 1, 57: 1, 58: 1, 59: 1, 60: 1, 61: 1, 62: 1, 63: 1, 64: 1, 65: 1, 66: 1, 67: 1, 68: 1, 69: 1, 70: 1, 71: 1, 72: 1, 73: 1, 74: 1, 75: 1, 76: 1, 77: 1, 78: 1, 79: 1, 80: 1, 81: 1, 82: 1, 83: 1, 84: 1, 85: 1}

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['q'])
        with self.initWindow() as experiment.mywindow:
            return_value = experiment.show_feedback_RT(
                N, number_of_patterns, patternERR, Npressed_in_block, accs_in_block, RT_all_list, RT_pattern_list)
            self.assertEqual(return_value, "quit")

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 1)

            self.assertEqualWithEOL(drawing_list[0].text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                                          "Pontosságod általában: 93,40 %\r\n"
                                                          "Átlagos reakcióidőd: 0,432 másodperc\r\n"
                                                          "Pontosságod a bejósolható elemeknél: 97,56 %\r\n"
                                                          "Átlagos reakcióidőd a bejósolható elemeknél: 0,412 másodperc\r\n\r\n\r\n")

    def testShowImplicitFeedbackWithNoASRT(self):
        inst_and_feedback_path = self.constructFilePath("default.txt")
        experiment = asrt.Experiment("")
        experiment.instructions = asrt.InstructionHelper(
            inst_and_feedback_path)
        experiment.instructions.read_insts_from_file()

        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.experiment_type = 'reaction-time'
        experiment.settings.key1 = 'z'
        experiment.settings.key2 = 'c'
        experiment.settings.key3 = 'b'
        experiment.settings.key4 = 'm'
        experiment.settings.key_quit = 'q'
        experiment.settings.whether_warning = False
        experiment.settings.asrt_types = {1: "noASRT"}

        number_of_patterns = 0
        patternERR = 0
        Npressed_in_block = 93
        accs_in_block = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        RT_all_list = [0.653660700074397, 0.7518959000008181, 0.13708830007817596, 0.3583502999972552, 0.39244239998515695, 0.3285357999848202, 0.40331540000624955, 0.3710296000353992, 0.341499499976635, 0.3568639999721199, 0.39840099995490164, 0.37202410004101694, 0.2702612999128178, 0.36594070005230606, 0.35062369995284826, 0.3946021000156179, 0.36215729999821633, 0.19734549999702722, 0.3566472999518737, 0.32603909994941205, 0.3238172000274062, 0.3006464000791311, 0.3807443000841886, 0.36516439996194094, 0.39862300001550466, 0.34062530007213354, 0.3909466000040993, 0.30183319991920143, 0.3250305000692606, 0.30275529995560646, 0.40316700004041195, 0.35280160000547767, 0.36223800003062934, 0.284529099939391, 0.29197169991675764, 0.38026559993159026, 0.20330660010222346, 0.2905216000508517, 0.42550909996498376, 0.2681467999937013, 0.358382000005804, 0.33629499992821366, 0.36083929997403175, 0.4591319999890402, 0.31307130004279315, 0.4129635998979211,
                       0.28134079999290407, 0.3975394999142736, 0.31700709997676313, 0.3627492000814527, 0.33818139997310936, 0.36467939999420196, 0.2352334000170231, 0.39265579998027533, 0.37120350007899106, 0.3655175999738276, 0.1576888000126928, 0.33888000005390495, 0.38786780007649213, 0.3193819000152871, 0.4400262999115512, 0.3161339000798762, 0.3188491000328213, 0.39650749997235835, 0.3570177999790758, 0.41444580000825226, 0.3331520000938326, 0.35156940005254, 0.35767449997365475, 0.3675121999112889, 0.40079760004300624, 0.3473584000021219, 0.3274419999215752, 0.32332600001245737, 0.40468409995082766, 0.3221442000940442, 0.3548591999569908, 0.2841093000024557, 0.344599699950777, 0.386243800050579, 0.3169913999736309, 0.34209890000056475, 0.3442977999802679, 0.34884620003867894, 0.31073750008363277, 0.31089399999473244, 0.13577060005627573, 0.36871519999112934, 0.39353580004535615, 0.2609264000784606, 0.2700346000492573, 0.20035449997521937, 0.3049739000853151]
        RT_pattern_list = []
        N = 86
        experiment.stim_sessionN = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1, 37: 1, 38: 1, 39: 1, 40: 1, 41: 1,
                                    42: 1, 43: 1, 44: 1, 45: 1, 46: 1, 47: 1, 48: 1, 49: 1, 50: 1, 51: 1, 52: 1, 53: 1, 54: 1, 55: 1, 56: 1, 57: 1, 58: 1, 59: 1, 60: 1, 61: 1, 62: 1, 63: 1, 64: 1, 65: 1, 66: 1, 67: 1, 68: 1, 69: 1, 70: 1, 71: 1, 72: 1, 73: 1, 74: 1, 75: 1, 76: 1, 77: 1, 78: 1, 79: 1, 80: 1, 81: 1, 82: 1, 83: 1, 84: 1, 85: 1}

        visual_mock = pvm.PsychoPyVisualMock()
        with self.initWindow() as experiment.mywindow:
            return_value = experiment.show_feedback_RT(
                N, number_of_patterns, patternERR, Npressed_in_block, accs_in_block, RT_all_list, RT_pattern_list)
            self.assertEqual(return_value, "continue")

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 1)

            self.assertEqualWithEOL(drawing_list[0].text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                                          "Pontosságod: 91,39 %\r\n"
                                                          "Átlagos reakcióidőd: 0,345 másodperc\r\n\r\n\r\n")

    def testShowExplicitFeedbackPracticeOnly(self):
        inst_and_feedback_path = self.constructFilePath("default.txt")
        experiment = asrt.Experiment("")
        experiment.instructions = asrt.InstructionHelper(
            inst_and_feedback_path)
        experiment.instructions.read_insts_from_file()

        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.experiment_type = 'reaction-time'
        experiment.settings.key1 = 'z'
        experiment.settings.key2 = 'c'
        experiment.settings.key3 = 'b'
        experiment.settings.key4 = 'm'
        experiment.settings.key_quit = 'q'
        experiment.settings.whether_warning = False
        experiment.settings.asrt_types = {1: "explicit"}

        number_of_patterns = 0
        patternERR = 0
        Npressed_in_block = 22
        accs_in_block = [0, 0, 0, 0, 0, 1, 0, 1, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        RT_all_list = [0.5794496000744402, 0.35619379999116063, 0.3814645999809727, 0.4804278000956401, 0.5123080000048503, 0.2316811999771744, 0.26849129993934184, 0.5066433999454603, 0.13152870000340044, 0.4178971000947058, 0.32583909993991256,
                       0.3743417999939993, 0.31053929997142404, 0.3420154999475926, 0.37570670002605766, 0.48097060003783554, 0.3754441000055522, 0.2967826999956742, 0.42367529997136444, 0.3725358999799937, 0.3507367999991402, 0.35236550006084144]
        RT_pattern_list = []
        N = 21
        experiment.stim_sessionN = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1,
                                    10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1}

        visual_mock = pvm.PsychoPyVisualMock()
        with self.initWindow() as experiment.mywindow:
            return_value = experiment.show_feedback_RT(
                N, number_of_patterns, patternERR, Npressed_in_block, accs_in_block, RT_all_list, RT_pattern_list)
            self.assertEqual(return_value, "continue")

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 1)

            self.assertEqualWithEOL(drawing_list[0].text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                                          "Pontosságod általában: 90,90 %\r\n"
                                                          "Átlagos reakcióidőd: 0,374 másodperc\r\n"
                                                          "Pontosságod a bejósolható elemeknél: N/A %\r\n"
                                                          "Átlagos reakcióidőd a bejósolható elemeknél: N/A másodperc\r\n\r\n\r\n")

    @pytest.mark.skipif(not asrt.g_tobii_available, reason="Can't run without tobii package")
    def testShowETFeedback(self):
        inst_and_feedback_path = self.constructFilePath("default.txt")
        experiment = asrt.Experiment("")
        experiment.instructions = asrt.InstructionHelper(inst_and_feedback_path)
        experiment.instructions.read_insts_from_file()

        with self.initWindow() as experiment.mywindow:
            experiment.settings = asrt.ExperimentSettings("", "")
            experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "eye-tracking")
            experiment.settings.experiment_type = 'eye-tracking'
            experiment.stimblock = {4: 10}
            experiment.last_N = 4
            experiment.last_block_RTs = ["0,512", "0,443", "0,335", "0,601", "0,213", "0,934", "0,912", "0,120"]
            experiment.fixation_cross_pos = (0.0, 0.0)
            experiment.fixation_cross = visual.TextStim(win=experiment.mywindow, text="+", height=3, units="cm",
                                                        color='black', pos=experiment.fixation_cross_pos)
            experiment.settings.instruction_sampling_window = 36
            experiment.current_sampling_window = 36
            experiment.settings.AOI_size = 1.0
            experiment.settings.monitor_width = 47.6
            experiment.monitor_settings()
            for i in range(0, experiment.settings.instruction_sampling_window):
                gazeData = {}
                gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
                gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
                gazeData['left_gaze_point_validity'] = True
                gazeData['right_gaze_point_validity'] = True
                gazeData['left_pupil_diameter'] = 3
                gazeData['right_pupil_diameter'] = 3
                gazeData['left_pupil_validity'] = True
                gazeData['right_pupil_validity'] = True
                experiment.eye_data_callback(gazeData)

            visual_mock = pvm.PsychoPyVisualMock()
            RT_all_list = [0.65598639997188, 0.45464539993554354, 1.0849266999866813, 0.5534022999927402, 1.295695999986492, 0.5086965999798849, 0.5509545999811962, 0.49283529992680997, 1.306051000021398, 0.3599263000069186, 1.0645024999976158, 0.35126660007517785, 0.5442889999831095, 0.5597730999579653, 0.4632732999743894, 0.38760909996926785, 0.40207119996193796, 0.3861942000221461, 0.367133199935779, 0.3983248999575153, 0.3604499000357464, 0.34099430008791387, 0.35795259999576956, 0.3002517999848351, 0.40677210001740605, 0.36937460000626743, 0.5297788999741897, 0.30175390001386404, 0.3833951000124216, 0.32731279998552054, 0.32933780003804713, 0.3291419999441132, 0.35642329999245703, 0.42876619996968657, 0.07691950001753867, 0.6399777999613434, 0.6637531999731436, 0.38063269993290305, 0.3111947000725195, 0.4043739999178797, 0.3144469999242574, 0.33679540001321584, 0.34361800004262477, 0.25880250008776784, 0.5984262999845669,
                           0.36898319993633777, 0.4533040000824258, 0.5535239999881014, 0.38425100001040846, 0.31791740003973246, 0.3305279000196606, 0.32816859998274595, 0.5189762000227347, 0.3558485999237746, 0.3522320000920445, 0.36312330001965165, 0.37158000003546476, 0.2955864999676123, 0.4330413000425324, 0.3794643000001088, 0.45566460001282394, 0.3158706999383867, 0.34224989998620003, 0.3549642999423668, 0.3268801999511197, 0.36288769997190684, 0.40274560009129345, 0.2780501999659464, 0.3742851000279188, 0.3305659000761807, 0.3156298000831157, 0.36038500000722706, 0.3795830000890419, 0.6264467999571934, 0.41464949992951006, 0.41580979991704226, 0.31482500000856817, 0.38916250003967434, 0.2932135999435559, 0.4401645000325516, 0.3866993000265211, 0.5504634999670088, 0.38067620003130287, 0.33521519997157156, 0.40001529990695417, 0.3918521999148652, 0.43088040000293404, 0.3855049000121653, 0.3882131999125704, 0.3904447000240907, 0.36844549991656095]
            return_value = experiment.show_feedback_ET(RT_all_list, False)
            self.assertEqual(return_value, "continue")

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 3)

            self.assertEqualWithEOL(drawing_list[0].text, "Most pihenhetsz egy kicsit.\n\n"
                                                          "Az előző blokkokban mért átlagos reakcióidők:\n\n"
                                                          "6. blokk: 0,213 másodperc.\n\n"
                                                          "7. blokk: 0,934 másodperc.\n\n"
                                                          "8. blokk: 0,912 másodperc.\n\n"
                                                          "9. blokk: 0,120 másodperc.\n\n"
                                                          "10. blokk: 0,432 másodperc.\n\n")
            self.assertEqualWithEOL(drawing_list[1].text, "+")
            self.assertEqualWithEOL(drawing_list[2].text, "A következő blokkra lépéshez néz a keresztre!")

    @pytest.mark.skipif(not asrt.g_tobii_available, reason="Can't run without tobii package")
    def testShowETFeedbackQuit(self):
        inst_and_feedback_path = self.constructFilePath("default.txt")
        experiment = asrt.Experiment("")
        experiment.instructions = asrt.InstructionHelper(inst_and_feedback_path)
        experiment.instructions.read_insts_from_file()

        with self.initWindow() as experiment.mywindow:
            experiment.settings = asrt.ExperimentSettings("", "")
            experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "eye-tracking")
            experiment.settings.experiment_type = 'eye-tracking'
            experiment.stimblock = {4: 10}
            experiment.last_N = 4
            experiment.last_block_RTs = ["0,512", "0,443", "0,335", "0,601", "0,213", "0,934", "0,912", "0,120"]
            experiment.fixation_cross_pos = (0.0, 0.0)
            experiment.fixation_cross = visual.TextStim(win=experiment.mywindow, text="+", height=3, units="cm",
                                                        color='black', pos=experiment.fixation_cross_pos)
            experiment.settings.instruction_sampling_window = 36
            experiment.current_sampling_window = 36
            experiment.settings.AOI_size = 1.0
            experiment.settings.monitor_width = 47.6

            visual_mock = pvm.PsychoPyVisualMock()
            visual_mock.setReturnKeyList(['q'])
            RT_all_list = [0.65598639997188, 0.45464539993554354, 1.0849266999866813, 0.5534022999927402, 1.295695999986492, 0.5086965999798849, 0.5509545999811962, 0.49283529992680997, 1.306051000021398, 0.3599263000069186, 1.0645024999976158, 0.35126660007517785, 0.5442889999831095, 0.5597730999579653, 0.4632732999743894, 0.38760909996926785, 0.40207119996193796, 0.3861942000221461, 0.367133199935779, 0.3983248999575153, 0.3604499000357464, 0.34099430008791387, 0.35795259999576956, 0.3002517999848351, 0.40677210001740605, 0.36937460000626743, 0.5297788999741897, 0.30175390001386404, 0.3833951000124216, 0.32731279998552054, 0.32933780003804713, 0.3291419999441132, 0.35642329999245703, 0.42876619996968657, 0.07691950001753867, 0.6399777999613434, 0.6637531999731436, 0.38063269993290305, 0.3111947000725195, 0.4043739999178797, 0.3144469999242574, 0.33679540001321584, 0.34361800004262477, 0.25880250008776784, 0.5984262999845669,
                           0.36898319993633777, 0.4533040000824258, 0.5535239999881014, 0.38425100001040846, 0.31791740003973246, 0.3305279000196606, 0.32816859998274595, 0.5189762000227347, 0.3558485999237746, 0.3522320000920445, 0.36312330001965165, 0.37158000003546476, 0.2955864999676123, 0.4330413000425324, 0.3794643000001088, 0.45566460001282394, 0.3158706999383867, 0.34224989998620003, 0.3549642999423668, 0.3268801999511197, 0.36288769997190684, 0.40274560009129345, 0.2780501999659464, 0.3742851000279188, 0.3305659000761807, 0.3156298000831157, 0.36038500000722706, 0.3795830000890419, 0.6264467999571934, 0.41464949992951006, 0.41580979991704226, 0.31482500000856817, 0.38916250003967434, 0.2932135999435559, 0.4401645000325516, 0.3866993000265211, 0.5504634999670088, 0.38067620003130287, 0.33521519997157156, 0.40001529990695417, 0.3918521999148652, 0.43088040000293404, 0.3855049000121653, 0.3882131999125704, 0.3904447000240907, 0.36844549991656095]
            return_value = experiment.show_feedback_ET(RT_all_list, False)
            self.assertEqual(return_value, "quit")

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 3)

            self.assertEqualWithEOL(drawing_list[0].text, "Most pihenhetsz egy kicsit.\n\n"
                                                          "Az előző blokkokban mért átlagos reakcióidők:\n\n"
                                                          "6. blokk: 0,213 másodperc.\n\n"
                                                          "7. blokk: 0,934 másodperc.\n\n"
                                                          "8. blokk: 0,912 másodperc.\n\n"
                                                          "9. blokk: 0,120 másodperc.\n\n"
                                                          "10. blokk: 0,432 másodperc.\n\n")
            self.assertEqualWithEOL(drawing_list[1].text, "+")
            self.assertEqualWithEOL(drawing_list[2].text, "A következő blokkra lépéshez néz a keresztre!")

    @pytest.mark.skipif(not asrt.g_tobii_available, reason="Can't run without tobii package")
    def testShowETFeedbackLastBlock(self):
        inst_and_feedback_path = self.constructFilePath("default.txt")
        experiment = asrt.Experiment("")
        experiment.instructions = asrt.InstructionHelper(inst_and_feedback_path)
        experiment.instructions.read_insts_from_file()

        with self.initWindow() as experiment.mywindow:
            experiment.settings = asrt.ExperimentSettings("", "")
            experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "eye-tracking")
            experiment.settings.experiment_type = 'eye-tracking'
            experiment.stimblock = {4: 10}
            experiment.last_N = 4
            experiment.last_block_RTs = ["0,512", "0,443", "0,335", "0,601", "0,213", "0,934", "0,912", "0,120"]
            experiment.fixation_cross_pos = (0.0, 0.0)
            experiment.fixation_cross = visual.TextStim(win=experiment.mywindow, text="+", height=3, units="cm",
                                                        color='black', pos=experiment.fixation_cross_pos)
            experiment.settings.instruction_sampling_window = 36
            experiment.current_sampling_window = 36
            experiment.settings.AOI_size = 1.0
            experiment.settings.monitor_width = 47.6
            experiment.monitor_settings()
            for i in range(0, experiment.settings.instruction_sampling_window):
                gazeData = {}
                gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
                gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
                gazeData['left_gaze_point_validity'] = True
                gazeData['right_gaze_point_validity'] = True
                gazeData['left_pupil_diameter'] = 3
                gazeData['right_pupil_diameter'] = 3
                gazeData['left_pupil_validity'] = True
                gazeData['right_pupil_validity'] = True
                experiment.eye_data_callback(gazeData)

            visual_mock = pvm.PsychoPyVisualMock()
            RT_all_list = [0.65598639997188, 0.45464539993554354, 1.0849266999866813, 0.5534022999927402, 1.295695999986492, 0.5086965999798849, 0.5509545999811962, 0.49283529992680997, 1.306051000021398, 0.3599263000069186, 1.0645024999976158, 0.35126660007517785, 0.5442889999831095, 0.5597730999579653, 0.4632732999743894, 0.38760909996926785, 0.40207119996193796, 0.3861942000221461, 0.367133199935779, 0.3983248999575153, 0.3604499000357464, 0.34099430008791387, 0.35795259999576956, 0.3002517999848351, 0.40677210001740605, 0.36937460000626743, 0.5297788999741897, 0.30175390001386404, 0.3833951000124216, 0.32731279998552054, 0.32933780003804713, 0.3291419999441132, 0.35642329999245703, 0.42876619996968657, 0.07691950001753867, 0.6399777999613434, 0.6637531999731436, 0.38063269993290305, 0.3111947000725195, 0.4043739999178797, 0.3144469999242574, 0.33679540001321584, 0.34361800004262477, 0.25880250008776784, 0.5984262999845669,
                           0.36898319993633777, 0.4533040000824258, 0.5535239999881014, 0.38425100001040846, 0.31791740003973246, 0.3305279000196606, 0.32816859998274595, 0.5189762000227347, 0.3558485999237746, 0.3522320000920445, 0.36312330001965165, 0.37158000003546476, 0.2955864999676123, 0.4330413000425324, 0.3794643000001088, 0.45566460001282394, 0.3158706999383867, 0.34224989998620003, 0.3549642999423668, 0.3268801999511197, 0.36288769997190684, 0.40274560009129345, 0.2780501999659464, 0.3742851000279188, 0.3305659000761807, 0.3156298000831157, 0.36038500000722706, 0.3795830000890419, 0.6264467999571934, 0.41464949992951006, 0.41580979991704226, 0.31482500000856817, 0.38916250003967434, 0.2932135999435559, 0.4401645000325516, 0.3866993000265211, 0.5504634999670088, 0.38067620003130287, 0.33521519997157156, 0.40001529990695417, 0.3918521999148652, 0.43088040000293404, 0.3855049000121653, 0.3882131999125704, 0.3904447000240907, 0.36844549991656095]
            return_value = experiment.show_feedback_ET(RT_all_list, True)
            self.assertEqual(return_value, "continue")

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 1)

            self.assertEqualWithEOL(drawing_list[0].text, "Most pihenhetsz egy kicsit.\n\n"
                                                          "Az előző blokkokban mért átlagos reakcióidők:\n\n"
                                                          "6. blokk: 0,213 másodperc.\n\n"
                                                          "7. blokk: 0,934 másodperc.\n\n"
                                                          "8. blokk: 0,912 másodperc.\n\n"
                                                          "9. blokk: 0,120 másodperc.\n\n"
                                                          "10. blokk: 0,432 másodperc.\n\n")


if __name__ == "__main__":
    unittest.main()  # run all tests
