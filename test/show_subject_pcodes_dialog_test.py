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

import psychopy_gui_mock as pgm

class showSubjectPCodesDialogTest(unittest.TestCase):

    def testDefaults(self):
        gui_mock = pgm.PsychoPyGuiMock()

        exp_settings = asrt.ExperimentSettings()
        exp_settings.numsessions = 1
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "implicit"

        PCodes, PCode_types = asrt.show_subject_PCodes_dialog(exp_settings)

        self.assertEqual(len(PCodes), exp_settings.numsessions)
        self.assertEqual(PCodes[1], "")
        self.assertEqual(PCode_types, "")

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 1)
        self.assertEqual(list_of_fields[0].label, "Session 1 PCode")

    def testCustomValue(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['1st'])

        exp_settings = asrt.ExperimentSettings()
        exp_settings.numsessions = 1
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "implicit"

        PCodes, PCode_types = asrt.show_subject_PCodes_dialog(exp_settings)

        self.assertEqual(len(PCodes), exp_settings.numsessions)
        self.assertEqual(PCodes[1], "1st")
        self.assertEqual(PCode_types, "1")

    def testMoreSessionsCustomValues(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['2nd', '1st', '6th', '3rd', '1st'])

        exp_settings = asrt.ExperimentSettings()
        exp_settings.numsessions = 5
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "implicit"
        exp_settings.asrt_types[2] = "implicit"
        exp_settings.asrt_types[3] = "implicit"
        exp_settings.asrt_types[4] = "implicit"
        exp_settings.asrt_types[5] = "implicit"

        PCodes, PCode_types = asrt.show_subject_PCodes_dialog(exp_settings)

        self.assertEqual(len(PCodes), exp_settings.numsessions)
        self.assertEqual(PCodes[1], "2nd")
        self.assertEqual(PCodes[2], "1st")
        self.assertEqual(PCodes[3], "6th")
        self.assertEqual(PCodes[4], "3rd")
        self.assertEqual(PCodes[5], "1st")
        self.assertEqual(PCode_types, "2=1=6=3")

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 5)
        self.assertEqual(list_of_fields[0].label, "Session 1 PCode")
        self.assertEqual(list_of_fields[1].label, "Session 2 PCode")
        self.assertEqual(list_of_fields[2].label, "Session 3 PCode")
        self.assertEqual(list_of_fields[3].label, "Session 4 PCode")
        self.assertEqual(list_of_fields[4].label, "Session 5 PCode")

    def testCancel(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.setReturnValue(False)

        exp_settings = asrt.ExperimentSettings()
        exp_settings.numsessions = 1
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "implicit"

        with self.assertRaises(SystemExit):
            PCodes, PCode_types = asrt.show_subject_PCodes_dialog(exp_settings)

    def testNoASRTSussions(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['2nd', '1st', 'noPattern', '3rd', 'noPattern'])

        exp_settings = asrt.ExperimentSettings()
        exp_settings.numsessions = 5
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "implicit"
        exp_settings.asrt_types[2] = "implicit"
        exp_settings.asrt_types[3] = "noASRT"
        exp_settings.asrt_types[4] = "implicit"
        exp_settings.asrt_types[5] = "noASRT"

        PCodes, PCode_types = asrt.show_subject_PCodes_dialog(exp_settings)

        self.assertEqual(len(PCodes), exp_settings.numsessions)
        self.assertEqual(PCodes[1], "2nd")
        self.assertEqual(PCodes[2], "1st")
        self.assertEqual(PCodes[3], "noPattern")
        self.assertEqual(PCodes[4], "3rd")
        self.assertEqual(PCodes[5], "noPattern")
        self.assertEqual(PCode_types, "2=1=3")

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 5)
        self.assertEqual(list_of_fields[0].label, "Session 1 PCode")
        self.assertEqual(list_of_fields[1].label, "Session 2 PCode")
        self.assertEqual(list_of_fields[2].label, "Session 3 PCode")
        self.assertEqual(list_of_fields[3].label, "Session 4 PCode")
        self.assertEqual(list_of_fields[4].label, "Session 5 PCode")

if __name__ == "__main__":
    unittest.main() # run all tests