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
# Add the local path to the main script so we can import it.
sys.path = [".."] + sys.path

import unittest
import asrt


class whichCodeTest(unittest.TestCase):

    def testRightPatterns(self):
        experiment = asrt.Experiment("")
        experiment.PCodes = {1: "6th - 1432", 2: '4th - 1342',
                             3: '5th - 1423', 4: '3rd - 1324', 5: '1st - 1234', 6: '2nd - 1243'}

        self.assertEqual(experiment.which_code(1), "1432")
        self.assertEqual(experiment.which_code(2), "1342")
        self.assertEqual(experiment.which_code(3), "1423")
        self.assertEqual(experiment.which_code(4), "1324")
        self.assertEqual(experiment.which_code(5), "1234")
        self.assertEqual(experiment.which_code(6), "1243")

    def testTypoInPCode(self):
        experiment = asrt.Experiment("")
        experiment.PCodes = {1: "6tj - 1432"}
        self.assertEqual(experiment.which_code(1), "noPattern")

    def testNoPattern(self):
        experiment = asrt.Experiment("")
        experiment.PCodes = {1: "noPattern"}
        self.assertEqual(experiment.which_code(1), "noPattern")

    def testWrongSession(self):
        experiment = asrt.Experiment("")
        experiment.PCodes = {1: "6th - 1432", 2: '4th - 1342',
                             3: '5th - 1423', 4: '3rd - 1324', 5: '1st - 1234', 6: '2nd - 1243'}
        with self.assertRaises(KeyError):
            experiment.which_code(7)
        with self.assertRaises(KeyError):
            experiment.which_code(0)


if __name__ == "__main__":
    unittest.main()  # run all tests
