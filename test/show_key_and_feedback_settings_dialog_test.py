#    Copyright (C) <2018>  <Tamás Zolnai>  <zolnaitamas2000@gmail.com>

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

import sys
# Add the local path to the main script so we can import it.
sys.path = [".."] + sys.path

import asrt

import psychopy_gui_mock as pgm

class showKeyAndFeedbackSettingsDialogTest(unittest.TestCase):

    def testDefaults(self):
        gui_mock = pgm.PsychoPyGuiMock()

        key_and_feedback_settings = asrt.show_key_and_feedback_settings_dialog()
        key1 = key_and_feedback_settings["key1"]
        key2 = key_and_feedback_settings["key2"]
        key3 = key_and_feedback_settings["key3"]
        key4 = key_and_feedback_settings["key4"]
        key_quit = key_and_feedback_settings["key_quit"]
        whether_warning = key_and_feedback_settings["whether_warning"]
        speed_warning = key_and_feedback_settings["speed_warning"]
        acc_warning = key_and_feedback_settings["acc_warning"]

        self.assertEqual(key1, 'y')
        self.assertEqual(key2, 'c')
        self.assertEqual(key3, 'b')
        self.assertEqual(key4, 'm')
        self.assertEqual(key_quit, 'q')
        self.assertEqual(whether_warning, True)
        self.assertEqual(speed_warning, 93)
        self.assertEqual(acc_warning, 91)

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 2)
        self.assertEqual(list_of_texts[0], "Válaszbillentyűk")
        self.assertEqual(list_of_texts[1], "Ha be van kapcsolva a figyelmeztetés, akkor...:")

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
        self.assertEqual(list_of_fields[5].label, "Figyelmeztetes pontossagra/sebessegre:")
        self.assertEqual(list_of_fields[5].initial, True)
        self.assertEqual(list_of_fields[6].label, "Figyelmeztetes sebessegre ezen pontossag felett (%):")
        self.assertEqual(list_of_fields[6].initial, 93)
        self.assertEqual(list_of_fields[7].label, "Figyelmeztetes sebessegre ezen pontossag felett (%):")
        self.assertEqual(list_of_fields[7].initial, 91)

    def testCancel(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.setReturnValue(False)

        with self.assertRaises(SystemExit):
            asrt.show_key_and_feedback_settings_dialog()

    def testCustomValues(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['a', 's', 'd', 'w', 'k', False, 80, 70])

        key_and_feedback_settings = asrt.show_key_and_feedback_settings_dialog()
        key1 = key_and_feedback_settings["key1"]
        key2 = key_and_feedback_settings["key2"]
        key3 = key_and_feedback_settings["key3"]
        key4 = key_and_feedback_settings["key4"]
        key_quit = key_and_feedback_settings["key_quit"]
        whether_warning = key_and_feedback_settings["whether_warning"]
        speed_warning = key_and_feedback_settings["speed_warning"]
        acc_warning = key_and_feedback_settings["acc_warning"]

        self.assertEqual(key1, 'a')
        self.assertEqual(key2, 's')
        self.assertEqual(key3, 'd')
        self.assertEqual(key4, 'w')
        self.assertEqual(key_quit, 'k')
        self.assertEqual(whether_warning, False)
        self.assertEqual(speed_warning, 80)
        self.assertEqual(acc_warning, 70)

if __name__ == "__main__":
    unittest.main() # run all tests