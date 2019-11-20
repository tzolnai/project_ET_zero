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
        self.experiment = asrt.Experiment(self.work_dir)
        self.calculate_stim_properties = self.experiment.calculate_stim_properties
        self.experiment.calculate_stim_properties = self.calculate_stim_properties_override
        self.frame_check = self.experiment.frame_check
        self.experiment.frame_check = self.frame_check_override

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

        # Change this variable to update all reference file
        self.update_references = False

    def tearDown(self):
        if self.update_references:
            reference_file_path = os.path.join(
                self.current_dir, "reference", "toth-bela_10__log.txt")
            workdir_output = os.path.join(
                self.work_dir, "logs", "toth-bela_10__log.txt")
            shutil.copyfile(workdir_output, reference_file_path)

        self.clearDir(self.work_dir)

        self.experiment.calculate_stim_properties = self.calculate_stim_properties
        self.experiment.frame_check = self.frame_check
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

    def calculate_stim_properties_override(self):
        self.calculate_stim_properties()
        # There are some instructions first
        self.key_list = [self.experiment.settings.key1,
                         self.experiment.settings.key1, self.experiment.settings.key1]

        # Then we have the stimuli
        trial = 1
        for stim in self.experiment.stimlist.values():
            if stim == 1:
                self.key_list.append(self.experiment.settings.key1)
            elif stim == 2:
                self.key_list.append(self.experiment.settings.key2)
            elif stim == 3:
                self.key_list.append(self.experiment.settings.key3)
            elif stim == 4:
                self.key_list.append(self.experiment.settings.key4)

            trial += 1

            # feedback at the end of the block
            if trial in self.experiment.settings.get_block_starts():
                self.key_list.append(self.experiment.settings.key1)

            if trial == self.experiment.end_at[trial - 1]:
                # ending screen
                self.key_list.append(self.experiment.settings.key1)
                # next session's instructions
                self.key_list.append(self.experiment.settings.key1)
                self.key_list.append(self.experiment.settings.key1)
                self.key_list.append(self.experiment.settings.key1)

        self.visual_mock.setReturnKeyList(self.key_list)

    def frame_check_override(self):
        self.experiment.frame_time = 0.0
        self.experiment.frame_sd = 0.0
        self.experiment.frame_rate = 60.0

    def checkOutputFile(self, check_timing=False, RSI_delta=0.002):
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
                    self.assertEqual(ref_values[1], act_values[1])  # group
                    self.assertEqual(ref_values[2], act_values[2])  # subject name
                    self.assertEqual(ref_values[3], act_values[3])  # subject number
                    self.assertEqual(ref_values[4], act_values[4])  # subject sex
                    self.assertEqual(ref_values[5], act_values[5])  # subject age
                    self.assertEqual(ref_values[6], act_values[6])  # asrt type
                    self.assertEqual(ref_values[7], act_values[7])  # pcode
                    self.assertEqual(ref_values[8], act_values[8])  # output_line
                    self.assertEqual(ref_values[9], act_values[9])  # session
                    self.assertEqual(ref_values[10], act_values[10])  # epoch
                    self.assertEqual(ref_values[11], act_values[11])  # block
                    self.assertEqual(ref_values[12], act_values[12])  # trial
                    if check_timing:
                        # RSI time, keep this low so the program will be precise inside a trial
                        self.assertAlmostEqual(
                            float(ref_values[13].replace(",", ".")),
                            float(act_values[13].replace(",", ".")), delta=RSI_delta)
                    self.assertEqual(ref_values[14], act_values[14])  # frame_rate
                    self.assertEqual(ref_values[15], act_values[15])  # frame_time
                    self.assertEqual(ref_values[16], act_values[16])  # frame_sd
                    # date
                    # time
                    self.assertEqual(ref_values[19], act_values[19])  # stimulus color
                    self.assertEqual(ref_values[20], act_values[20])  # PR
                    # triplet_type_hl
                    if ref_values[21] == "none" or ref_values[20] == "pattern":
                        self.assertEqual(ref_values[21], act_values[21])
                    self.assertEqual(ref_values[22], act_values[22])  # RT
                    self.assertEqual(ref_values[23], act_values[23])  # error
                    # stimulus
                    # response
                    self.assertEqual(ref_values[26], act_values[26])  # quitlog

    def testSimpleTestCase(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, 'férfi', 25, '3rd'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        self.experiment.run(window_gammaErrorPolicy='ignore')

        self.checkOutputFile(True)

    def calculate_stim_properties_override_quit(self):
        self.calculate_stim_properties_override()
        self.key_list[10] = self.experiment.settings.key_quit
        self.visual_mock.setReturnKeyList(self.key_list)

    def testQuitInsideABlock(self):
        self.experiment.calculate_stim_properties = self.calculate_stim_properties_override_quit

        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, 'férfi', 25, '3rd'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        with self.assertRaises(SystemExit):
            self.experiment.run(window_gammaErrorPolicy='ignore')

        self.checkOutputFile(True)

    def testExplicitASRT(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, 'férfi', 25, '3rd'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        self.experiment.run(window_gammaErrorPolicy='ignore')

        self.checkOutputFile()

    def calculate_stim_properties_override_wrong_button(self):
        self.calculate_stim_properties_override()
        self.key_list = self.key_list[0:10] + \
            [self.key_list[8]] + self.key_list[10:]
        self.visual_mock.setReturnKeyList(self.key_list)

    def testWrongPressedButton(self):
        self.experiment.calculate_stim_properties = self.calculate_stim_properties_override_wrong_button

        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, 'férfi', 25, '3rd'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        self.experiment.run(window_gammaErrorPolicy='ignore')

        self.checkOutputFile(True)

    def testMoreBlocks(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, 'férfi', 25, '3rd'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        self.experiment.run(window_gammaErrorPolicy='ignore')

        self.checkOutputFile(True, 0.01)

    def testMoreSessions(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(
            ['Tóth Béla', 10, 'férfi', 25, '3rd', '3rd', '3rd'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        self.experiment.run(window_gammaErrorPolicy='ignore')

        self.checkOutputFile(True)

    def presentation_override(self):
        # There are some instructions first
        self.key_list = [self.experiment.settings.key1,
                         self.experiment.settings.key1, self.experiment.settings.key1]

        # Then we have the stimuli
        trial = 1
        for stim in self.experiment.stimlist.values():
            # ignore first sessions' trials
            if trial > (self.experiment.settings.blockprepN + self.experiment.settings.blocklengthN) * self.experiment.settings.epochs[0] * self.experiment.settings.block_in_epochN:
                if stim == 1:
                    self.key_list.append(self.experiment.settings.key1)
                elif stim == 2:
                    self.key_list.append(self.experiment.settings.key2)
                elif stim == 3:
                    self.key_list.append(self.experiment.settings.key3)
                elif stim == 4:
                    self.key_list.append(self.experiment.settings.key4)

            trial += 1

            if trial - 1 > (self.experiment.settings.blockprepN + self.experiment.settings.blocklengthN) * self.experiment.settings.epochs[0] * self.experiment.settings.block_in_epochN:
                # feedback at the end of the block
                if trial in self.experiment.settings.get_block_starts():
                    self.key_list.append(self.experiment.settings.key1)

        # ending screen
        self.key_list += [self.experiment.settings.key1]
        self.visual_mock.setReturnKeyList(self.key_list)
        return self.presentation()

    def presentation_override_unexpected_quit_quit(self):
        # There are some instructions first
        self.key_list = [self.experiment.settings.key1,
                         self.experiment.settings.key1,
                         self.experiment.settings.key1]

        # Then we have the stimuli
        trial = 1
        for stim in self.experiment.stimlist.values():
            if trial > self.experiment.settings.get_maxtrial() / 2:
                self.key_list.append(self.experiment.settings.key_quit)
            # ignore first sessions' trials
            elif trial > self.experiment.last_N:
                if stim == 1:
                    self.key_list.append(self.experiment.settings.key1)
                elif stim == 2:
                    self.key_list.append(self.experiment.settings.key2)
                elif stim == 3:
                    self.key_list.append(self.experiment.settings.key3)
                elif stim == 4:
                    self.key_list.append(self.experiment.settings.key4)

            trial += 1

            if trial - 1 > self.experiment.last_N:
                # feedback at the end of the block
                if trial in self.experiment.settings.get_block_starts():
                    self.key_list.append(self.experiment.settings.key1)

        # ending screen
        self.key_list += [self.experiment.settings.key1]
        self.visual_mock.setReturnKeyList(self.key_list)
        return self.presentation()

    def presentation_override_unexpected_quit_continue(self):
        # There is one screen about the continuation
        self.key_list = [self.experiment.settings.key1]

        # Then we have the stimuli
        trial = 1
        for stim in self.experiment.stimlist.values():
            # ignore first sessions' trials
            if trial > self.experiment.last_N:
                if stim == 1:
                    self.key_list.append(self.experiment.settings.key1)
                elif stim == 2:
                    self.key_list.append(self.experiment.settings.key2)
                elif stim == 3:
                    self.key_list.append(self.experiment.settings.key3)
                elif stim == 4:
                    self.key_list.append(self.experiment.settings.key4)

            trial += 1

            if trial - 1 > self.experiment.last_N:
                # feedback at the end of the block
                if trial in self.experiment.settings.get_block_starts():
                    self.key_list.append(self.experiment.settings.key1)

        # ending screen
        self.key_list += [self.experiment.settings.key1]
        self.visual_mock.setReturnKeyList(self.key_list)
        return self.presentation()

    def testContinueAfterUnexpectedQuit(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, 'férfi', 25, '3rd', 'Tóth Béla', 10])

        # override this method to get the stimlist to be able to generate the keylist
        self.presentation = self.experiment.presentation
        self.experiment.presentation = self.presentation_override_unexpected_quit_quit

        self.visual_mock = pvm.PsychoPyVisualMock()

        with self.assertRaises(SystemExit):
            self.experiment.run(window_gammaErrorPolicy='ignore')

        self.experiment.presentation = self.presentation_override_unexpected_quit_continue

        self.experiment.run(window_gammaErrorPolicy='ignore')

        self.checkOutputFile(True)

        self.experiment.presentation = self.presentation

    def presentation_override_unexpected_quit_at_blockend(self):
        # There are some instructions first
        self.key_list = [self.experiment.settings.key1,
                         self.experiment.settings.key1,
                         self.experiment.settings.key1]

        # Then we have the stimuli
        trial = 1
        for stim in self.experiment.stimlist.values():
            # ignore first sessions' trials
            if trial > self.experiment.last_N:
                if stim == 1:
                    self.key_list.append(self.experiment.settings.key1)
                elif stim == 2:
                    self.key_list.append(self.experiment.settings.key2)
                elif stim == 3:
                    self.key_list.append(self.experiment.settings.key3)
                elif stim == 4:
                    self.key_list.append(self.experiment.settings.key4)

            trial += 1

            if trial - 1 > self.experiment.last_N:
                # feedback at the end of the block
                if trial in self.experiment.settings.get_block_starts():
                    if trial > self.experiment.settings.get_maxtrial() / 2:
                        self.key_list.append(self.experiment.settings.key_quit)
                    else:
                        self.key_list.append(self.experiment.settings.key1)

        # ending screen
        self.key_list += [self.experiment.settings.key1]
        self.visual_mock.setReturnKeyList(self.key_list)
        return self.presentation()

    def testContinueAfterQuitAtBlockEnd(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, 'férfi', 25, '5th', '3rd', 'Tóth Béla', 10])

        # override this method to get the stimlist to be able to generate the keylist
        self.presentation = self.experiment.presentation
        self.experiment.presentation = self.presentation_override_unexpected_quit_at_blockend

        self.visual_mock = pvm.PsychoPyVisualMock()

        with self.assertRaises(SystemExit):
            self.experiment.run(window_gammaErrorPolicy='ignore')

        self.experiment.presentation = self.presentation_override_unexpected_quit_continue

        self.experiment.run(window_gammaErrorPolicy='ignore')

        self.checkOutputFile()

        self.experiment.presentation = self.presentation

    def testMoreSessionsSubsequently(self):
        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, 'férfi', 25, '3rd', '5th', 'noPattern',
                                 '1st', 'Tóth Béla', 10, 'Tóth Béla', 10,
                                 'Tóth Béla', 10])

        self.visual_mock = pvm.PsychoPyVisualMock()

        for i in range(1, 5):
            self.experiment.run(window_gammaErrorPolicy='ignore')

        self.checkOutputFile()

    def testRSIInterval(self):
        # reset StaticPeriod
        core.StaticPeriod = self.StaticPeriod
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, 'férfi', 25, '3rd'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        self.experiment.run(window_gammaErrorPolicy='ignore')

        self.checkOutputFile(True, 0.03)

    def calculate_stim_properties_override_RT(self):
        self.calculate_stim_properties_override()
        self.key_list = self.key_list[0:10] + \
            [self.key_list[8]] + self.key_list[10:]

        # add time stamps to the reactions
        for i in range(0, len(self.key_list)):
            self.key_list[i] = (self.key_list[i], ((i % 5) * 100) + 200)

        self.visual_mock.setReturnKeyList(self.key_list)

    def testRT(self):
        self.experiment.calculate_stim_properties = self.calculate_stim_properties_override_RT

        # for setting participant data
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, 'férfi', 25, '3rd'])

        self.visual_mock = pvm.PsychoPyVisualMock()

        self.experiment.run(window_gammaErrorPolicy='ignore')

        self.checkOutputFile(True)


if __name__ == "__main__":
    unittest.main()  # run all tests
