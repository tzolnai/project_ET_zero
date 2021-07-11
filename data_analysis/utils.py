# !/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) <2019-2021>  <Tamás Zolnai>  <zolnaitamas2000@gmail.com>

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

import math

def strToFloat(data):
    return float(str(data).replace(",", "."))

def floatToStr(data):
    return str(data).replace(".", ",")

def calcRMS(values):
    square = 0.0
    for i in range(len(values)):
        square += pow(values[i], 2)

    mean = square / float(len(values))

    return math.sqrt(mean)

def convertToAngle(value_cm):
    eye_screen_distance_cm = 65.0
    return math.degrees(math.atan(value_cm / eye_screen_distance_cm))

def filter_epoch(subject_epoch_pair):
    # note_1: 4 additinal subjects were filtered out on site (failed on calibration validation)

    return subject_epoch_pair in [
                                  (14, 1), # missing data: 16.87 %
                                  (14, 2), # missing data: 18.21 %
                                  (14, 3), # missing data: 24.27 %
                                  (14, 4), # missing data: 25.10 %
                                  (14, 5), # missing data: 20.23 %
                                  (14, 6), # missing data: 21.20 %
                                  (14, 7), # missing data: 23.54 %
                                  (14, 8), # missing data: 26.79 %
                                  (17, 2), # RMS(E2E): 1.78
                                  (17, 3), # RMS(E2E): 1.9
                                  (17, 4), # RMS(E2E): 2.00
                                  (17, 5), # RMS(E2E): 2.12
                                  (19, 3), # RMS(E2E): 1.54
                                  (25, 2), # RMS(E2E): 1.57
                                  (25, 3), # RMS(E2E): 1.64
                                  (25, 4), # RMS(E2E): 1.73
                                  (25, 5), # RMS(E2E): 1.72
                                  (27, 2), # RMS(E2E): 1.61
                                  (27, 3), # RMS(E2E): 1.76
                                  (27, 4), # RMS(E2E): 1.95
                                  (27, 5), # RMS(E2E): 2.04
                                  (38, 8), # eye-screen distance: 52.07 cm
                                  (39, 1), # missing data: 24.97 %
                                  (39, 2), # missing data: 30.65 %
                                  (39, 6), # missing data: 19.9 %
                                  (39, 7), # missing data: 20.36 %
                                  (39, 8), # missing data: 17.18 %
                                  (40, 4), # RMS(E2E): 1.55
                                  (40, 6), # RMS(E2E): 1.64
                                  (40, 7), # RMS(E2E): 1.71
                                  (40, 8), # RMS(E2E): 2.06
                                  (44, 4), # missing data: 18.28 %
                                  (44, 5), # missing data: 18.21 %
                                  (44, 7), # missing data: 21.07 %
                                  (47, 1), # eye-screen distance: 44.21 cm
                                  (47, 2), # eye-screen distance: 48.48 cm
                                  (47, 3), # eye-screen distance: 49.70 cm
                                  (47, 4), # eye-screen distance: 50.89 cm
                                  (47, 5), # eye-screen distance: 49.02 cm
                                  (47, 7), # eye-screen distance: 53.74 cm
                                  (47, 8), # eye-screen distance: 53.48 cm
                                 ]

def filter_run(subject, test_type, run):
    # note_1: 4 additinal subjects were filtered out on site (failed on calibration validation)

    return (subject, test_type, run) in [
                                  (12, "inclusion", 2),
                                  (12, "inclusion", 4),
                                  (12, "exclusion", 2),
                                  (22, "exclusion", 4),
                                  (25, "inclusion", 4),
                                  (25, "exclusion", 2),
                                  (25, "exclusion", 3),
                                  (25, "exclusion", 4),
                                  (27, "exclusion", 1),
                                  (27, "exclusion", 2),
                                  (27, "exclusion", 3),
                                  (32, "exclusion", 4),
                                  (39, "exclusion", 2),
                                  (39, "exclusion", 3),
                                  (39, "exclusion", 4),
                                  (44, "exclusion", 1),
                                  (14, "inclusion", 1),
                                  (14, "inclusion", 2),
                                  (14, "inclusion", 3),
                                  (14, "exclusion", 2),
                                  (14, "exclusion", 3),
                                  (14, "exclusion", 4),
                                  (15, "inclusion", 1),
                                  (15, "inclusion", 2),
                                  (15, "inclusion", 3),
                                  (15, "inclusion", 4),
                                  (15, "exclusion", 1),
                                  (18, "inclusion", 4),
                                  (19, "inclusion", 2),
                                  (19, "inclusion", 4),
                                  (19, "exclusion", 1),
                                  (25, "inclusion", 2),
                                  (25, "inclusion", 3),
                                  (27, "inclusion", 4),
                                  (30, "inclusion", 1),
                                  (30, "inclusion", 3),
                                  (30, "inclusion", 4),
                                  (30, "exclusion", 1),
                                  (31, "exclusion", 3),
                                  (32, "inclusion", 4),
                                  (33, "exclusion", 3),
                                  (33, "exclusion", 4),
                                  (34, "inclusion", 4),
                                  (37, "inclusion", 4),
                                  (38, "inclusion", 4),
                                  (39, "inclusion", 1),
                                  (40, "inclusion", 2),
                                  (40, "inclusion", 3),
                                  (44, "inclusion", 3),
                                  (44, "inclusion", 4),
                                  (45, "inclusion", 1),
                                  (45, "inclusion", 2),
                                  (45, "inclusion", 3),
                                  (45, "inclusion", 4),
                                  (45, "exclusion", 1),
                                  (45, "exclusion", 2),
                                  (45, "exclusion", 3),
                                 ]