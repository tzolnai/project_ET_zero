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


class calculateStimpropertiesTest(unittest.TestCase):

    def testImplicitASRT(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.epochN = 10
        experiment.settings.epochs = [5, 5]
        experiment.settings.block_in_epochN = 5
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.asrt_rcolor = "Orange"
        experiment.settings.asrt_pcolor = "Green"
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit', 3: 'implicit', 4: 'implicit', 5: 'implicit', 6: 'implicit', 7: 'implicit',
                                          8: 'implicit', 9: 'implicit', 10: 'implicit', 11: 'implicit', 12: 'implicit'}

        experiment.stim_sessionN = {}
        experiment.end_at = {}
        experiment.stimepoch = {}
        experiment.stimblock = {}
        experiment.stimtrial = {}
        experiment.stimlist = {}
        experiment.stimpr = {}
        experiment.PCodes = {}
        for i in range(experiment.settings.epochN):
            experiment.PCodes[i + 1] = "1st - 1234"
        experiment.calculate_stim_properties()

        self.assertEqual(len(experiment.stim_sessionN),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.end_at),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimepoch),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimblock),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimtrial),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimlist),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimpr),
                         experiment.settings.get_maxtrial())

        for i in range(len(experiment.stim_sessionN)):
            if i < experiment.settings.get_maxtrial() / 2:
                self.assertEqual(experiment.stim_sessionN[i + 1], 1)
            else:
                self.assertEqual(experiment.stim_sessionN[i + 1], 2)

        for i in range(len(experiment.end_at)):
            if i < experiment.settings.get_maxtrial() / 2:
                self.assertEqual(
                    experiment.end_at[i + 1], experiment.settings.get_maxtrial() / 2 + 1)
            else:
                self.assertEqual(
                    experiment.end_at[i + 1], experiment.settings.get_maxtrial() + 1)

        for i in range(len(experiment.stimepoch)):
            self.assertEqual(experiment.stimepoch[i + 1], i // ((experiment.settings.blockprepN +
                                                                 experiment.settings.blocklengthN) * experiment.settings.block_in_epochN) + 1)

        for i in range(len(experiment.stimblock)):
            self.assertEqual(experiment.stimblock[i + 1], i // (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        for i in range(len(experiment.stimtrial)):
            self.assertEqual(experiment.stimtrial[i + 1], i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        oount_4 = 0
        for i in range(len(experiment.stimlist)):
            trial_num_in_block = i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
            if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                if experiment.stimlist[i + 1] == 1:
                    count_1 += 1
                elif experiment.stimlist[i + 1] == 2:
                    count_2 += 1
                elif experiment.stimlist[i + 1] == 3:
                    count_3 += 1
                elif experiment.stimlist[i + 1] == 4:
                    oount_4 += 1

        self.assertEqual(count_1, 500)
        self.assertEqual(count_2, 500)
        self.assertEqual(count_3, 500)
        self.assertEqual(oount_4, 500)

        for i in range(len(experiment.stimpr)):
            trial_num_in_block = i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
            if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                self.assertEqual(experiment.stimpr[i + 1], "pattern")
            else:
                self.assertEqual(experiment.stimpr[i + 1], "random")

    def testExplicitASRT(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.epochN = 10
        experiment.settings.epochs = [5, 5]
        experiment.settings.block_in_epochN = 5
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.asrt_rcolor = "Orange"
        experiment.settings.asrt_pcolor = "Green"
        experiment.settings.asrt_types = {1: 'explicit', 2: 'explicit', 3: 'explicit', 4: 'explicit', 5: 'explicit', 6: 'explicit', 7: 'explicit',
                                          8: 'explicit', 9: 'explicit', 10: 'explicit', 11: 'explicit', 12: 'explicit'}

        experiment.stim_sessionN = {}
        experiment.end_at = {}
        experiment.stimepoch = {}
        experiment.stimblock = {}
        experiment.stimtrial = {}
        experiment.stimlist = {}
        experiment.stimpr = {}
        experiment.PCodes = {}
        for i in range(experiment.settings.epochs[0]):
            experiment.PCodes[i + 1] = "2nd - 1243"
        for i in range(experiment.settings.epochs[1]):
            experiment.PCodes[5 + i + 1] = "3rd - 1324"
        experiment.calculate_stim_properties()

        self.assertEqual(len(experiment.stim_sessionN),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.end_at),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimepoch),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimblock),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimtrial),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimlist),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimpr),
                         experiment.settings.get_maxtrial())

        for i in range(len(experiment.stim_sessionN)):
            if i < experiment.settings.get_maxtrial() / 2:
                self.assertEqual(experiment.stim_sessionN[i + 1], 1)
            else:
                self.assertEqual(experiment.stim_sessionN[i + 1], 2)

        for i in range(len(experiment.end_at)):
            if i < experiment.settings.get_maxtrial() / 2:
                self.assertEqual(
                    experiment.end_at[i + 1], experiment.settings.get_maxtrial() / 2 + 1)
            else:
                self.assertEqual(
                    experiment.end_at[i + 1], experiment.settings.get_maxtrial() + 1)

        for i in range(len(experiment.stimepoch)):
            self.assertEqual(experiment.stimepoch[i + 1], i // ((experiment.settings.blockprepN +
                                                                 experiment.settings.blocklengthN) * experiment.settings.block_in_epochN) + 1)

        for i in range(len(experiment.stimblock)):
            self.assertEqual(experiment.stimblock[i + 1], i // (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        for i in range(len(experiment.stimtrial)):
            self.assertEqual(experiment.stimtrial[i + 1], i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        oount_4 = 0
        for i in range(len(experiment.stimlist)):
            trial_num_in_block = i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
            if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                if experiment.stimlist[i + 1] == 1:
                    count_1 += 1
                elif experiment.stimlist[i + 1] == 2:
                    count_2 += 1
                elif experiment.stimlist[i + 1] == 3:
                    count_3 += 1
                elif experiment.stimlist[i + 1] == 4:
                    oount_4 += 1

        self.assertEqual(count_1, 500)
        self.assertEqual(count_2, 500)
        self.assertEqual(count_3, 500)
        self.assertEqual(oount_4, 500)

        for i in range(len(experiment.stimpr)):
            trial_num_in_block = i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
            if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                self.assertEqual(experiment.stimpr[i + 1], "pattern")
            else:
                self.assertEqual(experiment.stimpr[i + 1], "random")

    def testNoASRT(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.epochN = 5
        experiment.settings.epochs = [5]
        experiment.settings.block_in_epochN = 5
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.asrt_rcolor = "Orange"
        experiment.settings.asrt_pcolor = "Green"
        experiment.settings.asrt_types = {1: 'noASRT', 2: 'noASRT', 3: 'noASRT', 4: 'noASRT', 5: 'noASRT'}

        experiment.stim_sessionN = {}
        experiment.end_at = {}
        experiment.stimepoch = {}
        experiment.stimblock = {}
        experiment.stimtrial = {}
        experiment.stimlist = {}
        experiment.stimpr = {}
        experiment.PCodes = {}
        for i in range(experiment.settings.epochN):
            experiment.PCodes[i + 1] = "noPattern"
        experiment.calculate_stim_properties()

        self.assertEqual(len(experiment.stim_sessionN),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.end_at),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimepoch),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimblock),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimtrial),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimlist),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimpr),
                         experiment.settings.get_maxtrial())

        # all trials are in the same session
        for i in range(len(experiment.stim_sessionN)):
            self.assertEqual(experiment.stim_sessionN[i + 1], 1)

        for i in range(len(experiment.end_at)):
            self.assertEqual(
                experiment.end_at[i + 1], experiment.settings.get_maxtrial() + 1)

        for i in range(len(experiment.stimepoch)):
            self.assertEqual(experiment.stimepoch[i + 1], i // ((experiment.settings.blockprepN +
                                                                 experiment.settings.blocklengthN) * experiment.settings.block_in_epochN) + 1)

        for i in range(len(experiment.stimblock)):
            self.assertEqual(experiment.stimblock[i + 1], i // (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        for i in range(len(experiment.stimtrial)):
            self.assertEqual(experiment.stimtrial[i + 1], i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        oount_4 = 0
        for i in range(len(experiment.stimlist)):
            trial_num_in_block = i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
            if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                if experiment.stimlist[i + 1] == 1:
                    count_1 += 1
                elif experiment.stimlist[i + 1] == 2:
                    count_2 += 1
                elif experiment.stimlist[i + 1] == 3:
                    count_3 += 1
                elif experiment.stimlist[i + 1] == 4:
                    oount_4 += 1

        # randomized data
        valid_random = False
        # it might happen that these counts are equal for randomized data
        # but it's unlikely to happen for four times
        for i in (1, 5):
            if count_1 != count_2 and count_3 != oount_4:
                valid_random = True
        self.assertTrue(valid_random)

        for i in range(len(experiment.stimpr)):
            self.assertEqual(experiment.stimpr[i + 1], "random")

    def testASRTWithoutPractice(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.epochN = 5
        experiment.settings.epochs = [5]
        experiment.settings.block_in_epochN = 5
        experiment.settings.blockprepN = 0
        experiment.settings.blocklengthN = 80
        experiment.settings.asrt_rcolor = "Orange"
        experiment.settings.asrt_pcolor = "Green"
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit', 3: 'implicit', 4: 'implicit', 5: 'implicit'}

        experiment.stim_sessionN = {}
        experiment.end_at = {}
        experiment.stimepoch = {}
        experiment.stimblock = {}
        experiment.stimtrial = {}
        experiment.stimlist = {}
        experiment.stimpr = {}
        experiment.PCodes = {}
        for i in range(experiment.settings.epochN):
            experiment.PCodes[i + 1] = "1st - 1234"
        experiment.calculate_stim_properties()

        self.assertEqual(len(experiment.stim_sessionN),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.end_at),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimepoch),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimblock),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimtrial),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimlist),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimpr),
                         experiment.settings.get_maxtrial())

        # all trials are in the same session
        for i in range(len(experiment.stim_sessionN)):
            self.assertEqual(experiment.stim_sessionN[i + 1], 1)

        for i in range(len(experiment.end_at)):
            self.assertEqual(
                experiment.end_at[i + 1], experiment.settings.get_maxtrial() + 1)

        for i in range(len(experiment.stimepoch)):
            self.assertEqual(experiment.stimepoch[i + 1], i // ((experiment.settings.blockprepN +
                                                                 experiment.settings.blocklengthN) * experiment.settings.block_in_epochN) + 1)

        for i in range(len(experiment.stimblock)):
            self.assertEqual(experiment.stimblock[i + 1], i // (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        for i in range(len(experiment.stimtrial)):
            self.assertEqual(experiment.stimtrial[i + 1], i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        oount_4 = 0
        for i in range(len(experiment.stimlist)):
            trial_num_in_block = i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
            if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                if experiment.stimlist[i + 1] == 1:
                    count_1 += 1
                elif experiment.stimlist[i + 1] == 2:
                    count_2 += 1
                elif experiment.stimlist[i + 1] == 3:
                    count_3 += 1
                elif experiment.stimlist[i + 1] == 4:
                    oount_4 += 1

        self.assertEqual(count_1, 250)
        self.assertEqual(count_2, 250)
        self.assertEqual(count_3, 250)
        self.assertEqual(oount_4, 250)

        for i in range(len(experiment.stimpr)):
            trial_num_in_block = i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
            if trial_num_in_block > experiment.settings.blockprepN and trial_num_in_block > 1 and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                self.assertEqual(experiment.stimpr[i + 1], "pattern")
            else:
                self.assertEqual(experiment.stimpr[i + 1], "random")

    def testASRTWithoutReal(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.epochN = 5
        experiment.settings.epochs = [5]
        experiment.settings.block_in_epochN = 5
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 0
        experiment.settings.asrt_rcolor = "Orange"
        experiment.settings.asrt_pcolor = "Green"
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit', 3: 'implicit', 4: 'implicit', 5: 'implicit'}

        experiment.stim_sessionN = {}
        experiment.end_at = {}
        experiment.stimepoch = {}
        experiment.stimblock = {}
        experiment.stimtrial = {}
        experiment.stimlist = {}
        experiment.stimpr = {}
        experiment.PCodes = {}
        for i in range(experiment.settings.epochN):
            experiment.PCodes[i + 1] = "1st - 1234"
        experiment.calculate_stim_properties()

        self.assertEqual(len(experiment.stim_sessionN),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.end_at),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimepoch),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimblock),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimtrial),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimlist),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimpr),
                         experiment.settings.get_maxtrial())

        # all trials are in the same session
        for i in range(len(experiment.stim_sessionN)):
            self.assertEqual(experiment.stim_sessionN[i + 1], 1)

        for i in range(len(experiment.end_at)):
            self.assertEqual(
                experiment.end_at[i + 1], experiment.settings.get_maxtrial() + 1)

        for i in range(len(experiment.stimepoch)):
            self.assertEqual(experiment.stimepoch[i + 1], i // ((experiment.settings.blockprepN +
                                                                 experiment.settings.blocklengthN) * experiment.settings.block_in_epochN) + 1)

        for i in range(len(experiment.stimblock)):
            self.assertEqual(experiment.stimblock[i + 1], i // (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        for i in range(len(experiment.stimtrial)):
            self.assertEqual(experiment.stimtrial[i + 1], i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        # random only
        for i in range(len(experiment.stimpr)):
            self.assertEqual(experiment.stimpr[i + 1], "random")

    def testWithEvenPracticeTrials(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.epochN = 5
        experiment.settings.epochs = [5]
        experiment.settings.block_in_epochN = 5
        experiment.settings.blockprepN = 6
        experiment.settings.blocklengthN = 80
        experiment.settings.asrt_rcolor = "Orange"
        experiment.settings.asrt_pcolor = "Green"
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit', 3: 'implicit', 4: 'implicit', 5: 'implicit'}

        experiment.stim_sessionN = {}
        experiment.end_at = {}
        experiment.stimepoch = {}
        experiment.stimblock = {}
        experiment.stimtrial = {}
        experiment.stimlist = {}
        experiment.stimpr = {}
        experiment.PCodes = {}
        for i in range(experiment.settings.epochN):
            experiment.PCodes[i + 1] = "1st - 1234"
        experiment.calculate_stim_properties()

        self.assertEqual(len(experiment.stim_sessionN),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.end_at),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimepoch),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimblock),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimtrial),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimlist),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimpr),
                         experiment.settings.get_maxtrial())

        # all trials are in the same session
        for i in range(len(experiment.stim_sessionN)):
            self.assertEqual(experiment.stim_sessionN[i + 1], 1)

        for i in range(len(experiment.end_at)):
            self.assertEqual(
                experiment.end_at[i + 1], experiment.settings.get_maxtrial() + 1)

        for i in range(len(experiment.stimepoch)):
            self.assertEqual(experiment.stimepoch[i + 1], i // ((experiment.settings.blockprepN +
                                                                 experiment.settings.blocklengthN) * experiment.settings.block_in_epochN) + 1)

        for i in range(len(experiment.stimblock)):
            self.assertEqual(experiment.stimblock[i + 1], i // (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        for i in range(len(experiment.stimtrial)):
            self.assertEqual(experiment.stimtrial[i + 1], i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        oount_4 = 0
        for i in range(len(experiment.stimlist)):
            trial_num_in_block = i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
            if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                if experiment.stimlist[i + 1] == 1:
                    count_1 += 1
                elif experiment.stimlist[i + 1] == 2:
                    count_2 += 1
                elif experiment.stimlist[i + 1] == 3:
                    count_3 += 1
                elif experiment.stimlist[i + 1] == 4:
                    oount_4 += 1

        self.assertEqual(count_1, 250)
        self.assertEqual(count_2, 250)
        self.assertEqual(count_3, 250)
        self.assertEqual(oount_4, 250)

        for i in range(len(experiment.stimpr)):
            trial_num_in_block = i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
            if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                self.assertEqual(experiment.stimpr[i + 1], "pattern")
            else:
                self.assertEqual(experiment.stimpr[i + 1], "random")

    def testWithOddRealTrials(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.epochN = 5
        experiment.settings.epochs = [5]
        experiment.settings.block_in_epochN = 5
        experiment.settings.blockprepN = 6
        experiment.settings.blocklengthN = 75
        experiment.settings.asrt_rcolor = "Orange"
        experiment.settings.asrt_pcolor = "Green"
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit', 3: 'implicit', 4: 'implicit', 5: 'implicit'}

        experiment.stim_sessionN = {}
        experiment.end_at = {}
        experiment.stimepoch = {}
        experiment.stimblock = {}
        experiment.stimtrial = {}
        experiment.stimlist = {}
        experiment.stimpr = {}
        experiment.PCodes = {}
        for i in range(experiment.settings.epochN):
            experiment.PCodes[i + 1] = "1st - 1234"
        experiment.calculate_stim_properties()

        self.assertEqual(len(experiment.stim_sessionN),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.end_at),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimepoch),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimblock),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimtrial),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimlist),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimpr),
                         experiment.settings.get_maxtrial())

        # all trials are in the same session
        for i in range(len(experiment.stim_sessionN)):
            self.assertEqual(experiment.stim_sessionN[i + 1], 1)

        for i in range(len(experiment.end_at)):
            self.assertEqual(
                experiment.end_at[i + 1], experiment.settings.get_maxtrial() + 1)

        for i in range(len(experiment.stimepoch)):
            self.assertEqual(experiment.stimepoch[i + 1], i // ((experiment.settings.blockprepN +
                                                                 experiment.settings.blocklengthN) * experiment.settings.block_in_epochN) + 1)

        for i in range(len(experiment.stimblock)):
            self.assertEqual(experiment.stimblock[i + 1], i // (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        for i in range(len(experiment.stimtrial)):
            self.assertEqual(experiment.stimtrial[i + 1], i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        oount_4 = 0
        for i in range(len(experiment.stimlist)):
            trial_num_in_block = i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
            if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                if experiment.stimlist[i + 1] == 1:
                    count_1 += 1
                elif experiment.stimlist[i + 1] == 2:
                    count_2 += 1
                elif experiment.stimlist[i + 1] == 3:
                    count_3 += 1
                elif experiment.stimlist[i + 1] == 4:
                    oount_4 += 1

        # there are some variance in the number, becuase some pattern trials are cut down at the end of the blocks
        self.assertAlmostEqual(count_1, 237, delta=20)
        self.assertAlmostEqual(count_2, 237, delta=20)
        self.assertAlmostEqual(count_3, 237, delta=20)
        self.assertAlmostEqual(oount_4, 237, delta=20)

        for i in range(len(experiment.stimpr)):
            trial_num_in_block = i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
            if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                self.assertEqual(experiment.stimpr[i + 1], "pattern")
            else:
                self.assertEqual(experiment.stimpr[i + 1], "random")

    def testMoreSessionsWithDifferentProperties(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.epochN = 10
        experiment.settings.epochs = [2, 5, 4]
        experiment.settings.block_in_epochN = 5
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.asrt_rcolor = "Orange"
        experiment.settings.asrt_pcolor = "Green"
        experiment.settings.asrt_types = {1: 'implicit', 2: 'implicit', 3: 'explicit', 4: 'explicit', 5: 'explicit',
                                          6: 'explicit', 7: 'explicit', 8: 'noASRT', 9: 'noASRT', 10: 'noASRT', 11: 'noASRT'}

        experiment.stim_sessionN = {}
        experiment.end_at = {}
        experiment.stimepoch = {}
        experiment.stimblock = {}
        experiment.stimtrial = {}
        experiment.stimlist = {}
        experiment.stimpr = {}
        experiment.PCodes = {}
        for i in range(experiment.settings.epochs[0]):
            experiment.PCodes[i + 1] = "2nd - 1243"
        for i in range(experiment.settings.epochs[1]):
            experiment.PCodes[2 + i + 1] = "3rd - 1324"
        for i in range(experiment.settings.epochs[2]):
            experiment.PCodes[7 + i + 1] = "noPattern"
        experiment.calculate_stim_properties()

        self.assertEqual(len(experiment.stim_sessionN),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.end_at),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimepoch),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimblock),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimtrial),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimlist),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimpr),
                         experiment.settings.get_maxtrial())

        first_session_last_trial = experiment.settings.epochs[0] * experiment.settings.block_in_epochN * (
            experiment.settings.blockprepN + experiment.settings.blocklengthN)
        second_session_last_trial = first_session_last_trial + \
            experiment.settings.epochs[1] * experiment.settings.block_in_epochN * (
                experiment.settings.blockprepN + experiment.settings.blocklengthN)
        third_session_last_trial = second_session_last_trial + \
            experiment.settings.epochs[2] * experiment.settings.block_in_epochN * (
                experiment.settings.blockprepN + experiment.settings.blocklengthN)

        for i in range(len(experiment.stim_sessionN)):
            if i < first_session_last_trial:
                self.assertEqual(experiment.stim_sessionN[i + 1], 1)
            elif i < second_session_last_trial:
                self.assertEqual(experiment.stim_sessionN[i + 1], 2)
            else:
                self.assertEqual(experiment.stim_sessionN[i + 1], 3)

        for i in range(len(experiment.end_at)):
            if i < first_session_last_trial:
                self.assertEqual(
                    experiment.end_at[i + 1], first_session_last_trial + 1)
            elif i < second_session_last_trial:
                self.assertEqual(
                    experiment.end_at[i + 1], second_session_last_trial + 1)
            else:
                self.assertEqual(
                    experiment.end_at[i + 1], third_session_last_trial + 1)

        for i in range(len(experiment.stimepoch)):
            self.assertEqual(experiment.stimepoch[i + 1], i // ((experiment.settings.blockprepN +
                                                                 experiment.settings.blocklengthN) * experiment.settings.block_in_epochN) + 1)

        for i in range(len(experiment.stimblock)):
            self.assertEqual(experiment.stimblock[i + 1], i // (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        for i in range(len(experiment.stimtrial)):
            self.assertEqual(experiment.stimtrial[i + 1], i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        count_4 = 0
        sequence = ""
        for i in range(len(experiment.stimlist)):
            if i >= second_session_last_trial:  # last session is random
                break

            trial_num_in_block = i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
            if trial_num_in_block == 1:
                sequence = ""

            if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                if experiment.stimlist[i + 1] == 1:
                    count_1 += 1
                    sequence += "1"
                elif experiment.stimlist[i + 1] == 2:
                    count_2 += 1
                    sequence += "2"
                elif experiment.stimlist[i + 1] == 3:
                    count_3 += 1
                    sequence += "3"
                elif experiment.stimlist[i + 1] == 4:
                    count_4 += 1
                    sequence += "4"
                sequence = sequence[-4:]

            if len(sequence) == 4:
                if i < first_session_last_trial:
                    self.assertTrue(sequence == "1243" or sequence ==
                                    "2431"or sequence == "4312"or sequence == "3124")
                elif i < second_session_last_trial:
                    self.assertTrue(sequence == "1324" or sequence ==
                                    "3241" or sequence == "2413"or sequence == "4132")

        self.assertEqual(count_1, count_2)
        self.assertEqual(count_2, count_3)
        self.assertEqual(count_3, count_4)

        for i in range(len(experiment.stimpr)):
            if i < second_session_last_trial:  # explicit or implicit
                trial_num_in_block = i % (
                    experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
                if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                    self.assertEqual(experiment.stimpr[i + 1], "pattern")
                else:
                    self.assertEqual(experiment.stimpr[i + 1], "random")
            else:  # noASRT
                self.assertEqual(experiment.stimpr[i + 1], "random")

    def testNoASRTAtTheBeginningOfSession(self):
        experiment = asrt.Experiment("")
        experiment.settings = asrt.ExperimentSettings("", "")
        experiment.settings.epochN = 5
        experiment.settings.epochs = [5]
        experiment.settings.block_in_epochN = 5
        experiment.settings.blockprepN = 5
        experiment.settings.blocklengthN = 80
        experiment.settings.asrt_rcolor = "Orange"
        experiment.settings.asrt_pcolor = "Green"
        experiment.settings.asrt_types = {1: 'noASRT', 2: 'implicit', 3: 'implicit', 4: 'implicit', 5: 'implicit'}

        experiment.stim_sessionN = {}
        experiment.end_at = {}
        experiment.stimepoch = {}
        experiment.stimblock = {}
        experiment.stimtrial = {}
        experiment.stimlist = {}
        experiment.stimpr = {}
        experiment.PCodes = {}
        experiment.PCodes[1] = "noPattern"
        for i in range(1, experiment.settings.epochN):
            experiment.PCodes[i + 1] = "1st - 1234"
        experiment.calculate_stim_properties()

        self.assertEqual(len(experiment.stim_sessionN),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.end_at),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimepoch),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimblock),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimtrial),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimlist),
                         experiment.settings.get_maxtrial())
        self.assertEqual(len(experiment.stimpr),
                         experiment.settings.get_maxtrial())

        # all trials are in the same session
        for i in range(len(experiment.stim_sessionN)):
            self.assertEqual(experiment.stim_sessionN[i + 1], 1)

        for i in range(len(experiment.end_at)):
            self.assertEqual(
                experiment.end_at[i + 1], experiment.settings.get_maxtrial() + 1)

        for i in range(len(experiment.stimepoch)):
            self.assertEqual(experiment.stimepoch[i + 1], i // ((experiment.settings.blockprepN +
                                                                 experiment.settings.blocklengthN) * experiment.settings.block_in_epochN) + 1)

        for i in range(len(experiment.stimblock)):
            self.assertEqual(experiment.stimblock[i + 1], i // (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        for i in range(len(experiment.stimtrial)):
            self.assertEqual(experiment.stimtrial[i + 1], i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1)

        count_1 = 0
        count_2 = 0
        count_3 = 0
        oount_4 = 0
        for i in range(len(experiment.stimlist)):
            trial_num_in_block = i % (
                experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
            if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                if experiment.stimlist[i + 1] == 1:
                    count_1 += 1
                elif experiment.stimlist[i + 1] == 2:
                    count_2 += 1
                elif experiment.stimlist[i + 1] == 3:
                    count_3 += 1
                elif experiment.stimlist[i + 1] == 4:
                    oount_4 += 1

        for i in range(len(experiment.stimpr)):
            if experiment.stim_sessionN[i + 1] > 1:
                trial_num_in_block = i % (
                    experiment.settings.blockprepN + experiment.settings.blocklengthN) + 1
                if trial_num_in_block > experiment.settings.blockprepN and (trial_num_in_block - experiment.settings.blockprepN) % 2 == 1:
                    self.assertEqual(experiment.stimpr[i + 1], "pattern")
                else:
                    self.assertEqual(experiment.stimpr[i + 1], "random")


if __name__ == "__main__":
    unittest.main()  # run all tests
