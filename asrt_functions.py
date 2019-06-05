
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

from psychopy import gui, core

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


### Settings dialogs

# Ask the user to specify the number of groups and the number of sessions
def show_basic_settings_dialog():
    expstart0=gui.Dlg(title=u'Beállítások')
    expstart0.addText(u'Még nincsenek beállítások mentve ehhez a kísérlethez...')
    expstart0.addText(u'A logfile optimalizálása érdekében kérjük add meg, hányféle csoporttal tervezed az adatfelvételt.')
    expstart0.addField(u'Kiserleti + Kontrollcsoportok szama osszesen', 2)
    expstart0.addText(u'Hány ülés (session) lesz a kísérletben?')
    expstart0.addField(u'Ulesek szama', 2)
    returned_data = expstart0.show()
    if expstart0.OK:
        return (returned_data[0], returned_data[1])
    else:
        core.quit()

# Ask the user to specify the name of the groups
# Returns the list of group names
def show_group_settings_dialog(numgroups, dict_accents):

    if numgroups>1:
        groups = []
        expstart01=gui.Dlg(title=u'Beállítások')
        expstart01.addText(u'A csoportok megnevezése a következő (pl. kísérleti, kontroll, ....) ')
        for i in range(numgroups):
            expstart01.addField(u'Csoport '+str(i+1))
        returned_data = expstart01.show()
        if expstart01.OK:
            for ii in returned_data:
                ii = ii.lower()
                ii = ii.replace(' ', '_')
                ii = ii.replace('-', '_')
                for accent in dict_accents.keys():
                    ii = ii.replace(accent, dict_accents[accent])
                groups.append(ii)
        else:
            core.quit()
    else:
        groups = ['nincsenek csoportok']

    return groups