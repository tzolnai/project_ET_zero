
#    ASRT script in Psychopy
#    Copyright (C) <2018>  <Emese Szegedi-Hallgató>
#                  <2019>  <Tamás Zolnai>  <zolnaitamas2000@gmail.com>

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

# !/usr/bin/env python
# -*- coding: utf-8 -*-


from psychopy import visual, core, event, gui, monitors
import shelve
import random
import codecs
import os
import time
import pyglet

import numbers


def ensure_dir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


class ExperimentSettings:
    """ This class handles all operation related to experiment settings
        These settings apply to all subjects in the specific experiment
    """

    def __init__(self, settings_file_path, reminder_file_path):
        self.numsessions = None         # number of sessions (e.g. 10)
        # list of group names (e.g. ["kontrol", "kiserleti"])
        self.groups = None

        # number of practice trials at the beginning of the block (e.g. 10)
        self.blockprepN = None
        # number of trials in one block (e.g. 10)
        self.blocklengthN = None
        # number of blocks in one epoch (e.g. 10)
        self.block_in_epochN = None
        # number of all epoch in all sessions (e.g. 12)
        self.epochN = None
        # list of epoch numbers of all sessions (e.g. [1, 2] (two sessions, first session has 1 epoch, the second has 2))
        self.epochs = None
        # list of asrt types of all sessions (e.g. ['implicit', 'explicit'] (two sessions, first session is an implicit asrt, the second one is explicit))
        self.asrt_types = None

        # monitor's physical with in 'cm' (e.g. 29)
        self.monitor_width = None
        # am imaginary name of the computer where the experiment is run
        self.computer_name = None
        self.asrt_distance = None
        self.asrt_size = None
        self.asrt_rcolor = None
        self.asrt_pcolor = None
        self.asrt_background = None
        self.RSI_time = None

        self.key1 = None                # key for the first stimulus (e.g. 'z')
        # key for the second stimulus (e.g. 'v')
        self.key2 = None
        self.key3 = None                # key for the third stimulus (e.g. 'b')
        # key for the fourth stimulus (e.g. 'm')
        self.key4 = None
        # key used to quit the running script (e.g. 'q')
        self.key_quit = None
        # whether display any feedback about speed and accuracy (e.g. True)
        self.whether_warning = None
        # an accuracy value, warn if the current accuracy is bigger than this value (e.g. 93)
        self.speed_warning = None
        # an accuracy value, warn if the current accuracy is smaller than this value (e.g. 91)
        self.acc_warning = None

        self.sessionstarts = None
        self.blockstarts = None

        self.settings_file_path = settings_file_path
        self.reminder_file_path = reminder_file_path

    def read_from_file(self):
        try:
            with shelve.open(self.settings_file_path, 'r') as settings_file:
                self.numsessions = settings_file['numsessions']
                self.groups = settings_file['groups']

                self.blockprepN = settings_file['blockprepN']
                self.blocklengthN = settings_file['blocklengthN']
                self.block_in_epochN = settings_file['block_in_epochN']
                self.epochN = settings_file['epochN']
                self.epochs = settings_file['epochs']

                self.asrt_types = settings_file['asrt_types']

                self.monitor_width = settings_file['monitor_width']
                self.computer_name = settings_file['computer_name']
                self.asrt_distance = settings_file['asrt_distance']
                self.asrt_size = settings_file['asrt_size']
                self.asrt_rcolor = settings_file['asrt_rcolor']
                self.asrt_pcolor = settings_file['asrt_pcolor']
                self.asrt_background = settings_file['asrt_background']
                self.RSI_time = settings_file['RSI_time']

                self.key1 = settings_file['key1']
                self.key2 = settings_file['key2']
                self.key3 = settings_file['key3']
                self.key4 = settings_file['key4']
                self.key_quit = settings_file['key_quit']
                self.whether_warning = settings_file['whether_warning']
                self.speed_warning = settings_file['speed_warning']
                self.acc_warning = settings_file['acc_warning']
        except Exception as exc:
            self.__init__(self.settings_file_path, self.reminder_file_path)
            raise exc

    def write_to_file(self):
        with shelve.open(self.settings_file_path, 'n') as settings_file:
            settings_file['numsessions'] = self.numsessions
            settings_file['groups'] = self.groups

            settings_file['blockprepN'] = self.blockprepN
            settings_file['blocklengthN'] = self.blocklengthN
            settings_file['block_in_epochN'] = self.block_in_epochN
            settings_file['epochN'] = self.epochN
            settings_file['epochs'] = self.epochs

            settings_file['asrt_types'] = self.asrt_types

            settings_file['monitor_width'] = self.monitor_width
            settings_file['computer_name'] = self.computer_name
            settings_file['asrt_distance'] = self.asrt_distance
            settings_file['asrt_size'] = self.asrt_size
            settings_file['asrt_rcolor'] = self.asrt_rcolor
            settings_file['asrt_pcolor'] = self.asrt_pcolor
            settings_file['asrt_background'] = self.asrt_background
            settings_file['RSI_time'] = self.RSI_time

            settings_file['key1'] = self.key1
            settings_file['key2'] = self.key2
            settings_file['key3'] = self.key3
            settings_file['key4'] = self.key4
            settings_file['key_quit'] = self.key_quit
            settings_file['whether_warning'] = self.whether_warning
            settings_file['speed_warning'] = self.speed_warning
            settings_file['acc_warning'] = self.acc_warning

    def write_out_reminder(self):
        with codecs.open(self.reminder_file_path, 'w', encoding='utf-8') as reminder_file:
            reminder_file.write(u'Beállítások \n' +
                                '\n' +
                                'Monitor Width: ' + '\t' + str(self.monitor_width).replace('.', ',')+'\n' +
                                'Computer Name: ' + '\t' + self.computer_name+'\n' +
                                'Response keys: ' + '\t' + self.key1+', ' + self.key2+', ' + self.key3+', ' + self.key4+'.'+'\n' +
                                'Quit key: ' + '\t' + self.key_quit + '\n' +
                                'Warning (speed, accuracy): ' + '\t' + str(self.whether_warning)+'\n' +
                                'Speed warning at:' + '\t' + str(self.speed_warning)+'\n' +
                                'Acc warning at:' + '\t' + str(self.acc_warning)+'\n' +
                                'Groups:' + '\t' + str(self.groups)[1:-1].replace("u'", '').replace("'", '')+'\n' +
                                'Sessions:' + '\t' + str(self.numsessions)+'\n' +
                                'Epochs in sessions:' + '\t' + str(self.epochs)[1:-1].replace("u'", '').replace("'", '')+'\n' +
                                'Blocks in epochs:' + '\t' + str(self.block_in_epochN)+'\n' +
                                'Preparatory Trials\\Block:' + '\t' + str(self.blockprepN)+'\n' +
                                'Trials\\Block:' + '\t' + str(self.blocklengthN)+'\n' +
                                'RSI:' + '\t' + str(self.RSI_time).replace('.', ',')+'\n' +
                                'Asrt stim distance:' + '\t' + str(self.asrt_distance)+'\n' +
                                'Asrt stim size:' + '\t' + str(self.asrt_size)+'\n' +
                                'Asrt stim color (implicit):' + '\t' + self.asrt_rcolor+'\n' +
                                'Asrt stim color (explicit, cued):' + '\t' + self.asrt_pcolor+'\n' +
                                'Background color:' + '\t' + self.asrt_background+'\n' +
                                '\n' +
                                'Az alábbi beállítások minden személyre érvényesek és irányadóak\n\n' +

                                'A beállítások azokra a kísérletekre vonatkoznak, amelyeket ebből a mappából,\n' +
                                'az itt található scripttel indítottak. Ha más beállításokat (is) szeretnél alkalmazni,\n' +
                                'úgy az asrt.py és az instrukciókat tartalmazó .txt fájlt másold át egy másik könyvtárba is,\n' +
                                'és annak a scriptnek az indításakor megadhatod a kívánt másmilyen beállításokat.\n\n' +

                                'Figyelj rá, hogy mindig abból a könyvtárból indítsd a scriptet, ahol a számodra megfelelő\n' +
                                'beállítások vannak elmentve.\n\n' +

                                'A settings.dat fájl kitörlésével a beállítások megváltoztathatóak; ugyanakkor a fájl\n' +
                                'törlése a későbbi átláthatóság miatt nem javasolt. Ha mégis a törlés mellett döntenél,\n' +
                                'jelen .txt fájlt előtte másold, hogy a korábbi beállításokra is emlékezhess, ha szükséges lesz.\n')

    def get_maxtrial(self):
        return (self.blockprepN + self.blocklengthN) * self.epochN * self.block_in_epochN

    def get_block_starts(self):
        if self.blockstarts == None:
            self.blockstarts = [1]
            for i in range(1, self.epochN * self.block_in_epochN + 2):
                self.blockstarts.append(
                    i * (self.blocklengthN + self.blockprepN) + 1)

        return self.blockstarts

    def get_session_starts(self):
        if self.sessionstarts == None:
            self.sessionstarts = [1]
            epochs_cumulative = []
            e_temp = 0
            for e in self.epochs:
                e_temp += e
                epochs_cumulative.append(e_temp)

            for e in epochs_cumulative:
                self.sessionstarts.append(
                    e * self.block_in_epochN * (self.blocklengthN + self.blockprepN) + 1)

        return self.sessionstarts

    def show_basic_settings_dialog(self):
        """ Ask the user to specify the number of groups and the number of sessions."""

        settings_dialog = gui.Dlg(title=u'Beállítások')
        settings_dialog.addText(
            u'Még nincsenek beállítások mentve ehhez a kísérlethez...')
        settings_dialog.addText(
            u'A logfile optimalizálása érdekében kérjük add meg, hányféle csoporttal tervezed az adatfelvételt.')
        settings_dialog.addField(
            u'Kiserleti + Kontrollcsoportok szama osszesen', 2)
        settings_dialog.addText(u'Hány ülés (session) lesz a kísérletben?')
        settings_dialog.addField(u'Ulesek szama', 2)
        returned_data = settings_dialog.show()
        if settings_dialog.OK:
            self.numsessions = returned_data[1]
            return returned_data[0]
        else:
            core.quit()

    def show_group_settings_dialog(self, numgroups, dict_accents):
        """Ask the user to specify the name of the groups.
           Returns the list of group names.
        """

        if numgroups > 1:
            self.groups = []
            settings_dialog = gui.Dlg(title=u'Beállítások')
            settings_dialog.addText(
                u'A csoportok megnevezése a következő (pl. kísérleti, kontroll, ....) ')
            for i in range(numgroups):
                settings_dialog.addField(u'Csoport ' + str(i + 1))
            returned_data = settings_dialog.show()
            if settings_dialog.OK:
                for ii in returned_data:
                    ii = ii.lower()
                    ii = ii.replace(' ', '_')
                    ii = ii.replace('-', '_')
                    for accent in dict_accents.keys():
                        ii = ii.replace(accent, dict_accents[accent])
                    self.groups.append(ii)
            else:
                core.quit()
        else:
            self.groups = ['nincsenek csoportok']

    def show_epoch_and_block_settings_dialog(self):
        """Ask the user to specify preparation trials' number, block length, number of blocks in an epoch
           epoch number and asrt type in the different sessions.
        """

        settings_dialog = gui.Dlg(title=u'Beállítások')
        settings_dialog.addText(u'Kísérlet felépítése ')
        settings_dialog.addField(
            u'Randomok gyakorlaskent a blokk elejen (ennyi db):', 5)
        settings_dialog.addField(u'Eles probak a blokkban:', 80)
        settings_dialog.addField(u'Blokkok szama egy epochban:', 5)
        for i in range(self.numsessions):
            settings_dialog.addField(
                u'Session ' + str(i + 1) + u' epochok szama', 5)
        for i in range(self.numsessions):
            settings_dialog.addField(
                u'Session ' + str(i + 1) + u' ASRT tipusa', choices=["implicit", "explicit", "noASRT"])
        returned_data = settings_dialog.show()
        if settings_dialog.OK:
            self.blockprepN = returned_data[0]
            self.blocklengthN = returned_data[1]
            self.block_in_epochN = returned_data[2]
            self.epochN = 0
            self.epochs = []
            self.asrt_types = {}
            for k in range(self.numsessions):
                self.epochN += returned_data[3 + k]
                self.epochs.append(returned_data[3 + k])
            for k in range(self.numsessions):
                self.asrt_types[k + 1] = returned_data[3 +
                                                       self.numsessions + k]
        else:
            core.quit()

    def show_computer_and_display_settings_dialog(self):
        """Ask the user to specify preparation trials' number, block length, number of blocks in an epoch
           epoch number and asrt type in the different sessions.
        """
        possible_colors = ["AliceBlue", "AntiqueWhite", "Aqua", "Aquamarine", "Azure", "Beige", "Bisque", "Black", "BlanchedAlmond", "Blue", "BlueViolet", "Brown", "BurlyWood", "CadetBlue", "Chartreuse", "Chocolate", "Coral", "CornflowerBlue", "Cornsilk", "Crimson", "Cyan", "DarkBlue", "DarkCyan", "DarkGoldenRod", "DarkGray", "DarkGrey", "DarkGreen", "DarkKhaki", "DarkMagenta", "DarkOliveGreen", "DarkOrange", "DarkOrchid", "DarkRed", "DarkSalmon", "DarkSeaGreen", "DarkSlateBlue", "DarkSlateGray", "DarkSlateGrey", "DarkTurquoise", "DarkViolet", "DeepPink", "DeepSkyBlue", "DimGray", "DimGrey", "DodgerBlue", "FireBrick", "FloralWhite", "ForestGreen", "Fuchsia", "Gainsboro", "GhostWhite", "Gold", "GoldenRod", "Gray", "Grey", "Green", "GreenYellow", "HoneyDew", "HotPink", "IndianRed", "Indigo", "Ivory", "Khaki", "Lavender", "LavenderBlush", "LawnGreen", "LemonChiffon", "LightBlue", "LightCoral", "LightCyan", "LightGoldenRodYellow", "LightGray", "LightGrey", "LightGreen",
                           "LightPink", "LightSalmon", "LightSeaGreen", "LightSkyBlue", "LightSlateGray", "LightSlateGrey", "LightSteelBlue", "LightYellow", "Lime", "LimeGreen", "Linen", "Magenta", "Maroon", "MediumAquaMarine", "MediumBlue", "MediumOrchid", "MediumPurple", "MediumSeaGreen", "MediumSlateBlue", "MediumSpringGreen", "MediumTurquoise", "MediumVioletRed", "MidnightBlue", "MintCream", "MistyRose", "Moccasin", "NavajoWhite", "Navy", "OldLace", "Olive", "OliveDrab", "Orange", "OrangeRed", "Orchid", "PaleGoldenRod", "PaleGreen", "PaleTurquoise", "PaleVioletRed", "PapayaWhip", "PeachPuff", "Peru", "Pink", "Plum", "PowderBlue", "Purple", "RebeccaPurple", "Red", "RosyBrown", "RoyalBlue", "SaddleBrown", "Salmon", "SandyBrown", "SeaGreen", "SeaShell", "Sienna", "Silver", "SkyBlue", "SlateBlue", "SlateGray", "SlateGrey", "Snow", "SpringGreen", "SteelBlue", "Tan", "Teal", "Thistle", "Tomato", "Turquoise", "Violet", "Wheat", "White", "WhiteSmoke", "Yellow", "YellowGreen"]

        settings_dialog = gui.Dlg(title=u'Beállítások')
        settings_dialog.addText(u'A számítógépről...')
        settings_dialog.addField(u'Hasznos kepernyo szelessege (cm)', 34.2)
        settings_dialog.addField(
            u'Szamitogep fantazianeve (ekezet nelkul)', u'Laposka')
        settings_dialog.addText(u'Megjelenés..')
        settings_dialog.addField(
            u'Ingerek tavolsaga (kozeppontok kozott) (cm)', 3)
        settings_dialog.addField(u'Ingerek sugara (cm)', 1)
        settings_dialog.addField(
            u'ASRT inger szine (elsodleges, R)', choices=possible_colors, initial="Orange")
        settings_dialog.addField(
            u'ASRT inger szine (masodlagos, P, explicit asrtnel)', choices=possible_colors, initial="Green")
        settings_dialog.addField(
            u'Hatter szine', choices=possible_colors, initial="Ivory")
        settings_dialog.addField(u'RSI (ms)', 120)
        returned_data = settings_dialog.show()
        if settings_dialog.OK:
            self.monitor_width = returned_data[0]
            self.computer_name = returned_data[1]
            self.asrt_distance = returned_data[2]
            self.asrt_size = returned_data[3]
            self.asrt_rcolor = returned_data[4]
            self.asrt_pcolor = returned_data[5]
            self.asrt_background = returned_data[6]
            self.RSI_time = float(returned_data[7]) / 1000
        else:
            core.quit()

    def show_key_and_feedback_settings_dialog(self):
        """Ask the user to specify the keys used during the experiement and also set options related to the displayed feedback."""

        settings_dialog = gui.Dlg(title=u'Beállítások')
        settings_dialog.addText(u'Válaszbillentyűk')
        settings_dialog.addField(u'Bal szelso:', 'y')
        settings_dialog.addField(u'Bal kozep', 'c')
        settings_dialog.addField(u'Jobb kozep', 'b')
        settings_dialog.addField(u'Jobb szelso', 'm')
        settings_dialog.addField(u'Kilepes', 'q')
        settings_dialog.addField(
            u'Figyelmeztetes pontossagra/sebessegre:', True)
        settings_dialog.addText(
            u'Ha be van kapcsolva a figyelmeztetés, akkor...:')
        settings_dialog.addField(
            u'Figyelmeztetes sebessegre ezen pontossag felett (%):', 93)
        settings_dialog.addField(
            u'Figyelmeztetes sebessegre ezen pontossag felett (%):', 91)
        returned_data = settings_dialog.show()
        if settings_dialog.OK:
            self.key1 = returned_data[0]
            self.key2 = returned_data[1]
            self.key3 = returned_data[2]
            self.key4 = returned_data[3]
            self.key_quit = returned_data[4]
            self.whether_warning = returned_data[5]
            self.speed_warning = returned_data[6]
            self.acc_warning = returned_data[7]
        else:
            core.quit()


