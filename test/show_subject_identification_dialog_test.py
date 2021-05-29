# !/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) <2019-2021>  <Tamás Zolnai>  <zolnaitamas2000@gmail.com>

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


class showSubjectIdentificationDialogTest(unittest.TestCase):

    def testDefaults(self):
        gui_mock = pgm.PsychoPyGuiMock()

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = ["kontrol", "exp1"]
        experiment.show_subject_identification_dialog()

        self.assertEqual(experiment.subject_number, 0)
        self.assertEqual(experiment.subject_group, 'kontrol')

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 2)
        self.assertEqual(list_of_fields[0].label, "Ksz. sorszáma")
        self.assertEqual(list_of_fields[0].initial, '0')
        self.assertEqual(list_of_fields[1].label, "Csoport")
        self.assertEqual(list_of_fields[1].initial, '')

    def testCancel(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.setReturnValue(False)

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = ["kontrol", "exp1"]
        with self.assertRaises(SystemExit):
            experiment.show_subject_identification_dialog()

    def testCustomValues(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues([10, 'kontrol', 'férfi', '25'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = ["kontrol", "exp1"]
        subject_settings = experiment.show_subject_identification_dialog()

        self.assertEqual(experiment.subject_number, 10)
        self.assertEqual(experiment.subject_group, 'kontrol')

    def testInvalidSubjectNumber(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['x', 'kontrol', 10, 'kontrol'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = ["kontrol", "exp1"]
        experiment.show_subject_identification_dialog()

        self.assertEqual(experiment.subject_number, 10)
        self.assertEqual(experiment.subject_group, 'kontrol')

        # the dialog is displayed twice because for the first time invalid value was specified
        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 2)
        self.assertEqual(list_of_texts[0], "")
        self.assertEqual(list_of_texts[1], "Pozitív egész számot adj meg a sorszámhoz!")

    def testInvalidSubjectNumber2(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues([-10, 'kontrol', 10, 'kontrol'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = ["kontrol", "exp1"]
        experiment.show_subject_identification_dialog()

        self.assertEqual(experiment.subject_number, 10)
        self.assertEqual(experiment.subject_group, 'kontrol')

        # the dialog is displayed twice because for the first time invalid value was specified
        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 2)
        self.assertEqual(list_of_texts[0], "")
        self.assertEqual(list_of_texts[1], "Pozitív egész számot adj meg a sorszámhoz!")

    def testNoGroups(self):
        gui_mock = pgm.PsychoPyGuiMock()

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = []
        experiment.show_subject_identification_dialog()

        self.assertEqual(experiment.subject_number, 0)
        self.assertEqual(experiment.subject_group, '')

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 1)
        self.assertEqual(list_of_fields[0].label, "Ksz. sorszáma")
        self.assertEqual(list_of_fields[0].initial, '0')


if __name__ == "__main__":
    unittest.main()  # run all tests
