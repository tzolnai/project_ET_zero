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

#!\\usr\\bin\\env python
# -*- coding: utf-8 -*-

import psychopy_gui_mock as pgm
import sys
import os
# Add the local path to the main script and external scripts so we can import them.
sys.path = [".."] + \
    [os.path.join("..", "externals", "psychopy_mock")] + sys.path

import unittest
import asrt


class showEpochAndBlockSettingsDialogTest(unittest.TestCase):

    def testDefaults(self):
        gui_mock = pgm.PsychoPyGuiMock()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.numsessions = 1
        exp_settings.show_epoch_and_block_settings_dialog()

        self.assertEqual(exp_settings.blockprepN, 5)
        self.assertEqual(exp_settings.blocklengthN, 80)
        self.assertEqual(exp_settings.block_in_epochN, 5)
        self.assertEqual(exp_settings.epochN, 5)
        self.assertEqual(len(exp_settings.epochs), 1)
        self.assertEqual(exp_settings.epochs[0], 5)
        self.assertEqual(len(exp_settings.asrt_types), 1)
        self.assertEqual(exp_settings.asrt_types[1], '')

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "Kísérlet felépítése ")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 5)
        self.assertEqual(
            list_of_fields[0].label, "Randomok gyakorlaskent a blokk elejen (ennyi db):")
        self.assertEqual(list_of_fields[0].initial, 5)
        self.assertEqual(list_of_fields[1].label, "Eles probak a blokkban:")
        self.assertEqual(list_of_fields[1].initial, 80)
        self.assertEqual(list_of_fields[2].label,
                         "Blokkok szama egy epochban:")
        self.assertEqual(list_of_fields[2].initial, 5)
        self.assertEqual(list_of_fields[3].label, "Session 1 epochok szama")
        self.assertEqual(list_of_fields[3].initial, 5)
        self.assertEqual(list_of_fields[4].label, "Session 1 ASRT tipusa")
        self.assertEqual(list_of_fields[4].initial, '')

    def testCancel(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.setReturnValue(False)

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.numsessions = 1

        with self.assertRaises(SystemExit):
            exp_settings.show_epoch_and_block_settings_dialog()

    def testNoSessions(self):
        gui_mock = pgm.PsychoPyGuiMock()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.numsessions = 0
        exp_settings.show_epoch_and_block_settings_dialog()

        self.assertEqual(exp_settings.blockprepN, 5)
        self.assertEqual(exp_settings.blocklengthN, 80)
        self.assertEqual(exp_settings.block_in_epochN, 5)
        self.assertEqual(exp_settings.epochN, 0)
        self.assertEqual(len(exp_settings.epochs), 0)
        self.assertEqual(len(exp_settings.asrt_types), 0)

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "Kísérlet felépítése ")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 3)
        self.assertEqual(
            list_of_fields[0].label, "Randomok gyakorlaskent a blokk elejen (ennyi db):")
        self.assertEqual(list_of_fields[0].initial, 5)
        self.assertEqual(list_of_fields[1].label, "Eles probak a blokkban:")
        self.assertEqual(list_of_fields[1].initial, 80)
        self.assertEqual(list_of_fields[2].label,
                         "Blokkok szama egy epochban:")
        self.assertEqual(list_of_fields[2].initial, 5)

    def testMoreSessions(self):
        gui_mock = pgm.PsychoPyGuiMock()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.numsessions = 3
        exp_settings.show_epoch_and_block_settings_dialog()

        self.assertEqual(exp_settings.blockprepN, 5)
        self.assertEqual(exp_settings.blocklengthN, 80)
        self.assertEqual(exp_settings.block_in_epochN, 5)
        self.assertEqual(exp_settings.epochN, 15)
        self.assertEqual(len(exp_settings.epochs), 3)
        self.assertEqual(exp_settings.epochs[0], 5)
        self.assertEqual(exp_settings.epochs[1], 5)
        self.assertEqual(exp_settings.epochs[2], 5)
        self.assertEqual(len(exp_settings.asrt_types), 3)

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "Kísérlet felépítése ")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 9)
        self.assertEqual(
            list_of_fields[0].label, "Randomok gyakorlaskent a blokk elejen (ennyi db):")
        self.assertEqual(list_of_fields[0].initial, 5)
        self.assertEqual(list_of_fields[1].label, "Eles probak a blokkban:")
        self.assertEqual(list_of_fields[1].initial, 80)
        self.assertEqual(list_of_fields[2].label,
                         "Blokkok szama egy epochban:")
        self.assertEqual(list_of_fields[2].initial, 5)
        self.assertEqual(list_of_fields[3].label, "Session 1 epochok szama")
        self.assertEqual(list_of_fields[3].initial, 5)
        self.assertEqual(list_of_fields[4].label, "Session 2 epochok szama")
        self.assertEqual(list_of_fields[4].initial, 5)
        self.assertEqual(list_of_fields[5].label, "Session 3 epochok szama")
        self.assertEqual(list_of_fields[5].initial, 5)
        self.assertEqual(list_of_fields[6].label, "Session 1 ASRT tipusa")
        self.assertEqual(list_of_fields[6].initial, '')
        self.assertEqual(list_of_fields[7].label, "Session 2 ASRT tipusa")
        self.assertEqual(list_of_fields[7].initial, '')
        self.assertEqual(list_of_fields[8].label, "Session 3 ASRT tipusa")
        self.assertEqual(list_of_fields[8].initial, '')

    def testCustomValues(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(
            [12, 79, 2, 3, 12, 7, 'implicit', 'explicit', 'noASRT'])

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.numsessions = 3
        exp_settings.show_epoch_and_block_settings_dialog()

        self.assertEqual(exp_settings.blockprepN, 12)
        self.assertEqual(exp_settings.blocklengthN, 79)
        self.assertEqual(exp_settings.block_in_epochN, 2)
        self.assertEqual(exp_settings.epochN, 22)
        self.assertEqual(len(exp_settings.epochs), 3)
        self.assertEqual(exp_settings.epochs[0], 3)
        self.assertEqual(exp_settings.epochs[1], 12)
        self.assertEqual(exp_settings.epochs[2], 7)
        self.assertEqual(len(exp_settings.asrt_types), 3)
        self.assertEqual(exp_settings.asrt_types[1], 'implicit')
        self.assertEqual(exp_settings.asrt_types[2], 'explicit')
        self.assertEqual(exp_settings.asrt_types[3], 'noASRT')


if __name__ == "__main__":
    unittest.main()  # run all tests
