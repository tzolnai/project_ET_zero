#    Copyright (C) <2018>  <Tamás Zolnai>    <zolnaitamas2000@gmail.com>

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

class showEpochAndBlockSettingsDialogTest(unittest.TestCase):

    def testDefaults(self):
        gui_mock = pgm.PsychoPyGuiMock()

        numsessions = 1
        epoch_block_result = asrt.show_epoch_and_block_settings_dialog(numsessions)
        blockprepN = epoch_block_result["blockprepN"]
        blocklengthN = epoch_block_result["blocklengthN"]
        block_in_epochN = epoch_block_result["block_in_epochN"]
        epochN = epoch_block_result["epochN"]
        epochs = epoch_block_result["epochs"]
        asrt_types = epoch_block_result["asrt_types"]

        self.assertEqual(blockprepN, 5)
        self.assertEqual(blocklengthN, 80)
        self.assertEqual(block_in_epochN, 5)
        self.assertEqual(epochN, 5)
        self.assertEqual(len(epochs), 1)
        self.assertEqual(epochs[0], 5)
        self.assertEqual(len(asrt_types), 1)
        self.assertEqual(asrt_types[1], '')

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "Kísérlet felépítése ")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 5)
        self.assertEqual(list_of_fields[0].label, "Randomok gyakorlaskent a blokk elejen (ennyi db):")
        self.assertEqual(list_of_fields[0].initial, 5)
        self.assertEqual(list_of_fields[1].label, "Eles probak a blokkban:")
        self.assertEqual(list_of_fields[1].initial, 80)
        self.assertEqual(list_of_fields[2].label, "Blokkok szama egy epochban:")
        self.assertEqual(list_of_fields[2].initial, 5)
        self.assertEqual(list_of_fields[3].label, "Session 1 epochok szama")
        self.assertEqual(list_of_fields[3].initial, 5)
        self.assertEqual(list_of_fields[4].label, "Session 1 ASRT tipusa")
        self.assertEqual(list_of_fields[4].initial, '')

    def testCancel(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.setReturnValue(False)

        numsessions = 1
        with self.assertRaises(SystemExit):
            epoch_block_result = asrt.show_epoch_and_block_settings_dialog(numsessions)

    def testNoSessions(self):
        gui_mock = pgm.PsychoPyGuiMock()

        numsessions = 0
        epoch_block_result = asrt.show_epoch_and_block_settings_dialog(numsessions)
        blockprepN = epoch_block_result["blockprepN"]
        blocklengthN = epoch_block_result["blocklengthN"]
        block_in_epochN = epoch_block_result["block_in_epochN"]
        epochN = epoch_block_result["epochN"]
        epochs = epoch_block_result["epochs"]
        asrt_types = epoch_block_result["asrt_types"]

        self.assertEqual(blockprepN, 5)
        self.assertEqual(blocklengthN, 80)
        self.assertEqual(block_in_epochN, 5)
        self.assertEqual(epochN, 0)
        self.assertEqual(len(epochs), 0)
        self.assertEqual(len(asrt_types), 0)

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "Kísérlet felépítése ")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 3)
        self.assertEqual(list_of_fields[0].label, "Randomok gyakorlaskent a blokk elejen (ennyi db):")
        self.assertEqual(list_of_fields[0].initial, 5)
        self.assertEqual(list_of_fields[1].label, "Eles probak a blokkban:")
        self.assertEqual(list_of_fields[1].initial, 80)
        self.assertEqual(list_of_fields[2].label, "Blokkok szama egy epochban:")
        self.assertEqual(list_of_fields[2].initial, 5)

    def testMoreSessions(self):
        gui_mock = pgm.PsychoPyGuiMock()

        numsessions = 3
        epoch_block_result = asrt.show_epoch_and_block_settings_dialog(numsessions)
        blockprepN = epoch_block_result["blockprepN"]
        blocklengthN = epoch_block_result["blocklengthN"]
        block_in_epochN = epoch_block_result["block_in_epochN"]
        epochN = epoch_block_result["epochN"]
        epochs = epoch_block_result["epochs"]
        asrt_types = epoch_block_result["asrt_types"]

        self.assertEqual(blockprepN, 5)
        self.assertEqual(blocklengthN, 80)
        self.assertEqual(block_in_epochN, 5)
        self.assertEqual(epochN, 15)
        self.assertEqual(len(epochs), 3)
        self.assertEqual(epochs[0], 5)
        self.assertEqual(epochs[1], 5)
        self.assertEqual(epochs[2], 5)
        self.assertEqual(len(asrt_types), 3)

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "Kísérlet felépítése ")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 9)
        self.assertEqual(list_of_fields[0].label, "Randomok gyakorlaskent a blokk elejen (ennyi db):")
        self.assertEqual(list_of_fields[0].initial, 5)
        self.assertEqual(list_of_fields[1].label, "Eles probak a blokkban:")
        self.assertEqual(list_of_fields[1].initial, 80)
        self.assertEqual(list_of_fields[2].label, "Blokkok szama egy epochban:")
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
        gui_mock.addFieldValues([12, 79, 2, 3, 12, 7, 'implicit', 'explicit', 'noASRT'])

        numsessions = 3
        epoch_block_result = asrt.show_epoch_and_block_settings_dialog(numsessions)
        blockprepN = epoch_block_result["blockprepN"]
        blocklengthN = epoch_block_result["blocklengthN"]
        block_in_epochN = epoch_block_result["block_in_epochN"]
        epochN = epoch_block_result["epochN"]
        epochs = epoch_block_result["epochs"]
        asrt_types = epoch_block_result["asrt_types"]

        self.assertEqual(blockprepN, 12)
        self.assertEqual(blocklengthN, 79)
        self.assertEqual(block_in_epochN, 2)
        self.assertEqual(epochN, 22)
        self.assertEqual(len(epochs), 3)
        self.assertEqual(epochs[0], 3)
        self.assertEqual(epochs[1], 12)
        self.assertEqual(epochs[2], 7)
        self.assertEqual(len(asrt_types), 3)
        self.assertEqual(asrt_types[1], 'implicit')
        self.assertEqual(asrt_types[2], 'explicit')
        self.assertEqual(asrt_types[3], 'noASRT')

if __name__ == "__main__":
    unittest.main() # run all tests