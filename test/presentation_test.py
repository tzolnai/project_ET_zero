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

#!\\usr\\bin\\env python
# -*- coding: utf-8 -*-

import unittest

import os

import sys
# Add the local path to the main script so we can import it.
sys.path = [".."] + [os.path.join("..", "externals", "psychopy_mock")]  + sys.path

import asrt
import shutil

import psychopy_visual_mock as pvm
import psychopy_gui_mock as pgm
from psychopy import visual, logging

# ignore warnings comming from psychopy
logging.console.setLevel(logging.ERROR)

dict_accents = {u'á':u'a',u'é':u'e',u'í':u'i',u'ó':u'o',u'ő':u'o',u'ö':u'o',u'ú':u'u',u'ű':u'u',u'ü':u'u'}

class participantIDTest(unittest.TestCase):

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
        filepath = os.path.join(filepath, "data", "presentation", file_name)
        return filepath

    def testSimpleTestCase(self):
        visual_mock = pvm.PsychoPyVisualMock()
        # load settings
        dict_accents = {u'á':u'a',u'é':u'e',u'í':u'i',u'ó':u'o',u'ő':u'o',u'ö':u'o',u'ú':u'u',u'ű':u'u',u'ü':u'u'}
        settings_path = os.path.join(self.constructFilePath("testSimpleTestCase"), "settings")
        exp_settings = asrt.ExperimentSettings(settings_path, "")
        asrt.all_settings_def(exp_settings, dict_accents)

        # load instructions
        inst_feedback_path = os.path.join(self.constructFilePath("testSimpleTestCase"), "inst_and_feedback.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        # set user settings
        thispath = os.path.join(self.constructFilePath("testSimpleTestCase"))
        asrt.ensure_dir(os.path.join(thispath, "settings"))
        asrt.ensure_dir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "logs"))

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])
        group, subject_nr, identif, person_data_handler, PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, last_N,  end_at, stim_colorN, stimpr = asrt.participant_id(thispath, exp_settings, dict_accents)


        # monitor settings
        my_monitor = asrt.monitor_settings(exp_settings)
        colors = { 'wincolor' : exp_settings.asrt_background, 'linecolor':'black', 'stimp':exp_settings.asrt_pcolor, 'stimr':exp_settings.asrt_rcolor}
        with visual.Window (size = my_monitor.getSizePix(), color = colors['wincolor'], fullscr = False, monitor = my_monitor, units = "cm") as mywindow:

            pressed_dict = {exp_settings.key1:1,exp_settings.key2:2,exp_settings.key3:3,exp_settings.key4:4}

            frame_time, frame_sd, frame_rate = 1.0, 0.12, 0.23 # use dummy values


            dict_pos = { 1:  ( float(exp_settings.asrt_distance)*(-1.5), 0),
                         2:  ( float(exp_settings.asrt_distance)*(-0.5), 0),
                         3:  ( float(exp_settings.asrt_distance)*  0.5,   0),
                         4:  ( float(exp_settings.asrt_distance)*  1.5,   0) }

            visual_mock = pvm.PsychoPyVisualMock()

            # generate the right keys
            key_list = []
            # There are some instructions first
            key_list = [exp_settings.key1, exp_settings.key1, exp_settings.key1]

            # Then we have the stimuli
            for stim in stimlist.values():
                if stim == 1:
                    key_list.append(exp_settings.key1)
                elif stim == 2:
                    key_list.append(exp_settings.key2)
                elif stim == 3:
                    key_list.append(exp_settings.key3)
                elif stim == 4:
                    key_list.append(exp_settings.key4)

            visual_mock.setReturnKeyList(key_list)
            last_N, stim_output_line = asrt.presentation(mywindow, exp_settings, instruction_helper, person_data_handler, colors, dict_pos, PCodes, pressed_dict,
                                                        last_N, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, end_at, stim_colorN,
                                                        group, identif, subject_nr, frame_rate, frame_time, frame_sd)

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 104)

            # first we have some instructions
            instruction_text = drawing_list[0]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nÜdvözlünk a feladatban!\r\n\r\n"
                                                "A képernyőn négy kör lesz, a kör egyika a többitől különböző színnel fog megjelenni.\r\n\r\n"
                                                "Az a feladatod, hogy az eltérő színű kör megjelenési helyének megfelelő gombot nyomd meg.\r\n\r\n"
                                                "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[1]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nA következő billenytűket kell használni: z, c, b, m\r\n\r\n"
                                                    "Minél pontosabban és gyorsabban kövesd le a megjelenő ingereket!\r\n\r\n"
                                                    "Ehhez mindkét kezedet használd, a középső és mutatóujjaidat.\r\n\r\n"
                                                    "Az eltérő színű kör egymás után többször ugyanazon a helyen is megjelenhet.\r\n\r\n"
                                                    "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[2]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nKb. percenként fogsz visszajelzést kapni arról,\r\n"
                                                    "hogy mennyire voltál gyors és pontos - ez alapján tudsz módosítani.\r\n\r\n"
                                                    "A feladat indításához nyomd meg valamelyik válaszgombot!\r\n\r\n")

            # then we have 11 trials
            for j in range(3, 102, 9):
                # empty cycles
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + i]
                    self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # empty cycles again
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + 4 + i]
                    self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # stimulus
                stim_circle = drawing_list[j + 8]
                self.assertTrue(isinstance(stim_circle, pvm.Circle))
                self.assertEqual(stim_circle.lineColor, 'black')
                self.assertEqual(stim_circle.fillColor, exp_settings.asrt_rcolor)

            # saving screen
            saving = drawing_list[102]
            self.assertTrue(isinstance(saving, pvm.TextStim))
            self.assertEqual(saving.text, "Adatok mentése és visszajelzés előkészítése...")

            # feedback screen
            feedback = drawing_list[103]
            self.assertTrue(isinstance(feedback, pvm.TextStim))
            self.assertEqual(feedback.text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                            "Pontosságod: 100,0 %\r\n"
                                            "Átlagos reakcióidőd: 0,0 másodperc\r\n\r\n"
                                            "Legyél gyorsabb!\r\n\r\n\r\n\r\n")

            self.assertTrue(os.path.join(thispath, "settings", "toth-bela_10__log.txt"))

        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "logs"))

    def testExplixitASRT(self):
        visual_mock = pvm.PsychoPyVisualMock()
        # load settings
        dict_accents = {u'á':u'a',u'é':u'e',u'í':u'i',u'ó':u'o',u'ő':u'o',u'ö':u'o',u'ú':u'u',u'ű':u'u',u'ü':u'u'}
        settings_path = os.path.join(self.constructFilePath("testExplixitASRT"), "settings")
        exp_settings = asrt.ExperimentSettings(settings_path, "")
        asrt.all_settings_def(exp_settings, dict_accents)

        # load instructions
        inst_feedback_path = os.path.join(self.constructFilePath("testExplixitASRT"), "inst_and_feedback.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        # set user settings
        thispath = os.path.join(self.constructFilePath("testExplixitASRT"))
        asrt.ensure_dir(os.path.join(thispath, "settings"))
        asrt.ensure_dir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "logs"))

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])
        group, subject_nr, identif, person_data_handler, PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, last_N,  end_at, stim_colorN, stimpr = asrt.participant_id(thispath, exp_settings, dict_accents)


        # monitor settings
        my_monitor = asrt.monitor_settings(exp_settings)
        colors = { 'wincolor' : exp_settings.asrt_background, 'linecolor':'black', 'stimp':exp_settings.asrt_pcolor, 'stimr':exp_settings.asrt_rcolor}
        with visual.Window (size = my_monitor.getSizePix(), color = colors['wincolor'], fullscr = False, monitor = my_monitor, units = "cm") as mywindow:

            pressed_dict = {exp_settings.key1:1,exp_settings.key2:2,exp_settings.key3:3,exp_settings.key4:4}

            frame_time, frame_sd, frame_rate = 1.0, 0.12, 0.23 # use dummy values


            dict_pos = { 1:  ( float(exp_settings.asrt_distance)*(-1.5), 0),
                         2:  ( float(exp_settings.asrt_distance)*(-0.5), 0),
                         3:  ( float(exp_settings.asrt_distance)*  0.5,   0),
                         4:  ( float(exp_settings.asrt_distance)*  1.5,   0) }

            visual_mock = pvm.PsychoPyVisualMock()

            # generate the right keys
            key_list = []
            # There are some instructions first
            key_list = [exp_settings.key1, exp_settings.key1, exp_settings.key1]

            # Then we have the stimuli
            for stim in stimlist.values():
                if stim == 1:
                    key_list.append(exp_settings.key1)
                elif stim == 2:
                    key_list.append(exp_settings.key2)
                elif stim == 3:
                    key_list.append(exp_settings.key3)
                elif stim == 4:
                    key_list.append(exp_settings.key4)

            visual_mock.setReturnKeyList(key_list)
            last_N, stim_output_line = asrt.presentation(mywindow, exp_settings, instruction_helper, person_data_handler, colors, dict_pos, PCodes, pressed_dict,
                                                        last_N, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, end_at, stim_colorN,
                                                        group, identif, subject_nr, frame_rate, frame_time, frame_sd)

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 104)

            # first we have some instructions
            instruction_text = drawing_list[0]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nÜdvözlünk a feladatban!\r\n\r\n"
                                                "A képernyőn négy kör lesz, a kör egyika a többitől különböző színnel fog megjelenni.\r\n\r\n"
                                                "Az a feladatod, hogy az eltérő színű kör megjelenési helyének megfelelő gombot nyomd meg.\r\n\r\n"
                                                "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[1]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nA következő billenytűket kell használni: z, c, b, m\r\n\r\n"
                                                    "Minél pontosabban és gyorsabban kövesd le a megjelenő ingereket!\r\n\r\n"
                                                    "Ehhez mindkét kezedet használd, a középső és mutatóujjaidat.\r\n\r\n"
                                                    "Az eltérő színű kör egymás után többször ugyanazon a helyen is megjelenhet.\r\n\r\n"
                                                    "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[2]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nKb. percenként fogsz visszajelzést kapni arról,\r\n"
                                                    "hogy mennyire voltál gyors és pontos - ez alapján tudsz módosítani.\r\n\r\n"
                                                    "A feladat indításához nyomd meg valamelyik válaszgombot!\r\n\r\n")

            # then we have 11 trials
            for j in range(3, 102, 9):
                # empty cycles
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + i]
                    self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # empty cycles again
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + 4 + i]
                    self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # stimulus
                stim_circle = drawing_list[j + 8]
                self.assertTrue(isinstance(stim_circle, pvm.Circle))
                self.assertEqual(stim_circle.lineColor, 'black')
                if stimpr[((j - 3) / 9) + 1] == 'P':
                    self.assertEqual(stim_circle.fillColor, exp_settings.asrt_pcolor)
                else:
                    self.assertEqual(stim_circle.fillColor, exp_settings.asrt_rcolor)

            # saving screen
            saving = drawing_list[102]
            self.assertTrue(isinstance(saving, pvm.TextStim))
            self.assertEqual(saving.text, "Adatok mentése és visszajelzés előkészítése...")

            # feedback screen
            feedback = drawing_list[103]
            self.assertTrue(isinstance(feedback, pvm.TextStim))
            self.assertEqual(feedback.text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                            "Pontosságod általában: 100,0 %\r\n"
                                            "Átlagos reakcióidőd: 0,0 másodperc\r\n"
                                            "Pontosságod a bejósolható elemeknél: 100,0 %\r\n"
                                            "Átlagos reakcióidőd a bejósolható elemeknél: 0,0 másodperc\r\n\r\n"
                                            "Legyél gyorsabb!\r\n\r\n\r\n\r\n")

            self.assertTrue(os.path.join(thispath, "settings", "toth-bela_10__log.txt"))

        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "logs"))

    def testQuitInsideABlock(self):
        visual_mock = pvm.PsychoPyVisualMock()
        # load settings
        dict_accents = {u'á':u'a',u'é':u'e',u'í':u'i',u'ó':u'o',u'ő':u'o',u'ö':u'o',u'ú':u'u',u'ű':u'u',u'ü':u'u'}
        settings_path = os.path.join(self.constructFilePath("testQuitInsideABlock"), "settings")
        exp_settings = asrt.ExperimentSettings(settings_path, "")
        asrt.all_settings_def(exp_settings, dict_accents)

        # load instructions
        inst_feedback_path = os.path.join(self.constructFilePath("testQuitInsideABlock"), "inst_and_feedback.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        # set user settings
        thispath = os.path.join(self.constructFilePath("testQuitInsideABlock"))
        asrt.ensure_dir(os.path.join(thispath, "settings"))
        asrt.ensure_dir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "logs"))

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])
        group, subject_nr, identif, person_data_handler, PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, last_N,  end_at, stim_colorN, stimpr = asrt.participant_id(thispath, exp_settings, dict_accents)


        # monitor settings
        my_monitor = asrt.monitor_settings(exp_settings)
        colors = { 'wincolor' : exp_settings.asrt_background, 'linecolor':'black', 'stimp':exp_settings.asrt_pcolor, 'stimr':exp_settings.asrt_rcolor}
        with visual.Window (size = my_monitor.getSizePix(), color = colors['wincolor'], fullscr = False, monitor = my_monitor, units = "cm") as mywindow:

            pressed_dict = {exp_settings.key1:1,exp_settings.key2:2,exp_settings.key3:3,exp_settings.key4:4}

            frame_time, frame_sd, frame_rate = 1.0, 0.12, 0.23 # use dummy values


            dict_pos = { 1:  ( float(exp_settings.asrt_distance)*(-1.5), 0),
                         2:  ( float(exp_settings.asrt_distance)*(-0.5), 0),
                         3:  ( float(exp_settings.asrt_distance)*  0.5,   0),
                         4:  ( float(exp_settings.asrt_distance)*  1.5,   0) }

            visual_mock = pvm.PsychoPyVisualMock()

            # generate the right keys
            key_list = []
            # There are some instructions first
            key_list = [exp_settings.key1, exp_settings.key1, exp_settings.key1]

            # Then we have the stimuli
            for stim in stimlist.values():
                if stim == 1:
                    key_list.append(exp_settings.key1)
                elif stim == 2:
                    key_list.append(exp_settings.key2)
                elif stim == 3:
                    key_list.append(exp_settings.key3)
                elif stim == 4:
                    key_list.append(exp_settings.key4)

            key_list[7] = exp_settings.key_quit
            visual_mock.setReturnKeyList(key_list)
            with self.assertRaises(SystemExit):
                last_N, stim_output_line = asrt.presentation(mywindow, exp_settings, instruction_helper, person_data_handler, colors, dict_pos, PCodes, pressed_dict,
                                                             last_N, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, end_at, stim_colorN,
                                                             group, identif, subject_nr, frame_rate, frame_time, frame_sd)

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 49)

            # first we have some instructions
            instruction_text = drawing_list[0]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nÜdvözlünk a feladatban!\r\n\r\n"
                                                "A képernyőn négy kör lesz, a kör egyika a többitől különböző színnel fog megjelenni.\r\n\r\n"
                                                "Az a feladatod, hogy az eltérő színű kör megjelenési helyének megfelelő gombot nyomd meg.\r\n\r\n"
                                                "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[1]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nA következő billenytűket kell használni: z, c, b, m\r\n\r\n"
                                                    "Minél pontosabban és gyorsabban kövesd le a megjelenő ingereket!\r\n\r\n"
                                                    "Ehhez mindkét kezedet használd, a középső és mutatóujjaidat.\r\n\r\n"
                                                    "Az eltérő színű kör egymás után többször ugyanazon a helyen is megjelenhet.\r\n\r\n"
                                                    "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[2]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nKb. percenként fogsz visszajelzést kapni arról,\r\n"
                                                    "hogy mennyire voltál gyors és pontos - ez alapján tudsz módosítani.\r\n\r\n"
                                                    "A feladat indításához nyomd meg valamelyik válaszgombot!\r\n\r\n")

            # then we have 11 trials
            for j in range(3, 48, 9):
                # empty cycles
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + i]
                    self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # empty cycles again
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + 4 + i]
                    self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # stimulus
                stim_circle = drawing_list[j + 8]
                self.assertTrue(isinstance(stim_circle, pvm.Circle))
                self.assertEqual(stim_circle.lineColor, 'black')
                if stimpr[((j - 3) / 9) + 1] == 'P':
                    self.assertEqual(stim_circle.fillColor, exp_settings.asrt_pcolor)
                else:
                    self.assertEqual(stim_circle.fillColor, exp_settings.asrt_rcolor)

            # quiting screen
            quit = drawing_list[48]
            self.assertTrue(isinstance(quit, pvm.TextStim))
            self.assertEqual(quit.text, "Quit...\nSaving data...")

            self.assertTrue(os.path.join(thispath, "settings", "toth-bela_10__log.txt"))

        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "logs"))

    def testWrongPressedButton(self):
        visual_mock = pvm.PsychoPyVisualMock()
        # load settings
        dict_accents = {u'á':u'a',u'é':u'e',u'í':u'i',u'ó':u'o',u'ő':u'o',u'ö':u'o',u'ú':u'u',u'ű':u'u',u'ü':u'u'}
        settings_path = os.path.join(self.constructFilePath("testWrongPressedButton"), "settings")
        exp_settings = asrt.ExperimentSettings(settings_path, "")
        asrt.all_settings_def(exp_settings, dict_accents)

        # load instructions
        inst_feedback_path = os.path.join(self.constructFilePath("testWrongPressedButton"), "inst_and_feedback.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        # set user settings
        thispath = os.path.join(self.constructFilePath("testWrongPressedButton"))
        asrt.ensure_dir(os.path.join(thispath, "settings"))
        asrt.ensure_dir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "logs"))

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])
        group, subject_nr, identif, person_data_handler, PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, last_N,  end_at, stim_colorN, stimpr = asrt.participant_id(thispath, exp_settings, dict_accents)

        # monitor settings
        my_monitor = asrt.monitor_settings(exp_settings)
        colors = { 'wincolor' : exp_settings.asrt_background, 'linecolor':'black', 'stimp':exp_settings.asrt_pcolor, 'stimr':exp_settings.asrt_rcolor}
        with visual.Window (size = my_monitor.getSizePix(), color = colors['wincolor'], fullscr = False, monitor = my_monitor, units = "cm") as mywindow:

            pressed_dict = {exp_settings.key1:1,exp_settings.key2:2,exp_settings.key3:3,exp_settings.key4:4}

            frame_time, frame_sd, frame_rate = 1.0, 0.12, 0.23 # use dummy values


            dict_pos = { 1:  ( float(exp_settings.asrt_distance)*(-1.5), 0),
                         2:  ( float(exp_settings.asrt_distance)*(-0.5), 0),
                         3:  ( float(exp_settings.asrt_distance)*  0.5,   0),
                         4:  ( float(exp_settings.asrt_distance)*  1.5,   0) }

            visual_mock = pvm.PsychoPyVisualMock()

            # generate the right keys
            key_list = []
            # There are some instructions first
            key_list = [exp_settings.key1, exp_settings.key1, exp_settings.key1]

            # Then we have the stimuli
            for stim in stimlist.values():
                if stim == 1:
                    key_list.append(exp_settings.key1)
                elif stim == 2:
                    key_list.append(exp_settings.key2)
                elif stim == 3:
                    key_list.append(exp_settings.key3)
                elif stim == 4:
                    key_list.append(exp_settings.key4)

            key_list = key_list[0:12] + [key_list[10]] + key_list[12:]
            visual_mock.setReturnKeyList(key_list)
            last_N, stim_output_line = asrt.presentation(mywindow, exp_settings, instruction_helper, person_data_handler, colors, dict_pos, PCodes, pressed_dict,
                                                         last_N, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, end_at, stim_colorN,
                                                         group, identif, subject_nr, frame_rate, frame_time, frame_sd)

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 109)

            # first we have some instructions
            instruction_text = drawing_list[0]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nÜdvözlünk a feladatban!\r\n\r\n"
                                                "A képernyőn négy kör lesz, a kör egyika a többitől különböző színnel fog megjelenni.\r\n\r\n"
                                                "Az a feladatod, hogy az eltérő színű kör megjelenési helyének megfelelő gombot nyomd meg.\r\n\r\n"
                                                "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[1]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nA következő billenytűket kell használni: z, c, b, m\r\n\r\n"
                                                    "Minél pontosabban és gyorsabban kövesd le a megjelenő ingereket!\r\n\r\n"
                                                    "Ehhez mindkét kezedet használd, a középső és mutatóujjaidat.\r\n\r\n"
                                                    "Az eltérő színű kör egymás után többször ugyanazon a helyen is megjelenhet.\r\n\r\n"
                                                    "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[2]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nKb. percenként fogsz visszajelzést kapni arról,\r\n"
                                                    "hogy mennyire voltál gyors és pontos - ez alapján tudsz módosítani.\r\n\r\n"
                                                    "A feladat indításához nyomd meg valamelyik válaszgombot!\r\n\r\n")

            # then we have 9 trials
            for j in range(3, 93, 9):
                # empty cycles
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + i]
                    self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # empty cycles again
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + 4 + i]
                    self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # stimulus
                stim_circle = drawing_list[j + 8]
                self.assertTrue(isinstance(stim_circle, pvm.Circle))
                self.assertEqual(stim_circle.lineColor, 'black')
                if stimpr[((j - 3) / 9) + 1] == 'P':
                    self.assertEqual(stim_circle.fillColor, exp_settings.asrt_pcolor)
                else:
                    self.assertEqual(stim_circle.fillColor, exp_settings.asrt_rcolor)

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
            self.assertEqual(stim_circle.fillColor, exp_settings.asrt_pcolor)

            # saving screen
            saving = drawing_list[107]
            self.assertTrue(isinstance(saving, pvm.TextStim))
            self.assertEqual(saving.text, "Adatok mentése és visszajelzés előkészítése...")

            # feedback screen
            feedback = drawing_list[108]
            self.assertTrue(isinstance(feedback, pvm.TextStim))
            self.assertEqual(feedback.text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                            "Pontosságod általában: 91,66 %\r\n"
                                            "Átlagos reakcióidőd: 0,0 másodperc\r\n"
                                            "Pontosságod a bejósolható elemeknél: 75,0 %\r\n"
                                            "Átlagos reakcióidőd a bejósolható elemeknél: 0,0 másodperc\r\n\r\n\r\n")

            self.assertTrue(os.path.join(thispath, "settings", "toth-bela_10__log.txt"))

        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "logs"))

    def testContinueAfterQuit(self):
        visual_mock = pvm.PsychoPyVisualMock()
        # load settings
        dict_accents = {u'á':u'a',u'é':u'e',u'í':u'i',u'ó':u'o',u'ő':u'o',u'ö':u'o',u'ú':u'u',u'ű':u'u',u'ü':u'u'}
        settings_path = os.path.join(self.constructFilePath("testContinueAfterQuit"), "settings")
        exp_settings = asrt.ExperimentSettings(settings_path, "")
        asrt.all_settings_def(exp_settings, dict_accents)

        # load instructions
        inst_feedback_path = os.path.join(self.constructFilePath("testContinueAfterQuit"), "inst_and_feedback.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        # set user settings
        thispath = os.path.join(self.constructFilePath("testContinueAfterQuit"))
        asrt.ensure_dir(os.path.join(thispath, "settings"))
        asrt.ensure_dir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))

        # copy participant settings file
        shutil.copyfile(os.path.join(thispath, "participant_settings.bak"), os.path.join(thispath, "settings", "participant_settings.bak"))
        shutil.copyfile(os.path.join(thispath, "participant_settings.dat"), os.path.join(thispath, "settings", "participant_settings.dat"))
        shutil.copyfile(os.path.join(thispath, "participant_settings.dir"), os.path.join(thispath, "settings", "participant_settings.dir"))
        shutil.copyfile(os.path.join(thispath, "toth-bela_10_.bak"), os.path.join(thispath, "settings", "toth-bela_10_.bak"))
        shutil.copyfile(os.path.join(thispath, "toth-bela_10_.dat"), os.path.join(thispath, "settings", "toth-bela_10_.dat"))
        shutil.copyfile(os.path.join(thispath, "toth-bela_10_.dir"), os.path.join(thispath, "settings", "toth-bela_10_.dir"))

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10])
        group, subject_nr, identif, person_data_handler, PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, last_N,  end_at, stim_colorN, stimpr = asrt.participant_id(thispath, exp_settings, dict_accents)

        # monitor settings
        my_monitor = asrt.monitor_settings(exp_settings)
        colors = { 'wincolor' : exp_settings.asrt_background, 'linecolor':'black', 'stimp':exp_settings.asrt_pcolor, 'stimr':exp_settings.asrt_rcolor}
        with visual.Window (size = my_monitor.getSizePix(), color = colors['wincolor'], fullscr = False, monitor = my_monitor, units = "cm") as mywindow:

            pressed_dict = {exp_settings.key1:1,exp_settings.key2:2,exp_settings.key3:3,exp_settings.key4:4}

            frame_time, frame_sd, frame_rate = 1.0, 0.12, 0.23 # use dummy values


            dict_pos = { 1:  ( float(exp_settings.asrt_distance)*(-1.5), 0),
                         2:  ( float(exp_settings.asrt_distance)*(-0.5), 0),
                         3:  ( float(exp_settings.asrt_distance)*  0.5,   0),
                         4:  ( float(exp_settings.asrt_distance)*  1.5,   0) }

            visual_mock = pvm.PsychoPyVisualMock()

            # generate the right keys
            key_list = []
            # There are some instructions first
            key_list = [exp_settings.key1]

            # Then we have the stimuli
            for i in range (last_N + 1, 12):
                stim = stimlist[i]
                if stim == 1:
                    key_list.append(exp_settings.key1)
                elif stim == 2:
                    key_list.append(exp_settings.key2)
                elif stim == 3:
                    key_list.append(exp_settings.key3)
                elif stim == 4:
                    key_list.append(exp_settings.key4)

            visual_mock.setReturnKeyList(key_list)
            last_N, stim_output_line = asrt.presentation(mywindow, exp_settings, instruction_helper, person_data_handler, colors, dict_pos, PCodes, pressed_dict,
                                                         last_N, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, end_at, stim_colorN,
                                                         group, identif, subject_nr, frame_rate, frame_time, frame_sd)

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 30)

            # first we have one instruction screen about the continuation
            instruction_text = drawing_list[0]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nVáratlan kilépés történt a feladatból. Folytatás. A feladat indításához nyomd meg valamelyik válaszbillentyűt.")

            # then we have 11 trials
            for j in range(1, 28, 9):
                # empty cycles
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + i]
                    self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # empty cycles again
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + 4 + i]
                    self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # stimulus
                stim_circle = drawing_list[j + 8]
                self.assertTrue(isinstance(stim_circle, pvm.Circle))
                self.assertEqual(stim_circle.lineColor, 'black')
                if stimpr[((j - 1) / 9) + 9] == 'P':
                    self.assertEqual(stim_circle.fillColor, exp_settings.asrt_pcolor)
                else:
                    self.assertEqual(stim_circle.fillColor, exp_settings.asrt_rcolor)

            # saving screen
            saving = drawing_list[28]
            self.assertTrue(isinstance(saving, pvm.TextStim))
            self.assertEqual(saving.text, "Adatok mentése és visszajelzés előkészítése...")

            # feedback screen
            feedback = drawing_list[29]
            self.assertTrue(isinstance(feedback, pvm.TextStim))
            self.assertEqual(feedback.text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                            "Pontosságod általában: 100,0 %\r\n"
                                            "Átlagos reakcióidőd: 0,0 másodperc\r\n"
                                            "Pontosságod a bejósolható elemeknél: 100,0 %\r\n"
                                            "Átlagos reakcióidőd a bejósolható elemeknél: 0,0 másodperc\r\n\r\n"
                                            "Legyél gyorsabb!\r\n\r\n\r\n\r\n")

            self.assertTrue(os.path.join(thispath, "settings", "toth-bela_10__log.txt"))

        self.clearDir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))

    def testQuitOnFeedbackScreen(self):
        visual_mock = pvm.PsychoPyVisualMock()
        # load settings
        dict_accents = {u'á':u'a',u'é':u'e',u'í':u'i',u'ó':u'o',u'ő':u'o',u'ö':u'o',u'ú':u'u',u'ű':u'u',u'ü':u'u'}
        settings_path = os.path.join(self.constructFilePath("testQuitOnFeedbackScreen"), "settings")
        exp_settings = asrt.ExperimentSettings(settings_path, "")
        asrt.all_settings_def(exp_settings, dict_accents)

        # load instructions
        inst_feedback_path = os.path.join(self.constructFilePath("testQuitOnFeedbackScreen"), "inst_and_feedback.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        # set user settings
        thispath = os.path.join(self.constructFilePath("testQuitOnFeedbackScreen"))
        asrt.ensure_dir(os.path.join(thispath, "settings"))
        asrt.ensure_dir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "logs"))

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])
        group, subject_nr, identif, person_data_handler, PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, last_N,  end_at, stim_colorN, stimpr = asrt.participant_id(thispath, exp_settings, dict_accents)


        # monitor settings
        my_monitor = asrt.monitor_settings(exp_settings)
        colors = { 'wincolor' : exp_settings.asrt_background, 'linecolor':'black', 'stimp':exp_settings.asrt_pcolor, 'stimr':exp_settings.asrt_rcolor}
        with visual.Window (size = my_monitor.getSizePix(), color = colors['wincolor'], fullscr = False, monitor = my_monitor, units = "cm") as mywindow:

            pressed_dict = {exp_settings.key1:1,exp_settings.key2:2,exp_settings.key3:3,exp_settings.key4:4}

            frame_time, frame_sd, frame_rate = 1.0, 0.12, 0.23 # use dummy values


            dict_pos = { 1:  ( float(exp_settings.asrt_distance)*(-1.5), 0),
                         2:  ( float(exp_settings.asrt_distance)*(-0.5), 0),
                         3:  ( float(exp_settings.asrt_distance)*  0.5,   0),
                         4:  ( float(exp_settings.asrt_distance)*  1.5,   0) }

            visual_mock = pvm.PsychoPyVisualMock()

            # generate the right keys
            key_list = []
            # There are some instructions first
            key_list = [exp_settings.key1, exp_settings.key1, exp_settings.key1]

            # Then we have the stimuli
            for stim in stimlist.values():
                if stim == 1:
                    key_list.append(exp_settings.key1)
                elif stim == 2:
                    key_list.append(exp_settings.key2)
                elif stim == 3:
                    key_list.append(exp_settings.key3)
                elif stim == 4:
                    key_list.append(exp_settings.key4)

            key_list.append(exp_settings.key_quit)
            visual_mock.setReturnKeyList(key_list)
            with self.assertRaises(SystemExit):
                last_N, stim_output_line = asrt.presentation(mywindow, exp_settings, instruction_helper, person_data_handler, colors, dict_pos, PCodes, pressed_dict,
                                                             last_N, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, end_at, stim_colorN,
                                                             group, identif, subject_nr, frame_rate, frame_time, frame_sd)

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 105)

            # first we have some instructions
            instruction_text = drawing_list[0]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nÜdvözlünk a feladatban!\r\n\r\n"
                                                "A képernyőn négy kör lesz, a kör egyika a többitől különböző színnel fog megjelenni.\r\n\r\n"
                                                "Az a feladatod, hogy az eltérő színű kör megjelenési helyének megfelelő gombot nyomd meg.\r\n\r\n"
                                                "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[1]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nA következő billenytűket kell használni: z, c, b, m\r\n\r\n"
                                                    "Minél pontosabban és gyorsabban kövesd le a megjelenő ingereket!\r\n\r\n"
                                                    "Ehhez mindkét kezedet használd, a középső és mutatóujjaidat.\r\n\r\n"
                                                    "Az eltérő színű kör egymás után többször ugyanazon a helyen is megjelenhet.\r\n\r\n"
                                                    "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")

            instruction_text = drawing_list[2]
            self.assertTrue(isinstance(instruction_text, pvm.TextStim))
            self.assertEqual(instruction_text.text, "\r\n\r\nKb. percenként fogsz visszajelzést kapni arról,\r\n"
                                                    "hogy mennyire voltál gyors és pontos - ez alapján tudsz módosítani.\r\n\r\n"
                                                    "A feladat indításához nyomd meg valamelyik válaszgombot!\r\n\r\n")

            # then we have 11 trials
            for j in range(3, 102, 9):
                # empty cycles
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + i]
                    self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # empty cycles again
                for i in range(0, 4):
                    stim_background_circle = drawing_list[j + 4 + i]
                    self.assertTrue(isinstance(stim_background_circle, pvm.Circle))
                    self.assertEqual(stim_background_circle.lineColor, 'black')
                    self.assertEqual(stim_background_circle.fillColor, None)

                # stimulus
                stim_circle = drawing_list[j + 8]
                self.assertTrue(isinstance(stim_circle, pvm.Circle))
                self.assertEqual(stim_circle.lineColor, 'black')
                if stimpr[((j - 3) / 9) + 1] == 'P':
                    self.assertEqual(stim_circle.fillColor, exp_settings.asrt_pcolor)
                else:
                    self.assertEqual(stim_circle.fillColor, exp_settings.asrt_rcolor)

            # saving screen
            saving = drawing_list[102]
            self.assertTrue(isinstance(saving, pvm.TextStim))
            self.assertEqual(saving.text, "Adatok mentése és visszajelzés előkészítése...")

            # feedback screen
            feedback = drawing_list[103]
            self.assertTrue(isinstance(feedback, pvm.TextStim))
            self.assertEqual(feedback.text, "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                            "Pontosságod általában: 100,0 %\r\n"
                                            "Átlagos reakcióidőd: 0,0 másodperc\r\n"
                                            "Pontosságod a bejósolható elemeknél: 100,0 %\r\n"
                                            "Átlagos reakcióidőd a bejósolható elemeknél: 0,0 másodperc\r\n\r\n"
                                            "Legyél gyorsabb!\r\n\r\n\r\n\r\n")
            # quit screen
            quit = drawing_list[104]
            self.assertTrue(isinstance(quit, pvm.TextStim))
            self.assertEqual(quit.text, "Quit...\nSaving data...")

            self.assertTrue(os.path.join(thispath, "settings", "toth-bela_10__log.txt"))

        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "logs"))

if __name__ == "__main__":
    unittest.main() # run all tests