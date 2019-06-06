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

possible_colors = ["AliceBlue","AntiqueWhite","Aqua","Aquamarine","Azure","Beige","Bisque","Black","BlanchedAlmond","Blue","BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGrey","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","DarkOrange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkSlateGrey","DarkTurquoise","DarkViolet","DeepPink","DeepSkyBlue","DimGray","DimGrey","DodgerBlue","FireBrick","FloralWhite","ForestGreen","Fuchsia","Gainsboro","GhostWhite","Gold","GoldenRod","Gray","Grey","Green","GreenYellow","HoneyDew","HotPink","IndianRed","Indigo","Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGrey","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray","LightSlateGrey","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen","MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive","OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue","Purple","RebeccaPurple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray","SlateGrey","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","White","WhiteSmoke","Yellow","YellowGreen"]

class showComputerAndDisplaySettingsDialogTest(unittest.TestCase):

    def testDefaults(self):
        gui_mock = pgm.PsychoPyGuiMock()

        computer_and_display_settings = asrt.show_computer_and_display_settings_dialog(possible_colors)
        monitor_width = computer_and_display_settings["monitor_width"]
        computer_name = computer_and_display_settings["computer_name"]
        refreshrate = computer_and_display_settings["refreshrate"]
        asrt_distance = computer_and_display_settings["asrt_distance"]
        asrt_size = computer_and_display_settings["asrt_size"]
        asrt_rcolor = computer_and_display_settings["asrt_rcolor"]
        asrt_pcolor = computer_and_display_settings["asrt_pcolor"]
        asrt_background = computer_and_display_settings["asrt_background"]
        asrt_circle_background = computer_and_display_settings["asrt_circle_background"]
        RSI_time = computer_and_display_settings["RSI_time"]

        self.assertEqual(monitor_width, 34.2)
        self.assertEqual(computer_name, "Laposka")
        self.assertEqual(refreshrate, 60)
        self.assertEqual(asrt_distance, 3)
        self.assertEqual(asrt_size, 1)
        self.assertEqual(asrt_rcolor, "Orange")
        self.assertEqual(asrt_pcolor, "Green")
        self.assertEqual(asrt_background, "Ivory")
        self.assertEqual(asrt_circle_background, "Beige")
        self.assertEqual(RSI_time, 0.12)

        list_of_texts = gui_mock.getListOfTexts()
        self.assertEqual(len(list_of_texts), 2)
        self.assertEqual(list_of_texts[0], "A számítógépről...")
        self.assertEqual(list_of_texts[1], "Megjelenés..")

        list_of_fields = gui_mock.getListOfFields()
        self.assertEqual(len(list_of_fields), 10)
        self.assertEqual(list_of_fields[0].label, "Hasznos kepernyo szelessege (cm)")
        self.assertEqual(list_of_fields[0].initial, 34.2)
        self.assertEqual(list_of_fields[1].label, "Szamitogep fantazianeve (ekezet nelkul)")
        self.assertEqual(list_of_fields[1].initial, "Laposka")
        self.assertEqual(list_of_fields[2].label, "Kepernyofrissitesi frekvencia (Hz)")
        self.assertEqual(list_of_fields[2].initial, 60)
        self.assertEqual(list_of_fields[3].label, "Ingerek tavolsaga (kozeppontok kozott) (cm)")
        self.assertEqual(list_of_fields[3].initial, 3)
        self.assertEqual(list_of_fields[4].label, "Ingerek sugara (cm)")
        self.assertEqual(list_of_fields[4].initial, 1)
        self.assertEqual(list_of_fields[5].label, "ASRT inger szine (elsodleges, R)")
        self.assertEqual(list_of_fields[5].initial, "Orange")
        self.assertEqual(list_of_fields[6].label, "ASRT inger szine (masodlagos, P, explicit asrtnel)")
        self.assertEqual(list_of_fields[6].initial, "Green")
        self.assertEqual(list_of_fields[7].label, "Hatter szine")
        self.assertEqual(list_of_fields[7].initial, "Ivory")
        self.assertEqual(list_of_fields[8].label, "Nem aktiv inger szine")
        self.assertEqual(list_of_fields[8].initial, "Beige")
        self.assertEqual(list_of_fields[9].label, "RSI (ms)")
        self.assertEqual(list_of_fields[9].initial, 120)

    def testCancel(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.setReturnValue(False)

        with self.assertRaises(SystemExit):
            asrt.show_computer_and_display_settings_dialog(possible_colors)

    def testCustomValues(self):
        gui_mock = pgm.PsychoPyGuiMock()
        gui_mock.addFieldValues([17, "Alma", 51, 2.3, 1.2, "Black", "White", "Green", "Orange", 205])

        computer_and_display_settings = asrt.show_computer_and_display_settings_dialog(possible_colors)
        monitor_width = computer_and_display_settings["monitor_width"]
        computer_name = computer_and_display_settings["computer_name"]
        refreshrate = computer_and_display_settings["refreshrate"]
        asrt_distance = computer_and_display_settings["asrt_distance"]
        asrt_size = computer_and_display_settings["asrt_size"]
        asrt_rcolor = computer_and_display_settings["asrt_rcolor"]
        asrt_pcolor = computer_and_display_settings["asrt_pcolor"]
        asrt_background = computer_and_display_settings["asrt_background"]
        asrt_circle_background = computer_and_display_settings["asrt_circle_background"]
        RSI_time = computer_and_display_settings["RSI_time"]

        self.assertEqual(monitor_width, 17)
        self.assertEqual(computer_name, "Alma")
        self.assertEqual(refreshrate, 51)
        self.assertEqual(asrt_distance, 2.3)
        self.assertEqual(asrt_size, 1.2)
        self.assertEqual(asrt_rcolor, "Black")
        self.assertEqual(asrt_pcolor, "White")
        self.assertEqual(asrt_background, "Green")
        self.assertEqual(asrt_circle_background, "Orange")
        self.assertEqual(RSI_time, 0.205)

if __name__ == "__main__":
    unittest.main() # run all tests