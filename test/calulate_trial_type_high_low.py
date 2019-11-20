# !/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) <2019>  <Tamás Zolnai>    <zolnaitamas2000@gmail.com>

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
import time
import shelve
import dbm
import codecs
from psychopy import monitors


class calculateTripletTypeHighLowTest(unittest.TestCase):

    def testNoPattern(self):
        experiment = asrt.Experiment("")
        experiment.stim_sessionN = {1: 1}
        experiment.PCodes = {1: 'noPattern'}

        triplet_type = experiment.calulate_trial_type_high_low(1)
        self.assertEqual(triplet_type, "none")

    def testFirstTwoTrials(self):
        experiment = asrt.Experiment("")
        experiment.stimtrial = {1: 1, 2: 2}
        experiment.stim_sessionN = {1: 1, 2: 1}
        experiment.PCodes = {1: '1st - 1234'}

        triplet_type = experiment.calulate_trial_type_high_low(1)
        self.assertEqual(triplet_type, "none")

        triplet_type = experiment.calulate_trial_type_high_low(2)
        self.assertEqual(triplet_type, "none")

    def testHighPattern(self):
        experiment = asrt.Experiment("")
        experiment.stimtrial = {1: 1, 2: 2, 3: 3}
        experiment.stim_sessionN = {1: 1, 2: 1, 3: 1}
        experiment.stimpr = {1: "pattern", 2: "random", 3: "pattern"}
        experiment.PCodes = {1: '1st - 1234'}

        triplet_type = experiment.calulate_trial_type_high_low(3)
        self.assertEqual(triplet_type, "high")

    def testLowRandom(self):
        experiment = asrt.Experiment("")
        experiment.stim_sessionN = {1: 1, 2: 1, 3: 1, 4: 1}
        experiment.PCodes = {1: '1st - 1234'}
        experiment.stimtrial = {1: 1, 2: 2, 3: 3, 4: 4}
        experiment.stimpr = {1: "pattern", 2: "random", 3: "pattern", 4: "random"}
        experiment.stimlist = {1: 1, 2: 2, 3: 2, 4: 4}

        triplet_type = experiment.calulate_trial_type_high_low(4)
        self.assertEqual(triplet_type, "low")

    def testHighRandom(self):
        experiment = asrt.Experiment("")
        experiment.stim_sessionN = {1: 1, 2: 1, 3: 1, 4: 1}
        experiment.PCodes = {1: '1st - 1234'}
        experiment.stimtrial = {1: 1, 2: 2, 3: 3, 4: 4}
        experiment.stimpr = {1: "pattern", 2: "random", 3: "pattern", 4: "random"}
        experiment.stimlist = {1: 1, 2: 3, 3: 2, 4: 4}

        triplet_type = experiment.calulate_trial_type_high_low(4)
        self.assertEqual(triplet_type, "high")

if __name__ == "__main__":
    unittest.main()  # run all tests
