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

# asrt.py version: 0.0.1

import sys
import os
# Add the local path to the main script and external scripts so we can import them.
sys.path = [".."] + sys.path

import shelve
import codecs
from psychopy import visual, core
import asrt
import platform


class EyeTrackingReplay():

    def run(self, file_name, settings_file):
        with codecs.open(file_name, 'r', encoding='utf-8') as output_file:
            output_lines = output_file.readlines()

        experiment = asrt.Experiment('')
        experiment.settings = asrt.ExperimentSettings(settings_file, "")
        experiment.all_settings_def()

        experiment.monitor_settings()
        experiment.dict_pos = {1: (float(experiment.settings.asrt_distance) * (-0.5), float(experiment.settings.asrt_distance) * (-0.5)),
                               2: (float(experiment.settings.asrt_distance) * 0.5, float(experiment.settings.asrt_distance) * (-0.5)),
                               3: (float(experiment.settings.asrt_distance) * (-0.5), float(experiment.settings.asrt_distance) * 0.5),
                               4: (float(experiment.settings.asrt_distance) * 0.5, float(experiment.settings.asrt_distance) * 0.5)}
        experiment.colors = {'wincolor': 'White', 'linecolor': 'black',
                             'stimp': experiment.settings.asrt_pcolor, 'stimr': experiment.settings.asrt_rcolor}
        if platform.system() == "Linux":
            win_type = 'pygame'
        else:
            win_type = 'pyglet'
        with visual.Window(size=experiment.mymonitor.getSizePix(), color=experiment.colors['wincolor'], fullscr=False, monitor=experiment.mymonitor, units="cm", winType=win_type) as experiment.mywindow:

            stimP = visual.Circle(win=experiment.mywindow, radius=experiment.settings.asrt_size, units="cm",
                                  fillColor=experiment.colors['stimp'], lineColor=experiment.colors['linecolor'], pos=experiment.dict_pos[1])
            stimR = visual.Circle(win=experiment.mywindow, radius=experiment.settings.asrt_size, units="cm",
                                  fillColor=experiment.colors['stimr'], lineColor=experiment.colors['linecolor'], pos=experiment.dict_pos[1])
            stimbg = visual.Circle(win=experiment.mywindow, radius=experiment.settings.asrt_size, units="cm",
                                   fillColor=None, lineColor=experiment.colors['linecolor'])
            eye_pos = visual.Circle(win=experiment.mywindow, radius=experiment.settings.asrt_size / 2.0, units="cm",
                                    fillColor='Red', lineColor='Red')
            AOI_rect = visual.Rect(win=experiment.mywindow, width=experiment.settings.AOI_size, height=experiment.settings.AOI_size, units="cm",
                                   fillColor=None, lineColor='Red', lineWidth=2.0)

            last_trial = -1
            last_trial_phase = 'before_stimulus'
            sampling_counter = 0
            block_displayed = False
            for line in output_lines[1:]:

                trial_pos = output_lines[0].split('\t').index("trial")
                pattern_random_pos = output_lines[0].split('\t').index("pattern_or_random")
                asrt_type_pos = output_lines[0].split('\t').index("asrt_type")
                stimulus_pos = output_lines[0].split('\t').index("stimulus")
                block_pos = output_lines[0].split('\t').index("block")
                RSI_pos = output_lines[0].split('\t').index("RSI_time")
                trial_phase_pos = output_lines[0].split('\t').index("trial_phase")

                current_trial = line.split('\t')[trial_pos]
                current_pattern_random = line.split('\t')[pattern_random_pos]
                asrt_type = line.split('\t')[asrt_type_pos]
                current_stimulus = int(line.split('\t')[stimulus_pos])
                trial_phase = line.split('\t')[trial_phase_pos]
                block_number = line.split('\t')[block_pos]
                RSI_time = line.split('\t')[RSI_pos]

                if current_trial == '1' and trial_phase == 'before_stimulus':
                    if not block_displayed:
                        text_stim = visual.TextStim(experiment.mywindow, text=block_number + ". blokk kezdete...",
                                                    units='cm', height=1.0, wrapWidth=20, color='black')
                        text_stim.draw()
                        experiment.mywindow.flip()
                        core.wait(1.5)
                        block_displayed = True
                    last_trial = current_trial
                    continue

                block_displayed = False
                if sampling_counter > 4:
                    sampling_counter = 0
                    left_gaze_XY = (float(line.split('\t')[23].replace(',', '.')), float(line.split('\t')[24].replace(',', '.')))
                    left_gaze_valid = bool(line.split('\t')[32])
                    right_gaze_XY = (float(line.split('\t')[25].replace(',', '.')), float(line.split('\t')[26].replace(',', '.')))
                    right_gaze_valid = bool(line.split('\t')[33])
                    x_coord = None
                    y_coord = None
                    if left_gaze_valid and right_gaze_valid:
                        x_coord = (left_gaze_XY[0] + right_gaze_XY[0]) / 2
                        y_coord = (left_gaze_XY[1] + right_gaze_XY[1]) / 2
                    elif left_gaze_valid:
                        x_coord = left_gaze_XY[0]
                        y_coord = left_gaze_XY[1]
                    elif right_gaze_valid:
                        x_coord = right_gaze_XY[0]
                        y_coord = right_gaze_XY[1]

                    eye_pos.setPos(experiment.ADCS_to_PCMCS((x_coord, y_coord)))
                    eye_pos.draw()
                    eye_pos_drawn = True

                if current_trial != last_trial or last_trial_phase != trial_phase or eye_pos_drawn:
                    experiment.stim_bg(stimbg)
                    experiment.stim_bg(AOI_rect)

                    if trial_phase != 'before_stimulus':
                        if current_pattern_random == 'pattern':
                            if asrt_type == 'explicit':
                                stimP.fillColor = experiment.colors['stimp']
                            else:
                                stimP.fillColor = experiment.colors['stimr']
                            stimP.setPos(experiment.dict_pos[current_stimulus])
                        else:
                            stimR.setPos(experiment.dict_pos[current_stimulus])
                        if current_pattern_random == 'pattern':
                            stimP.draw()
                        else:
                            stimR.draw()
                    text_stim = visual.TextStim(experiment.mywindow, text=current_trial + ". trial",
                                                units='cm', height=0.8, wrapWidth=20, color='black', pos=(0.0, 12.0))
                    text_stim.draw()
                    experiment.mywindow.flip()

                core.wait(0.008)
                last_trial = current_trial
                last_trial_phase = trial_phase
                sampling_counter += 1
                eye_pos_drawn = False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("You need to specify the path of an output txt file and the path of the settings.dat file.")
        core.quit()

    if not os.path.isfile(sys.argv[1]):
        print("The first parameter should be a valid file's path: " + sys.argv[1])
        core.quit()

    if not os.path.isfile(sys.argv[2]):
        print("The second parameter should be a valid file's path: " + sys.argv[2])
        core.quit()

    settings_file = sys.argv[2]
    if settings_file.endswith('.dat'):
        settings_file = settings_file[:-4]

    replay = EyeTrackingReplay()
    replay.run(sys.argv[1], settings_file)
