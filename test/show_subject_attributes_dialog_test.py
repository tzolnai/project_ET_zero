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


class showSubjectAttributesDialogTest(unittest.TestCase):

    def testDefaults(self):
        gui_mock = pgm.PsychoPyGuiMock()

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.numsessions = 2
        experiment.settings.epochs = [2, 3]
        experiment.settings.epochN = 5
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit', 3: 'implicit', 4: 'implicit', 5: 'implicit'}

        experiment.show_subject_attributes_dialog()

        self.assertEqual(len(experiment.PCodes), 5)
        self.assertEqual(experiment.PCodes, {1: '1st - 1234', 2: '1st - 1234', 3: '1st - 1234', 4: '1st - 1234', 5: '1st - 1234'})
        self.assertEqual(experiment.subject_sex, "male")
        self.assertEqual(experiment.subject_age, "25")

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 4)
        self.assertEqual(list_of_fields[0].label, "Nem")
        self.assertEqual(list_of_fields[0].initial, '')
        self.assertEqual(list_of_fields[1].label, "Életkor")
        self.assertEqual(list_of_fields[1].initial, '25')
        self.assertEqual(list_of_fields[2].label, "Első PCode")
        self.assertEqual(list_of_fields[3].label, "Második PCode")

    def testCustomValue(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['férfi', 25, '1st', '6th'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.numsessions = 2
        experiment.settings.epochs = [2, 3]
        experiment.settings.epochN = 5
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit', 3: 'implicit', 4: 'implicit', 5: 'implicit'}

        experiment.show_subject_attributes_dialog()

        self.assertEqual(len(experiment.PCodes), 5)
        self.assertEqual(experiment.PCodes, {1: '1st - 1234', 2: '1st - 1234', 3: '1st - 1234', 4: '6th - 1432', 5: '1st - 1234'})
        self.assertEqual(experiment.subject_sex, "male")
        self.assertEqual(experiment.subject_age, "25")

    def testCancel(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.setReturnValue(False)

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.numsessions = 2
        experiment.settings.epochs = [2, 3]
        experiment.settings.epochN = 5
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit', 3: 'implicit', 4: 'implicit', 5: 'implicit'}

        with self.assertRaises(SystemExit):
            experiment.show_subject_attributes_dialog()

    def testNoASRTEpochs(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['férfi', 25, '3rd', '6th'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.numsessions = 2
        experiment.settings.epochs = [5, 3]
        experiment.settings.epochN = 8
        experiment.settings.asrt_types = {1: 'noASRT', 2: 'implicit', 3: 'implicit',
                                          4: 'implicit', 5: 'implicit', 6: 'implicit', 7: 'implicit', 8: 'implicit'}

        experiment.show_subject_attributes_dialog()

        self.assertEqual(len(experiment.PCodes), 8)
        self.assertEqual(experiment.PCodes, {1: 'noPattern', 2: '3rd - 1324', 3: '3rd - 1324', 4: '3rd - 1324', 5: '3rd - 1324',
                                             6: '3rd - 1324', 7: '6th - 1432', 8: '3rd - 1324'})
        self.assertEqual(experiment.subject_sex, "male")
        self.assertEqual(experiment.subject_age, "25")

    def testWrongSubjectNumber(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['férfi', "alma", '1st'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.numsessions = 2
        experiment.settings.epochs = [2, 3]
        experiment.settings.epochN = 5
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit', 3: 'implicit', 4: 'implicit', 5: 'implicit'}

        with self.assertRaises(SystemExit):
            experiment.show_subject_attributes_dialog()


if __name__ == "__main__":
    unittest.main()  # run all tests
