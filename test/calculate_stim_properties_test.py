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

class calculateStimPropertiesTest(unittest.TestCase):

    def testImplicitASRT(self):

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.epochN = 10
        exp_settings.epochs = [5, 5]
        exp_settings.block_in_epochN = 5
        exp_settings.blockprepN = 5
        exp_settings.blocklengthN = 80
        exp_settings.asrt_rcolor = "Orange"
        exp_settings.asrt_pcolor = "Green"
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "implicit"
        exp_settings.asrt_types[2] = "implicit"

        stim_sessionN = {}
        end_at = {}
        stimepoch = {}
        stimblock = {}
        stimtrial = {}
        stimlist = {}
        stim_colorN = {}
        stimpr = {}
        PCodes = {}
        PCodes [1] = "1st - 1234"
        PCodes [2] = "1st - 1234"
        asrt.calculate_stim_properties(stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, exp_settings)

        self.assertEqual(len(stim_sessionN), exp_settings.getMaxtrial())
        self.assertEqual(len(end_at), exp_settings.getMaxtrial())
        self.assertEqual(len(stimepoch), exp_settings.getMaxtrial())
        self.assertEqual(len(stimblock), exp_settings.getMaxtrial())
        self.assertEqual(len(stimtrial), exp_settings.getMaxtrial())
        self.assertEqual(len(stimlist), exp_settings.getMaxtrial())
        self.assertEqual(len(stim_colorN), exp_settings.getMaxtrial())
        self.assertEqual(len(stimpr), exp_settings.getMaxtrial())

        for i in range(len(stim_sessionN)):
            if i < exp_settings.getMaxtrial() / 2:
                self.assertEqual(stim_sessionN[i+1], 1)
            else:
                self.assertEqual(stim_sessionN[i+1], 2)

        for i in range(len(end_at)):
            if i < exp_settings.getMaxtrial() / 2:
                self.assertEqual(end_at[i+1], exp_settings.getMaxtrial() / 2 + 1)
            else:
                self.assertEqual(end_at[i+1], exp_settings.getMaxtrial() + 1)

        for i in range(len(stimepoch)):
            self.assertEqual(stimepoch[i+1], i // ((exp_settings.blockprepN+exp_settings.blocklengthN)*exp_settings.block_in_epochN) + 1)

        for i in range(len(stimblock)):
            self.assertEqual(stimblock[i+1], i // (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        for i in range(len(stimtrial)):
            self.assertEqual(stimtrial[i+1], i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        oount_4 = 0
        for i in range(len(stimlist)):
            trial_num_in_block = i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1
            if trial_num_in_block > exp_settings.blockprepN and (trial_num_in_block - exp_settings.blockprepN) % 2 == 1:
                if stimlist[i+1] == 1:
                    count_1 += 1
                elif stimlist[i+1] == 2:
                    count_2 += 1
                elif stimlist[i+1] == 3:
                    count_3 += 1
                elif stimlist[i+1] == 4:
                    oount_4 += 1

        self.assertEqual(count_1, 500)
        self.assertEqual(count_2, 500)
        self.assertEqual(count_3, 500)
        self.assertEqual(oount_4, 500)

        # implicit asrt
        for i in range(len(stim_colorN)):
            self.assertEqual(stim_colorN[i+1], "Orange")

        for i in range(len(stimpr)):
            trial_num_in_block = i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1
            if trial_num_in_block > exp_settings.blockprepN and (trial_num_in_block - exp_settings.blockprepN) % 2 == 1:
                self.assertEqual(stimpr[i+1], "P")
            else:
                self.assertEqual(stimpr[i+1], "R")

    def testExplicitASRT(self):

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.epochN = 10
        exp_settings.epochs = [5, 5]
        exp_settings.block_in_epochN = 5
        exp_settings.blockprepN = 5
        exp_settings.blocklengthN = 80
        exp_settings.asrt_rcolor = "Orange"
        exp_settings.asrt_pcolor = "Green"
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "explicit"
        exp_settings.asrt_types[2] = "explicit"

        stim_sessionN = {}
        end_at = {}
        stimepoch = {}
        stimblock = {}
        stimtrial = {}
        stimlist = {}
        stim_colorN = {}
        stimpr = {}
        PCodes = {}
        PCodes [1] = "2nd - 1243"
        PCodes [2] = "3rd - 1324"
        asrt.calculate_stim_properties(stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, exp_settings)

        self.assertEqual(len(stim_sessionN), exp_settings.getMaxtrial())
        self.assertEqual(len(end_at), exp_settings.getMaxtrial())
        self.assertEqual(len(stimepoch), exp_settings.getMaxtrial())
        self.assertEqual(len(stimblock), exp_settings.getMaxtrial())
        self.assertEqual(len(stimtrial), exp_settings.getMaxtrial())
        self.assertEqual(len(stimlist), exp_settings.getMaxtrial())
        self.assertEqual(len(stim_colorN), exp_settings.getMaxtrial())
        self.assertEqual(len(stimpr), exp_settings.getMaxtrial())

        for i in range(len(stim_sessionN)):
            if i < exp_settings.getMaxtrial() / 2:
                self.assertEqual(stim_sessionN[i+1], 1)
            else:
                self.assertEqual(stim_sessionN[i+1], 2)

        for i in range(len(end_at)):
            if i < exp_settings.getMaxtrial() / 2:
                self.assertEqual(end_at[i+1], exp_settings.getMaxtrial() / 2 + 1)
            else:
                self.assertEqual(end_at[i+1], exp_settings.getMaxtrial() + 1)

        for i in range(len(stimepoch)):
            self.assertEqual(stimepoch[i+1], i // ((exp_settings.blockprepN+exp_settings.blocklengthN)*exp_settings.block_in_epochN) + 1)

        for i in range(len(stimblock)):
            self.assertEqual(stimblock[i+1], i // (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        for i in range(len(stimtrial)):
            self.assertEqual(stimtrial[i+1], i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        oount_4 = 0
        for i in range(len(stimlist)):
            trial_num_in_block = i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1
            if trial_num_in_block > exp_settings.blockprepN and (trial_num_in_block - exp_settings.blockprepN) % 2 == 1:
                if stimlist[i+1] == 1:
                    count_1 += 1
                elif stimlist[i+1] == 2:
                    count_2 += 1
                elif stimlist[i+1] == 3:
                    count_3 += 1
                elif stimlist[i+1] == 4:
                    oount_4 += 1

        self.assertEqual(count_1, 500)
        self.assertEqual(count_2, 500)
        self.assertEqual(count_3, 500)
        self.assertEqual(oount_4, 500)

        # implicit asrt
        for i in range(len(stim_colorN)):
            trial_num_in_block = i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1
            if trial_num_in_block > exp_settings.blockprepN and (trial_num_in_block - exp_settings.blockprepN) % 2 == 1:
                self.assertEqual(stim_colorN[i+1], "Green")
            else:
                self.assertEqual(stim_colorN[i+1], "Orange")

        for i in range(len(stimpr)):
            trial_num_in_block = i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1
            if trial_num_in_block > exp_settings.blockprepN and (trial_num_in_block - exp_settings.blockprepN) % 2 == 1:
                self.assertEqual(stimpr[i+1], "P")
            else:
                self.assertEqual(stimpr[i+1], "R")

    def testNoASRT(self):

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.epochN = 5
        exp_settings.epochs = [5]
        exp_settings.block_in_epochN = 5
        exp_settings.blockprepN = 5
        exp_settings.blocklengthN = 80
        exp_settings.asrt_rcolor = "Orange"
        exp_settings.asrt_pcolor = "Green"
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "noASRT"

        stim_sessionN = {}
        end_at = {}
        stimepoch = {}
        stimblock = {}
        stimtrial = {}
        stimlist = {}
        stim_colorN = {}
        stimpr = {}
        PCodes = {}
        PCodes [1] = "noPattern"
        asrt.calculate_stim_properties(stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, exp_settings)

        self.assertEqual(len(stim_sessionN), exp_settings.getMaxtrial())
        self.assertEqual(len(end_at), exp_settings.getMaxtrial())
        self.assertEqual(len(stimepoch), exp_settings.getMaxtrial())
        self.assertEqual(len(stimblock), exp_settings.getMaxtrial())
        self.assertEqual(len(stimtrial), exp_settings.getMaxtrial())
        self.assertEqual(len(stimlist), exp_settings.getMaxtrial())
        self.assertEqual(len(stim_colorN), exp_settings.getMaxtrial())
        self.assertEqual(len(stimpr), exp_settings.getMaxtrial())

        # all trials are in the same session
        for i in range(len(stim_sessionN)):
            self.assertEqual(stim_sessionN[i+1], 1)

        for i in range(len(end_at)):
            self.assertEqual(end_at[i+1], exp_settings.getMaxtrial() + 1)

        for i in range(len(stimepoch)):
            self.assertEqual(stimepoch[i+1], i // ((exp_settings.blockprepN+exp_settings.blocklengthN)*exp_settings.block_in_epochN) + 1)

        for i in range(len(stimblock)):
            self.assertEqual(stimblock[i+1], i // (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        for i in range(len(stimtrial)):
            self.assertEqual(stimtrial[i+1], i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        oount_4 = 0
        for i in range(len(stimlist)):
            trial_num_in_block = i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1
            if trial_num_in_block > exp_settings.blockprepN and (trial_num_in_block - exp_settings.blockprepN) % 2 == 1:
                if stimlist[i+1] == 1:
                    count_1 += 1
                elif stimlist[i+1] == 2:
                    count_2 += 1
                elif stimlist[i+1] == 3:
                    count_3 += 1
                elif stimlist[i+1] == 4:
                    oount_4 += 1

        # randomized data
        self.assertTrue(count_1 != count_2)
        self.assertTrue(count_3 != oount_4)

        # implicit asrt
        for i in range(len(stim_colorN)):
            self.assertEqual(stim_colorN[i+1], "Orange")

        for i in range(len(stimpr)):
            self.assertEqual(stimpr[i+1], "R")

    def testASRTWithoutPractice(self):

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.epochN = 5
        exp_settings.epochs = [5]
        exp_settings.block_in_epochN = 5
        exp_settings.blockprepN = 0
        exp_settings.blocklengthN = 80
        exp_settings.asrt_rcolor = "Orange"
        exp_settings.asrt_pcolor = "Green"
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "implicit"

        stim_sessionN = {}
        end_at = {}
        stimepoch = {}
        stimblock = {}
        stimtrial = {}
        stimlist = {}
        stim_colorN = {}
        stimpr = {}
        PCodes = {}
        PCodes [1] = "1st - 1234"
        asrt.calculate_stim_properties(stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, exp_settings)

        self.assertEqual(len(stim_sessionN), exp_settings.getMaxtrial())
        self.assertEqual(len(end_at), exp_settings.getMaxtrial())
        self.assertEqual(len(stimepoch), exp_settings.getMaxtrial())
        self.assertEqual(len(stimblock), exp_settings.getMaxtrial())
        self.assertEqual(len(stimtrial), exp_settings.getMaxtrial())
        self.assertEqual(len(stimlist), exp_settings.getMaxtrial())
        self.assertEqual(len(stim_colorN), exp_settings.getMaxtrial())
        self.assertEqual(len(stimpr), exp_settings.getMaxtrial())

        # all trials are in the same session
        for i in range(len(stim_sessionN)):
            self.assertEqual(stim_sessionN[i+1], 1)

        for i in range(len(end_at)):
            self.assertEqual(end_at[i+1], exp_settings.getMaxtrial() + 1)

        for i in range(len(stimepoch)):
            self.assertEqual(stimepoch[i+1], i // ((exp_settings.blockprepN+exp_settings.blocklengthN)*exp_settings.block_in_epochN) + 1)

        for i in range(len(stimblock)):
            self.assertEqual(stimblock[i+1], i // (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        for i in range(len(stimtrial)):
            self.assertEqual(stimtrial[i+1], i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        oount_4 = 0
        for i in range(len(stimlist)):
            trial_num_in_block = i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1
            if trial_num_in_block > exp_settings.blockprepN and (trial_num_in_block - exp_settings.blockprepN) % 2 == 1:
                if stimlist[i+1] == 1:
                    count_1 += 1
                elif stimlist[i+1] == 2:
                    count_2 += 1
                elif stimlist[i+1] == 3:
                    count_3 += 1
                elif stimlist[i+1] == 4:
                    oount_4 += 1

        self.assertEqual(count_1, 250)
        self.assertEqual(count_2, 250)
        self.assertEqual(count_3, 250)
        self.assertEqual(oount_4, 250)

        # implicit asrt
        for i in range(len(stim_colorN)):
            self.assertEqual(stim_colorN[i+1], "Orange")

        for i in range(len(stimpr)):
            trial_num_in_block = i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1
            if trial_num_in_block > exp_settings.blockprepN and (trial_num_in_block - exp_settings.blockprepN) % 2 == 1:
                self.assertEqual(stimpr[i+1], "P")
            else:
                self.assertEqual(stimpr[i+1], "R")

    def testASRTWithoutReal(self):
        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.epochN = 5
        exp_settings.epochs = [5]
        exp_settings.block_in_epochN = 5
        exp_settings.blockprepN = 5
        exp_settings.blocklengthN = 0
        exp_settings.asrt_rcolor = "Orange"
        exp_settings.asrt_pcolor = "Green"
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "implicit"

        stim_sessionN = {}
        end_at = {}
        stimepoch = {}
        stimblock = {}
        stimtrial = {}
        stimlist = {}
        stim_colorN = {}
        stimpr = {}
        PCodes = {}
        PCodes [1] = "1st - 1234"
        asrt.calculate_stim_properties(stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, exp_settings)

        self.assertEqual(len(stim_sessionN), exp_settings.getMaxtrial())
        self.assertEqual(len(end_at), exp_settings.getMaxtrial())
        self.assertEqual(len(stimepoch), exp_settings.getMaxtrial())
        self.assertEqual(len(stimblock), exp_settings.getMaxtrial())
        self.assertEqual(len(stimtrial), exp_settings.getMaxtrial())
        self.assertEqual(len(stimlist), exp_settings.getMaxtrial())
        self.assertEqual(len(stim_colorN), exp_settings.getMaxtrial())
        self.assertEqual(len(stimpr), exp_settings.getMaxtrial())

        # all trials are in the same session
        for i in range(len(stim_sessionN)):
            self.assertEqual(stim_sessionN[i+1], 1)

        for i in range(len(end_at)):
            self.assertEqual(end_at[i+1], exp_settings.getMaxtrial() + 1)

        for i in range(len(stimepoch)):
            self.assertEqual(stimepoch[i+1], i // ((exp_settings.blockprepN+exp_settings.blocklengthN)*exp_settings.block_in_epochN) + 1)

        for i in range(len(stimblock)):
            self.assertEqual(stimblock[i+1], i // (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        for i in range(len(stimtrial)):
            self.assertEqual(stimtrial[i+1], i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        # random only
        for i in range(len(stim_colorN)):
            self.assertEqual(stim_colorN[i+1], "Orange")

        # random only
        for i in range(len(stimpr)):
            self.assertEqual(stimpr[i+1], "R")

    def testWithEvenPracticeTrials(self):

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.epochN = 5
        exp_settings.epochs = [5]
        exp_settings.block_in_epochN = 5
        exp_settings.blockprepN = 6
        exp_settings.blocklengthN = 80
        exp_settings.asrt_rcolor = "Orange"
        exp_settings.asrt_pcolor = "Green"
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "implicit"

        stim_sessionN = {}
        end_at = {}
        stimepoch = {}
        stimblock = {}
        stimtrial = {}
        stimlist = {}
        stim_colorN = {}
        stimpr = {}
        PCodes = {}
        PCodes [1] = "1st - 1234"
        asrt.calculate_stim_properties(stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, exp_settings)

        self.assertEqual(len(stim_sessionN), exp_settings.getMaxtrial())
        self.assertEqual(len(end_at), exp_settings.getMaxtrial())
        self.assertEqual(len(stimepoch), exp_settings.getMaxtrial())
        self.assertEqual(len(stimblock), exp_settings.getMaxtrial())
        self.assertEqual(len(stimtrial), exp_settings.getMaxtrial())
        self.assertEqual(len(stimlist), exp_settings.getMaxtrial())
        self.assertEqual(len(stim_colorN), exp_settings.getMaxtrial())
        self.assertEqual(len(stimpr), exp_settings.getMaxtrial())

        # all trials are in the same session
        for i in range(len(stim_sessionN)):
            self.assertEqual(stim_sessionN[i+1], 1)

        for i in range(len(end_at)):
            self.assertEqual(end_at[i+1], exp_settings.getMaxtrial() + 1)

        for i in range(len(stimepoch)):
            self.assertEqual(stimepoch[i+1], i // ((exp_settings.blockprepN+exp_settings.blocklengthN)*exp_settings.block_in_epochN) + 1)

        for i in range(len(stimblock)):
            self.assertEqual(stimblock[i+1], i // (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        for i in range(len(stimtrial)):
            self.assertEqual(stimtrial[i+1], i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        oount_4 = 0
        for i in range(len(stimlist)):
            trial_num_in_block = i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1
            if trial_num_in_block > exp_settings.blockprepN and (trial_num_in_block - exp_settings.blockprepN) % 2 == 1:
                if stimlist[i+1] == 1:
                    count_1 += 1
                elif stimlist[i+1] == 2:
                    count_2 += 1
                elif stimlist[i+1] == 3:
                    count_3 += 1
                elif stimlist[i+1] == 4:
                    oount_4 += 1

        self.assertEqual(count_1, 250)
        self.assertEqual(count_2, 250)
        self.assertEqual(count_3, 250)
        self.assertEqual(oount_4, 250)

        # implicit asrt
        for i in range(len(stim_colorN)):
            self.assertEqual(stim_colorN[i+1], "Orange")

        for i in range(len(stimpr)):
            trial_num_in_block = i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1
            if trial_num_in_block > exp_settings.blockprepN and (trial_num_in_block - exp_settings.blockprepN) % 2 == 1:
                self.assertEqual(stimpr[i+1], "P")
            else:
                self.assertEqual(stimpr[i+1], "R")

    def testWithOddRealTrials(self):

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.epochN = 5
        exp_settings.epochs = [5]
        exp_settings.block_in_epochN = 5
        exp_settings.blockprepN = 6
        exp_settings.blocklengthN = 75
        exp_settings.asrt_rcolor = "Orange"
        exp_settings.asrt_pcolor = "Green"
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "implicit"

        stim_sessionN = {}
        end_at = {}
        stimepoch = {}
        stimblock = {}
        stimtrial = {}
        stimlist = {}
        stim_colorN = {}
        stimpr = {}
        PCodes = {}
        PCodes [1] = "1st - 1234"
        asrt.calculate_stim_properties(stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, exp_settings)

        self.assertEqual(len(stim_sessionN), exp_settings.getMaxtrial())
        self.assertEqual(len(end_at), exp_settings.getMaxtrial())
        self.assertEqual(len(stimepoch), exp_settings.getMaxtrial())
        self.assertEqual(len(stimblock), exp_settings.getMaxtrial())
        self.assertEqual(len(stimtrial), exp_settings.getMaxtrial())
        self.assertEqual(len(stimlist), exp_settings.getMaxtrial())
        self.assertEqual(len(stim_colorN), exp_settings.getMaxtrial())
        self.assertEqual(len(stimpr), exp_settings.getMaxtrial())

        # all trials are in the same session
        for i in range(len(stim_sessionN)):
            self.assertEqual(stim_sessionN[i+1], 1)

        for i in range(len(end_at)):
            self.assertEqual(end_at[i+1], exp_settings.getMaxtrial() + 1)

        for i in range(len(stimepoch)):
            self.assertEqual(stimepoch[i+1], i // ((exp_settings.blockprepN+exp_settings.blocklengthN)*exp_settings.block_in_epochN) + 1)

        for i in range(len(stimblock)):
            self.assertEqual(stimblock[i+1], i // (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        for i in range(len(stimtrial)):
            self.assertEqual(stimtrial[i+1], i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        oount_4 = 0
        for i in range(len(stimlist)):
            trial_num_in_block = i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1
            if trial_num_in_block > exp_settings.blockprepN and (trial_num_in_block - exp_settings.blockprepN) % 2 == 1:
                if stimlist[i+1] == 1:
                    count_1 += 1
                elif stimlist[i+1] == 2:
                    count_2 += 1
                elif stimlist[i+1] == 3:
                    count_3 += 1
                elif stimlist[i+1] == 4:
                    oount_4 += 1

        # there are some variance in the number, becuase some pattern trials are cut down at the end of the blocks
        self.assertAlmostEqual(count_1, 237, delta=5)
        self.assertAlmostEqual(count_2, 237, delta=5)
        self.assertAlmostEqual(count_3, 237, delta=5)
        self.assertAlmostEqual(oount_4, 237, delta=5)

        # implicit asrt
        for i in range(len(stim_colorN)):
            self.assertEqual(stim_colorN[i+1], "Orange")

        for i in range(len(stimpr)):
            trial_num_in_block = i % (exp_settings.blockprepN+exp_settings.blocklengthN) + 1
            if trial_num_in_block > exp_settings.blockprepN and (trial_num_in_block - exp_settings.blockprepN) % 2 == 1:
                self.assertEqual(stimpr[i+1], "P")
            else:
                self.assertEqual(stimpr[i+1], "R")

if __name__ == "__main__":
    unittest.main() # run all tests