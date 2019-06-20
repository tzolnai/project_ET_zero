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

class showSubjectContinuationDialogTest(unittest.TestCase):

    def testFinishedSession(self):

        gui_mock = pgm.PsychoPyGuiMock()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.numsessions = 1
        exp_settings.blockprepN = 5
        exp_settings.blocklengthN = 80
        exp_settings.block_in_epochN = 5
        exp_settings.epochN = 5

        stim_sessionN = {}
        stimepoch = {}
        stimblock = {}
        stimtrial = {}
        last_N = exp_settings.get_maxtrial()
        for i in range(1, exp_settings.get_maxtrial() + 1):
            stim_sessionN[i] = 1
            stimepoch[i] = i / 5
            stimblock[i] = i / (exp_settings.blockprepN + exp_settings.blocklengthN)
            stimtrial[i] = i % (exp_settings.blockprepN + exp_settings.blocklengthN)

        with self.assertRaises(SystemExit):
            asrt.show_subject_continuation_dialog(stim_sessionN, stimepoch, stimblock, stimtrial, last_N, exp_settings)

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 2)
        self.assertEqual(list_of_texts[0], "A személy adatait beolvastam.")
        self.assertEqual(list_of_texts[1], "A személy végigcsinálta a feladatot.")

    def testNullTrial(self):

        gui_mock = pgm.PsychoPyGuiMock()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.numsessions = 1
        exp_settings.blockprepN = 5
        exp_settings.blocklengthN = 80
        exp_settings.block_in_epochN = 5
        exp_settings.epochN = 5

        stim_sessionN = {}
        stimepoch = {}
        stimblock = {}
        stimtrial = {}
        last_N = 0
        for i in range(1, exp_settings.get_maxtrial() + 1):
            stim_sessionN[i] = 1
            stimepoch[i] = i // 5 + 1
            stimblock[i] = i // (exp_settings.blockprepN + exp_settings.blocklengthN) + 1
            stimtrial[i] = i % (exp_settings.blockprepN + exp_settings.blocklengthN)

        asrt.show_subject_continuation_dialog(stim_sessionN, stimepoch, stimblock, stimtrial, last_N, exp_settings)

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 6)
        self.assertEqual(list_of_texts[0], "A személy adatait beolvastam.")
        self.assertEqual(list_of_texts[1], "Folytatás innen...")
        self.assertEqual(list_of_texts[2], "Session: 1")
        self.assertEqual(list_of_texts[3], "Epoch: 1")
        self.assertEqual(list_of_texts[4], "Block: 1")
        self.assertEqual(list_of_texts[5], "Trial: 1")

    def testInnerTrial(self):

        gui_mock = pgm.PsychoPyGuiMock()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.numsessions = 1
        exp_settings.blockprepN = 5
        exp_settings.blocklengthN = 80
        exp_settings.block_in_epochN = 5
        exp_settings.epochN = 5

        stim_sessionN = {}
        stimepoch = {}
        stimblock = {}
        stimtrial = {}
        last_N = exp_settings.get_maxtrial() // 2
        for i in range(1, exp_settings.get_maxtrial() + 1):
            stim_sessionN[i] = 1
            stimepoch[i] = i // ((exp_settings.blockprepN + exp_settings.blocklengthN) * exp_settings.block_in_epochN) + 1
            stimblock[i] = i // (exp_settings.blockprepN + exp_settings.blocklengthN) + 1
            stimtrial[i] = i % (exp_settings.blockprepN + exp_settings.blocklengthN)

        asrt.show_subject_continuation_dialog(stim_sessionN, stimepoch, stimblock, stimtrial, last_N, exp_settings)

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 6)
        self.assertEqual(list_of_texts[0], "A személy adatait beolvastam.")
        self.assertEqual(list_of_texts[1], "Folytatás innen...")
        self.assertEqual(list_of_texts[2], "Session: 1")
        self.assertEqual(list_of_texts[3], "Epoch: 3")
        self.assertEqual(list_of_texts[4], "Block: 13")
        self.assertEqual(list_of_texts[5], "Trial: 43")

    def testCancelDialog(self):

        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.setReturnValue(False)

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.numsessions = 1
        exp_settings.blockprepN = 5
        exp_settings.blocklengthN = 80
        exp_settings.block_in_epochN = 5
        exp_settings.epochN = 5

        stim_sessionN = {}
        stimepoch = {}
        stimblock = {}
        stimtrial = {}
        last_N = 0
        for i in range(1, exp_settings.get_maxtrial() + 1):
            stim_sessionN[i] = 1
            stimepoch[i] = i // 5 + 1
            stimblock[i] = i // (exp_settings.blockprepN + exp_settings.blocklengthN) + 1
            stimtrial[i] = i % (exp_settings.blockprepN + exp_settings.blocklengthN)

        with self.assertRaises(SystemExit):
            asrt.show_subject_continuation_dialog(stim_sessionN, stimepoch, stimblock, stimtrial, last_N, exp_settings)

if __name__ == "__main__":
    unittest.main() # run all tests