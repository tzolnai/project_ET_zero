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
import platform

try:
    import tobii_research as tobii
    g_tobii_available = True

    class EyeTrackerMock:
        def subscribe_to(self, subscription_type, callback, as_dictionary=False):
            global gaze_data_callback
            gaze_data_callback = callback

        def unsubscribe_from(self, subscription_type, callback=None):
            global gaze_data_callback
            gaze_data_callback = None

    def get_system_time_stamp_mock():
        return 1000000

    tobii.get_system_time_stamp = get_system_time_stamp_mock
except:
    g_tobii_available = False


def DummyFunction(*argv):
    pass


core.wait = DummyFunction

random_generator_g = 1


def choice_mock(list):
    global random_generator_g
    if random_generator_g == 1:
        random_generator_g = 2
    elif random_generator_g == 2:
        random_generator_g = 3
    elif random_generator_g == 3:
        random_generator_g = 4
    else:
        random_generator_g = 1
    return list[random_generator_g - 1]


# ignore warnings comming from psychopy
logging.console.setLevel(logging.ERROR)


@pytest.mark.skipif(not asrt.g_tobii_available, reason="Can't run without tobii package")
class jacobiPresentationTest(unittest.TestCase):

    def setUp(self):
        # Init work directory
        filepath = os.path.abspath(__file__)
        (filepath, trail) = os.path.split(filepath)
        test_name = self.id().split(".")[2]
        self.current_dir = os.path.join(filepath, "data", "jacobi_presentation", test_name)
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
        filepath = os.path.join(filepath, "data", "jacobi_presentation", file_name, "workdir")
        return filepath

    def wait_for_eye_response_override(self, expected_eye_pos_list, sampling_window):
        gazeData = {}
        if len(expected_eye_pos_list) > 1:
            expected_eye_pos = choice_mock(expected_eye_pos_list)
        else:
            expected_eye_pos = expected_eye_pos_list[0]

        gazeData['left_gaze_point_on_display_area'] = self.PCMCS_to_ADCS(expected_eye_pos)
        gazeData['right_gaze_point_on_display_area'] = self.PCMCS_to_ADCS(expected_eye_pos)

        gazeData['left_gaze_origin_in_user_coordinate_system'] = (10, 10, 10)
        gazeData['right_gaze_origin_in_user_coordinate_system'] = (10, 10, 10)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = 1
        gazeData['right_pupil_validity'] = 1

        for i in range(sampling_window):
            self.experiment.eye_data_callback_jacobi(gazeData)

        return self.experiment.wait_for_eye_response_original(expected_eye_pos_list, sampling_window)

    def wait_for_leave_pos_override(self, expected_eye_pos, sampling_window):
        gazeData = {}
        new_expected_eye_pos = (expected_eye_pos[0] + 4.0, expected_eye_pos[1] + 4.0)
        gazeData['left_gaze_point_on_display_area'] = self.PCMCS_to_ADCS(new_expected_eye_pos)
        gazeData['right_gaze_point_on_display_area'] = self.PCMCS_to_ADCS(new_expected_eye_pos)
        gazeData['left_gaze_origin_in_user_coordinate_system'] = (10, 10, 10)
        gazeData['right_gaze_origin_in_user_coordinate_system'] = (10, 10, 10)
        gazeData['left_gaze_point_validity'] = 1
        gazeData['right_gaze_point_validity'] = 1
        gazeData['left_pupil_diameter'] = 3
        gazeData['right_pupil_diameter'] = 3
        gazeData['left_pupil_validity'] = 1
        gazeData['right_pupil_validity'] = 1

        for i in range(sampling_window):
            self.experiment.eye_data_callback_jacobi(gazeData)

        return self.experiment.wait_for_leave_pos_original(expected_eye_pos, sampling_window)

    def PCMCS_to_ADCS(self, pos_PCMCS):
        aspect_ratio = self.experiment.mymonitor.getSizePix()[1] / self.experiment.mymonitor.getSizePix()[0]
        monitor_width_cm = self.experiment.settings.monitor_width
        monitor_height_cm = monitor_width_cm * aspect_ratio

        # shift origin
        shift_x = monitor_width_cm / 2
        shift_y = monitor_height_cm / 2

        # scale coordinates and mirror the y coordinates
        pos_ADCS = ((pos_PCMCS[0] + shift_x) / monitor_width_cm,
                    ((pos_PCMCS[1] * -1) + shift_y) / monitor_height_cm)

        return pos_ADCS

    def testRunJacobiTest(self):
        visual_mock = pvm.PsychoPyVisualMock()
        thispath = os.path.join(self.constructFilePath("testRunJacobiTest"))
        self.experiment = asrt.Experiment(thispath)

        self.experiment.wait_for_eye_response_original = self.experiment.wait_for_eye_response
        self.experiment.wait_for_eye_response = self.wait_for_eye_response_override

        self.experiment.wait_for_leave_pos_original = self.experiment.wait_for_leave_pos
        self.experiment.wait_for_leave_pos = self.wait_for_leave_pos_override

        # load settings
        settings_path = os.path.join(self.constructFilePath("testRunJacobiTest"), "settings")
        self.experiment.settings = asrt.ExperimentSettings(settings_path, "")
        self.experiment.all_settings_def()

        # set user settings
        asrt.ensure_dir(os.path.join(thispath, "settings"))
        asrt.ensure_dir(os.path.join(thispath, "subject_settings"))
        asrt.ensure_dir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "subject_settings"))
        self.clearDir(os.path.join(thispath, "logs"))

        self.experiment.jacobi_run = 0
        self.experiment.jacobi_trial = 0
        self.experiment.jacobi_trial_phase = 'none'
        self.experiment.jacobi_test_phase = 'none'

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])
        self.experiment.participant_id()

        # monitor settings
        self.experiment.monitor_settings()
        self.experiment.colors = {'wincolor': self.experiment.settings.asrt_background, 'linecolor': 'black',
                                  'stimp': self.experiment.settings.asrt_pcolor, 'stimr': self.experiment.settings.asrt_rcolor}

        with visual.Window(size=self.experiment.mymonitor.getSizePix(), color=self.experiment.colors['wincolor'], fullscr=False,
                           monitor=self.experiment.mymonitor, units="cm", gammaErrorPolicy='ignore') as self.experiment.mywindow:

            self.experiment.pressed_dict = {self.experiment.settings.key1: 1, self.experiment.settings.key2: 2,
                                            self.experiment.settings.key3: 3, self.experiment.settings.key4: 4}

            # use dummy values
            self.experiment.frame_time, self.experiment.frame_sd, self.experiment.frame_rate = 1.0, 0.12, 0.23

            self.experiment.dict_pos = {1: (float(self.experiment.settings.asrt_distance) * (-1.5), 0),
                                        2: (float(self.experiment.settings.asrt_distance) * (-0.5), 0),
                                        3: (float(self.experiment.settings.asrt_distance) * 0.5, 0),
                                        4: (float(self.experiment.settings.asrt_distance) * 1.5, 0)}

            aspect_ratio = self.experiment.mymonitor.getSizePix()[1] / self.experiment.mymonitor.getSizePix()[0]
            monitor_width_cm = self.experiment.settings.monitor_width
            monitor_height_cm = monitor_width_cm * aspect_ratio
            self.experiment.fixation_cross_pos = (monitor_width_cm / 2 - 3, -(monitor_height_cm / 2 - 3))
            self.experiment.fixation_cross = visual.TextStim(win=self.experiment.mywindow, text="+", height=3,
                                                             units="cm", color='black', pos=self.experiment.fixation_cross_pos)

            visual_mock = pvm.PsychoPyVisualMock()

            self.experiment.run_jacobi_test()

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 873)

            index = 0
            for run in range(4):
                for trial in range(24):
                    for i in range(8):
                        drawing = drawing_list[index]
                        self.assertTrue(isinstance(drawing, pvm.Circle))
                        self.assertEqual(drawing.lineColor, 'black')
                        self.assertEqual(drawing.fillColor, None)
                        index = index + 1

                    drawing = drawing_list[index]
                    self.assertTrue(isinstance(drawing, pvm.Circle))
                    self.assertEqual(drawing.lineColor, 'black')
                    self.assertEqual(drawing.fillColor, 'Orange')
                    index = index + 1

                if run < 3:
                    instruction_text = drawing_list[index]
                    self.assertTrue(isinstance(instruction_text, pvm.TextStim))
                    self.assertEqualWithEOL(instruction_text.text, "Most pihenhetsz egy kicsit.\n\n")

                    # fixation cross
                    fixation_cross = drawing_list[index + 1]
                    self.assertTrue(isinstance(fixation_cross, pvm.TextStim))
                    self.assertEqualWithEOL(fixation_cross.text, str("+"))

                    instruction_text = drawing_list[index + 2]
                    self.assertTrue(isinstance(instruction_text, pvm.TextStim))
                    self.assertEqualWithEOL(instruction_text.text, "A feladat folytatásához néz a keresztre!\n\n")
                    index += 3

            self.assertEqual(index, 873)

    def checkDefaultJacobiScreen(self, drawing_list, index):
        for i in range(4):
            drawing = drawing_list[index]
            self.assertTrue(isinstance(drawing, pvm.Circle))
            index = index + 1
        return index

    def checkJacobiScreenWithText(self, drawing_list, index):
        drawing = drawing_list[index]
        self.assertTrue(isinstance(drawing, pvm.TextStim))
        index = index + 1
        for i in range(4):
            drawing = drawing_list[index]
            self.assertTrue(isinstance(drawing, pvm.Circle))
            index = index + 1
        return index

    def checkJacobiScreenWithTextAndActiveStim(self, drawing_list, index):
        index = self.checkJacobiScreenWithText(drawing_list, index)

        drawing = drawing_list[index]
        self.assertTrue(isinstance(drawing, pvm.Circle))
        self.assertEqual(drawing.fillColor, 'DarkBlue')
        index = index + 1
        return index

    def testJacobiPresentation(self):
        visual_mock = pvm.PsychoPyVisualMock()
        thispath = os.path.join(self.constructFilePath("testJacobiPresentation"))
        self.experiment = asrt.Experiment(thispath)

        self.experiment.wait_for_eye_response_original = self.experiment.wait_for_eye_response
        self.experiment.wait_for_eye_response = self.wait_for_eye_response_override

        self.experiment.wait_for_leave_pos_original = self.experiment.wait_for_leave_pos
        self.experiment.wait_for_leave_pos = self.wait_for_leave_pos_override

        # load settings
        settings_path = os.path.join(self.constructFilePath("testJacobiPresentation"), "settings")
        self.experiment.settings = asrt.ExperimentSettings(settings_path, "")
        self.experiment.all_settings_def()

        # set user settings
        asrt.ensure_dir(os.path.join(thispath, "settings"))
        asrt.ensure_dir(os.path.join(thispath, "subject_settings"))
        asrt.ensure_dir(os.path.join(thispath, "logs"))
        self.clearDir(os.path.join(thispath, "settings"))
        self.clearDir(os.path.join(thispath, "subject_settings"))
        self.clearDir(os.path.join(thispath, "logs"))

        self.experiment.jacobi_run = 0
        self.experiment.jacobi_trial = 0
        self.experiment.jacobi_trial_phase = 'none'
        self.experiment.jacobi_test_phase = 'none'
        self.experiment.eye_tracker = EyeTrackerMock()

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, '3rd - 1324'])
        self.experiment.participant_id()

        # monitor settings
        self.experiment.monitor_settings()
        self.experiment.colors = {'wincolor': self.experiment.settings.asrt_background, 'linecolor': 'black',
                                  'stimp': self.experiment.settings.asrt_pcolor, 'stimr': self.experiment.settings.asrt_rcolor}

        with visual.Window(size=self.experiment.mymonitor.getSizePix(), color=self.experiment.colors['wincolor'], fullscr=False,
                           monitor=self.experiment.mymonitor, units="cm", gammaErrorPolicy='ignore') as self.experiment.mywindow:

            self.experiment.pressed_dict = {self.experiment.settings.key1: 1, self.experiment.settings.key2: 2,
                                            self.experiment.settings.key3: 3, self.experiment.settings.key4: 4}

            # use dummy values
            self.experiment.frame_time, self.experiment.frame_sd, self.experiment.frame_rate = 1.0, 0.12, 0.23

            self.experiment.dict_pos = {1: (float(self.experiment.settings.asrt_distance) * (-1.5), 0),
                                        2: (float(self.experiment.settings.asrt_distance) * (-0.5), 0),
                                        3: (float(self.experiment.settings.asrt_distance) * 0.5, 0),
                                        4: (float(self.experiment.settings.asrt_distance) * 1.5, 0)}

            aspect_ratio = self.experiment.mymonitor.getSizePix()[1] / self.experiment.mymonitor.getSizePix()[0]
            monitor_width_cm = self.experiment.settings.monitor_width
            monitor_height_cm = monitor_width_cm * aspect_ratio
            self.experiment.fixation_cross_pos = (monitor_width_cm / 2 - 3, -(monitor_height_cm / 2 - 3))
            self.experiment.fixation_cross = visual.TextStim(win=self.experiment.mywindow, text="+", height=3,
                                                             units="cm", color='black', pos=self.experiment.fixation_cross_pos)

            visual_mock = pvm.PsychoPyVisualMock()
            self.experiment.jacobi_ET_presentation()

            drawing_list = visual_mock.getListOfDrawings()
            self.assertEqual(len(drawing_list), 1874)

            index = 0

            # initial message
            drawing = drawing_list[index]
            self.assertTrue(isinstance(drawing, pvm.TextStim))
            self.assertEqualWithEOL(drawing.text, "+")
            index = index + 1

            drawing = drawing_list[index]
            self.assertTrue(isinstance(drawing, pvm.TextStim))
            self.assertEqualWithEOL(drawing.text, "A következőkben az lesz a feladatot, hogy a tekinteteddel jelöld ki az egyes köröket.\n\n"
                                                  "Egy kör kékre vált, ha sikerült kijelölni.\n\n"
                                    "Ha egy üres helyre nézel a kijelölés törlődik, így kétszer egymás után ki tudod jelülni ugyanazt a kört.\n\n"
                                    "A gyakorlás megkezdéséhez néz a keresztre!\n\n")
            index = index + 1

            # practices
            for i in range(11):
                index = self.checkJacobiScreenWithText(drawing_list, index)
                index = self.checkJacobiScreenWithTextAndActiveStim(drawing_list, index)

            # inclusion text
            drawing = drawing_list[index]
            self.assertTrue(isinstance(drawing, pvm.TextStim))
            self.assertEqualWithEOL(drawing.text, "+")
            index = index + 1

            drawing = drawing_list[index]
            self.assertTrue(isinstance(drawing, pvm.TextStim))
            self.assertEqualWithEOL(drawing.text, "Vége a gyakorlásnak.\n\n"
                                                  "A következő feladat az lesz, hogy próbáld meg olyan sorrendben kijelölni a köröket, amely sorrendben a kísérlet első felében megjelentek.\n\n"
                                                  "A feladat elkezdéséhez néz a keresztre!\n\n")
            index = index + 1

            for run in range(4):
                for trial in range(24):
                    index = self.checkDefaultJacobiScreen(drawing_list, index)
                    index = self.checkDefaultJacobiScreen(drawing_list, index)

                    drawing = drawing_list[index]
                    self.assertTrue(isinstance(drawing, pvm.Circle))
                    self.assertEqual(drawing.lineColor, 'black')
                    self.assertEqual(drawing.fillColor, 'DarkBlue')
                    index = index + 1

                if run < 3:
                    instruction_text = drawing_list[index]
                    self.assertTrue(isinstance(instruction_text, pvm.TextStim))
                    self.assertEqualWithEOL(instruction_text.text, "Most pihenhetsz egy kicsit.\n\n")

                    # fixation cross
                    fixation_cross = drawing_list[index + 1]
                    self.assertTrue(isinstance(fixation_cross, pvm.TextStim))
                    self.assertEqualWithEOL(fixation_cross.text, str("+"))

                    instruction_text = drawing_list[index + 2]
                    self.assertTrue(isinstance(instruction_text, pvm.TextStim))
                    self.assertEqualWithEOL(instruction_text.text, "A feladat folytatásához néz a keresztre!\n\n")
                    index += 3

            # exclusion text
            drawing = drawing_list[index]
            self.assertTrue(isinstance(drawing, pvm.TextStim))
            self.assertEqualWithEOL(drawing.text, "FIGYELEM! Most változik a feladatot!\n\n")
            index = index + 1

            drawing = drawing_list[index]
            self.assertTrue(isinstance(drawing, pvm.TextStim))
            self.assertEqualWithEOL(drawing.text, "+")
            index = index + 1

            drawing = drawing_list[index]
            self.assertTrue(isinstance(drawing, pvm.TextStim))
            self.assertEqualWithEOL(drawing.text, "Az előzőekhez képest most az lesz a feladatot, hogy MÁS sorrendben jelöld ki a köröket, amely sorrendben a kísérlet első felében megjelentek.\n\n"
                                                  "A feladat elkezdéséhez néz a keresztre!\n\n")
            index = index + 1

            for run in range(4):
                for trial in range(24):
                    index = self.checkDefaultJacobiScreen(drawing_list, index)
                    index = self.checkDefaultJacobiScreen(drawing_list, index)

                    drawing = drawing_list[index]
                    self.assertTrue(isinstance(drawing, pvm.Circle))
                    self.assertEqual(drawing.lineColor, 'black')
                    self.assertEqual(drawing.fillColor, 'DarkBlue')
                    index = index + 1

                if run < 3:
                    instruction_text = drawing_list[index]
                    self.assertTrue(isinstance(instruction_text, pvm.TextStim))
                    self.assertEqualWithEOL(instruction_text.text, "Most pihenhetsz egy kicsit.\n\n")

                    # fixation cross
                    fixation_cross = drawing_list[index + 1]
                    self.assertTrue(isinstance(fixation_cross, pvm.TextStim))
                    self.assertEqualWithEOL(fixation_cross.text, str("+"))

                    instruction_text = drawing_list[index + 2]
                    self.assertTrue(isinstance(instruction_text, pvm.TextStim))
                    self.assertEqualWithEOL(instruction_text.text, "A feladat folytatásához néz a keresztre!\n\n")
                    index += 3

            self.assertEqual(index, 1874)


if __name__ == "__main__":
    unittest.main()  # run all tests
