
#    Copyright (C) <2018>  <Emese Szegedi-Hallgató>
#                  <2018>  <Tamás Zolnai>    <zolnaitamas2000@gmail.com>

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

#!\\usr\\bin\\env python
# -*- coding: utf-8 -*-

import codecs

# Be aware of that line endings are preserved during reading instructions
def read_instructions(inst_feedback_path):
    try:
        with codecs.open(inst_feedback_path, 'r', encoding = 'utf-8') as inst_feedback:
            all_inst_feedback = inst_feedback.read().split('***')
    except:
        all_inst_feedback=[]

    insts= []
    feedback_exp = []
    feedback_imp = []
    feedback_speed = []
    feedback_accuracy = []
    ending = []
    unexp_quit = []

    for all in all_inst_feedback:
        all = all.split('#')
        if len(all) >= 2:
            if 'inst' in all[0]:
                insts.append(all[1])
            elif 'feedback explicit' in all[0]:
                feedback_exp.append(all[1])
            elif 'feedback implicit' in all[0]:
                feedback_imp.append(all[1])
            elif 'speed' in all[0]:
                feedback_speed.append(all[1])
            elif 'accuracy' in all[0]:
                feedback_accuracy.append(all[1])
            elif 'ending' in all[0]:
                ending.append(all[1])
            elif 'unexpected quit' in all[0]:
                unexp_quit.append(all[1])

    return insts, feedback_exp, feedback_imp, feedback_speed, feedback_accuracy, ending, unexp_quit