class InstructionHelper:
    """ Class for handle instruction strings (reading from file, storing and displaying)"""

    def __init__(self, instructions_file_path):
        self.insts = []                 # instructions in the beginning of the experiment
        # feedback for the subject about speed and accuracy in the explicit asrt case
        self.feedback_exp = []
        # feedback for the subject about speed and accuracy in the explicit asrt case
        self.feedback_imp = []
        # speed feedback line embedded into feedback_imp / feedback_exp
        self.feedback_speed = []
        # accuracy feedback line embedded into feedback_imp / feedback_exp
        self.feedback_accuracy = []
        self.ending = []                # message in the end of the experiment
        # shown message when continuing sessions after the previous data recoding was quited
        self.unexp_quit = []

        self.instructions_file_path = instructions_file_path

    def read_insts_from_file(self):
        """Be aware of that line endings are preserved during reading instructions."""

        try:
            with codecs.open(self.instructions_file_path, 'r', encoding='utf-8') as inst_feedback:
                all_inst_feedback = inst_feedback.read().split('***')
        except:
            all_inst_feedback = []

        for all in all_inst_feedback:
            all = all.split('#')
            if len(all) >= 2:
                if 'inst' in all[0]:
                    self.insts.append(all[1])
                elif 'feedback explicit' in all[0]:
                    self.feedback_exp.append(all[1])
                elif 'feedback implicit' in all[0]:
                    self.feedback_imp.append(all[1])
                elif 'speed' in all[0]:
                    self.feedback_speed.append(all[1])
                elif 'accuracy' in all[0]:
                    self.feedback_accuracy.append(all[1])
                elif 'ending' in all[0]:
                    self.ending.append(all[1])
                elif 'unexpected quit' in all[0]:
                    self.unexp_quit.append(all[1])

    def __print_to_screen(self, mytext, mywindow):
        """Display given string in the given window."""

        text_stim = visual.TextStim(
            mywindow, text=mytext, units='cm', height=0.6, color='black')
        text_stim.draw()

    def __show_message(self, instruction_list, mywindow, expriment_settings):
        """Display simple instructions on the screen."""

        # There can be more instructions to display successively
        for inst in instruction_list:
            self.__print_to_screen(inst, mywindow)
            mywindow.flip()
            tempkey = event.waitKeys(keyList=[expriment_settings.key1, expriment_settings.key2,
                                              expriment_settings.key3, expriment_settings.key4, expriment_settings.key_quit])
            if expriment_settings.key_quit in tempkey:
                core.quit()

    def show_instructions(self, mywindow, expriment_settings):
        self.__show_message(self.insts, mywindow, expriment_settings)

    def show_unexp_quit(self, mywindow, expriment_settings):
        self.__show_message(self.unexp_quit, mywindow, expriment_settings)

    def show_ending(self, mywindow, expriment_settings):
        self.__show_message(self.ending, mywindow, expriment_settings)

    def feedback_explicit(self, rt_mean, rt_mean_p, acc_for_pattern, acc_for_the_whole, acc_for_the_whole_str, mywindow, expriment_settings):

        for l in self.feedback_exp:
            l = l.replace('*MEANRT*', rt_mean)
            l = l.replace('*MEANRTP*', rt_mean_p)
            l = l.replace('*PERCACCP*', acc_for_pattern)
            l = l.replace('*PERCACC*', acc_for_the_whole_str)

            if expriment_settings.whether_warning is True:
                if acc_for_the_whole > expriment_settings.speed_warning:
                    l = l.replace('*SPEEDACC*', self.feedback_speed[0])
                elif acc_for_the_whole < expriment_settings.acc_warning:
                    l = l.replace('*SPEEDACC*', self.feedback_accuracy[0])
                else:
                    l = l.replace('*SPEEDACC*', '')
            else:
                l = l.replace('*SPEEDACC*', '')

            self.__print_to_screen(l, mywindow)
            mywindow.flip()
            tempkey = event.waitKeys(keyList=[expriment_settings.key1, expriment_settings.key2,
                                              expriment_settings.key3, expriment_settings.key4, expriment_settings.key_quit])
        if expriment_settings.key_quit in tempkey:
            return 'quit'
        else:
            return 'continue'

    def feedback_implicit(self, rt_mean, acc_for_the_whole, acc_for_the_whole_str, mywindow, expriment_settings):

        for i in self.feedback_imp:
            i = i.replace('*MEANRT*', rt_mean)
            i = i.replace('*PERCACC*', acc_for_the_whole_str)

            if expriment_settings.whether_warning is True:
                if acc_for_the_whole > expriment_settings.speed_warning:
                    i = i.replace('*SPEEDACC*', self.feedback_speed[0])
                elif acc_for_the_whole < expriment_settings.acc_warning:
                    i = i.replace('*SPEEDACC*', self.feedback_accuracy[0])
                else:
                    i = i.replace('*SPEEDACC*', '')
            else:
                i = i.replace('*SPEEDACC*', '')

            self.__print_to_screen(i, mywindow)
            mywindow.flip()
            tempkey = event.waitKeys(keyList=[expriment_settings.key1, expriment_settings.key2,
                                              expriment_settings.key3, expriment_settings.key4, expriment_settings.key_quit])
        if expriment_settings.key_quit in tempkey:
            return 'quit'
        else:
            return 'continue'


