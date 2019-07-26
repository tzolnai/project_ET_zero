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
from psychopy import visual

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
            
            self.assertTrue(os.path.join(thispath, "settings", "toth-bela_10__log.txt"))

        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "logs"))

if __name__ == "__main__":
    unittest.main() # run all tests