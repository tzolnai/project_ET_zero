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
import psychopy_visual_mock as pvm
import psychopy_gui_mock as pgm
from psychopy import visual, logging
import platform


# ignore warnings comming from psychopy
logging.console.setLevel(logging.ERROR)

dict_accents = {u'á': u'a', u'é': u'e', u'í': u'i', u'ó': u'o',
                u'ő': u'o', u'ö': u'o', u'ú': u'u', u'ű': u'u', u'ü': u'u'}


class presentationTest(unittest.TestCase):

    def setUp(self):
        # Init work directory
        filepath = os.path.abspath(__file__)
        (filepath, trail) = os.path.split(filepath)
        test_name = self.id().split(".")[2]
        self.current_dir = os.path.join(
            filepath, "data", "presentation", test_name)
        self.work_dir = os.path.join(self.current_dir, "workdir")
        asrt.ensure_dir(self.work_dir)
        self.clearDir(self.work_dir)
        self.copyFilesToWorkdir()

    def tearDown(self):
        self.clearDir(self.work_dir)

    def assertEqualWithEOL(self, string1, string2):
        string1 = string1.replace("\r", "")
        string2 = string2.replace("\r", "")
        self.assertEqual(string1, string2)

    def copyFilesToWorkdir(self):
        this_path = self.current_dir

        for file in os.listdir(self.current_dir):
            file_path = os.path.join(self.current_dir, file)
            if os.path.isfile(file_path):
                shutil.copyfile(file_path, os.path.join(self.work_dir, file))

    def clearDir(self, dir_path):
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def constructFilePath(self, file_name):
        filepath = os.path.abspath(__file__)
        (filepath, trail) = os.path.split(filepath)
        filepath = os.path.join(
            filepath, "data", "presentation", file_name, "workdir")
        return filepath

    def testSimpleTestCase(self):
        visual_mock = pvm.PsychoPyVisualMock()
        thispath = os.path.join(self.constructFilePath("testSimpleTestCase"))
        experiment = asrt.Experiment(thispath)
        # load settings
        settings_path = os.path.join(
            self.constructFilePath("testSimpleTestCase"), "settings")
        experiment.settings = asrt.ExperimentSettings(settings_path, "")
        experiment.all_settings_def()

        # load instructions
        inst_feedback_path = os.path.join(self.constructFilePath(
            "testSimpleTestCase"), "inst_and_feedback.txt")
        experiment.instructions = asrt.InstructionHelper(inst_feedback_path)
        experiment.instructions.read_insts_from_file()

        # set user settings
        asrt.ensure_dir(os.path.join(thispath, "settings"))
        asrt.ensure_dir(os.path.join(thispath, "subject_settings"))
        asrt.ensure_dir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "subject_settings"))
        self.clearDir(os.path.join(thispath, "logs"))

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])
        experiment.participant_id()

        # monitor settings
        experiment.monitor_settings()
        experiment.colors = {'wincolor': experiment.settings.asrt_background, 'linecolor': 'black',
                             'stimp': experiment.settings.asrt_pcolor, 'stimr': experiment.settings.asrt_rcolor}

        with visual.Window(size=experiment.mymonitor.getSizePix(), color=experiment.colors['wincolor'], fullscr=False,
                           monitor=experiment.mymonitor, units="cm", gammaErrorPolicy='ignore') as experiment.mywindow:

            experiment.pressed_dict = {experiment.settings.key1: 1, experiment.settings.key2: 2,
                                       experiment.settings.key3: 3, experiment.settings.key4: 4}

            # use dummy values
            experiment.frame_time, experiment.frame_sd, experiment.frame_rate = 1.0, 0.12, 0.23

            experiment.dict_pos = {1: (float(experiment.settings.asrt_distance) * (-1.5), 0),
                                   2: (float(experiment.settings.asrt_distance) * (-0.5), 0),
                                   3: (float(experiment.settings.asrt_distance) * 0.5, 0),
                                   4: (float(experiment.settings.asrt_distance) * 1.5, 0)}

            visual_mock = pvm.PsychoPyVisualMock()

            # generate the right keys
            key_list = []
            # There are some instructions first
            key_list = [experiment.settings.key1,
                        experiment.settings.key1, experiment.settings.key1]

            # Then we have the stimuli
            for stim in experiment.stimlist.values():
                if stim == 1:
                    key_list.append(experiment.settings.key1)
                elif stim == 2:
                    key_list.append(experiment.settings.key2)
                elif stim == 3:
                    key_list.append(experiment.settings.key3)
                elif stim == 4:
                    key_list.append(experiment.settings.key4)

            visual_mock.setReturnKeyList(key_list)
            experiment.presentation()

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 104)

            # first we have some instructions
            instruction_text = drawing_list[0]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nÜdvözlünk a feladatban!\r\n\r\n"
                                    "A képernyőn négy kör lesz, a kör egyika a többitől különböző színnel fog megjelenni.\r\n\r\n"
                                    "Az a feladatod, hogy az eltérő színű kör megjelenési helyének megfelelő gombot nyomd meg.\r\n\r\n"
                                    "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[1]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nA következő billenytűket kell használni: z, c, b, m\r\n\r\n"
                                                           "Minél pontosabban és gyorsabban kövesd le a megjelenő ingereket!\r\n\r\n"
                                                           "Ehhez mindkét kezedet használd, a középső és mutatóujjaidat.\r\n\r\n"
                                                           "Az eltérő színű kör egymás után többször ugyanazon a helyen is megjelenhet.\r\n\r\n"
                                                           "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[2]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nKb. percenként fogsz visszajelzést kapni arról,\r\n"
                                                           "hogy mennyire voltál gyors és pontos - ez alapján tudsz módosítani.\r\n\r\n"
                                                           "A feladat indításához nyomd meg valamelyik válaszgombot!\r\n\r\n")

            # then we have 11 trials
            for j in range(3, 102, 9):
                # empty cycles
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + i]
                    self.assertTrue(isinstance(
                        stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # empty cycles again
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + 4 + i]
                    self.assertTrue(isinstance(
                        stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # stimulus
                stim_circle = drawing_list[j + 8]
                self.assertTrue(isinstance(stim_circle, pvm.Circle))
                self.assertEqual(stim_circle.lineColor, 'black')
                self.assertEqual(stim_circle.fillColor,
                                 experiment.settings.asrt_rcolor)

            # saving screen
            saving = drawing_list[102]
            self.assertTrue(isinstance(saving, pvm.TextStim))
            self.assertEqual(
                saving.text, "Adatok mentése és visszajelzés előkészítése...")

            # feedback screen
            feedback = drawing_list[103]
            self.assertTrue(isinstance(feedback, pvm.TextStim))
            self.assertEqualWithEOL(feedback.text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                                   "Pontosságod: 100,0 %\r\n"
                                                   "Átlagos reakcióidőd: 0,0 másodperc\r\n\r\n"
                                                   "Legyél gyorsabb!\r\n\r\n\r\n\r\n")

            self.assertTrue(os.path.join(
                thispath, "subject_settings", "toth-bela_10__log.txt"))

        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "subject_settings"))
        self.clearDir(os.path.join(thispath, "logs"))

    def testExplixitASRT(self):
        visual_mock = pvm.PsychoPyVisualMock()
        thispath = os.path.join(self.constructFilePath("testExplixitASRT"))
        experiment = asrt.Experiment(thispath)
        # load settings
        settings_path = os.path.join(
            self.constructFilePath("testExplixitASRT"), "settings")
        experiment.settings = asrt.ExperimentSettings(settings_path, "")
        experiment.all_settings_def()

        # load instructions
        inst_feedback_path = os.path.join(self.constructFilePath(
            "testExplixitASRT"), "inst_and_feedback.txt")
        experiment.instructions = asrt.InstructionHelper(inst_feedback_path)
        experiment.instructions.read_insts_from_file()

        # set user settings
        asrt.ensure_dir(os.path.join(thispath, "settings"))
        asrt.ensure_dir(os.path.join(thispath, "subject_settings"))
        asrt.ensure_dir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "subject_settings"))
        self.clearDir(os.path.join(thispath, "logs"))

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])
        experiment.participant_id()

        # monitor settings
        experiment.monitor_settings()
        experiment.colors = {'wincolor': experiment.settings.asrt_background, 'linecolor': 'black',
                             'stimp': experiment.settings.asrt_pcolor, 'stimr': experiment.settings.asrt_rcolor}

        with visual.Window(size=experiment.mymonitor.getSizePix(), color=experiment.colors['wincolor'], fullscr=False,
                           monitor=experiment.mymonitor, units="cm", gammaErrorPolicy='ignore') as experiment.mywindow:

            experiment.pressed_dict = {experiment.settings.key1: 1, experiment.settings.key2: 2,
                                       experiment.settings.key3: 3, experiment.settings.key4: 4}

            # use dummy values
            experiment.frame_time, experiment.frame_sd, experiment.frame_rate = 1.0, 0.12, 0.23

            experiment.dict_pos = {1: (float(experiment.settings.asrt_distance) * (-1.5), 0),
                                   2: (float(experiment.settings.asrt_distance) * (-0.5), 0),
                                   3: (float(experiment.settings.asrt_distance) * 0.5, 0),
                                   4: (float(experiment.settings.asrt_distance) * 1.5, 0)}

            visual_mock = pvm.PsychoPyVisualMock()

            # generate the right keys
            key_list = []
            # There are some instructions first
            key_list = [experiment.settings.key1,
                        experiment.settings.key1, experiment.settings.key1]

            # Then we have the stimuli
            for stim in experiment.stimlist.values():
                if stim == 1:
                    key_list.append(experiment.settings.key1)
                elif stim == 2:
                    key_list.append(experiment.settings.key2)
                elif stim == 3:
                    key_list.append(experiment.settings.key3)
                elif stim == 4:
                    key_list.append(experiment.settings.key4)

            visual_mock.setReturnKeyList(key_list)
            experiment.presentation()

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 104)

            # first we have some instructions
            instruction_text = drawing_list[0]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nÜdvözlünk a feladatban!\r\n\r\n"
                                    "A képernyőn négy kör lesz, a kör egyika a többitől különböző színnel fog megjelenni.\r\n\r\n"
                                    "Az a feladatod, hogy az eltérő színű kör megjelenési helyének megfelelő gombot nyomd meg.\r\n\r\n"
                                    "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[1]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nA következő billenytűket kell használni: z, c, b, m\r\n\r\n"
                                                           "Minél pontosabban és gyorsabban kövesd le a megjelenő ingereket!\r\n\r\n"
                                                           "Ehhez mindkét kezedet használd, a középső és mutatóujjaidat.\r\n\r\n"
                                                           "Az eltérő színű kör egymás után többször ugyanazon a helyen is megjelenhet.\r\n\r\n"
                                                           "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[2]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nKb. percenként fogsz visszajelzést kapni arról,\r\n"
                                                           "hogy mennyire voltál gyors és pontos - ez alapján tudsz módosítani.\r\n\r\n"
                                                           "A feladat indításához nyomd meg valamelyik válaszgombot!\r\n\r\n")

            # then we have 11 trials
            for j in range(3, 102, 9):
                # empty cycles
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + i]
                    self.assertTrue(isinstance(
                        stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # empty cycles again
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + 4 + i]
                    self.assertTrue(isinstance(
                        stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # stimulus
                stim_circle = drawing_list[j + 8]
                self.assertTrue(isinstance(stim_circle, pvm.Circle))
                self.assertEqual(stim_circle.lineColor, 'black')
                if experiment.stimpr[((j - 3) / 9) + 1] == 'pattern':
                    self.assertEqual(stim_circle.fillColor,
                                     experiment.settings.asrt_pcolor)
                else:
                    self.assertEqual(stim_circle.fillColor,
                                     experiment.settings.asrt_rcolor)

            # saving screen
            saving = drawing_list[102]
            self.assertTrue(isinstance(saving, pvm.TextStim))
            self.assertEqual(
                saving.text, "Adatok mentése és visszajelzés előkészítése...")

            # feedback screen
            feedback = drawing_list[103]
            self.assertTrue(isinstance(feedback, pvm.TextStim))
            self.assertEqualWithEOL(feedback.text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                                   "Pontosságod általában: 100,0 %\r\n"
                                                   "Átlagos reakcióidőd: 0,0 másodperc\r\n"
                                                   "Pontosságod a bejósolható elemeknél: 100,0 %\r\n"
                                                   "Átlagos reakcióidőd a bejósolható elemeknél: 0,0 másodperc\r\n\r\n"
                                                   "Legyél gyorsabb!\r\n\r\n\r\n\r\n")

            self.assertTrue(os.path.join(
                thispath, "subject_settings", "toth-bela_10__log.txt"))

        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "subject_settings"))
        self.clearDir(os.path.join(thispath, "logs"))

    def testQuitInsideABlock(self):
        visual_mock = pvm.PsychoPyVisualMock()
        thispath = os.path.join(self.constructFilePath("testQuitInsideABlock"))
        experiment = asrt.Experiment(thispath)
        # load settings
        settings_path = os.path.join(self.constructFilePath(
            "testQuitInsideABlock"), "settings")
        experiment.settings = asrt.ExperimentSettings(settings_path, "")
        experiment.all_settings_def()

        # load instructions
        inst_feedback_path = os.path.join(self.constructFilePath(
            "testQuitInsideABlock"), "inst_and_feedback.txt")
        experiment.instructions = asrt.InstructionHelper(inst_feedback_path)
        experiment.instructions.read_insts_from_file()

        # set user settings
        asrt.ensure_dir(os.path.join(thispath, "settings"))
        asrt.ensure_dir(os.path.join(thispath, "subject_settings"))
        asrt.ensure_dir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "subject_settings"))
        self.clearDir(os.path.join(thispath, "logs"))

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])
        experiment.participant_id()

        # monitor settings
        experiment.monitor_settings()
        experiment.colors = {'wincolor': experiment.settings.asrt_background, 'linecolor': 'black',
                             'stimp': experiment.settings.asrt_pcolor, 'stimr': experiment.settings.asrt_rcolor}

        with visual.Window(size=experiment.mymonitor.getSizePix(), color=experiment.colors['wincolor'], fullscr=False,
                           monitor=experiment.mymonitor, units="cm", gammaErrorPolicy='ignore') as experiment.mywindow:

            experiment.pressed_dict = {experiment.settings.key1: 1, experiment.settings.key2: 2,
                                       experiment.settings.key3: 3, experiment.settings.key4: 4}

            # use dummy values
            experiment.frame_time, experiment.frame_sd, experiment.frame_rate = 1.0, 0.12, 0.23

            experiment.dict_pos = {1: (float(experiment.settings.asrt_distance) * (-1.5), 0),
                                   2: (float(experiment.settings.asrt_distance) * (-0.5), 0),
                                   3: (float(experiment.settings.asrt_distance) * 0.5, 0),
                                   4: (float(experiment.settings.asrt_distance) * 1.5, 0)}

            visual_mock = pvm.PsychoPyVisualMock()

            # generate the right keys
            key_list = []
            # There are some instructions first
            key_list = [experiment.settings.key1,
                        experiment.settings.key1, experiment.settings.key1]

            # Then we have the stimuli
            for stim in experiment.stimlist.values():
                if stim == 1:
                    key_list.append(experiment.settings.key1)
                elif stim == 2:
                    key_list.append(experiment.settings.key2)
                elif stim == 3:
                    key_list.append(experiment.settings.key3)
                elif stim == 4:
                    key_list.append(experiment.settings.key4)

            key_list[7] = experiment.settings.key_quit
            visual_mock.setReturnKeyList(key_list)
            with self.assertRaises(SystemExit):
                experiment.presentation()

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 49)

            # first we have some instructions
            instruction_text = drawing_list[0]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nÜdvözlünk a feladatban!\r\n\r\n"
                                    "A képernyőn négy kör lesz, a kör egyika a többitől különböző színnel fog megjelenni.\r\n\r\n"
                                    "Az a feladatod, hogy az eltérő színű kör megjelenési helyének megfelelő gombot nyomd meg.\r\n\r\n"
                                    "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[1]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nA következő billenytűket kell használni: z, c, b, m\r\n\r\n"
                                                           "Minél pontosabban és gyorsabban kövesd le a megjelenő ingereket!\r\n\r\n"
                                                           "Ehhez mindkét kezedet használd, a középső és mutatóujjaidat.\r\n\r\n"
                                                           "Az eltérő színű kör egymás után többször ugyanazon a helyen is megjelenhet.\r\n\r\n"
                                                           "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[2]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nKb. percenként fogsz visszajelzést kapni arról,\r\n"
                                                           "hogy mennyire voltál gyors és pontos - ez alapján tudsz módosítani.\r\n\r\n"
                                                           "A feladat indításához nyomd meg valamelyik válaszgombot!\r\n\r\n")

            # then we have 11 trials
            for j in range(3, 48, 9):
                # empty cycles
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + i]
                    self.assertTrue(isinstance(
                        stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # empty cycles again
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + 4 + i]
                    self.assertTrue(isinstance(
                        stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # stimulus
                stim_circle = drawing_list[j + 8]
                self.assertTrue(isinstance(stim_circle, pvm.Circle))
                self.assertEqual(stim_circle.lineColor, 'black')
                if experiment.stimpr[((j - 3) / 9) + 1] == 'pattern':
                    self.assertEqual(stim_circle.fillColor,
                                     experiment.settings.asrt_pcolor)
                else:
                    self.assertEqual(stim_circle.fillColor,
                                     experiment.settings.asrt_rcolor)

            # quiting screen
            quit = drawing_list[48]
            self.assertTrue(isinstance(quit, pvm.TextStim))
            self.assertEqual(quit.text, "Kilépés...\nAdatok mentése...")

            self.assertTrue(os.path.join(
                thispath, "subject_settings", "toth-bela_10__log.txt"))

        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "subject_settings"))
        self.clearDir(os.path.join(thispath, "logs"))

    def testWrongPressedButton(self):
        visual_mock = pvm.PsychoPyVisualMock()
        thispath = os.path.join(
            self.constructFilePath("testWrongPressedButton"))
        experiment = asrt.Experiment(thispath)
        # load settings
        settings_path = os.path.join(self.constructFilePath(
            "testWrongPressedButton"), "settings")
        experiment.settings = asrt.ExperimentSettings(settings_path, "")
        experiment.all_settings_def()

        # load instructions
        inst_feedback_path = os.path.join(self.constructFilePath(
            "testWrongPressedButton"), "inst_and_feedback.txt")
        experiment.instructions = asrt.InstructionHelper(inst_feedback_path)
        experiment.instructions.read_insts_from_file()

        # set user settings
        asrt.ensure_dir(os.path.join(thispath, "settings"))
        asrt.ensure_dir(os.path.join(thispath, "subject_settings"))
        asrt.ensure_dir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "subject_settings"))
        self.clearDir(os.path.join(thispath, "logs"))

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])
        experiment.participant_id()

        # monitor settings
        experiment.monitor_settings()
        experiment.colors = {'wincolor': experiment.settings.asrt_background, 'linecolor': 'black',
                             'stimp': experiment.settings.asrt_pcolor, 'stimr': experiment.settings.asrt_rcolor}

        with visual.Window(size=experiment.mymonitor.getSizePix(), color=experiment.colors['wincolor'], fullscr=False,
                           monitor=experiment.mymonitor, units="cm", gammaErrorPolicy='ignore') as experiment.mywindow:

            experiment.pressed_dict = {experiment.settings.key1: 1, experiment.settings.key2: 2,
                                       experiment.settings.key3: 3, experiment.settings.key4: 4}

            # use dummy values
            experiment.frame_time, experiment.frame_sd, experiment.frame_rate = 1.0, 0.12, 0.23

            experiment.dict_pos = {1: (float(experiment.settings.asrt_distance) * (-1.5), 0),
                                   2: (float(experiment.settings.asrt_distance) * (-0.5), 0),
                                   3: (float(experiment.settings.asrt_distance) * 0.5, 0),
                                   4: (float(experiment.settings.asrt_distance) * 1.5, 0)}

            visual_mock = pvm.PsychoPyVisualMock()

            # generate the right keys
            key_list = []
            # There are some instructions first
            key_list = [experiment.settings.key1,
                        experiment.settings.key1, experiment.settings.key1]

            # Then we have the stimuli
            for stim in experiment.stimlist.values():
                if stim == 1:
                    key_list.append(experiment.settings.key1)
                elif stim == 2:
                    key_list.append(experiment.settings.key2)
                elif stim == 3:
                    key_list.append(experiment.settings.key3)
                elif stim == 4:
                    key_list.append(experiment.settings.key4)

            key_list = key_list[0:12] + [key_list[10]] + key_list[12:]
            visual_mock.setReturnKeyList(key_list)
            experiment.presentation()

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 109)

            # first we have some instructions
            instruction_text = drawing_list[0]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nÜdvözlünk a feladatban!\r\n\r\n"
                                    "A képernyőn négy kör lesz, a kör egyika a többitől különböző színnel fog megjelenni.\r\n\r\n"
                                    "Az a feladatod, hogy az eltérő színű kör megjelenési helyének megfelelő gombot nyomd meg.\r\n\r\n"
                                    "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[1]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nA következő billenytűket kell használni: z, c, b, m\r\n\r\n"
                                                           "Minél pontosabban és gyorsabban kövesd le a megjelenő ingereket!\r\n\r\n"
                                                           "Ehhez mindkét kezedet használd, a középső és mutatóujjaidat.\r\n\r\n"
                                                           "Az eltérő színű kör egymás után többször ugyanazon a helyen is megjelenhet.\r\n\r\n"
                                                           "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[2]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nKb. percenként fogsz visszajelzést kapni arról,\r\n"
                                                           "hogy mennyire voltál gyors és pontos - ez alapján tudsz módosítani.\r\n\r\n"
                                                           "A feladat indításához nyomd meg valamelyik válaszgombot!\r\n\r\n")

            # then we have 9 trials
            for j in range(3, 93, 9):
                # empty cycles
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + i]
                    self.assertTrue(isinstance(
                        stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # empty cycles again
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + 4 + i]
                    self.assertTrue(isinstance(
                        stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # stimulus
                stim_circle = drawing_list[j + 8]
                self.assertTrue(isinstance(stim_circle, pvm.Circle))
                self.assertEqual(stim_circle.lineColor, 'black')
                if experiment.stimpr[((j - 3) / 9) + 1] == 'pattern':
                    self.assertEqual(stim_circle.fillColor,
                                     experiment.settings.asrt_pcolor)
                else:
                    self.assertEqual(stim_circle.fillColor,
                                     experiment.settings.asrt_rcolor)

            # last stimuli is displayed again
            # empty cycles
            for i in range(0, 4):
                stim_background_circle = drawing_list[93 + i]
                self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
                self.assertEqual(stim_background_circle.lineColor, 'black')
                self.assertEqual(stim_background_circle.fillColor, None)

            # stimulus
            stim_circle = drawing_list[97]
            self.assertTrue(isinstance(stim_circle, pvm.Circle))
            self.assertEqual(stim_circle.lineColor, 'black')
            self.assertEqual(stim_circle.fillColor,
                             experiment.settings.asrt_pcolor)

            # saving screen
            saving = drawing_list[107]
            self.assertTrue(isinstance(saving, pvm.TextStim))
            self.assertEqual(
                saving.text, "Adatok mentése és visszajelzés előkészítése...")

            # feedback screen
            feedback = drawing_list[108]
            self.assertTrue(isinstance(feedback, pvm.TextStim))
            self.assertEqualWithEOL(feedback.text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                                   "Pontosságod általában: 91,66 %\r\n"
                                                   "Átlagos reakcióidőd: 0,0 másodperc\r\n"
                                                   "Pontosságod a bejósolható elemeknél: 75,0 %\r\n"
                                                   "Átlagos reakcióidőd a bejósolható elemeknél: 0,0 másodperc\r\n\r\n\r\n")

            self.assertTrue(os.path.join(
                thispath, "subject_settings", "toth-bela_10__log.txt"))

        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "subject_settings"))
        self.clearDir(os.path.join(thispath, "logs"))

    def testQuitOnFeedbackScreen(self):
        visual_mock = pvm.PsychoPyVisualMock()
        thispath = os.path.join(
            self.constructFilePath("testQuitOnFeedbackScreen"))
        experiment = asrt.Experiment(thispath)
        # load settings
        settings_path = os.path.join(self.constructFilePath(
            "testQuitOnFeedbackScreen"), "settings")
        experiment.settings = asrt.ExperimentSettings(settings_path, "")
        experiment.all_settings_def()

        # load instructions
        inst_feedback_path = os.path.join(self.constructFilePath(
            "testQuitOnFeedbackScreen"), "inst_and_feedback.txt")
        experiment.instructions = asrt.InstructionHelper(inst_feedback_path)
        experiment.instructions.read_insts_from_file()

        # set user settings
        asrt.ensure_dir(os.path.join(thispath, "settings"))
        asrt.ensure_dir(os.path.join(thispath, "subject_settings"))
        asrt.ensure_dir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "subject_settings"))
        self.clearDir(os.path.join(thispath, "logs"))

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])
        experiment.participant_id()

        # monitor settings
        experiment.monitor_settings()
        experiment.colors = {'wincolor': experiment.settings.asrt_background, 'linecolor': 'black',
                             'stimp': experiment.settings.asrt_pcolor, 'stimr': experiment.settings.asrt_rcolor}

        with visual.Window(size=experiment.mymonitor.getSizePix(), color=experiment.colors['wincolor'], fullscr=False,
                           monitor=experiment.mymonitor, units="cm", gammaErrorPolicy='ignore') as experiment.mywindow:

            experiment.pressed_dict = {experiment.settings.key1: 1, experiment.settings.key2: 2,
                                       experiment.settings.key3: 3, experiment.settings.key4: 4}

            # use dummy values
            experiment.frame_time, experiment.frame_sd, experiment.frame_rate = 1.0, 0.12, 0.23

            experiment.dict_pos = {1: (float(experiment.settings.asrt_distance) * (-1.5), 0),
                                   2: (float(experiment.settings.asrt_distance) * (-0.5), 0),
                                   3: (float(experiment.settings.asrt_distance) * 0.5, 0),
                                   4: (float(experiment.settings.asrt_distance) * 1.5, 0)}

            visual_mock = pvm.PsychoPyVisualMock()

            # generate the right keys
            key_list = []
            # There are some instructions first
            key_list = [experiment.settings.key1,
                        experiment.settings.key1, experiment.settings.key1]

            # Then we have the stimuli
            for stim in experiment.stimlist.values():
                if stim == 1:
                    key_list.append(experiment.settings.key1)
                elif stim == 2:
                    key_list.append(experiment.settings.key2)
                elif stim == 3:
                    key_list.append(experiment.settings.key3)
                elif stim == 4:
                    key_list.append(experiment.settings.key4)

            key_list.append(experiment.settings.key_quit)
            visual_mock.setReturnKeyList(key_list)
            with self.assertRaises(SystemExit):
                experiment.presentation()

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 105)

            # first we have some instructions
            instruction_text = drawing_list[0]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nÜdvözlünk a feladatban!\r\n\r\n"
                                    "A képernyőn négy kör lesz, a kör egyika a többitől különböző színnel fog megjelenni.\r\n\r\n"
                                    "Az a feladatod, hogy az eltérő színű kör megjelenési helyének megfelelő gombot nyomd meg.\r\n\r\n"
                                    "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[1]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nA következő billenytűket kell használni: z, c, b, m\r\n\r\n"
                                                           "Minél pontosabban és gyorsabban kövesd le a megjelenő ingereket!\r\n\r\n"
                                                           "Ehhez mindkét kezedet használd, a középső és mutatóujjaidat.\r\n\r\n"
                                                           "Az eltérő színű kör egymás után többször ugyanazon a helyen is megjelenhet.\r\n\r\n"
                                                           "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[2]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqualWithEOL(instruction_text.text, "\r\n\r\nKb. percenként fogsz visszajelzést kapni arról,\r\n"
                                                           "hogy mennyire voltál gyors és pontos - ez alapján tudsz módosítani.\r\n\r\n"
                                                           "A feladat indításához nyomd meg valamelyik válaszgombot!\r\n\r\n")

            # then we have 11 trials
            for j in range(3, 102, 9):
                # empty cycles
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + i]
                    self.assertTrue(isinstance(
                        stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # empty cycles again
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + 4 + i]
                    self.assertTrue(isinstance(
                        stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # stimulus
                stim_circle = drawing_list[j + 8]
                self.assertTrue(isinstance(stim_circle, pvm.Circle))
                self.assertEqual(stim_circle.lineColor, 'black')
                if experiment.stimpr[((j - 3) / 9) + 1] == 'pattern':
                    self.assertEqual(stim_circle.fillColor,
                                     experiment.settings.asrt_pcolor)
                else:
                    self.assertEqual(stim_circle.fillColor,
                                     experiment.settings.asrt_rcolor)

            # saving screen
            saving = drawing_list[102]
            self.assertTrue(isinstance(saving, pvm.TextStim))
            self.assertEqual(
                saving.text, "Adatok mentése és visszajelzés előkészítése...")

            # feedback screen
            feedback = drawing_list[103]
            self.assertTrue(isinstance(feedback, pvm.TextStim))
            self.assertEqualWithEOL(feedback.text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                                   "Pontosságod általában: 100,0 %\r\n"
                                                   "Átlagos reakcióidőd: 0,0 másodperc\r\n"
                                                   "Pontosságod a bejósolható elemeknél: 100,0 %\r\n"
                                                   "Átlagos reakcióidőd a bejósolható elemeknél: 0,0 másodperc\r\n\r\n"
                                                   "Legyél gyorsabb!\r\n\r\n\r\n\r\n")
            # quit screen
            quit = drawing_list[104]
            self.assertTrue(isinstance(quit, pvm.TextStim))
            self.assertEqual(quit.text, "Kilépés...\nAdatok mentése...")

            self.assertTrue(os.path.join(
                thispath, "subject_settings", "toth-bela_10__log.txt"))

        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "subject_settings"))
        self.clearDir(os.path.join(thispath, "logs"))


if __name__ == "__main__":
    unittest.main()  # run all tests
