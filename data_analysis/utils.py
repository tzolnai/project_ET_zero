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