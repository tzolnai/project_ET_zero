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

# pattern = 12341

import random

trial_count = 100000


def generate_stim_random(stim_list):
    for i in range(1, trial_count):
        stim_list.append(random.choice([1, 2, 3, 4]))


def check_high_frequency(stim_list):
    pattern = "12341"
    high_count = 0
    for i in range(2, trial_count - 1):
        if str(stim_list[i]) + str(stim_list[i - 2]) in pattern:
            high_count += 1

    print('High triplet frequency is: ' + str(high_count / trial_count * 100))

def check_trill_frequency(stim_list):
    trill_count = 0
    for i in range(2, trial_count - 1):
        if stim_list[i] == stim_list[i - 2]:
            trill_count += 1

    print('Trill triplet frequency is: ' + str(trill_count / trial_count * 100))

def check_high_frequency_without_trills(stim_list):
    pattern = "12341"
    high_count = 0
    for i in range(2, trial_count - 1):
        if str(stim_list[i]) + str(stim_list[i - 2]) in pattern:
            high_count += 1

    trill_count = 0
    for i in range(2, trial_count - 1):
        if stim_list[i] == stim_list[i - 2]:
            trill_count += 1

    print('Trill triplet frequency is: ' + str(high_count / (trial_count - trill_count) * 100))


def generate_stim_random_no_repeat(stim_list):
    for i in range(1, trial_count):
        stim_choices = [1, 2, 3, 4]
        if i > 1:
            stim_choices.remove(stim_list[len(stim_list) - 1])

        stim_list.append(random.choice(stim_choices))


def generate_stim_random_no_repeat2(stim_list):
    for i in range(1, trial_count):
        stim_choices = [1, 2, 3, 4]
        if i > 2:
            stim_choices.remove(stim_list[len(stim_list) - 2])

        stim_list.append(random.choice(stim_choices))


if __name__ == "__main__":
    stim_list = []
    generate_stim_random(stim_list)

    check_high_frequency(stim_list)

    check_trill_frequency(stim_list)
    
    check_high_frequency_without_trills(stim_list)
