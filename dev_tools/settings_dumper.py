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
# Add the local path to the asrt script
sys.path = [".."] + sys.path

import asrt
import os


class ExperimentSettingsDumper():

    def dump(self, file_path, file_name):
        print(os.path.join(file_path, file_name))
        print(os.path.join(file_path, "settings_reminder.txt"))
        exp_settings = asrt.ExperimentSettings(os.path.join(file_path, file_name), os.path.join(file_path, "settings_reminder.txt"))
        exp_settings.read_from_file()
        exp_settings.write_out_reminder()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("You need to specify a settings file path and name (without extension).")
        exit(1)

    setting_dumper = ExperimentSettingsDumper()
    setting_dumper.dump(sys.argv[1], sys.argv[2])
