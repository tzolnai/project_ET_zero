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

import unittest
import os

if __name__ == "__main__":
    os.system('pytest all_settings_def_test.py')
    os.system('pytest calculate_stim_properties_test.py')
    os.system('pytest coordinate_test.py')
    os.system('pytest draw_instructions_test.py')
    os.system('pytest experiment_settings_file_handling_test.py')
    os.system('pytest eye_tracking_timing_test.py')
    os.system('pytest participant_id_test.py')