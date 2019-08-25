# !/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) <2019>  <Tamás Zolnai>    <zolnaitamas2000@gmail.com>

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


class showComputerAndDisplaySettingsDialogTest(unittest.TestCase):

    def testDefaults(self):
        gui_mock = pgm.PsychoPyGuiMock()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.experiment_type = 'reaction-time'
        exp_settings.show_computer_and_display_settings_dialog()

        self.assertEqual(exp_settings.monitor_width, 34.2)
        self.assertEqual(exp_settings.computer_name, "Laposka")
        self.assertEqual(exp_settings.asrt_distance, 3)
        self.assertEqual(exp_settings.asrt_size, 1)
        self.assertEqual(exp_settings.asrt_rcolor, "Orange")
        self.assertEqual(exp_settings.asrt_pcolor, "Green")
        self.assertEqual(exp_settings.asrt_background, "Ivory")
        self.assertEqual(exp_settings.RSI_time, 0.12)

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 2)
        self.assertEqual(list_of_texts[0], "A számítógépről...")
        self.assertEqual(list_of_texts[1], "Megjelenés..")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 8)
        self.assertEqual(list_of_fields[0].label,
                         "Hasznos kepernyo szelessege (cm)")
        self.assertEqual(list_of_fields[0].initial, 34.2)
        self.assertEqual(list_of_fields[1].label,
                         "Szamitogep fantazianeve (ekezet nelkul)")
        self.assertEqual(list_of_fields[1].initial, "Laposka")
        self.assertEqual(
            list_of_fields[2].label, "Ingerek tavolsaga (kozeppontok kozott) (cm)")
        self.assertEqual(list_of_fields[2].initial, 3)
        self.assertEqual(list_of_fields[3].label, "Ingerek sugara (cm)")
        self.assertEqual(list_of_fields[3].initial, 1)
        self.assertEqual(list_of_fields[4].label,
                         "ASRT inger szine (elsodleges, R)")
        self.assertEqual(list_of_fields[4].initial, "Orange")
        self.assertEqual(
            list_of_fields[5].label, "ASRT inger szine (masodlagos, P, explicit asrtnel)")
        self.assertEqual(list_of_fields[5].initial, "Green")
        self.assertEqual(list_of_fields[6].label, "Hatter szine")
        self.assertEqual(list_of_fields[6].initial, "Ivory")
        self.assertEqual(list_of_fields[7].label, "RSI (ms)")
        self.assertEqual(list_of_fields[7].initial, 120)

    def testCancel(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.setReturnValue(False)

        with self.assertRaises(SystemExit):
            exp_settings = asrt.ExperimentSettings("", "")
            exp_settings.show_computer_and_display_settings_dialog()

    def testCustomValues(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(
            [17, "Alma", 2.3, 1.2, "Black", "White", "Green", 205])

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.show_computer_and_display_settings_dialog()

        self.assertEqual(exp_settings.monitor_width, 17)
        self.assertEqual(exp_settings.computer_name, "Alma")
        self.assertEqual(exp_settings.asrt_distance, 2.3)
        self.assertEqual(exp_settings.asrt_size, 1.2)
        self.assertEqual(exp_settings.asrt_rcolor, "Black")
        self.assertEqual(exp_settings.asrt_pcolor, "White")
        self.assertEqual(exp_settings.asrt_background, "Green")
        self.assertEqual(exp_settings.RSI_time, 0.205)


if __name__ == "__main__":
    unittest.main()  # run all tests
