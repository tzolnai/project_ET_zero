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


class showSubjectContinuationDialogTest(unittest.TestCase):

    def testFinishedSession(self):
        gui_mock = pgm.PsychoPyGuiMock()

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.numsessions = 1
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.block_in_epochN = 5
        experiment.settings.epochN = 5

        experiment.stim_sessionN = {}
        experiment.stimepoch = {}
        experiment.stimblock = {}
        experiment.last_N = experiment.settings.get_maxtrial()
        for i in range(1, experiment.settings.get_maxtrial() + 1):
            experiment.stim_sessionN[i] = 1
            experiment.stimepoch[i] = i / 5
            experiment.stimblock[i] = i / (experiment.settings.blockprepN + experiment.settings.blocklengthN)

        experiment.show_subject_continuation_dialog()

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 2)
        self.assertEqual(list_of_texts[0], "A személy adatait beolvastam.")
        self.assertEqual(list_of_texts[1], "A jacobi teszt maradt hátra.")

    def testNullTrial(self):
        gui_mock = pgm.PsychoPyGuiMock()

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.numsessions = 1
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.block_in_epochN = 5
        experiment.settings.epochN = 5

        experiment.stim_sessionN = {}
        experiment.stimepoch = {}
        experiment.stimblock = {}
        experiment.last_N = 0
        for i in range(1, experiment.settings.get_maxtrial() + 1):
            experiment.stim_sessionN[i] = 1
            experiment.stimepoch[i] = i // 5 + 1
            experiment.stimblock[i] = i // (experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1

        experiment.show_subject_continuation_dialog()

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 5)
        self.assertEqual(list_of_texts[0], "A személy adatait beolvastam.")
        self.assertEqual(list_of_texts[1], "Folytatás innen...")
        self.assertEqual(list_of_texts[2], "Session: 1")
        self.assertEqual(list_of_texts[3], "Epoch: 1")
        self.assertEqual(list_of_texts[4], "Block: 1")

    def testInnerTrial(self):
        gui_mock = pgm.PsychoPyGuiMock()

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.numsessions = 1
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.block_in_epochN = 5
        experiment.settings.epochN = 5

        experiment.stim_sessionN = {}
        experiment.stimepoch = {}
        experiment.stimblock = {}
        experiment.stimtrial = {}
        experiment.last_N = experiment.settings.get_maxtrial() // 2
        for i in range(1, experiment.settings.get_maxtrial() + 1):
            experiment.stim_sessionN[i] = 1
            experiment.stimepoch[i] = i // ((experiment.settings.blockprepN +
                                             experiment.settings.blocklengthN) * experiment.settings.block_in_epochN) + 1
            experiment.stimblock[i] = i // (experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1

        experiment.show_subject_continuation_dialog()

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 5)
        self.assertEqual(list_of_texts[0], "A személy adatait beolvastam.")
        self.assertEqual(list_of_texts[1], "Folytatás innen...")
        self.assertEqual(list_of_texts[2], "Session: 1")
        self.assertEqual(list_of_texts[3], "Epoch: 3")
        self.assertEqual(list_of_texts[4], "Block: 13")

    def testCancelDialog(self):

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.setReturnValue(False)

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.numsessions = 1
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.block_in_epochN = 5
        experiment.settings.epochN = 5

        experiment.stim_sessionN = {}
        experiment.stimepoch = {}
        experiment.stimblock = {}
        experiment.stimtrial = {}
        experiment.last_N = 0
        for i in range(1, experiment.settings.get_maxtrial() + 1):
            experiment.stim_sessionN[i] = 1
            experiment.stimepoch[i] = i // 5 + 1
            experiment.stimblock[i] = i // (experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1

        with self.assertRaises(SystemExit):
            experiment.show_subject_continuation_dialog()


if __name__ == "__main__":
    unittest.main()  # run all tests