class PersonDataHandler:

    def __init__(self, subject_id, all_settings_file_path, all_IDs_file_path, subject_list_file_path, output_file_path):
        self.subject_id = subject_id
        self.all_settings_file_path = all_settings_file_path
        self.all_IDs_file_path = all_IDs_file_path
        self.subject_list_file_path = subject_list_file_path
        self.output_file_path = output_file_path

    def load_person_settings(self, experiment):
        try:
            with shelve.open(self.all_settings_file_path, 'r') as this_person_settings:

                experiment.PCodes = this_person_settings['PCodes']
                experiment.stim_output_line = this_person_settings['stim_output_line']

                experiment.stim_sessionN = this_person_settings['stim_sessionN']
                experiment.stimepoch = this_person_settings['stimepoch']
                experiment.stimblock = this_person_settings['stimblock']
                experiment.stimtrial = this_person_settings['stimtrial']

                experiment.stimlist = this_person_settings['stimlist']
                experiment.stimpr = this_person_settings['stimpr']
                experiment.last_N = this_person_settings['last_N']
                experiment.end_at = this_person_settings['end_at']
        except:
            experiment.PCodes = {}
            experiment.stim_output_line = 0
            experiment.stim_sessionN = {}
            experiment.stimepoch = {}
            experiment.stimblock = {}
            experiment.stimtrial = {}
            experiment.stimlist = {}
            experiment.stimpr = {}
            experiment.last_N = 0
            experiment.end_at = {}

    def save_person_settings(self, experiment):
        with shelve.open(self.all_settings_file_path, 'n') as this_person_settings:
            this_person_settings['PCodes'] = experiment.PCodes
            this_person_settings['stim_output_line'] = experiment.stim_output_line

            this_person_settings['stim_sessionN'] = experiment.stim_sessionN
            this_person_settings['stimepoch'] = experiment.stimepoch
            this_person_settings['stimblock'] = experiment.stimblock
            this_person_settings['stimtrial'] = experiment.stimtrial

            this_person_settings['stimlist'] = experiment.stimlist
            this_person_settings['stimpr'] = experiment.stimpr
            this_person_settings['last_N'] = experiment.last_N
            this_person_settings['end_at'] = experiment.end_at

    def update_subject_IDs_files(self):
        all_IDs = []
        with shelve.open(self.all_IDs_file_path) as all_IDs_file:
            try:
                all_IDs = all_IDs_file['ids']
            except:
                all_IDs = []

            if self.subject_id not in all_IDs:
                all_IDs.append(self.subject_id)
                all_IDs_file['ids'] = all_IDs

        with codecs.open(self.subject_list_file_path, 'w', encoding='utf-8') as subject_list_file:
            for id in all_IDs:
                id_segmented = id.replace('_', '\t', 2)
                subject_list_file.write(id_segmented)
                subject_list_file.write('\n')

    def append_to_output_file(self, string_to_append):
        if not os.path.isfile(self.output_file_path):
            with codecs.open(self.output_file_path, 'w', encoding='utf-8') as output_file:
                self.add_heading_to_output(output_file)
                output_file.write(string_to_append)
        else:
            with codecs.open(self.output_file_path, 'a+', encoding='utf-8') as output_file:
                output_file.write(string_to_append)

    def write_data_to_output(self, experiment, asrt_type, PCode, N, stim_RSI, stim_RT_time, stim_RT_date, stimRT, stimACC, stimbutton, stimcolor):
        output_data = [experiment.settings.computer_name,
                       experiment.group,
                       experiment.identif,
                       experiment.subject_nr,
                       asrt_type,
                       PCode,

                       experiment.stim_output_line,

                       experiment.stim_sessionN[N],
                       experiment.stimepoch[N],
                       experiment.stimblock[N],
                       experiment.stimtrial[N],

                       stim_RSI,
                       experiment.frame_rate,
                       experiment.frame_time,
                       experiment.frame_sd,
                       stim_RT_time,
                       stim_RT_date,

                       stimcolor,
                       experiment.stimpr[N],
                       stimRT,
                       stimACC,

                       experiment.stimlist[N],
                       stimbutton]
        output = "\n"
        for data in output_data:
            if isinstance(data, numbers.Number):
                data = str(data)
                data = data.replace('.', ',')
            else:
                data = str(data)
            output += data + '\t'
        self.append_to_output_file(output)

    def add_heading_to_output(self, output_file):
        heading_list = ['computer_name',
                        'Group',
                        'Subject_ID',
                        'Subject_nr',
                        'asrt_type',
                        'PCode',

                        'output_line',

                        'session',
                        'epoch',
                        'block',
                        'trial',

                        'RSI_time',
                        'frame_rate',
                        'frame_time',
                        'frame_sd',
                        'date',
                        'time',

                        'stimulus_color',
                        'PR',
                        'RT',
                        'error',
                        'stimulus',
                        'stimbutton',
                        'quit_log']

        for h in heading_list:
            output_file.write(h + '\t')


