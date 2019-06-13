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
sys.path = [".."] + sys.path

import asrt

class whichCodeTest(unittest.TestCase):

    def testRightPatterns(self):
        PCodes = { 1: "6th - 1432", 2 : '4th - 1342', 3 : '5th - 1423', 4 : '3rd - 1324', 5 : '1st - 1234', 6 : '2nd - 1243'}

        self.assertEqual(asrt.which_code(1, PCodes), "1432")
        self.assertEqual(asrt.which_code(2, PCodes), "1342")
        self.assertEqual(asrt.which_code(3, PCodes), "1423")
        self.assertEqual(asrt.which_code(4, PCodes), "1324")
        self.assertEqual(asrt.which_code(5, PCodes), "1234")
        self.assertEqual(asrt.which_code(6, PCodes), "1243")

    def testTypoInPCode(self):
        PCodes = {1 : "6tj - 1432"}
        self.assertEqual(asrt.which_code(1, PCodes), "noPattern")

    def testNoPattern(self):
        PCodes = {1 : "noPattern"}
        self.assertEqual(asrt.which_code(1, PCodes), "noPattern")

    def testWrongSession(self):
        PCodes = {1 : "6th - 1432", 2 : '4th - 1342', 3 : '5th - 1423', 4 : '3rd - 1324', 5 : '1st - 1234', 6 : '2nd - 1243'}
        with self.assertRaises(KeyError):
            asrt.which_code(7, PCodes)
        with self.assertRaises(KeyError):
            asrt.which_code(0, PCodes)

if __name__ == "__main__":
    unittest.main() # run all tests