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
#    along with this program.  If not, see <http://www.gnu.org/licenses

#!\\usr\\bin\\env python
# -*- coding: utf-8 -*-

import unittest

import sys
# Add the local path to the main script so we can import it.
sys.path = [".."] + sys.path

import asrt

import psychopy_gui_mock as pgm

dict_accents = {u'á':u'a',u'é':u'e',u'í':u'i',u'ó':u'o',u'ő':u'o',u'ö':u'o',u'ú':u'u',u'ű':u'u',u'ü':u'u',
                u'Á':u'A',u'É':u'E',u'Í':u'I',u'Ó':u'O',u'Ö':u'O',u'Ő':u'O',u'Ú':u'U',u'Ű':u'U',u'Ü':u'U'}

class showGroupSettingsDialogTest(unittest.TestCase):

    def testDefault(self):
        gui_mock = pgm.PsychoPyGuiMock()
        groups = []
        groups = asrt.show_group_settings_dialog(2, dict_accents)

        self.assertEqual(len(groups), 2)

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "A csoportok megnevezése a következő (pl. kísérleti, kontroll, ....) ")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 2)
        self.assertEqual(list_of_fields[0].label, "Csoport 1")
        self.assertEqual(list_of_fields[1].label, "Csoport 2")

    def testMoreGropus(self):
        gui_mock = pgm.PsychoPyGuiMock()
        groups = []
        numgroups = 3
        groups = asrt.show_group_settings_dialog(numgroups, dict_accents)

        self.assertEqual(len(groups), numgroups)

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 1)
        self.assertEqual(list_of_texts[0], "A csoportok megnevezése a következő (pl. kísérleti, kontroll, ....) ")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), numgroups)
        self.assertEqual(list_of_fields[0].label, "Csoport 1")
        self.assertEqual(list_of_fields[1].label, "Csoport 2")
        self.assertEqual(list_of_fields[2].label, "Csoport 3")

    def testNoGroup(self):
        gui_mock = pgm.PsychoPyGuiMock()
        groups = []
        numgroups = 0
        groups = asrt.show_group_settings_dialog(numgroups, dict_accents)

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0], "nincsenek csoportok")

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 0)

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), numgroups)

    def testCancel(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.setReturnValue(False)
        groups = []
        numgroups = 2
        with self.assertRaises(SystemExit):
            groups = asrt.show_group_settings_dialog(numgroups, dict_accents)

    def testAccentCharacters(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(["áaéeíióoőöúuűüÁAÉEÍIÓOŐÖÚUŰÜ", "kontrol"])
        groups = []
        numgroups = 2
        groups = asrt.show_group_settings_dialog(numgroups, dict_accents)

        self.assertEqual(len(groups), numgroups)
        self.assertEqual(groups[0], "aaeeiioooouuuuaaeeiioooouuuu")
        self.assertEqual(groups[1], "kontrol")

    def testSpecialCharacters(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues(["áaéeíió-oőö-úuű-üÁ AÉEÍ IÓOŐ ÖÚUŰÜ", "kontrol"])
        groups = []
        numgroups = 2
        groups = asrt.show_group_settings_dialog(numgroups, dict_accents)

        self.assertEqual(len(groups), numgroups)
        self.assertEqual(groups[0], "aaeeiio_ooo_uuu_ua_aeei_iooo_ouuuu")
        self.assertEqual(groups[1], "kontrol")


if __name__ == "__main__":
    unittest.main() # run all tests