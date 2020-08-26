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
sys.path = [".."] + sys.path

import shelve
import codecs
import asrt
from io import StringIO
import tobii_research as tobii
from psychopy import visual, event

def get_system_time_stamp_mock():
    return 1000000

tobii.get_system_time_stamp = get_system_time_stamp_mock

def GetKeys(keyList=[], modifiers = False, timeStamped = False):
    global keys
    current_keys = keys[0]
    keys = keys[1:]
    return current_keys

keys = []
event.getKeys = GetKeys

def DummyConvert(pos):
    return pos

def convert(raw_file_name, new_file_name, experiment):

    with codecs.open(raw_file_name, 'r', encoding='utf-8') as raw_output_file:
        raw_lines = raw_output_file.readlines()

    new_file_data = StringIO()
    end_pos = raw_lines[0].find("trial_phase")
    new_file_data.write(raw_lines[0][:end_pos])
    new_file_data.write('RT (ms)')
    new_file_data.write('\n')

    trial_pos = raw_lines[0].split('\t').index("trial")
    block_pos = raw_lines[0].split('\t').index("block")
    trial_phase_pos = raw_lines[0].split('\t').index("trial_phase")
    time_stamp_pos = raw_lines[0].split('\t').index("gaze_data_time_stamp")
    stim_pos = raw_lines[0].split('\t').index("stimulus")
    left_gazeX_pos = raw_lines[0].split('\t').index("left_gaze_data_X_PCMCS")
    left_gazeY_pos = raw_lines[0].split('\t').index("left_gaze_data_Y_PCMCS")
    left_gaze_valid_pos = raw_lines[0].split('\t').index("left_gaze_validity")
    right_gazeX_pos = raw_lines[0].split('\t').index("right_gaze_data_X_PCMCS")
    right_gazeY_pos = raw_lines[0].split('\t').index("right_gaze_data_Y_PCMCS")
    right_gaze_valid_pos = raw_lines[0].split('\t').index("right_gaze_validity")

    last_trial = "1"
    start_time = 0
    end_time = 0
    start_time_found = False
    end_time_found = False
    current_line = 1
    fixation_found = False
    
    # load settings
    all_settings_file_path = os.path.join(experiment.workdir_path, "settings", "settings")
    reminder_file_path = os.path.join(experiment.workdir_path, "settings", "settings_reminder.txt")
    experiment.settings = asrt.ExperimentSettings(all_settings_file_path, reminder_file_path, experiment.project_ET_zero)
    experiment.all_settings_def()
    experiment.settings.dispersion_threshold = 3.0
    
    # find out the current subject
    experiment.person_data = asrt.PersonDataHandler("", "", "", "", "", "")

    # init eye data
    experiment.gaze_data_list.clear()
    experiment.current_sampling_window = experiment.settings.stim_fixation_threshold
    experiment.ADCS_to_PCMCS = DummyConvert
    experiment.distance_ADCS_to_PCMCS = DummyConvert
    
    # stim positions
    dict_pos = {1: (float(-7.5), float(-7.5)),
                2: (float(7.5), float(-7.5)),
                3: (float(-7.5), float(7.5)),
                4: (float(7.5), float(7.5))}
                
    ignore_trial = False
    
    for line in raw_lines[1:]:
    
        if ignore_trial:
            if last_trial == line.split('\t')[trial_pos]:
                if line_to_write.split('\t')[block_pos] != "0":
                    print("ignore line")
                continue
                current_line += 1
            else:
                if line_to_write.split('\t')[block_pos] != "0":
                    print("go to next trial")
                    print(line.split('\t')[trial_pos])
                last_trial = line.split('\t')[trial_pos]
                start_time_found = False
                end_time_found = False
                fixation_found = False
                ignore_trial = False
       
        current_stimulus = int(line.split('\t')[stim_pos])
        left_gaze_XY = (float(line.split('\t')[left_gazeX_pos].replace(',', '.')), float(line.split('\t')[left_gazeY_pos].replace(',', '.')))
        left_gaze_valid = bool(line.split('\t')[left_gaze_valid_pos])
        right_gaze_XY = (float(line.split('\t')[right_gazeX_pos].replace(',', '.')), float(line.split('\t')[right_gazeY_pos].replace(',', '.')))
        right_gaze_valid = bool(line.split('\t')[right_gaze_valid_pos])

        # call eye_data_callback
        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = left_gaze_XY
        gazeData['right_gaze_point_on_display_area'] = right_gaze_XY
        gazeData['left_gaze_point_validity'] = left_gaze_valid
        gazeData['right_gaze_point_validity'] = right_gaze_valid
        experiment.eye_data_callback(gazeData)

        # call fixation algorithm
        if line.split('\t')[trial_phase_pos] == "stimulus_on_screen":
            global keys
            keys = [[],['q']]
            response = experiment.wait_for_eye_response(dict_pos[current_stimulus], experiment.current_sampling_window)
            if experiment.main_loop_lock.locked():
                experiment.main_loop_lock.release()
            keys = []
            if response != -1:
                fixation_found = True
                print ("fixation_found")

        if last_trial != line.split('\t')[trial_pos] or line == raw_lines[len(raw_lines) - 1] or fixation_found:
            line_to_write = raw_lines[current_line - 1]
            end_pos = find_variable_str_index(line_to_write, trial_phase_pos)
            if line_to_write.split('\t')[block_pos] != "0":
                print("writedata")
                new_file_data.write(line_to_write[:end_pos])
                new_file_data.write('\t')

                if start_time_found and end_time_found:
                    new_file_data.write(str((end_time - start_time) / 1000.0).replace(".", ","))
                elif start_time_found:
                    end_time = int(line.split('\t')[time_stamp_pos])
                    new_file_data.write(str((end_time - start_time) / 1000.0).replace(".", ","))
                else:
                    new_file_data.write("0")
                new_file_data.write('\n')

            if last_trial == line.split('\t')[trial_pos]:
                if line_to_write.split('\t')[block_pos] != "0":
                    print("ignore_trial")
                    print(last_trial)
                    print(str((end_time - start_time) / 1000.0).replace(".", ","))
                ignore_trial = True

            last_trial = line.split('\t')[trial_pos]
            start_time_found = False
            end_time_found = False
            fixation_found = False

        if line.split('\t')[trial_phase_pos] == "stimulus_on_screen" and not start_time_found:
            start_time = int(line.split('\t')[time_stamp_pos])
            start_time_found = True

        if line.split('\t')[trial_phase_pos] == "after_reaction" and not end_time_found:
            end_time = int(line.split('\t')[time_stamp_pos])
            end_time_found = True
        current_line += 1

    with codecs.open(new_file_name, 'w', encoding='utf-8') as new_output_file:
        new_output_file.write(new_file_data.getvalue())
    new_file_data.close()


def find_variable_str_index(string, variable_pos):
    begin_index = 0
    for i in range(variable_pos - 1):
        begin_index = string.find("\t", begin_index) + 1
    return string.find("\t", begin_index)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("You need to specify the path of an output txt file.")
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print("The passed parameter should be a valid file's path: " + sys.argv[1])
        exit(1)

    thispath = os.path.split(os.path.abspath(__file__))[0]
    thispath = os.path.split(thispath)[0]
    experiment = asrt.Experiment(thispath, True)
    convert(sys.argv[1], sys.argv[2], experiment)
