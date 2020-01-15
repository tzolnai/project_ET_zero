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
# Add the local path to the main script and external scripts so we can import them.
sys.path = [".."] + sys.path

import unittest
import asrt
import platform


class readInstructionsTest(unittest.TestCase):

    def assertEqualWithEOL(self, string1, string2):
        string1 = string1.replace("\r", "")
        string2 = string2.replace("\r", "")
        self.assertEqual(string1, string2)

    def constructFilePath(self, file_name):
        filepath = os.path.abspath(__file__)
        (inst_feedback_path, trail) = os.path.split(filepath)
        inst_feedback_path = os.path.join(
            inst_feedback_path, "data", "instr_and_feedback", file_name)
        return inst_feedback_path

    def testDefaultInstructionSet(self):
        inst_feedback_path = self.constructFilePath("default.txt")

        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        self.assertEqual(len(instruction_helper.insts), 3)
        self.assertEqual(len(instruction_helper.feedback_exp), 1)
        self.assertEqual(len(instruction_helper.feedback_imp), 1)
        self.assertEqual(len(instruction_helper.feedback_speed), 1)
        self.assertEqual(len(instruction_helper.feedback_accuracy), 1)
        self.assertEqual(len(instruction_helper.ending), 1)
        self.assertEqual(len(instruction_helper.unexp_quit), 1)

        self.assertEqualWithEOL(instruction_helper.insts[0], "\r\n\r\nÜdvözlünk a feladatban!\r\n\r\n"
                                                             "A képernyőn négy kör lesz, a kör egyikén megjelenik egy kutya.\r\n\r\n"
                                                             "Az a feladatod, hogy a kutya megjelenési helyének megfelelő gombot nyomd meg.\r\n\r\n"
                                                             "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")
        self.assertEqualWithEOL(instruction_helper.insts[1], "\r\n\r\nA következő billenytűket kell használni: z, c, b, m\r\n\r\n"
                                                             "Minél pontosabban és gyorsabban kövesd le a megjelenő ingereket!\r\n\r\n"
                                                             "Ehhez mindkét kezedet használd, a középső és mutatóujjaidat.\r\n\r\n"
                                                             "A kutya egymás után többször ugyanazon a helyen is megjelenhet.\r\n\r\n"
                                                             "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")
        self.assertEqualWithEOL(instruction_helper.insts[2], "\r\n\r\nKb. percenként fogsz visszajelzést kapni arról,\r\n"
                                                             "hogy mennyire voltál gyors és pontos - ez alapján tudsz módosítani.\r\n\r\n"
                                                             "A feladat indításához nyomd meg valamelyik válaszgombot!\r\n\r\n")

        self.assertEqualWithEOL(instruction_helper.feedback_imp[0], "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                                                    "Pontosságod: *PERCACC* %\r\n"
                                                                    "Átlagos reakcióidőd: *MEANRT* másodperc\r\n"
                                                                    "*SPEEDACC*\r\n\r\n")

        self.assertEqualWithEOL(instruction_helper.feedback_exp[0], "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                                                    "Pontosságod általában: *PERCACC* %\r\n"
                                                                    "Átlagos reakcióidőd: *MEANRT* másodperc\r\n"
                                                                    "Pontosságod a bejósolható elemeknél: *PERCACCP* %\r\n"
                                                                    "Átlagos reakcióidőd a bejósolható elemeknél: *MEANRTP* másodperc\r\n"
                                                                    "*SPEEDACC*\r\n\r\n")

        self.assertEqualWithEOL(
            instruction_helper.feedback_speed[0], "\r\nLegyél gyorsabb!\r\n\r\n")

        self.assertEqualWithEOL(
            instruction_helper.feedback_accuracy[0], "\r\nLegyél pontosabb!\r\n\r\n")

        self.assertEqualWithEOL(
            instruction_helper.unexp_quit[0], "\r\n\r\nVáratlan kilépés történt a feladatból. Folytatás. A feladat indításához nyomd meg valamelyik válaszbillentyűt.")

    def testOneInstruction(self):
        inst_feedback_path = self.constructFilePath("one_instruction.txt")

        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        self.assertEqual(len(instruction_helper.insts), 1)
        self.assertEqual(len(instruction_helper.feedback_exp), 0)
        self.assertEqual(len(instruction_helper.feedback_imp), 0)
        self.assertEqual(len(instruction_helper.feedback_speed), 0)
        self.assertEqual(len(instruction_helper.feedback_accuracy), 0)
        self.assertEqual(len(instruction_helper.ending), 0)
        self.assertEqual(len(instruction_helper.unexp_quit), 0)

    def testTypoInInstructionName(self):
        inst_feedback_path = self.constructFilePath(
            "typo_in_instruction_name.txt")

        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        self.assertEqual(len(instruction_helper.insts), 0)
        self.assertEqual(len(instruction_helper.feedback_exp), 0)
        self.assertEqual(len(instruction_helper.feedback_imp), 0)
        self.assertEqual(len(instruction_helper.feedback_speed), 0)
        self.assertEqual(len(instruction_helper.feedback_accuracy), 0)
        self.assertEqual(len(instruction_helper.ending), 0)
        self.assertEqual(len(instruction_helper.unexp_quit), 0)

    def testWeirdButWorkingInstruction(self):
        inst_feedback_path = self.constructFilePath(
            "weird_but_working_instruction.txt")

        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        # instagram is recognized as an 'inst'
        self.assertEqual(len(instruction_helper.insts), 1)
        self.assertEqual(len(instruction_helper.feedback_exp), 0)
        self.assertEqual(len(instruction_helper.feedback_imp), 0)
        self.assertEqual(len(instruction_helper.feedback_speed), 0)
        self.assertEqual(len(instruction_helper.feedback_accuracy), 0)
        self.assertEqual(len(instruction_helper.ending), 0)
        self.assertEqual(len(instruction_helper.unexp_quit), 0)

    def testMissingFile(self):
        inst_feedback_path = self.constructFilePath("missing_file.txt")

        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        self.assertEqual(len(instruction_helper.insts), 0)
        self.assertEqual(len(instruction_helper.feedback_exp), 0)
        self.assertEqual(len(instruction_helper.feedback_imp), 0)
        self.assertEqual(len(instruction_helper.feedback_speed), 0)
        self.assertEqual(len(instruction_helper.feedback_accuracy), 0)
        self.assertEqual(len(instruction_helper.ending), 0)
        self.assertEqual(len(instruction_helper.unexp_quit), 0)

    def testMoreInstructionsWithTheSameType(self):
        inst_feedback_path = self.constructFilePath(
            "more_instructions_with_the_same_type.txt")

        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        self.assertEqual(len(instruction_helper.insts), 2)
        self.assertEqual(len(instruction_helper.feedback_exp), 2)
        self.assertEqual(len(instruction_helper.feedback_imp), 2)
        self.assertEqual(len(instruction_helper.feedback_speed), 3)
        self.assertEqual(len(instruction_helper.feedback_accuracy), 3)
        self.assertEqual(len(instruction_helper.ending), 3)
        self.assertEqual(len(instruction_helper.unexp_quit), 4)

    def testEmptyFile(self):
        inst_feedback_path = self.constructFilePath("empty.txt")

        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        self.assertEqual(len(instruction_helper.insts), 0)
        self.assertEqual(len(instruction_helper.feedback_exp), 0)
        self.assertEqual(len(instruction_helper.feedback_imp), 0)
        self.assertEqual(len(instruction_helper.feedback_speed), 0)
        self.assertEqual(len(instruction_helper.feedback_accuracy), 0)
        self.assertEqual(len(instruction_helper.ending), 0)
        self.assertEqual(len(instruction_helper.unexp_quit), 0)

    def testInvalidFile(self):
        inst_feedback_path = self.constructFilePath("invalid.txt")

        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        self.assertEqual(len(instruction_helper.insts), 0)
        self.assertEqual(len(instruction_helper.feedback_exp), 0)
        self.assertEqual(len(instruction_helper.feedback_imp), 0)
        self.assertEqual(len(instruction_helper.feedback_speed), 0)
        self.assertEqual(len(instruction_helper.feedback_accuracy), 0)
        self.assertEqual(len(instruction_helper.ending), 0)
        self.assertEqual(len(instruction_helper.unexp_quit), 0)

    def testNoLineEnding(self):
        inst_feedback_path = self.constructFilePath("no_line_ending.txt")

        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        self.assertEqual(len(instruction_helper.insts), 1)
        self.assertEqual(len(instruction_helper.feedback_exp), 0)
        self.assertEqual(len(instruction_helper.feedback_imp), 0)
        self.assertEqual(len(instruction_helper.feedback_speed), 0)
        self.assertEqual(len(instruction_helper.feedback_accuracy), 0)
        self.assertEqual(len(instruction_helper.ending), 0)
        self.assertEqual(len(instruction_helper.unexp_quit), 0)

        self.assertEqual(instruction_helper.insts[0], "Üdvözlünk a feladatban!")

    def testKeywordWithoutContent(self):
        inst_feedback_path = self.constructFilePath(
            "keyword_without_content.txt")

        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        self.assertEqual(len(instruction_helper.insts), 0)
        self.assertEqual(len(instruction_helper.feedback_exp), 0)
        self.assertEqual(len(instruction_helper.feedback_imp), 0)
        self.assertEqual(len(instruction_helper.feedback_speed), 0)
        self.assertEqual(len(instruction_helper.feedback_accuracy), 0)
        self.assertEqual(len(instruction_helper.ending), 0)
        self.assertEqual(len(instruction_helper.unexp_quit), 0)

    def testDefaultRTInstructionSetValidation(self):
        inst_feedback_path = self.constructFilePath("default.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.experiment_type = 'reaction-time'
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "explicit"
        exp_settings.asrt_types[2] = "implicit"
        exp_settings.asrt_types[3] = "noASRT"

        instruction_helper.validate_instructions(exp_settings)

    def testDefaultERInstructionSetValidation(self):
        inst_feedback_path = self.constructFilePath("ET_default.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.experiment_type = 'eye-tracking'
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "explicit"
        exp_settings.asrt_types[2] = "implicit"
        exp_settings.asrt_types[3] = "noASRT"

        instruction_helper.validate_instructions(exp_settings)

    def testValidationMissingStartingInstruction(self):
        inst_feedback_path = self.constructFilePath("missing_starting_instruction.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.experiment_type = 'reaction-time'
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "explicit"
        exp_settings.asrt_types[2] = "implicit"
        exp_settings.asrt_types[3] = "noASRT"

        with self.assertRaises(SystemExit):
            instruction_helper.validate_instructions(exp_settings)

    def testValidationMissingEnding(self):
        inst_feedback_path = self.constructFilePath("missing_ending.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.experiment_type = 'reaction-time'
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "explicit"
        exp_settings.asrt_types[2] = "implicit"
        exp_settings.asrt_types[3] = "noASRT"

        with self.assertRaises(SystemExit):
            instruction_helper.validate_instructions(exp_settings)

    def testValidationMissingUnexpectedQuit(self):
        inst_feedback_path = self.constructFilePath("missing_unexpected_quit.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.experiment_type = 'reaction-time'
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "explicit"
        exp_settings.asrt_types[2] = "implicit"
        exp_settings.asrt_types[3] = "noASRT"

        with self.assertRaises(SystemExit):
            instruction_helper.validate_instructions(exp_settings)

    def testValidationMissingFeedbackSpeed(self):
        inst_feedback_path = self.constructFilePath("missing_feedback_speed.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.experiment_type = 'reaction-time'
        exp_settings.whether_warning = True
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "explicit"
        exp_settings.asrt_types[2] = "implicit"
        exp_settings.asrt_types[3] = "noASRT"

        with self.assertRaises(SystemExit):
            instruction_helper.validate_instructions(exp_settings)

        # no problem when there is no warning set
        exp_settings.whether_warning = False
        instruction_helper.validate_instructions(exp_settings)

        # no problem when we have eye-tracking version
        exp_settings.experiment_type = 'eye-tracking'
        exp_settings.whether_warning = True
        instruction_helper.validate_instructions(exp_settings)

    def testValidationMissingFeedbackAccuracy(self):
        inst_feedback_path = self.constructFilePath("missing_feedback_accuracy.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.experiment_type = 'reaction-time'
        exp_settings.whether_warning = True
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "explicit"
        exp_settings.asrt_types[2] = "implicit"
        exp_settings.asrt_types[3] = "noASRT"

        with self.assertRaises(SystemExit):
            instruction_helper.validate_instructions(exp_settings)

        # no problem when there is no warning set
        exp_settings.whether_warning = False
        instruction_helper.validate_instructions(exp_settings)

        # no problem when we have eye-tracking version
        exp_settings.experiment_type = 'eye-tracking'
        exp_settings.whether_warning = True
        instruction_helper.validate_instructions(exp_settings)

    def testValidationMissingImplicitFeedback(self):
        inst_feedback_path = self.constructFilePath("missing_implicit_feedback.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.experiment_type = 'reaction-time'
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "explicit"
        exp_settings.asrt_types[2] = "implicit"
        exp_settings.asrt_types[3] = "noASRT"

        with self.assertRaises(SystemExit):
            instruction_helper.validate_instructions(exp_settings)

        # no problem when there is no implicit asrt type
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "explicit"
        exp_settings.asrt_types[2] = "noASRT"
        instruction_helper.validate_instructions(exp_settings)

        # no problem when we have eye-tracking version
        exp_settings.experiment_type = 'eye-tracking'
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "explicit"
        exp_settings.asrt_types[2] = "implicit"
        exp_settings.asrt_types[3] = "noASRT"
        instruction_helper.validate_instructions(exp_settings)

    def testValidationMissingExplicitFeedback(self):
        inst_feedback_path = self.constructFilePath("missing_explicit_feedback.txt")
        instruction_helper = asrt.InstructionHelper(inst_feedback_path)
        instruction_helper.read_insts_from_file()

        exp_settings = asrt.ExperimentSettings("", "")
        exp_settings.experiment_type = 'reaction-time'
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "explicit"
        exp_settings.asrt_types[2] = "implicit"
        exp_settings.asrt_types[3] = "noASRT"

        with self.assertRaises(SystemExit):
            instruction_helper.validate_instructions(exp_settings)

        # no problem when there is no implicit asrt type
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "implicit"
        exp_settings.asrt_types[2] = "noASRT"
        instruction_helper.validate_instructions(exp_settings)

        # no problem when we have eye-tracking version
        exp_settings.experiment_type = 'eye-tracking'
        exp_settings.asrt_types = {}
        exp_settings.asrt_types[1] = "explicit"
        exp_settings.asrt_types[2] = "implicit"
        exp_settings.asrt_types[3] = "noASRT"
        instruction_helper.validate_instructions(exp_settings)


if __name__ == "__main__":
    unittest.main()  # run all tests
