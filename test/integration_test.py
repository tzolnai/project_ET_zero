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
from psychopy import visual, logging, core

# ignore warnings comming from psychopy
logging.console.setLevel(logging.ERROR)

def DummyFunction(*argv):
    pass

core.wait = DummyFunction

class integrationTest(unittest.TestCase):

    def setUp(self):
        # Init work directories
        filepath = os.path.abspath(__file__)
        (filepath, trail) = os.path.split(filepath)
        test_name = self.id().split(".")[2]
        self.current_dir = os.path.join(filepath, "data", "integration", test_name)
        self.work_dir = os.path.join(self.current_dir, "workdir")
        asrt.ensure_dir(self.work_dir)
        self.clearDir(self.work_dir)
        self.copyFilesToWorkdir()

        # override this method to get the stimlist to be able to generate the keylist
        self.calculate_stim_properties = asrt.calculate_stim_properties
        asrt.calculate_stim_properties = self.calculate_stim_properties_override
        self.frame_check = asrt.frame_check
        asrt.frame_check = self.frame_check_override

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

        dict_accents = {u'á':u'a',u'é':u'e',u'í':u'i',u'ó':u'o',u'ő':u'o',u'ö':u'o',u'ú':u'u',u'ű':u'u',u'ü':u'u'}
        settings_path = os.path.join(self.work_dir, "settings", "settings")
        self.exp_settings = asrt.ExperimentSettings(settings_path, "")
        asrt.all_settings_def(self.exp_settings, dict_accents)

    def tearDown(self):
        self.clearDir(self.work_dir)        
        
        asrt.calculate_stim_properties = self.calculate_stim_properties
        asrt.frame_check = self.frame_check        
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
                        shutil.copyfile(sub_file_path, os.path.join(self.work_dir, "settings", sub_file))
                    else:
                        shutil.copyfile(sub_file_path, os.path.join(self.work_dir, "logs", sub_file))

    def clearDir(self, dir_path):
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def calculate_stim_properties_override(self, stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, experiment_settings):
        self.calculate_stim_properties(stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, experiment_settings)
        self.stimtrial = stimtrial

        # There are some instructions first
        self.key_list = [self.exp_settings.key1, self.exp_settings.key1, self.exp_settings.key1]

        # Then we have the stimuli
        trial = 1
        for stim in stimlist.values():
            if stim == 1:
                self.key_list.append(self.exp_settings.key1)
            elif stim == 2:
                self.key_list.append(self.exp_settings.key2)
            elif stim == 3:
                self.key_list.append(self.exp_settings.key3)
            elif stim == 4:
                self.key_list.append(self.exp_settings.key4)

            trial += 1

            # feedback at the end of the block
            if trial in experiment_settings.get_block_starts():
                    self.key_list.append(self.exp_settings.key1)

            if trial == end_at[trial - 1]:
                # ending screen
                self.key_list.append(self.exp_settings.key1)
                # next session's instructions
                self.key_list.append(self.exp_settings.key1)
                self.key_list.append(self.exp_settings.key1)
                self.key_list.append(self.exp_settings.key1)

        self.visual_mock.setReturnKeyList(self.key_list)

    def frame_check_override(self, mywindow):
        return 0.0, 0.0, 60.0

    def checkOutputFile(self):
        reference_file_path = os.path.join(self.current_dir, "reference", "toth-bela_10__log.txt")
        workdir_output = os.path.join(self.work_dir, "logs", "toth-bela_10__log.txt")

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
                        self.assertEqual(ref_line, output_line) # first line is equal (headers)
                        continue

                    self.assertEqual(ref_values[0], act_values[0]) # computer name
                    self.assertEqual(ref_values[1], act_values[1]) # group
                    self.assertEqual(ref_values[2], act_values[2]) # subject name
                    self.assertEqual(ref_values[3], act_values[3]) # subject number
                    self.assertEqual(ref_values[4], act_values[4]) # asrt type
                    self.assertEqual(ref_values[5], act_values[5]) # pcode
                    self.assertEqual(ref_values[6], act_values[6]) # output_line
                    self.assertEqual(ref_values[7], act_values[7]) # session
                    self.assertEqual(ref_values[8], act_values[8]) # epoch
                    self.assertEqual(ref_values[9], act_values[9]) # block
                    self.assertEqual(ref_values[10], act_values[10]) # trial
                    # RSI time
                    self.assertEqual(ref_values[12], act_values[12]) # frame_rate
                    self.assertEqual(ref_values[13], act_values[13]) # frame_time
                    self.assertEqual(ref_values[14], act_values[14]) # frame_sd
                    # date
                    # time
                    self.assertEqual(ref_values[17], act_values[17]) # stimulus color
                    self.assertEqual(ref_values[18], act_values[18]) # PR
                    self.assertEqual(ref_values[19], act_values[19]) # RT
                    self.assertEqual(ref_values[20], act_values[20]) # error
                    # stimulus
                    # stimbutton
                    self.assertEqual(ref_values[23], act_values[23]) # quitlog

    def testSimpleTestCase(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        asrt.main(self.work_dir)

        self.checkOutputFile()

    def calculate_stim_properties_override_quit(self, stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, experiment_settings):
        self.calculate_stim_properties_override(stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, experiment_settings)
        self.key_list[10] = self.exp_settings.key_quit
        self.visual_mock.setReturnKeyList(self.key_list)

    def testQuitInsideABlock(self):
        asrt.calculate_stim_properties = self.calculate_stim_properties_override_quit

        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        with self.assertRaises(SystemExit):
            asrt.main(self.work_dir)

        self.checkOutputFile()

    def testExplicitASRT(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        asrt.main(self.work_dir)

        self.checkOutputFile()

    def calculate_stim_properties_override_wrong_button(self, stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, experiment_settings):
        self.calculate_stim_properties_override(stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, experiment_settings)
        self.key_list = self.key_list[0:10] + [self.key_list[8]] + self.key_list[10:]
        self.visual_mock.setReturnKeyList(self.key_list)

    def testWrongPressedButton(self):
        asrt.calculate_stim_properties = self.calculate_stim_properties_override_wrong_button

        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        asrt.main(self.work_dir)

        self.checkOutputFile()

    def testMoreBlocks(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        asrt.main(self.work_dir)

        self.checkOutputFile()

    def testMoreSessions(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324', '3rd - 1324', '3rd - 1324'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        asrt.main(self.work_dir)

        self.checkOutputFile()

    def presentation_override(self, mywindow, exp_settings, instruction_helper, person_data_handler, colors, dict_pos, PCodes, pressed_dict,
                              last_N, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, end_at, stim_colorN,
                              group, identif, subject_nr, frame_rate, frame_time, frame_sd):

        # There are some instructions first
        self.key_list = [self.exp_settings.key1, self.exp_settings.key1, self.exp_settings.key1]

        # Then we have the stimuli
        trial = 1
        for stim in stimlist.values():
            # ignore first sessions' trials
            if trial > (exp_settings.blockprepN + exp_settings.blocklengthN) * exp_settings.epochs[0] * exp_settings.block_in_epochN:
                if stim == 1:
                    self.key_list.append(self.exp_settings.key1)
                elif stim == 2:
                    self.key_list.append(self.exp_settings.key2)
                elif stim == 3:
                    self.key_list.append(self.exp_settings.key3)
                elif stim == 4:
                    self.key_list.append(self.exp_settings.key4)

            trial += 1

            if trial - 1 > (exp_settings.blockprepN + exp_settings.blocklengthN) * exp_settings.epochs[0] * exp_settings.block_in_epochN:
                # feedback at the end of the block
                if trial in exp_settings.get_block_starts():
                        self.key_list.append(self.exp_settings.key1)

        # ending screen
        self.key_list += [self.exp_settings.key1]
        self.visual_mock.setReturnKeyList(self.key_list)
        return self.presentation(mywindow, exp_settings, instruction_helper, person_data_handler, colors, dict_pos, PCodes, pressed_dict,
                                 last_N, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, end_at, stim_colorN,
                                 group, identif, subject_nr, frame_rate, frame_time, frame_sd)

    def testContinueWithSecondSession(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10])

        # override this method to get the stimlist to be able to generate the keylist
        self.presentation = asrt.presentation
        asrt.presentation = self.presentation_override

        self.visual_mock = pvm.PsychoPyVisualMock()

        asrt.main(self.work_dir)

        self.checkOutputFile()
        
        asrt.presentation = self.presentation

    def presentation_override_unexpected_quit(self, mywindow, exp_settings, instruction_helper, person_data_handler, colors, dict_pos, PCodes, pressed_dict,
                              last_N, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, end_at, stim_colorN,
                              group, identif, subject_nr, frame_rate, frame_time, frame_sd):

        # There is one screen about the continuation
        self.key_list = [self.exp_settings.key1]

        # Then we have the stimuli
        trial = 1
        for stim in stimlist.values():
            # ignore first sessions' trials
            if trial > last_N:
                if stim == 1:
                    self.key_list.append(self.exp_settings.key1)
                elif stim == 2:
                    self.key_list.append(self.exp_settings.key2)
                elif stim == 3:
                    self.key_list.append(self.exp_settings.key3)
                elif stim == 4:
                    self.key_list.append(self.exp_settings.key4)

            trial += 1

            if trial - 1 > last_N:
                # feedback at the end of the block
                if trial in exp_settings.get_block_starts():
                        self.key_list.append(self.exp_settings.key1)

        # ending screen
        self.key_list += [self.exp_settings.key1]
        self.visual_mock.setReturnKeyList(self.key_list)
        return self.presentation(mywindow, exp_settings, instruction_helper, person_data_handler, colors, dict_pos, PCodes, pressed_dict,
                                 last_N, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, end_at, stim_colorN,
                                 group, identif, subject_nr, frame_rate, frame_time, frame_sd)

    def testContinueAfterUnexpectedQuit(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10])

        # override this method to get the stimlist to be able to generate the keylist
        self.presentation = asrt.presentation
        asrt.presentation = self.presentation_override_unexpected_quit

        self.visual_mock = pvm.PsychoPyVisualMock()

        asrt.main(self.work_dir)

        self.checkOutputFile()
        
        asrt.presentation = self.presentation

    def testMoreSessionsSubsequently(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324', '5th - 1423', 'noPattern', '1st - 1234', 'Tóth Béla', 10, 'Tóth Béla', 10, 'Tóth Béla', 10])

        self.visual_mock = pvm.PsychoPyVisualMock()

        for i in range(1,5):
            asrt.main(self.work_dir)

        self.checkOutputFile()


if __name__ == "__main__":
    unittest.main() # run all tests