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

class showSubjectSettingsDialogTest(unittest.TestCase):

    def testDefaults(self):
        gui_mock = pgm.PsychoPyGuiMock()        
        
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = ["kontrol", "exp1"]
        experiment.show_subject_settings_dialog()

        self.assertEqual(experiment.identif, "alattomos-aladar")
        self.assertEqual(experiment.subject_nr, 0)
        self.assertEqual(experiment.group, '')

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 2)
        self.assertEqual(list_of_texts[0], "")
        self.assertEqual(list_of_texts[1], "")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 3)
        self.assertEqual(list_of_fields[0].label, "Nev")
        self.assertEqual(list_of_fields[0].initial, 'Alattomos Aladar')
        self.assertEqual(list_of_fields[1].label, "Sorszam")
        self.assertEqual(list_of_fields[1].initial, '0')
        self.assertEqual(list_of_fields[2].label, "Csoport")
        self.assertEqual(list_of_fields[2].initial, '')

    def testCancel(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.setReturnValue(False)

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = ["kontrol", "exp1"]
        with self.assertRaises(SystemExit):
            experiment.show_subject_settings_dialog()

    def testCustomValues(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Béla', 10, 'kontrol'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = ["kontrol", "exp1"]
        subject_settings = experiment.show_subject_settings_dialog()

        self.assertEqual(experiment.identif, "toth-bela")
        self.assertEqual(experiment.subject_nr, 10)
        self.assertEqual(experiment.group, 'kontrol')

    def testAccentCharacters(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['áaéeíióoőöúuűüÁAÉEÍIÓOŐÖÚUŰÜ', 10, 'kontrol'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = ["kontrol", "exp1"]
        experiment.show_subject_settings_dialog()

        self.assertEqual(experiment.identif, "aaeeiioooouuuuaaeeiioooouuuu")
        self.assertEqual(experiment.subject_nr, 10)
        self.assertEqual(experiment.group, 'kontrol')

    def testSpecialCharacters(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['áaée íióoőö úuűüÁA ÉEÍIÓOŐÖ ÚUŰÜ', 10, 'kontrol'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = ["kontrol", "exp1"]
        experiment.show_subject_settings_dialog()

        self.assertEqual(experiment.identif, "aaee-iioooo-uuuuaa-eeiioooo-uuuu")
        self.assertEqual(experiment.subject_nr, 10)
        self.assertEqual(experiment.group, 'kontrol')

    def testInvalidSubjectNumber(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Csaba', 'x', 'kontrol', 'Tóth Csaba', 10, 'kontrol'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = ["kontrol", "exp1"]
        experiment.show_subject_settings_dialog()

        self.assertEqual(experiment.identif, "toth-csaba")
        self.assertEqual(experiment.subject_nr, 10)
        self.assertEqual(experiment.group, 'kontrol')

        # the dialog is displayed twice because for the first time invalid value was specified
        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 4)
        self.assertEqual(list_of_texts[0], "")
        self.assertEqual(list_of_texts[1], "")
        self.assertEqual(list_of_texts[2], "")
        self.assertEqual(list_of_texts[3], "Pozitív egész számot adj meg a sorszámhoz!")

    def testInvalidSubjectNumber2(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(['Tóth Csaba', -10, 'kontrol', 'Tóth Csaba', 10, 'kontrol'])

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = ["kontrol", "exp1"]
        experiment.show_subject_settings_dialog()

        self.assertEqual(experiment.identif, "toth-csaba")
        self.assertEqual(experiment.subject_nr, 10)
        self.assertEqual(experiment.group, 'kontrol')

        # the dialog is displayed twice because for the first time invalid value was specified
        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 4)
        self.assertEqual(list_of_texts[0], "")
        self.assertEqual(list_of_texts[1], "")
        self.assertEqual(list_of_texts[2], "")
        self.assertEqual(list_of_texts[3], "Pozitív egész számot adj meg a sorszámhoz!")
        
    def testNoGroups(self):
        gui_mock = pgm.PsychoPyGuiMock()

        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.groups = []
        experiment.show_subject_settings_dialog()

        self.assertEqual(experiment.identif, "alattomos-aladar")
        self.assertEqual(experiment.subject_nr, 0)
        self.assertEqual(experiment.group, '')

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 2)
        self.assertEqual(list_of_texts[0], "")
        self.assertEqual(list_of_texts[1], "")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 2)
        self.assertEqual(list_of_fields[0].label, "Nev")
        self.assertEqual(list_of_fields[0].initial, 'Alattomos Aladar')
        self.assertEqual(list_of_fields[1].label, "Sorszam")
        self.assertEqual(list_of_fields[1].initial, '0')

if __name__ == "__main__":
    unittest.main() # run all tests 