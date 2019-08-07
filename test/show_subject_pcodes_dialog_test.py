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

import psychopy_gui_mock as pgm
import asrt
import unittest

import os

import sys
# Add the local path to the main script so we can import it.
sys.path = [".."] + \
    [os.path.join("..", "externals", "psychopy_mock")] + sys.path


class showSubjectPCodesDialogTest(unittest.TestCase):

    def testDefaults(self):
        gui_mock = pgm.PsychoPyGuiMock()

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.numsessions = 1
        experiment.settings.asrt_types = {}
        experiment.settings.asrt_types[1] = "implicit"

        experiment.show_subject_PCodes_dialog()

        self.assertEqual(len(experiment.PCodes),
                         experiment.settings.numsessions)
        self.assertEqual(experiment.PCodes[1], "")

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 1)
        self.assertEqual(list_of_fields[0].label, "Session 1 PCode")

    def testCustomValue(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['1st'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.numsessions = 1
        experiment.settings.asrt_types = {}
        experiment.settings.asrt_types[1] = "implicit"

        experiment.show_subject_PCodes_dialog()

        self.assertEqual(len(experiment.PCodes),
                         experiment.settings.numsessions)
        self.assertEqual(experiment.PCodes[1], "1st")

    def testMoreSessionsCustomValues(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['2nd', '1st', '6th', '3rd', '1st'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")

        experiment.settings.numsessions = 5
        experiment.settings.asrt_types = {}
        experiment.settings.asrt_types[1] = "implicit"
        experiment.settings.asrt_types[2] = "implicit"
        experiment.settings.asrt_types[3] = "implicit"
        experiment.settings.asrt_types[4] = "implicit"
        experiment.settings.asrt_types[5] = "implicit"

        experiment.show_subject_PCodes_dialog()

        self.assertEqual(len(experiment.PCodes),
                         experiment.settings.numsessions)
        self.assertEqual(experiment.PCodes[1], "2nd")
        self.assertEqual(experiment.PCodes[2], "1st")
        self.assertEqual(experiment.PCodes[3], "6th")
        self.assertEqual(experiment.PCodes[4], "3rd")
        self.assertEqual(experiment.PCodes[5], "1st")

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

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.numsessions = 1
        experiment.settings.asrt_types = {}
        experiment.settings.asrt_types[1] = "implicit"

        with self.assertRaises(SystemExit):
            experiment.show_subject_PCodes_dialog()

    def testNoASRTSussions(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(
            ['2nd', '1st', 'noPattern', '3rd', 'noPattern'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.numsessions = 5
        experiment.settings.asrt_types = {}
        experiment.settings.asrt_types[1] = "implicit"
        experiment.settings.asrt_types[2] = "implicit"
        experiment.settings.asrt_types[3] = "noASRT"
        experiment.settings.asrt_types[4] = "implicit"
        experiment.settings.asrt_types[5] = "noASRT"

        experiment.show_subject_PCodes_dialog()

        self.assertEqual(len(experiment.PCodes),
                         experiment.settings.numsessions)
        self.assertEqual(experiment.PCodes[1], "2nd")
        self.assertEqual(experiment.PCodes[2], "1st")
        self.assertEqual(experiment.PCodes[3], "noPattern")
        self.assertEqual(experiment.PCodes[4], "3rd")
        self.assertEqual(experiment.PCodes[5], "noPattern")

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
    unittest.main()  # run all tests
