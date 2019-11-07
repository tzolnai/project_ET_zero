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
import psychopy_gui_mock as pgm


class showKeyAndFeedbackSettingsDialogTest(unittest.TestCase):

    def testDefaults(self):
        gui_mock = pgm.PsychoPyGuiMock()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.experiment_type = 'reaction-time'
        exp_settings.show_key_and_feedback_settings_dialog()

        self.assertEqual(exp_settings.key1, 'y')
        self.assertEqual(exp_settings.key2, 'c')
        self.assertEqual(exp_settings.key3, 'b')
        self.assertEqual(exp_settings.key4, 'm')
        self.assertEqual(exp_settings.key_quit, 'q')
        self.assertEqual(exp_settings.whether_warning, True)
        self.assertEqual(exp_settings.speed_warning, 93)
        self.assertEqual(exp_settings.acc_warning, 91)

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 2)
        self.assertEqual(list_of_texts[0], "Válaszbillentyűk")
        self.assertEqual(
            list_of_texts[1], "Ha be van kapcsolva a figyelmeztetés, akkor...:")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 8)
        self.assertEqual(list_of_fields[0].label, "Bal szelso:")
        self.assertEqual(list_of_fields[0].initial, 'y')
        self.assertEqual(list_of_fields[1].label, "Bal kozep")
        self.assertEqual(list_of_fields[1].initial, 'c')
        self.assertEqual(list_of_fields[2].label, "Jobb kozep")
        self.assertEqual(list_of_fields[2].initial, 'b')
        self.assertEqual(list_of_fields[3].label, "Jobb szelso")
        self.assertEqual(list_of_fields[3].initial, 'm')
        self.assertEqual(list_of_fields[4].label, "Kilepes")
        self.assertEqual(list_of_fields[4].initial, 'q')
        self.assertEqual(list_of_fields[5].label,
                         "Figyelmeztetes pontossagra/sebessegre:")
        self.assertEqual(list_of_fields[5].initial, True)
        self.assertEqual(
            list_of_fields[6].label, "Figyelmeztetes sebessegre ezen pontossag felett (%):")
        self.assertEqual(list_of_fields[6].initial, 93)
        self.assertEqual(
            list_of_fields[7].label, "Figyelmeztetes pontosságra ezen pontossag alatt (%):")
        self.assertEqual(list_of_fields[7].initial, 91)

    def testCancel(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.setReturnValue(False)

        exp_settings = asrt.ExperimentSettings("", "")

        with self.assertRaises(SystemExit):
            exp_settings.show_key_and_feedback_settings_dialog()

    def testCustomValues(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['a', 's', 'd', 'w', 'k', False, 80, 70])

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.experiment_type = 'reaction-time'
        exp_settings.show_key_and_feedback_settings_dialog()

        self.assertEqual(exp_settings.key1, 'a')
        self.assertEqual(exp_settings.key2, 's')
        self.assertEqual(exp_settings.key3, 'd')
        self.assertEqual(exp_settings.key4, 'w')
        self.assertEqual(exp_settings.key_quit, 'k')
        self.assertEqual(exp_settings.whether_warning, False)
        self.assertEqual(exp_settings.speed_warning, 80)
        self.assertEqual(exp_settings.acc_warning, 70)


if __name__ == "__main__":
    unittest.main()  # run all tests