class Experiment:

    def __init__(self, thispath):
        self.thispath = thispath
        self.dict_accents = {u'á': u'a', u'é': u'e', u'í': u'i', u'ó': u'o',
                             u'ő': u'o', u'ö': u'o', u'ú': u'u', u'ű': u'u', u'ü': u'u'}

        self.colors = None
        self.settings = None
        self.instructions = None
        self.pressed_dict = None
        self.dict_pos = None

        self.mywindow = None
        self.frame_time = None
        self.frame_sd = None
        self.frame_rate = None

        self.group = None
        self.subject_nr = None
        self.identif = None

        self.person_data = None

        self.PCodes = None
        self.stim_output_line = None
        self.stim_sessionN = None
        self.stimepoch = None
        self.stimblock = None
        self.stimtrial = None
        self.stimlist = None
        self.last_N = None
        self.end_at = None
        self.stimpr = None

    def all_settings_def(self):

        try:
            # check whether the settings file is in place
            self.settings.read_from_file()

        # if there is no settings file, we ask the user to specfiy the settings
        except:
            # get the number of groups and number of sessions
            numgroups = self.settings.show_basic_settings_dialog()

            # get the group names from the user
            self.settings.show_group_settings_dialog(
                numgroups, self.dict_accents)

            # get epoch and block settings (block number, trial number, epoch number, etc)
            self.settings.show_epoch_and_block_settings_dialog()

            # get montior / computer settings, and also options about displaying (stimulus size, stimulus distance, etc)
            self.settings.show_computer_and_display_settings_dialog()

            # get keyboard settings (reaction keys and quit key) and also feedback settings (accuracy and speed feedback, etc)
            self.settings.show_key_and_feedback_settings_dialog()

            # save the settings sepcifed by the user in the different dialogs
            self.settings.write_to_file()

            # write out a text file with the experiment settings data, so the user can check settings in a human readable form
            self.settings.write_out_reminder()

    def show_subject_settings_dialog(self):
        """Ask the user to specify the subject's attributes (name, subject number, group)."""

        warningtext = ''
        itsOK = False
        while not itsOK:
            settings_dialog = gui.Dlg(title=u'Beállítások')
            settings_dialog.addText('')
            settings_dialog.addText(warningtext, color='Red')
            settings_dialog.addField(u'Nev', u"Alattomos Aladar")
            settings_dialog.addField(u'Sorszam', "0")
            if len(self.settings.groups) > 1:
                settings_dialog.addField(
                    u'Csoport', choices=self.settings.groups)

            returned_data = settings_dialog.show()
            if settings_dialog.OK:
                name = returned_data[0]
                name = name.lower()
                name = name.replace(' ', '-')
                name = name.replace('_', '-')
                for accent in self.dict_accents.keys():
                    name = name.replace(accent, self.dict_accents[accent])
                self.identif = name

                subject_number = returned_data[1]
                if len(self.settings.groups) > 1:
                    self.group = returned_data[2]
                else:
                    self.group = ""

                try:
                    subject_number = int(subject_number)
                    if subject_number >= 0:
                        itsOK = 1
                        self.subject_nr = subject_number
                    else:
                        warningtext = u'Pozitív egész számot adj meg a sorszámhoz!'

                except:
                    warningtext = u'Pozitív egész számot adj meg a sorszámhoz!'

            else:
                core.quit()

    def show_subject_continuation_dialog(self):
        if self.last_N + 1 <= self.settings.get_maxtrial():
            expstart11 = gui.Dlg(title=u'Feladat indítása...')
            expstart11.addText(u'A személy adatait beolvastam.')
            expstart11.addText(u'Folytatás innen...')
            expstart11.addText(
                'Session: ' + str(self.stim_sessionN[self.last_N + 1]))
            expstart11.addText('Epoch: '+str(self.stimepoch[self.last_N + 1]))
            expstart11.addText('Block: '+str(self.stimblock[self.last_N + 1]))
            expstart11.addText('Trial: '+str(self.stimtrial[self.last_N + 1]))
            expstart11.show()
            if not expstart11.OK:
                core.quit()
        else:
            expstart11 = gui.Dlg(title=u'Feladat indítása...')
            expstart11.addText(u'A személy adatait beolvastam.')
            expstart11.addText(u'A személy végigcsinálta a feladatot.')
            expstart11.show()
            core.quit()

    def show_subject_PCodes_dialog(self):
        settings_dialog = gui.Dlg(title=u'Beállítások')
        settings_dialog.addText('')
        for z in range(self.settings.numsessions):
            if self.settings.asrt_types[z+1] == "noASRT":
                settings_dialog.addFixedField(
                    u'Session ' + str(z+1) + ' PCode', 'noPattern')
            else:
                settings_dialog.addField(u'Session ' + str(z+1) + ' PCode', choices=[
                                         '1st - 1234', '2nd - 1243', '3rd - 1324', '4th - 1342', '5th - 1423', '6th - 1432'])

        returned_data = settings_dialog.show()
        if settings_dialog.OK:
            self.PCodes = {}

            for zz in range(self.settings.numsessions):
                self.PCodes[zz+1] = returned_data[zz]

            return self.PCodes
        else:
            core.quit()

    def which_code(self, session_number):
        pcode_raw = self.PCodes[session_number]
        PCode = 'noPattern'

        if pcode_raw == '1st - 1234':
            PCode = '1234'
        elif pcode_raw == '2nd - 1243':
            PCode = '1243'
        elif pcode_raw == '3rd - 1324':
            PCode = '1324'
        elif pcode_raw == '4th - 1342':
            PCode = '1342'
        elif pcode_raw == '5th - 1423':
            PCode = '1423'
        elif pcode_raw == '6th - 1432':
            PCode = '1432'
        return PCode

    def calculate_stim_properties(self):
        all_trial_Nr = 0
        block_num = 0

        sessionsstarts = self.settings.get_session_starts()
        for trial_num in range(1, self.settings.get_maxtrial()+1):
            for session_num in range(1, len(sessionsstarts)):
                if trial_num >= sessionsstarts[session_num-1] and trial_num < sessionsstarts[session_num]:
                    self.stim_sessionN[trial_num] = session_num
                    self.end_at[trial_num] = sessionsstarts[session_num]

        for epoch in range(1, self.settings.epochN+1):

            for block in range(1, self.settings.block_in_epochN+1):
                block_num += 1
                current_trial_num = 0

                # practice
                for practice in range(1, self.settings.blockprepN+1):
                    current_trial_num += 1

                    all_trial_Nr += 1
                    asrt_type = self.settings.asrt_types[self.stim_sessionN[all_trial_Nr]]

                    current_stim = random.choice([1, 2, 3, 4])
                    self.stimlist[all_trial_Nr] = current_stim
                    self.stimpr[all_trial_Nr] = "R"
                    self.stimtrial[all_trial_Nr] = current_trial_num
                    self.stimblock[all_trial_Nr] = block_num
                    self.stimepoch[all_trial_Nr] = epoch

                # real
                for real in range(1, self.settings.blocklengthN+1):

                    current_trial_num += 1
                    all_trial_Nr += 1

                    asrt_type = self.settings.asrt_types[self.stim_sessionN[all_trial_Nr]]
                    PCode = self.which_code(self.stim_sessionN[all_trial_Nr])

                    dict_HL = {}
                    if not PCode == "noPattern":
                        dict_HL[PCode[0]] = PCode[1]
                        dict_HL[PCode[1]] = PCode[2]
                        dict_HL[PCode[2]] = PCode[3]
                        dict_HL[PCode[3]] = PCode[0]

                    if self.settings.blockprepN % 2 == 1:
                        mod_pattern = 0
                    else:
                        mod_pattern = 1

                    if current_trial_num % 2 == mod_pattern and asrt_type != "noASRT":
                        if all_trial_Nr > 2:
                            current_stim = int(
                                dict_HL[str(self.stimlist[all_trial_Nr-2])])
                        else:
                            # first pattern stim is random
                            current_stim = random.choice([1, 2, 3, 4])
                        self.stimpr[all_trial_Nr] = "P"
                    else:
                        current_stim = random.choice([1, 2, 3, 4])
                        self.stimpr[all_trial_Nr] = "R"

                    self.stimlist[all_trial_Nr] = current_stim
                    self.stimtrial[all_trial_Nr] = current_trial_num
                    self.stimblock[all_trial_Nr] = block_num
                    self.stimepoch[all_trial_Nr] = epoch

    def participant_id(self):
        self.show_subject_settings_dialog()

        subject_id = self.identif + '_' + \
            str(self.subject_nr) + '_' + self.group
        all_settings_file_path = os.path.join(
            self.thispath, "settings", subject_id)
        all_IDs_file_path = os.path.join(
            self.thispath, "settings", "participant_settings")
        subject_list_file_path = os.path.join(
            self.thispath, "settings", "participants_in_experiment.txt")
        output_file_path = os.path.join(
            self.thispath, "logs", subject_id + '_log.txt')
        self.person_data = PersonDataHandler(
            subject_id,  all_settings_file_path, all_IDs_file_path, subject_list_file_path, output_file_path)

        self.person_data.update_subject_IDs_files()

        self.person_data.load_person_settings(self)

        if self.last_N > 0:
            self.show_subject_continuation_dialog()

        else:
            self.show_subject_PCodes_dialog()

            self.calculate_stim_properties()

            self.person_data.save_person_settings(self)

    def monitor_settings(self):
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()

        # Monitor beállítása
        my_monitor = monitors.Monitor('myMon')
        my_monitor.setSizePix([screen.width, screen.height])
        my_monitor.setWidth(self.settings.monitor_width)  # cm-ben
        my_monitor.saveMon()

        return my_monitor

    def print_to_screen(self, mytext):
        xtext = visual.TextStim(
            self.mywindow, text=mytext, units="cm", height=0.6, color="black")
        xtext.draw()

    def frame_check(self):
        # monitorral kapcsolatos informáciok
        self.print_to_screen(
            u'Adatok előkészítése folyamatban. \nEz eltarthat pár másodpercig. \nAddig semmit sem fogsz látni a képernyőn...')
        self.mywindow.flip()
        core.wait(2)

        ms_per_frame = self.mywindow.getMsPerFrame(nFrames=120)
        self.frame_time = ms_per_frame[0]
        self.frame_sd = ms_per_frame[1]
        self.frame_rate = self.mywindow.getActualFrameRate()

    def stim_bg(self):
        stimbg = visual.Circle(win=self.mywindow, radius=1, units="cm",
                               fillColor=None, lineColor=self.colors['linecolor'])
        for i in range(1, 5):
            stimbg.pos = self.dict_pos[i]
            stimbg.draw()

    def show_feedback(self, N, number_of_patterns, patternERR, Npressed_in_block, accs_in_block, RT_all_list, RT_pattern_list):

        acc_for_the_whole = 100 * \
            float(Npressed_in_block - sum(accs_in_block)) / Npressed_in_block
        acc_for_the_whole_str = str(acc_for_the_whole)[0:5].replace('.', ',')

        rt_mean = float(sum(RT_all_list)) / len(RT_all_list)
        rt_mean_str = str(rt_mean)[:5].replace('.', ',')

        if self.settings.asrt_types[self.stim_sessionN[N-1]] == 'explicit':

            try:
                rt_mean_p = float(sum(RT_pattern_list)) / len(RT_pattern_list)
                rt_mean_p_str = str(rt_mean_p)[:5].replace('.', ',')
            except:
                rt_mean_p_str = 'N/A'

            try:
                acc_for_patterns = 100 * \
                    float(number_of_patterns - patternERR) / number_of_patterns
                acc_for_patterns_str = str(acc_for_patterns)[
                    0:5].replace('.', ',')
            except:
                acc_for_patterns_str = 'N/A'

            whatnow = self.instructions.feedback_explicit(
                rt_mean_str, rt_mean_p_str, acc_for_patterns_str, acc_for_the_whole, acc_for_the_whole_str, self.mywindow, self.settings)
        else:
            whatnow = self.instructions.feedback_implicit(
                rt_mean_str, acc_for_the_whole, acc_for_the_whole_str, self.mywindow, self.settings)

        return whatnow

    def presentation(self):

        # Init circle stimulus
        stimP = visual.Circle(win=self.mywindow, radius=self.settings.asrt_size, units="cm",
                              fillColor=self.colors['stimp'], lineColor=self.colors['linecolor'], pos=self.dict_pos[1])
        stimR = visual.Circle(win=self.mywindow, radius=self.settings.asrt_size, units="cm",
                              fillColor=self.colors['stimr'], lineColor=self.colors['linecolor'], pos=self.dict_pos[1])

        RSI_timer = 0.0
        N = self.last_N + 1

        # Show instructions or continuation message
        if N in self.settings.get_session_starts():
            self.instructions.show_instructions(self.mywindow, self.settings)

        else:
            self.instructions.show_unexp_quit(self.mywindow, self.settings)

        Npressed_in_block = 0
        accs_in_block = []

        asrt_type = self.settings.asrt_types[self.stim_sessionN[N]]
        PCode = self.which_code(self.stim_sessionN[N])

        allACC = 0
        patternERR = 0
        number_of_patterns = 0

        RT_pattern_list = []
        RT_all_list = []

        RSI = core.StaticPeriod(screenHz=self.frame_rate)
        RSI_clock = core.Clock()
        trial_clock = core.Clock()

        while True:

            self.stim_bg()
            self.mywindow.flip()

            RSI_clock.reset()
            RSI.start(self.settings.RSI_time)

            if self.stimpr[N] == 'P':
                if self.settings.asrt_types[self.stim_sessionN[N]] == 'explicit':
                    stimP.fillColor = self.colors['stimp']
                else:
                    stimP.fillColor = self.colors['stimr']
                stimcolor = stimP.fillColor
                stimP.setPos(self.dict_pos[self.stimlist[N]])
            else:
                stimcolor = self.colors['stimr']
                stimR.setPos(self.dict_pos[self.stimlist[N]])

            RSI.complete()

            cycle = 0
            allACC = 0

            while True:
                cycle += 1
                self.stim_bg()

                if self.stimpr[N] == 'P':
                    stimP.draw()
                else:
                    stimR.draw()
                self.mywindow.flip()

                if cycle == 1:
                    RSI_timer = RSI_clock.getTime()

                trial_clock.reset()
                press = event.waitKeys(keyList=[self. settings.key1, self.settings.key2, self.settings.key3,
                                                self.settings.key4, self.settings.key_quit], timeStamped=trial_clock)

                stim_RT_time = time.strftime('%H:%M:%S')
                stim_RT_date = time.strftime('%d/%m/%Y')
                stimRT = press[0][1]

                self.stim_output_line += 1
                Npressed_in_block += 1

                if cycle == 1:
                    stim_first_RT = press[0][1]

                stimbutton = press[0][0]
                stim_RSI = RSI_timer

                if press[0][0] == self.settings.key_quit:
                    self.print_to_screen("Quit...\nSaving data...")
                    self.mywindow.flip()

                    self.person_data.append_to_output_file('userquit')

                    self.stim_output_line -= 1

                    if N >= 1:
                        self.last_N = N-1

                    self.person_data.save_person_settings(self)
                    core.quit()

                elif self.pressed_dict[press[0][0]] == self.stimlist[N]:
                    stimACC = 0
                    accs_in_block.append(0)

                    if self.stimpr[N] == 'P':
                        number_of_patterns += 1
                        RT_pattern_list.append(stimRT)
                    RT_all_list.append(stimRT)

                else:
                    stimACC = 1
                    allACC += 1
                    accs_in_block.append(1)

                    if self.stimpr[N] == 'P':
                        patternERR += 1
                        number_of_patterns += 1
                        RT_pattern_list.append(stimRT)
                    RT_all_list.append(stimRT)
                stim_allACC = allACC

                self.person_data.write_data_to_output(
                    self, asrt_type, PCode, N, stim_RSI, stim_RT_time, stim_RT_date, stimRT, stimACC, stimbutton, stimcolor)

                if stimACC == 0:
                    self.last_N = N
                    N += 1

                    break

            if N in self.settings.get_block_starts():  # n+1 volt

                self.print_to_screen(
                    u"Adatok mentése és visszajelzés előkészítése...")
                self.mywindow.flip()

                whatnow = self.show_feedback(
                    N, number_of_patterns, patternERR, Npressed_in_block, accs_in_block, RT_all_list, RT_pattern_list)

                if whatnow == 'quit':
                    self.print_to_screen("Quit...\nSaving data...")
                    self.mywindow.flip()

                    self.person_data.append_to_output_file('userquit')

                    if N >= 1:
                        self.last_N = N-1

                    self.person_data.save_person_settings(self)
                    core.quit()

                patternERR = 0
                allACC = 0
                Npressed_in_block = 0

                RT_pattern_list = []
                RT_all_list = []

                accs_in_block = []

            if N == self.end_at[N-1]:
                break

    def run(self):
        ensure_dir(os.path.join(self.thispath, "logs"))
        ensure_dir(os.path.join(self.thispath, "settings"))

        # Load settings if exist or ask the user to specify them
        all_settings_file_path = os.path.join(
            self.thispath, "settings", "settings")
        reminder_file_path = os.path.join(
            self.thispath, "settings", "settings_reminder.txt")
        self.settings = ExperimentSettings(
            all_settings_file_path, reminder_file_path)
        self.all_settings_def()

        self.colors = {'wincolor': self.settings.asrt_background,
                       'linecolor': 'black',
                       'stimp': self.settings.asrt_pcolor,
                       'stimr': self.settings.asrt_rcolor}
        self.pressed_dict = {self.settings.key1: 1,
                             self.settings.key2: 2,
                             self.settings.key3: 3,
                             self.settings.key4: 4}
        self.dict_pos = {1: (float(self.settings.asrt_distance) * (-1.5), 0),
                         2: (float(self.settings.asrt_distance) * (-0.5), 0),
                         3: (float(self.settings.asrt_distance) * 0.5, 0),
                         4: (float(self.settings.asrt_distance) * 1.5, 0)}

        # Read instruction strings
        inst_feedback_path = os.path.join(
            self.thispath, "inst_and_feedback.txt")
        self.instructions = InstructionHelper(inst_feedback_path)
        self.instructions.read_insts_from_file()

        self.participant_id()

        # Init window
        my_monitor = self.monitor_settings()
        with visual.Window(size=my_monitor.getSizePix(), color=self.colors['wincolor'], fullscr=False, monitor=my_monitor, units="cm") as self.mywindow:
            # Check frame rate
            self.frame_check()

            # Show the experiment screen
            self.presentation()

            # Save user data
            self.person_data.save_person_settings(self)
            self.person_data.append_to_output_file('sessionend_planned_quit')

            # Show ending screen
            self.instructions.show_ending(self.mywindow, self.settings)


if __name__ == "__main__":
    thispath = os.path.split(os.path.abspath(__file__))[0]
    experiment = Experiment(thispath)
    experiment.run()
