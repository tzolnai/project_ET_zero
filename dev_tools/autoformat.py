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

import os


def format_files_in_directory(dir_path):
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path) and file_path.endswith(".py"):
            print("Formating file: " + file_path)

            # Run autopep8
            os.system("autopep8 -i --ignore E402 --max-line-length 150 " + file_path)

            # Replace line endings (use Linux line endings consitently)
            with open(file_path, 'rb') as open_file:
                content = open_file.read()
            if b'\r\n' in content:
                content = content.replace(b'\r\n', b'\n')
                with open(file_path, 'wb') as open_file:
                    open_file.write(content)

        elif os.path.isdir(file_path) and not file_path.endswith("externals"):
            print("Stepping into directory: " + file_path)
            format_files_in_directory(file_path)


this_path = os.path.split(os.path.abspath(__file__))[0]
root_path = os.path.split(this_path)[0]
format_files_in_directory(root_path)
