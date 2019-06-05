
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

import unittest

import sys
# Add the local path to the main script so we can import it.
sys.path = [".."] + sys.path

import os
import asrt_functions as asrt

class readInstructionsTest(unittest.TestCase):

    def constructFilePath(self, file_name):
        filepath = os.path.abspath(__file__)
        (inst_feedback_path, trail) = os.path.split(filepath)
        inst_feedback_path = os.path.join(inst_feedback_path, "data")
        inst_feedback_path = os.path.join(inst_feedback_path, "instr_and_feedback")
        inst_feedback_path = os.path.join(inst_feedback_path, file_name)
        return inst_feedback_path

    def testDefaultInstructionSet(self):
        inst_feedback_path = self.constructFilePath("default.txt")

        insts, feedback_exp, feedback_imp, feedback_speed, feedback_accuracy, ende, unexp_quit = asrt.read_instructions(inst_feedback_path)
        self.assertEqual(len(insts), 3)
        self.assertEqual(len(feedback_exp), 0)
        self.assertEqual(len(feedback_imp), 1)
        self.assertEqual(len(feedback_speed), 1)
        self.assertEqual(len(feedback_accuracy), 1)
        self.assertEqual(len(ende), 1)
        self.assertEqual(len(unexp_quit), 1)

        self.assertEqual(insts[0], "\r\n\r\nÜdvözlünk a feladatban!\r\n\r\n"
                                   "A képernyőn négy kör lesz, a kör egyikén megjelenik egy kutya.\r\n\r\n"
                                   "Az a feladatod, hogy a kutya megjelenési helyének megfelelő gombot nyomd meg.\r\n\r\n"
                                   "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")
        self.assertEqual(insts[1], "\r\n\r\nA következő billenytűket kell használni: z, c, b, m\r\n\r\n"
                                   "Minél pontosabban és gyorsabban kövesd le a megjelenő ingereket!\r\n\r\n"
                                   "Ehhez mindkét kezedet használd, a középső és mutatóujjaidat.\r\n\r\n"
                                   "A kutya egymás után többször ugyanazon a helyen is megjelenhet.\r\n\r\n"
                                   "A további instrukciók megtekintéséhez nyomd meg valamelyik válaszgombot!\r\n\r\n")
        self.assertEqual(insts[2], "\r\n\r\nKb. percenként fogsz visszajelzést kapni arról,\r\n"
                                   "hogy mennyire voltál gyors és pontos - ez alapján tudsz módosítani.\r\n\r\n"
                                   "A feladat indításához nyomd meg valamelyik válaszgombot!\r\n\r\n")

        self.assertEqual(feedback_imp[0], "\r\n\r\nMost pihenhetsz egy kicsit.\r\n\r\n"
                                          "Pontosságod: *PERCACC* %\r\n"
                                          "Átlagos reakcióidőd: *MEANRT* másodperc\r\n"
                                          "*SPEEDACC*\r\n\r\n")

        self.assertEqual(feedback_speed[0], "\r\nLegyél gyorsabb!\r\n\r\n")

        self.assertEqual(feedback_accuracy[0], "\r\nLegyél pontosabb!\r\n\r\n")

        self.assertEqual(unexp_quit[0], "\r\n\r\nVáratlan kilépés történt a feladatból. Folytatás. A feladat indításához nyomd meg valamelyik válaszbillentyűt.")

    def testOneInstruction(self):
        inst_feedback_path = self.constructFilePath("one_instruction.txt")

        insts, feedback_exp, feedback_imp, feedback_speed, feedback_accuracy, ende, unexp_quit = asrt.read_instructions(inst_feedback_path)
        self.assertEqual(len(insts), 1)
        self.assertEqual(len(feedback_exp), 0)
        self.assertEqual(len(feedback_imp), 0)
        self.assertEqual(len(feedback_speed), 0)
        self.assertEqual(len(feedback_accuracy), 0)
        self.assertEqual(len(ende), 0)
        self.assertEqual(len(unexp_quit), 0)

    def testTypoInInstructionName(self):
        inst_feedback_path = self.constructFilePath("typo_in_instruction_name.txt")

        insts, feedback_exp, feedback_imp, feedback_speed, feedback_accuracy, ende, unexp_quit = asrt.read_instructions(inst_feedback_path)
        self.assertEqual(len(insts), 0)
        self.assertEqual(len(feedback_exp), 0)
        self.assertEqual(len(feedback_imp), 0)
        self.assertEqual(len(feedback_speed), 0)
        self.assertEqual(len(feedback_accuracy), 0)
        self.assertEqual(len(ende), 0)
        self.assertEqual(len(unexp_quit), 0)

    def testWeirdButWorkingInstruction(self):
        inst_feedback_path = self.constructFilePath("weird_but_working_instruction.txt")

        insts, feedback_exp, feedback_imp, feedback_speed, feedback_accuracy, ende, unexp_quit = asrt.read_instructions(inst_feedback_path)
        self.assertEqual(len(insts), 1) # instagram is recognized as an 'inst'
        self.assertEqual(len(feedback_exp), 0)
        self.assertEqual(len(feedback_imp), 0)
        self.assertEqual(len(feedback_speed), 0)
        self.assertEqual(len(feedback_accuracy), 0)
        self.assertEqual(len(ende), 0)
        self.assertEqual(len(unexp_quit), 0)

    def testMissingFile(self):
        inst_feedback_path = self.constructFilePath("missing_file.txt")

        insts, feedback_exp, feedback_imp, feedback_speed, feedback_accuracy, ende, unexp_quit = asrt.read_instructions(inst_feedback_path)
        self.assertEqual(len(insts), 0)
        self.assertEqual(len(feedback_exp), 0)
        self.assertEqual(len(feedback_imp), 0)
        self.assertEqual(len(feedback_speed), 0)
        self.assertEqual(len(feedback_accuracy), 0)
        self.assertEqual(len(ende), 0)
        self.assertEqual(len(unexp_quit), 0)

    def testMoreInstructionsWithTheSameType(self):
        inst_feedback_path = self.constructFilePath("more_instructions_with_the_same_type.txt")

        insts, feedback_exp, feedback_imp, feedback_speed, feedback_accuracy, ende, unexp_quit = asrt.read_instructions(inst_feedback_path)
        self.assertEqual(len(insts), 2)
        self.assertEqual(len(feedback_exp), 2)
        self.assertEqual(len(feedback_imp), 2)
        self.assertEqual(len(feedback_speed), 3)
        self.assertEqual(len(feedback_accuracy), 3)
        self.assertEqual(len(ende), 3)
        self.assertEqual(len(unexp_quit), 4)

    def testEmptyFile(self):
        inst_feedback_path = self.constructFilePath("empty.txt")

        insts, feedback_exp, feedback_imp, feedback_speed, feedback_accuracy, ende, unexp_quit = asrt.read_instructions(inst_feedback_path)
        self.assertEqual(len(insts), 0)
        self.assertEqual(len(feedback_exp), 0)
        self.assertEqual(len(feedback_imp), 0)
        self.assertEqual(len(feedback_speed), 0)
        self.assertEqual(len(feedback_accuracy), 0)
        self.assertEqual(len(ende), 0)
        self.assertEqual(len(unexp_quit), 0)

    def testInvalidFile(self):
        inst_feedback_path = self.constructFilePath("invalid.txt")

        insts, feedback_exp, feedback_imp, feedback_speed, feedback_accuracy, ende, unexp_quit = asrt.read_instructions(inst_feedback_path)
        self.assertEqual(len(insts), 0)
        self.assertEqual(len(feedback_exp), 0)
        self.assertEqual(len(feedback_imp), 0)
        self.assertEqual(len(feedback_speed), 0)
        self.assertEqual(len(feedback_accuracy), 0)
        self.assertEqual(len(ende), 0)
        self.assertEqual(len(unexp_quit), 0)

    def testNoLineEnding(self):
        inst_feedback_path = self.constructFilePath("no_line_ending.txt")

        insts, feedback_exp, feedback_imp, feedback_speed, feedback_accuracy, ende, unexp_quit = asrt.read_instructions(inst_feedback_path)
        self.assertEqual(len(insts), 1)
        self.assertEqual(len(feedback_exp), 0)
        self.assertEqual(len(feedback_imp), 0)
        self.assertEqual(len(feedback_speed), 0)
        self.assertEqual(len(feedback_accuracy), 0)
        self.assertEqual(len(ende), 0)
        self.assertEqual(len(unexp_quit), 0)

        self.assertEqual(insts[0], "Üdvözlünk a feladatban!")

if __name__ == "__main__":
    unittest.main() # run all tests