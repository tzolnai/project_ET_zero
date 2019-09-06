# !/usr/bin/env python
# -*- coding: utf-8 -*-

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

from psychopy import visual, core, event, gui, monitors
import shelve
import random
import codecs
import os
import pyglet
import platform
import numbers
from datetime import datetime
from io import StringIO

try:
    import tobii_research as tobii
    g_tobii_available = True
except:
    g_tobii_available = False


def ensure_dir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


def normalize_string(string, blank_char):
    dict_accents = {u'á': u'a', u'é': u'e', u'í': u'i', u'ó': u'o',
                    u'ő': u'o', u'ö': u'o', u'ú': u'u', u'ű': u'u', u'ü': u'u'}
    string = string.lower()
    string = string.replace(' ', blank_char)
    for accent in dict_accents.keys():
        string = string.replace(accent, dict_accents[accent])

    return string


class ExperimentSettings:
    """This class handles all operation related to experiment settings.
       These settings apply to all subjects in the specific experiment.
    """

    def __init__(self, settings_file_path, reminder_file_path):
        # type of the experiment (reaction time or eyetracking
        self.experiment_type = None
        # number of sessions (e.g. 10)
        self.numsessions = None
        # list of group names (e.g. ["kontrol", "kiserleti"])
        self.groups = None

        # number of practice trials at the beginning of the block (e.g. 10)
        self.blockprepN = None
        # number of real trials in one block (e.g. 10)
        self.blocklengthN = None
        # number of blocks in one epoch (e.g. 10)
        self.block_in_epochN = None
        # number of all epoch in all sessions (e.g. 12)
        self.epochN = None
        # list of epoch numbers of all sessions (e.g. [1, 2] (two sessions, first session has 1 epoch, the second has 2))
        self.epochs = None
        # list of asrt types of all sessions (e.g. ['implicit', 'explicit'] (two sessions, first session is an implicit asrt, the second one is explicit))
        self.asrt_types = None

        # monitor's physical width in 'cm' (e.g. 29)
        self.monitor_width = None
        # an imaginary name of the computer where the experiment is run (e.g. Laposka)
        self.computer_name = None
        # distance of the neighbour stimulus circles in cm (center to center distance)
        self.asrt_distance = None
        # radius of the stimulus circle in cm (e.g. 1)
        self.asrt_size = None
        # AOI (area of interest) is a suqare with the same origin as the stimuli, this size means the size of this square's side
        self.AOI_size = None
        # fill color of the random stimulus or all stimulus in case of implicit asrt (e.g. "Orange")
        self.asrt_rcolor = None
        # fill color of the "pattern" stimulus in case of explicit asrt (e.g. "Orange")
        self.asrt_pcolor = None
        # background color behind the stimulus circles  (e.g. "Ivory")
        self.asrt_background = None
        # response-to-next-stimulus time in millisecond (e.g. 120)
        self.RSI_time = None

        # key for the first stimulus (e.g. 'z')
        self.key1 = None
        # key for the second stimulus (e.g. 'v')
        self.key2 = None
        # key for the third stimulus (e.g. 'b')
        self.key3 = None
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

        # list of trial numbers indicating the first trials of the different sessions (calulcated number, e.g [1, 86, 171])
        self.sessionstarts = None
        # list of trial numbers indicating the first trials of the different blocks (calulcated number, e.g [1, 86, 171])
        self.blockstarts = None

        # settings shelve file's path
        self.settings_file_path = settings_file_path
        # settings reminder text file's path
        self.reminder_file_path = reminder_file_path

    def read_from_file(self):
        """Open settings shelve file in read-only mode and read all settings from it.

           This method expects that all known settings are in the file.
           If something is missing all read settings are dropped and also
           an exception is raised.
        """
        try:
            with shelve.open(self.settings_file_path, 'r') as settings_file:
                self.experiment_type = settings_file['experiment_type']
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
                if self.experiment_type == 'eye-tracking':
                    self.AOI_size = settings_file['AOI_size']
                self.asrt_rcolor = settings_file['asrt_rcolor']
                self.asrt_pcolor = settings_file['asrt_pcolor']
                self.asrt_background = settings_file['asrt_background']
                self.RSI_time = settings_file['RSI_time']

                if self.experiment_type == 'reaction-time':
                    self.key1 = settings_file['key1']
                    self.key2 = settings_file['key2']
                    self.key3 = settings_file['key3']
                    self.key4 = settings_file['key4']
                    self.key_quit = settings_file['key_quit']
                elif self.experiment_type == 'eye-tracking':
                    self.key_quit = 'q'

                self.whether_warning = settings_file['whether_warning']
                self.speed_warning = settings_file['speed_warning']
                self.acc_warning = settings_file['acc_warning']
        except Exception as exception:
            self.__init__(self.settings_file_path, self.reminder_file_path)
            raise exception

    def write_to_file(self):
        """Create a new settings file and write all settings into it."""

        with shelve.open(self.settings_file_path, 'n') as settings_file:
            settings_file['experiment_type'] = self.experiment_type
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
            if self.experiment_type == 'eye-tracking':
                settings_file['AOI_size'] = self.AOI_size
            settings_file['asrt_rcolor'] = self.asrt_rcolor
            settings_file['asrt_pcolor'] = self.asrt_pcolor
            settings_file['asrt_background'] = self.asrt_background
            settings_file['RSI_time'] = self.RSI_time

            if self.experiment_type == 'reaction-time':
                settings_file['key1'] = self.key1
                settings_file['key2'] = self.key2
                settings_file['key3'] = self.key3
                settings_file['key4'] = self.key4
                settings_file['key_quit'] = self.key_quit

            settings_file['whether_warning'] = self.whether_warning
            settings_file['speed_warning'] = self.speed_warning
            settings_file['acc_warning'] = self.acc_warning

    def write_out_reminder(self):
        """Write out a short summary of the settings into a text file."""

        with codecs.open(self.reminder_file_path, 'w', encoding='utf-8') as reminder_file:
            reminder = str('Beállítások\n' +
                           '\n' +
                           'Monitor Width: ' + '\t' + str(self.monitor_width).replace('.', ',') + '\n' +
                           'Computer Name: ' + '\t' + self.computer_name + '\n' +
                           'Experiment type:' + '\t' + self.experiment_type + '\n')
            if self.experiment_type == 'reaction-time':
                reminder += str('Response keys: ' + '\t' + self.key1 + ', ' + self.key2 + ', ' + self.key3 + ', ' + self.key4 + '.' + '\n' +
                                'Quit key: ' + '\t' + self.key_quit + '\n' +
                                'Warning (speed, accuracy): ' + '\t' + str(self.whether_warning) + '\n' +
                                'Speed warning at:' + '\t' + str(self.speed_warning) + '\n' +
                                'Acc warning at:' + '\t' + str(self.acc_warning) + '\n')

            reminder += str('Groups:' + '\t' + str(self.groups)[1:-1].replace("u'", '').replace("'", '') + '\n' +
                            'Sessions:' + '\t' + str(self.numsessions) + '\n' +
                            'Epochs in sessions:' + '\t' + str(self.epochs)[1:-1].replace("u'", '').replace("'", '') + '\n' +
                            'Blocks in epochs:' + '\t' + str(self.block_in_epochN) + '\n' +
                            'Preparatory Trials\\Block:' + '\t' + str(self.blockprepN) + '\n' +
                            'Trials\\Block:' + '\t' + str(self.blocklengthN) + '\n' +
                            'RSI:' + '\t' + str(self.RSI_time).replace('.', ',') + '\n' +
                            'Asrt stim distance:' + '\t' + str(self.asrt_distance) + '\n' +
                            'Asrt stim size:' + '\t' + str(self.asrt_size) + '\n')
            if self.experiment_type == 'eye-tracking':
                reminder += str('AOI size:' + '\t' + str(self.AOI_size) + '\n')

            reminder += str('Asrt stim color (implicit):' + '\t' + self.asrt_rcolor + '\n' +
                            'Asrt stim color (explicit, cued):' + '\t' + self.asrt_pcolor + '\n' +
                            'Background color:' + '\t' + self.asrt_background + '\n' +
                            '\n' +
                            'Az alábbi beállítások minden személyre érvényesek és irányadóak\n\n' +

                            'A beállítások azokra a kísérletekre vonatkoznak, amelyeket ebből a mappából,\n' +
                            'az itt található scripttel indítottak. Ha más beállításokat (is) szeretnél alkalmazni,\n' +
                            'úgy az asrt.py és az instrukciókat tartalmazó inst_and_feedback.txt fájlt másold át egy,\n' +
                            'másik könyvtárba is, és annak a scriptnek az indításakor megadhatod a kívánt másmilyen beállításokat.\n\n' +

                            'Figyelj rá, hogy mindig abból a könyvtárból indítsd a scriptet, ahol a számodra megfelelő\n' +
                            'beállítások vannak elmentve.\n\n' +

                            'A settings/settings fájl kitörlésével a beállítások megváltoztathatóak; ugyanakkor a fájl\n' +
                            'törlése a későbbi átláthatóság miatt nem javasolt. Ha mégis a törlés mellett döntenél,\n' +
                            'jelen .txt fájlt előtte másold le, hogy a korábbi beállításokra is emlékezhess, ha szükséges lesz.\n')

            reminder_file.write(reminder)

    def get_maxtrial(self):
        """Get number of all trials in the whole experiment (in all sessions)."""

        return (self.blockprepN + self.blocklengthN) * self.epochN * self.block_in_epochN

    def get_block_starts(self):
        """Return with a list of numbers indicating the first trials of the different blocks."""

        if self.blockstarts == None:
            self.blockstarts = [1]
            for i in range(1, self.epochN * self.block_in_epochN + 2):
                self.blockstarts.append(
                    i * (self.blocklengthN + self.blockprepN) + 1)

        return self.blockstarts

    def get_session_starts(self):
        """Return with a list of numbers indicating the first trials of the different sessions."""

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

    def get_key_list(self):
        if self.experiment_type == 'reaction-time':
            return [self.key1, self.key2, self.key3, self.key4, self.key_quit]
        elif self.experiment_type == 'eye-tracking':
            return ['return', self.key_quit]
        else:
            return None

    def show_basic_settings_dialog(self):
        """ Ask the user to specify the number of groups and the number of sessions."""

        settings_dialog = gui.Dlg(title=u'Beállítások')
        settings_dialog.addText(
            u'Még nincsenek beállítások mentve ehhez a kísérlethez...')
        settings_dialog.addField(u'Kísérlet típusa:', choices=[
                                 'reakció idő', 'eye-tracking'], initial="reakció idő")
        settings_dialog.addText(
            u'A logfile optimalizálása érdekében kérjük add meg, hányféle csoporttal tervezed az adatfelvételt.')
        settings_dialog.addField(
            u'Kiserleti + Kontrollcsoportok szama osszesen', 2)
        settings_dialog.addText(u'Hány ülés (session) lesz a kísérletben?')
        settings_dialog.addField(u'Ulesek szama', 2)
        returned_data = settings_dialog.show()
        if settings_dialog.OK:
            self.numsessions = returned_data[2]
            if returned_data[0] == 'reakció idő':
                self.experiment_type = 'reaction-time'
            else:
                self.experiment_type = 'eye-tracking'
                if not g_tobii_available:
                    print(
                        "For running the eye-tracking version of the experiment we need tobii_research module to be installed!")
                    core.quit()
            return returned_data[1]
        else:
            core.quit()

    def show_group_settings_dialog(self, numgroups):
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
                    ii = normalize_string(ii, "_")
                    ii = ii.replace("-", "_")
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
        settings_dialog.addField(u'Randomok gyakorlaskent a blokk elejen (ennyi db):', 5)
        settings_dialog.addField(u'Eles probak a blokkban:', 80)
        settings_dialog.addField(u'Blokkok szama egy epochban:', 5)
        for i in range(self.numsessions):
            settings_dialog.addField(u'Session ' + str(i + 1) + u' epochok szama', 5)
        for i in range(self.numsessions):
            settings_dialog.addField(u'Session ' + str(i + 1) + u' ASRT tipusa',
                                     choices=["implicit", "explicit", "noASRT"])
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
                self.asrt_types[k + 1] = returned_data[3 + self.numsessions + k]
        else:
            core.quit()

    def show_computer_and_display_settings_dialog(self):
        """Ask the user specific infromation about the computer and also change display settings."""

        possible_colors = ["AliceBlue", "AntiqueWhite", "Aqua", "Aquamarine", "Azure", "Beige", "Bisque", "Black", "BlanchedAlmond", "Blue", "BlueViolet", "Brown", "BurlyWood", "CadetBlue", "Chartreuse", "Chocolate", "Coral", "CornflowerBlue", "Cornsilk", "Crimson", "Cyan", "DarkBlue", "DarkCyan", "DarkGoldenRod", "DarkGray", "DarkGrey", "DarkGreen", "DarkKhaki", "DarkMagenta", "DarkOliveGreen", "DarkOrange", "DarkOrchid", "DarkRed", "DarkSalmon", "DarkSeaGreen", "DarkSlateBlue", "DarkSlateGray", "DarkSlateGrey", "DarkTurquoise", "DarkViolet", "DeepPink", "DeepSkyBlue", "DimGray", "DimGrey", "DodgerBlue", "FireBrick", "FloralWhite", "ForestGreen", "Fuchsia", "Gainsboro", "GhostWhite", "Gold", "GoldenRod", "Gray", "Grey", "Green", "GreenYellow", "HoneyDew", "HotPink", "IndianRed", "Indigo", "Ivory", "Khaki", "Lavender", "LavenderBlush", "LawnGreen", "LemonChiffon", "LightBlue", "LightCoral", "LightCyan", "LightGoldenRodYellow", "LightGray", "LightGrey", "LightGreen",
                           "LightPink", "LightSalmon", "LightSeaGreen", "LightSkyBlue", "LightSlateGray", "LightSlateGrey", "LightSteelBlue", "LightYellow", "Lime", "LimeGreen", "Linen", "Magenta", "Maroon", "MediumAquaMarine", "MediumBlue", "MediumOrchid", "MediumPurple", "MediumSeaGreen", "MediumSlateBlue", "MediumSpringGreen", "MediumTurquoise", "MediumVioletRed", "MidnightBlue", "MintCream", "MistyRose", "Moccasin", "NavajoWhite", "Navy", "OldLace", "Olive", "OliveDrab", "Orange", "OrangeRed", "Orchid", "PaleGoldenRod", "PaleGreen", "PaleTurquoise", "PaleVioletRed", "PapayaWhip", "PeachPuff", "Peru", "Pink", "Plum", "PowderBlue", "Purple", "RebeccaPurple", "Red", "RosyBrown", "RoyalBlue", "SaddleBrown", "Salmon", "SandyBrown", "SeaGreen", "SeaShell", "Sienna", "Silver", "SkyBlue", "SlateBlue", "SlateGray", "SlateGrey", "Snow", "SpringGreen", "SteelBlue", "Tan", "Teal", "Thistle", "Tomato", "Turquoise", "Violet", "Wheat", "White", "WhiteSmoke", "Yellow", "YellowGreen"]

        settings_dialog = gui.Dlg(title=u'Beállítások')
        settings_dialog.addText(u'A számítógépről...')
        settings_dialog.addField(u'Hasznos kepernyo szelessege (cm)', 34.2)
        settings_dialog.addField(u'Szamitogep fantazianeve (ekezet nelkul)', u'Laposka')
        settings_dialog.addText(u'Megjelenés..')

        if self.experiment_type == 'reaction-time':
            settings_dialog.addField(u'Ingerek tavolsaga (kozeppontok kozott) (cm)', 3)
        else:  # 'eye-tracking'
            settings_dialog.addField(u'Ingerek tavolsaga (kozeppontok kozott) (cm)', 10)

        settings_dialog.addField(u'Ingerek sugara (cm)', 1)
        if self.experiment_type == 'eye-tracking':
            settings_dialog.addField(u'AOI négyzetek oldahossza (cm)', 3)

        settings_dialog.addField(u'ASRT inger szine (elsodleges, R)',
                                 choices=possible_colors, initial="Orange")
        settings_dialog.addField(
            u'ASRT inger szine (masodlagos, P, explicit asrtnel)', choices=possible_colors, initial="Green")
        settings_dialog.addField(u'Hatter szine', choices=possible_colors, initial="Ivory")

        if self.experiment_type == 'reaction-time':
            settings_dialog.addField(u'RSI (ms)', 120)
        else:  # 'eye-tracking'
            settings_dialog.addField(u'RSI (ms)', 500)

        returned_data = settings_dialog.show()
        if settings_dialog.OK:
            self.monitor_width = returned_data[0]
            self.computer_name = returned_data[1]
            self.asrt_distance = returned_data[2]
            self.asrt_size = returned_data[3]
            rcolor_index = 4
            if self.experiment_type == 'eye-tracking':
                self.AOI_size = returned_data[4]
                rcolor_index = 5

            self.asrt_rcolor = returned_data[rcolor_index]
            self.asrt_pcolor = returned_data[rcolor_index + 1]
            self.asrt_background = returned_data[rcolor_index + 2]
            self.RSI_time = float(returned_data[rcolor_index + 3]) / 1000
        else:
            core.quit()

    def show_key_and_feedback_settings_dialog(self):
        """Ask the user to specify the keys used during the experiement and also set options related to the displayed feedback."""

        settings_dialog = gui.Dlg(title=u'Beállítások')
        if self.experiment_type == 'reaction-time':
            settings_dialog.addText(u'Válaszbillentyűk')
            settings_dialog.addField(u'Bal szelso:', 'y')
            settings_dialog.addField(u'Bal kozep', 'c')
            settings_dialog.addField(u'Jobb kozep', 'b')
            settings_dialog.addField(u'Jobb szelso', 'm')
            settings_dialog.addField(u'Kilepes', 'q')
        settings_dialog.addField(u'Figyelmeztetes pontossagra/sebessegre:', True)
        settings_dialog.addText(u'Ha be van kapcsolva a figyelmeztetés, akkor...:')
        settings_dialog.addField(u'Figyelmeztetes sebessegre ezen pontossag felett (%):', 93)
        settings_dialog.addField(u'Figyelmeztetes sebessegre ezen pontossag felett (%):', 91)
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
        # instructions in the beginning of the experiment (might have more elements)
        self.insts = []
        # feedback for the subject about speed and accuracy in the explicit asrt case (might be empty)
        self.feedback_exp = []
        # feedback for the subject about speed and accuracy in the implicit asrt case
        self.feedback_imp = []
        # speed feedback line embedded into feedback_imp / feedback_exp
        self.feedback_speed = []
        # accuracy feedback line embedded into feedback_imp / feedback_exp
        self.feedback_accuracy = []
        # message in the end of the experiment
        self.ending = []
        # shown message when continuing sessions after the previous data recoding was quited
        self.unexp_quit = []

        self.instructions_file_path = instructions_file_path

    def read_insts_from_file(self):
        """Read instruction strings from the instruction file using the special structure of this file.
           Be aware of that line endings are preserved during reading instructions.
        """

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

    def validate_instructions(self, settings):
        '''Do a minimal validation of the read instructions to get error messages early,
           before a missing string actualy causes an issue.'''

        if len(self.insts) == 0:
            print("Starting instruction was not specified!")
            core.quit()
        if len(self.ending) == 0:
            print("Ending message was not specified!")
            core.quit()
        if len(self.unexp_quit) == 0:
            print("Unexpected quit message was not specified!")
            core.quit()
        if settings.whether_warning and len(self.feedback_speed) == 0:
            print("Speed warning message was not specified, but warning is enabled in the settings!")
            core.quit()
        if settings.whether_warning and len(self.feedback_accuracy) == 0:
            print("Accuracy warning message was not specified, but warning is enabled in the settings!")
            core.quit()
        if 'implicit' in settings.asrt_types.values() and len(self.feedback_imp) == 0:
            print("Implicit feedback message was not specified, but there is an implicit session in the experiment!")
            core.quit()
        if 'explicit' in settings.asrt_types.values() and len(self.feedback_exp) == 0:
            print("Explicit feedback message was not specified, but there is an explicit session in the experiment!")
            core.quit()

    def __print_to_screen(self, mytext, mywindow):
        """Display given string in the given window."""

        text_stim = visual.TextStim(mywindow, text=mytext, units='cm', height=0.6, color='black')
        text_stim.draw()
        mywindow.flip()

    def __show_message(self, instruction_list, mywindow, expriment_settings):
        """Display simple instructions on the screen."""

        # There can be more instructions to display successively
        for inst in instruction_list:
            self.__print_to_screen(inst, mywindow)
            tempkey = event.waitKeys(keyList=expriment_settings.get_key_list())
            if expriment_settings.key_quit in tempkey:
                core.quit()

    def show_instructions(self, mywindow, expriment_settings):
        self.__show_message(self.insts, mywindow, expriment_settings)

    def show_unexp_quit(self, mywindow, expriment_settings):
        self.__show_message(self.unexp_quit, mywindow, expriment_settings)

    def show_ending(self, mywindow, expriment_settings):
        self.__show_message(self.ending, mywindow, expriment_settings)

    def feedback_explicit_RT(self, rt_mean, rt_mean_p, acc_for_pattern, acc_for_the_whole, acc_for_the_whole_str, mywindow, expriment_settings):
        """Display feedback screen in case of an explicit ASRT.

           The feedback string contains placeholders for reaction time and accuracy.
           Based on the settings the feedback might contain extra warning
           about the speed or accuray.
        """

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
            tempkey = event.waitKeys(keyList=expriment_settings.get_key_list())
        if expriment_settings.key_quit in tempkey:
            return 'quit'
        else:
            return 'continue'

    def feedback_implicit_RT(self, rt_mean, acc_for_the_whole, acc_for_the_whole_str, mywindow, expriment_settings):
        """Display feedback screen in case of an implicit ASRT.

           The feedback string contains placeholders for reaction time and accuracy.
           Based on the settings the feedback might contain extra warning
           about the speed or accuray.
        """
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
            tempkey = event.waitKeys(keyList=expriment_settings.get_key_list())
        if expriment_settings.key_quit in tempkey:
            return 'quit'
        else:
            return 'continue'

    def feedback_explicit_ET(self, rt_mean, rt_mean_p, mywindow, expriment_settings):
        """Display feedback screen in case of an explicit ASRT.

           The feedback string contains placeholders for reaction times.
        """

        for l in self.feedback_exp:
            l = l.replace('*MEANRT*', rt_mean)
            l = l.replace('*MEANRTP*', rt_mean_p)
            self.__print_to_screen(l, mywindow)
            tempkey = event.waitKeys(keyList=expriment_settings.get_key_list())
        if expriment_settings.key_quit in tempkey:
            return 'quit'
        else:
            return 'continue'

    def feedback_implicit_ET(self, rt_mean, mywindow, expriment_settings):
        """Display feedback screen in case of an implicit ASRT.

           The feedback string contains placeholders for reaction times.
        """
        for i in self.feedback_imp:
            i = i.replace('*MEANRT*', rt_mean)
            self.__print_to_screen(i, mywindow)
            tempkey = event.waitKeys(keyList=expriment_settings.get_key_list())
        if expriment_settings.key_quit in tempkey:
            return 'quit'
        else:
            return 'continue'


class PersonDataHandler:
    """Class for handle subject related settings and data."""

    def __init__(self, subject_id, all_settings_file_path, all_IDs_file_path, subject_list_file_path, output_file_path, output_file_type):
        # generated, unique ID of the subject (consist of a name, a number and an optional group name
        self.subject_id = subject_id
        # path to the settings file of the current subject storing the state of the experiment
        self.all_settings_file_path = all_settings_file_path
        # path to the file containing the IDs for all subjects
        self.all_IDs_file_path = all_IDs_file_path
        # path to a text file containing a list of all subjects
        self.subject_list_file_path = subject_list_file_path
        # output text file for the measured data of the current subject
        self.output_file_path = output_file_path
        # type of the experiment indicating the output variables ('reaction-time' or 'eye-tracking')
        self.output_file_type = output_file_type
        # we store all neccessary data in this list of lists to be able to generate the output at the end of all blocks
        self.output_data_buffer = []

    def load_person_settings(self, experiment):
        """Open settings file of the current subject and read the current state."""

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
        """Write out the current state of the experiment run with current subject,
           so we can continue the experiment from that point where the subject finished it."""

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
        """Add the new subject ID into the list of all IDs and save it to the IDs file.
           Also generate a text file with the list of all subjects participating in the experiment
        """

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
        """ Append a string to the end on the output text file."""

        if not os.path.isfile(self.output_file_path):
            with codecs.open(self.output_file_path, 'w', encoding='utf-8') as output_file:
                if self.output_file_type == 'reaction-time':
                    self.add_RT_heading_to_output(output_file)
                else:
                    self.add_ET_heading_to_output(output_file)
                output_file.write(string_to_append)
        else:
            with codecs.open(self.output_file_path, 'a+', encoding='utf-8') as output_file:
                output_file.write(string_to_append)

    def flush_data_to_output(self, experiment):
        if self.output_file_type == 'reaction-time':
            self.flush_RT_data_to_output(experiment)
        else:
            self.flush_ET_data_to_output(experiment)

    def flush_RT_data_to_output(self, experiment):
        """ Write out the ouptut date of the current trial into the output text file (reaction-time exp. type)."""
        assert self.output_file_type == 'reaction-time'

        output_buffer = StringIO()
        for data in self.output_data_buffer:
            N = data[0]
            session = experiment.stim_sessionN[N]
            PCode = experiment.which_code(session)
            asrt_type = experiment.settings.asrt_types[session]

            output_data = [experiment.settings.computer_name,
                           experiment.subject_group,
                           experiment.subject_name,
                           experiment.subject_number,
                           asrt_type,
                           PCode,

                           data[8],

                           experiment.stim_sessionN[N],
                           experiment.stimepoch[N],
                           experiment.stimblock[N],
                           experiment.stimtrial[N],

                           data[1],
                           experiment.frame_rate,
                           experiment.frame_time,
                           experiment.frame_sd,
                           data[2],
                           data[3],

                           data[7],
                           experiment.stimpr[N],
                           data[4],
                           data[5],

                           experiment.stimlist[N],
                           data[6]]
            output_buffer.write("\n")
            for data in output_data:
                if isinstance(data, numbers.Number):
                    data = str(data)
                    data = data.replace('.', ',')
                else:
                    data = str(data)
                output_buffer.write(data + '\t')

        self.append_to_output_file(output_buffer.getvalue())
        output_buffer.close()
        self.output_data_buffer.clear()

    def add_RT_heading_to_output(self, output_file):
        """Add the first line to the ouput with the names of the different variables (reaction-time exp. type)."""
        assert self.output_file_type == 'reaction-time'

        heading_list = ['computer_name',
                        'subject_group',
                        'subject_name',
                        'subject_number',
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
                        'response',
                        'quit_log']

        for h in heading_list:
            output_file.write(h + '\t')

    def flush_ET_data_to_output(self, experiment):
        """ Write out the ouptut date of the current trial into the output text file (eye-tracking exp. type)."""
        assert self.output_file_type == 'eye-tracking'

        output_buffer = StringIO()
        for data in self.output_data_buffer:

            N = data[0] + 1
            session = experiment.stim_sessionN[N]
            PCode = experiment.which_code(session)
            asrt_type = experiment.settings.asrt_types[session]
            if experiment.stimpr[N] == 'P':
                if experiment.settings.asrt_types[session] == 'explicit':
                    stimcolor = experiment.colors['stimp']
                else:
                    stimcolor = experiment.colors['stimr']
            else:
                stimcolor = experiment.colors['stimr']

            left_gaze_data = data[3]['left_gaze_point_on_display_area']
            right_gaze_data = data[3]['right_gaze_point_on_display_area']
            left_gaze_validity = data[3]['left_gaze_point_validity']
            right_gaze_validity = data[3]['right_gaze_point_validity']

            left_pupil_diameter = data[3]['left_pupil_diameter']
            right_pupil_diameter = data[3]['right_pupil_diameter']
            left_pupil_validity = data[3]['left_pupil_validity']
            right_pupil_validity = data[3]['right_pupil_validity']

            output_data = [experiment.settings.computer_name,
                           experiment.subject_group,
                           experiment.subject_name,
                           experiment.subject_number,
                           asrt_type,
                           PCode,

                           experiment.stim_sessionN[N],
                           experiment.stimepoch[N],
                           experiment.stimblock[N],
                           experiment.stimtrial[N],

                           data[1],
                           experiment.frame_rate,
                           experiment.frame_time,
                           experiment.frame_sd,

                           stimcolor,
                           experiment.stimpr[N],
                           experiment.stimlist[N],
                           data[2],
                           left_gaze_data[0],
                           left_gaze_data[1],
                           right_gaze_data[0],
                           right_gaze_data[1],
                           left_gaze_validity,
                           right_gaze_validity,
                           left_pupil_diameter,
                           right_pupil_diameter,
                           left_pupil_validity,
                           right_pupil_validity]

            output_buffer.write("\n")
            for data in output_data:
                if isinstance(data, numbers.Number):
                    data = str(data)
                    data = data.replace('.', ',')
                else:
                    data = str(data)
                output_buffer.write(data + '\t')

        self.append_to_output_file(output_buffer.getvalue())
        output_buffer.close()
        self.output_data_buffer.clear()

    def add_ET_heading_to_output(self, output_file):
        """Add the first line to the ouput with the names of the different variables (eye-tracking exp. type)."""
        assert self.output_file_type == 'eye-tracking'

        heading_list = ['computer_name',
                        'subject_group',
                        'subject_name',
                        'subject_number',
                        'asrt_type',
                        'PCode',

                        'session',
                        'epoch',
                        'block',
                        'trial',

                        'RSI_time',
                        'frame_rate',
                        'frame_time',
                        'frame_sd',

                        'stimulus_color',
                        'PR',
                        'stimulus',
                        'stimulus_on_screen',
                        'left_gaze_data_X',
                        'left_gaze_data_Y',
                        'right_gaze_data_X',
                        'right_gaze_data_Y',
                        'left_gaze_validity',
                        'right_gaze_validity',
                        'left_pupil_diameter',
                        'right_pupil_diameter',
                        'left_pupil_validity',
                        'right_pupil_validity',
                        'quit_log']

        for h in heading_list:
            output_file.write(h + '\t')


class Experiment:
    """ Class for running the ASRT experiment."""

    def __init__(self, workdir_path):
        # working directory of the experiment, the script reads settings and writer output under this directory
        self.workdir_path = workdir_path

        # all experiment settings globally used for all subjects
        self.settings = None
        # instruction strings used to display messages during the experiment
        self.instructions = None
        # handler object for loadin and saving subject settings and output
        self.person_data = None

        # a predefined list of colors used for stimulus presentation (e.g. stimuli color, window color)
        self.colors = None
        # pressed button -> stimulus number maping (e.g. {'z': 1, 'c' : 2, 'b' : 3, 'm' : 4}
        self.pressed_dict = None
        # positions of the four stimulus circle
        self.dict_pos = None

        # tobii EyeTracker object for handling eye-tracker input
        self.eye_tracker = None
        self.gaze_data_list = []

        # visual.Window object for displaying experiment
        self.mywindow = None
        self.mymonitor = None
        # avarage time of displaying one frame on the screen in ms (e.g. 15.93 for 50 Hz)
        self.frame_time = None
        # standard deviation of displaying one frame on the screen in ms (e.g. 0.02)
        self.frame_sd = None
        # measured frame rate in Hz (e.g. 59.45)
        self.frame_rate = None

        # group of the current subject
        self.subject_group = None
        # serial number of the current subject
        self.subject_number = None
        # name of the current subject
        self.subject_name = None

        # a dictionary of pcodes for the different sessions (e.g. {1 : '1st - 1234', 2 : '5th - 1423'})
        # pcode means pattern code, which defines the order of the pattern series, expected to be learnt by the subject
        self.PCodes = None
        # serial number of the next line in the output file (e.g. 10)
        self.stim_output_line = None
        # global trial number -> session number mapping (e.g. {1 : 1, 2 : 1, 3 : 2, 4 : 2} - two sessions with two trials in each)
        self.stim_sessionN = None
        # global trial number -> epoch number mapping (e.g. {1 : 1, 2 : 2, 3 : 2, 4 : 2} - two epochs with two trials in each)
        self.stimepoch = None
        # global trial number -> block number mapping (e.g. {1 : 1, 2 : 2, 3 : 2, 4 : 2} - two blocks with two trials in each)
        self.stimblock = None
        # global trial number -> trial number inside the block mapping (e.g. {1 : 1, 2 : 2, 3 : 1, 4 : 2} - two blocks with two trials in each)
        self.stimtrial = None
        # global trial number -> stimulus number mapping (e.g. {1 : 1, 2 : 2, 3 : 2, 4 : 4})
        self.stimlist = None
        # global trial number -> first trial of the next session mapping (e. g.{1 : 3, 2 : 3, 3 : 5, 4 : 5} - two sessions with two trials in each)
        self.end_at = None
        # global trial number -> pattern or random stimulus mapping (e. g.{1 : 'P', 2 : 'R', 3 : 'P', 4 : 'R'} - two sessions with two trials in each)
        self.stimpr = None
        # number of the last trial (it is 0 in the beggining and it is always equal with the last displayed stimulus's serial number
        self.last_N = None
        # this variable has a meaning during presentation, current stimulus is on the screen or we are in the RSI interval
        self.stimulus_on_screen = None
        # this variable has a meaning during presentation, last measured RSI
        self.last_RSI = None

    def all_settings_def(self):

        try:
            # check whether the settings file is in place
            self.settings.read_from_file()

        # if there is no settings file, we ask the user to specfiy the settings
        except:
            # get experiment type, the number of groups and number of sessions
            numgroups = self.settings.show_basic_settings_dialog()

            # get the group names
            self.settings.show_group_settings_dialog(numgroups)

            # get epoch and block settings (block number, trial number, epoch number, etc)
            self.settings.show_epoch_and_block_settings_dialog()

            # get montior / computer settings, and also options about displaying (stimulus size, stimulus distance, etc)
            self.settings.show_computer_and_display_settings_dialog()

            # get keyboard settings (reaction keys and quit key) and also feedback settings (accuracy and speed feedback, etc)
            if self.settings.experiment_type == 'reaction-time':
                self.settings.show_key_and_feedback_settings_dialog()

            # save the settings
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
                settings_dialog.addField(u'Csoport', choices=self.settings.groups)

            returned_data = settings_dialog.show()
            if settings_dialog.OK:
                name = returned_data[0]
                name = normalize_string(name, "-")
                name = name.replace("_", "-")
                self.subject_name = name

                subject_number = returned_data[1]
                if len(self.settings.groups) > 1:
                    self.subject_group = returned_data[2]
                else:
                    self.subject_group = ""

                try:
                    subject_number = int(subject_number)
                    if subject_number >= 0:
                        itsOK = 1
                        self.subject_number = subject_number
                    else:
                        warningtext = u'Pozitív egész számot adj meg a sorszámhoz!'

                except:
                    warningtext = u'Pozitív egész számot adj meg a sorszámhoz!'

            else:
                core.quit()

    def show_subject_continuation_dialog(self):
        """Dialog shown after restart of the experiment for a subject.
           Displays the state of the experiment for the given subject.
        """

        if self.last_N + 1 <= self.settings.get_maxtrial():
            expstart11 = gui.Dlg(title=u'Feladat indítása...')
            expstart11.addText(u'A személy adatait beolvastam.')
            expstart11.addText(u'Folytatás innen...')
            expstart11.addText('Session: ' + str(self.stim_sessionN[self.last_N + 1]))
            expstart11.addText('Epoch: ' + str(self.stimepoch[self.last_N + 1]))
            expstart11.addText('Block: ' + str(self.stimblock[self.last_N + 1]))
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
        """Select pattern sequences for the different sessions for the current subject."""

        settings_dialog = gui.Dlg(title=u'Beállítások')
        settings_dialog.addText('')
        for z in range(self.settings.numsessions):
            if self.settings.asrt_types[z + 1] == "noASRT":
                settings_dialog.addFixedField(u'Session ' + str(z + 1) + ' PCode', 'noPattern')
            else:
                settings_dialog.addField(u'Session ' + str(z + 1) + ' PCode', choices=[
                                         '1st - 1234', '2nd - 1243', '3rd - 1324', '4th - 1342', '5th - 1423', '6th - 1432'])

        returned_data = settings_dialog.show()
        if settings_dialog.OK:
            self.PCodes = {}

            for zz in range(self.settings.numsessions):
                self.PCodes[zz + 1] = returned_data[zz]

            return self.PCodes
        else:
            core.quit()

    def which_code(self, session_number):
        """Convert sessions pattern code to a raw code containing only the series of stimulus numbers."""

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
        """Calculate all variables used during the trials before the presentation starts."""

        all_trial_Nr = 0
        block_num = 0

        sessionsstarts = self.settings.get_session_starts()
        for trial_num in range(1, self.settings.get_maxtrial() + 1):
            for session_num in range(1, len(sessionsstarts)):
                if trial_num >= sessionsstarts[session_num - 1] and trial_num < sessionsstarts[session_num]:
                    self.stim_sessionN[trial_num] = session_num
                    self.end_at[trial_num] = sessionsstarts[session_num]

        for epoch in range(1, self.settings.epochN + 1):

            for block in range(1, self.settings.block_in_epochN + 1):
                block_num += 1
                current_trial_num = 0

                # practice
                for practice in range(1, self.settings.blockprepN + 1):
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
                for real in range(1, self.settings.blocklengthN + 1):

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
                            current_stim = int(dict_HL[str(self.stimlist[all_trial_Nr - 2])])
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
        """Find out the current subject and read subject settings / progress if he/she already has any data."""

        self.show_subject_settings_dialog()

        # unique subject ID
        subject_id = self.subject_name + '_' + str(self.subject_number) + '_' + self.subject_group

        # init subject data handler with the rigth file paths
        all_settings_file_path = os.path.join(self.workdir_path, "settings", subject_id)
        all_IDs_file_path = os.path.join(self.workdir_path, "settings", "participant_settings")
        subject_list_file_path = os.path.join(self.workdir_path, "settings",
                                              "participants_in_experiment.txt")
        output_file_path = os.path.join(self.workdir_path, "logs", subject_id + '_log.txt')
        self.person_data = PersonDataHandler(subject_id, all_settings_file_path,
                                             all_IDs_file_path, subject_list_file_path,
                                             output_file_path, self.settings.experiment_type)

        # update ID file containing all participating subject's ID
        self.person_data.update_subject_IDs_files()

        # try to load settings and progress for the given subject ID
        self.person_data.load_person_settings(self)

        if self.last_N > 0:
            # the current subject already started the experiment
            self.show_subject_continuation_dialog()
        # we have a new subject
        else:
            # ask about the pattern codes used in the different sessions
            self.show_subject_PCodes_dialog()
            # calculate stimulus properties for the experiment
            self.calculate_stim_properties()
            # save data of the new subject
            self.person_data.save_person_settings(self)

    def init_eyetracker(self):
        # Sometimes the eyetracker is not identified for the first time. Try more times.
        loopCount = 1
        allTrackers = tobii.find_all_eyetrackers()
        while not allTrackers and loopCount < 50:
            allTrackers = tobii.find_all_eyetrackers()
            core.wait(0.02)
            loopCount += 1

        if len(allTrackers) < 1:
            print("Cannot find any eyetrackers.")
            core.quit()

        self.eye_tracker = allTrackers[0]

    def eye_data_callback(self, gazeData):
        max_length = 8

        left_gaze_XY = gazeData['left_gaze_point_on_display_area']
        right_gaze_XY = gazeData['right_gaze_point_on_display_area']
        left_gaze_valid = gazeData['left_gaze_point_validity']
        right_gaze_valid = gazeData['right_gaze_point_validity']

        x_coord = None
        y_coord = None
        if left_gaze_valid and right_gaze_valid:
            x_coord = (left_gaze_XY[0] + right_gaze_XY[0]) / 2
            y_coord = (left_gaze_XY[1] + right_gaze_XY[1]) / 2
        elif left_gaze_valid:
            x_coord = left_gaze_XY[0]
            y_coord = left_gaze_XY[1]
        elif right_gaze_valid:
            x_coord = right_gaze_XY[0]
            y_coord = right_gaze_XY[1]

        if x_coord != None and y_coord != None:
            self.gaze_data_list.append((x_coord, y_coord))
            if len(self.gaze_data_list) > max_length:
                self.gaze_data_list.pop(0)

        self.person_data.output_data_buffer.append(
            [self.last_N, self.last_RSI, self.stimulus_on_screen, gazeData])

    def point_is_in_rectangle(self, point, rect_center, rect_size):
        if abs(point[0] - rect_center[0]) <= rect_size and abs(point[1] - rect_center[1]) <= rect_size:
            return True
        else:
            return False

    def wait_for_eye_response(self, expected_response):
        max_length = 8

        while (True):

            if 'q' in event.getKeys():
                return -1

            if len(self.gaze_data_list) < max_length:
                continue

            # calculate avarage gage position
            sum_x = 0
            sum_y = 0
            for pos in self.gaze_data_list:
                sum_x += pos[0]
                sum_y += pos[1]

            # we have the pos in eye-tracker's display area normalized coordinates with the
            # origin at the upper left corner
            avg_pos_norm = (sum_x / len(self.gaze_data_list), sum_y / len(self.gaze_data_list))

            # we need to convert it to psychopy cm coordinates, where the origin is at the
            # center and y coordinates are mirrored.
            aspect_ratio = self.mymonitor.getSizePix()[1] / self.mymonitor.getSizePix()[0]
            monitor_width_cm = self.settings.monitor_width
            monitor_height_cm = monitor_width_cm * aspect_ratio

            # shift origin
            shift_x = monitor_width_cm / 2
            shift_y = monitor_height_cm / 2

            # need to mirror the y coordinates
            avg_pos_cm = ((avg_pos_norm[0] * monitor_width_cm) - shift_x,
                          ((avg_pos_norm[1] * monitor_height_cm) - shift_y) * - 1)

            if self.point_is_in_rectangle(avg_pos_cm, self.dict_pos[expected_response], self.settings.AOI_size):
                return expected_response

    def monitor_settings(self):
        """Specify monitor settings."""

        # use default screen resolution
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        self.mymonitor = monitors.Monitor('myMon')
        self.mymonitor.setSizePix([screen.width, screen.height])
        # need to set monitor width in cm to be able to use cm unit for stimulus
        self.mymonitor.setWidth(self.settings.monitor_width)
        self.mymonitor.saveMon()

    def print_to_screen(self, mytext):
        """Display any string on the screen."""

        xtext = visual.TextStim(self.mywindow, text=mytext, units="cm", height=0.6, color="black")
        xtext.draw()
        self.mywindow.flip()

    def frame_check(self):
        """Measure the frame rate, using different measurements."""

        self.print_to_screen(
            u'Adatok előkészítése folyamatban.\n\nEz eltarthat pár másodpercig.\n\nAddig semmit sem fogsz látni a képernyőn...')
        core.wait(2)

        ms_per_frame = self.mywindow.getMsPerFrame(nFrames=120)
        self.frame_time = ms_per_frame[0]
        self.frame_sd = ms_per_frame[1]
        self.frame_rate = self.mywindow.getActualFrameRate()

    def stim_bg(self, stimbg):
        """Draw empty stimulus circles."""

        for i in range(1, 5):
            stimbg.pos = self.dict_pos[i]
            stimbg.draw()

    def show_feedback_RT(self, N, number_of_patterns, patternERR, responses_in_block, accs_in_block, RT_all_list, RT_pattern_list):
        """ Display feedback in the end of the blocks, showing some data about speed and accuracy."""

        acc_for_the_whole = 100 * float(responses_in_block -
                                        sum(accs_in_block)) / responses_in_block
        acc_for_the_whole_str = str(acc_for_the_whole)[0:5].replace('.', ',')

        rt_mean = float(sum(RT_all_list)) / len(RT_all_list)
        rt_mean_str = str(rt_mean)[:5].replace('.', ',')

        if self.settings.asrt_types[self.stim_sessionN[N - 1]] == 'explicit':

            try:
                rt_mean_p = float(sum(RT_pattern_list)) / len(RT_pattern_list)
                rt_mean_p_str = str(rt_mean_p)[:5].replace('.', ',')
            except:
                rt_mean_p_str = 'N/A'

            try:
                acc_for_patterns = 100 * float(number_of_patterns - patternERR) / number_of_patterns
                acc_for_patterns_str = str(acc_for_patterns)[
                    0:5].replace('.', ',')
            except:
                acc_for_patterns_str = 'N/A'

            whatnow = self.instructions.feedback_explicit_RT(
                rt_mean_str, rt_mean_p_str, acc_for_patterns_str, acc_for_the_whole, acc_for_the_whole_str, self.mywindow, self.settings)
        else:
            whatnow = self.instructions.feedback_implicit_RT(
                rt_mean_str, acc_for_the_whole, acc_for_the_whole_str, self.mywindow, self.settings)

        return whatnow

    def show_feedback_ET(self, N, RT_all_list, RT_pattern_list):
        """ Display feedback in the end of the blocks, showing some data about reaction time."""

        rt_mean = float(sum(RT_all_list)) / len(RT_all_list)
        rt_mean_str = str(rt_mean)[:5].replace('.', ',')

        if self.settings.asrt_types[self.stim_sessionN[N - 1]] == 'explicit':

            try:
                rt_mean_p = float(sum(RT_pattern_list)) / len(RT_pattern_list)
                rt_mean_p_str = str(rt_mean_p)[:5].replace('.', ',')
            except:
                rt_mean_p_str = 'N/A'

            whatnow = self.instructions.feedback_explicit_ET(rt_mean_str, rt_mean_p_str, self.mywindow, self.settings)
        else:
            whatnow = self.instructions.feedback_implicit_ET(rt_mean_str, self.mywindow, self.settings)

        return whatnow

    def wait_for_response(self, expected_response, response_clock):
        if self.settings.experiment_type == 'reaction-time':
            press = event.waitKeys(keyList=self.settings.get_key_list(),
                                   timeStamped=response_clock)
            if press[0][0] == 'q':
                return (-1, press[0][1])
            return (self.pressed_dict[press[0][0]], press[0][1])
        # for ET version we wait for getting the right response (there is no wrong answer)
        else:
            response = self.wait_for_eye_response(expected_response)
            # this RT is not precise, but good enough to give a feedback for the subject
            return (response, response_clock.getTime())

    def quit_presentation(self):
        self.print_to_screen("Kilépés...\nAdatok mentése...")

        if self.eye_tracker is not None:
            self.eye_tracker.unsubscribe_from(tobii.EYETRACKER_GAZE_DATA, self.eye_data_callback)

        self.person_data.append_to_output_file('userquit')
        core.quit()

    def presentation(self):
        """The real experiment happens here. This method displays the stimulus window and records the reactions."""

        # init presented objects
        stimP = visual.Circle(win=self.mywindow, radius=self.settings.asrt_size, units="cm",
                              fillColor=self.colors['stimp'], lineColor=self.colors['linecolor'], pos=self.dict_pos[1])
        stimR = visual.Circle(win=self.mywindow, radius=self.settings.asrt_size, units="cm",
                              fillColor=self.colors['stimr'], lineColor=self.colors['linecolor'], pos=self.dict_pos[1])
        stimbg = visual.Circle(win=self.mywindow, radius=1, units="cm",
                               fillColor=None, lineColor=self.colors['linecolor'])

        stim_RSI = 0.0
        N = self.last_N + 1

        # show instructions or continuation message
        if N in self.settings.get_session_starts():
            self.instructions.show_instructions(self.mywindow, self.settings)

        else:
            self.instructions.show_unexp_quit(self.mywindow, self.settings)

        responses_in_block = 0
        accs_in_block = []

        asrt_type = self.settings.asrt_types[self.stim_sessionN[N]]
        PCode = self.which_code(self.stim_sessionN[N])

        patternERR = 0
        number_of_patterns = 0

        RT_pattern_list = []
        RT_all_list = []

        RSI = core.StaticPeriod(screenHz=self.frame_rate)
        RSI_clock = core.Clock()
        trial_clock = core.Clock()

        first_trial_in_block = True

        self.stimulus_on_screen = False
        self.last_RSI = -1

        # start recording gaze data
        if self.eye_tracker is not None:
            self.eye_tracker.subscribe_to(tobii.EYETRACKER_GAZE_DATA,
                                          self.eye_data_callback, as_dictionary=True)

        while True:
            # four empty circles where the actual stimulus can be placed
            self.stim_bg(stimbg)
            self.mywindow.flip()
            self.stimulus_on_screen = False
            self.last_RSI = -1

            # set the actual stimulus' position and fill color
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

            # wait before the next stimulus to have the set RSI
            if not first_trial_in_block:
                RSI.complete()

            cycle = 0

            while True:
                cycle += 1
                self.stim_bg(stimbg)

                # display the actual stimulus
                if self.stimpr[N] == 'P':
                    stimP.draw()
                else:
                    stimR.draw()
                self.mywindow.flip()
                self.stimulus_on_screen = True

                # we measure the actual RSI
                if cycle == 1:
                    if first_trial_in_block:
                        stim_RSI = 0.0
                    else:
                        stim_RSI = RSI_clock.getTime()
                self.last_RSI = stim_RSI

                if cycle == 1:
                    trial_clock.reset()
                (response, time_stamp) = self.wait_for_response(self.stimlist[N], trial_clock)

                # start of the RSI timer
                RSI_clock.reset()
                RSI.start(self.settings.RSI_time)

                now = datetime.now()
                stim_RT_time = now.strftime('%H:%M:%S.%f')
                stim_RT_date = now.strftime('%d/%m/%Y')
                stimRT = time_stamp

                self.stim_output_line += 1
                responses_in_block += 1

                # quit during the experiment
                if response == -1:
                    self.stim_output_line -= 1

                    if N >= 1:
                        self.last_N = N - 1

                    self.quit_presentation()

                # right response
                elif response == self.stimlist[N]:
                    stimACC = 0
                    accs_in_block.append(0)

                    if self.stimpr[N] == 'P':
                        number_of_patterns += 1
                        RT_pattern_list.append(stimRT)
                    RT_all_list.append(stimRT)

                # wrong response -> let's wait for the next response
                else:
                    stimACC = 1
                    accs_in_block.append(1)

                    if self.stimpr[N] == 'P':
                        patternERR += 1
                        number_of_patterns += 1
                        RT_pattern_list.append(stimRT)
                    RT_all_list.append(stimRT)

                # save data of the last trial (for ET we save data for every sample)
                if self.settings.experiment_type == 'reaction-time':
                    self.person_data.output_data_buffer.append([N, stim_RSI, stim_RT_time, stim_RT_date,
                                                                stimRT, stimACC, response, stimcolor, self.stim_output_line])

                if stimACC == 0:
                    self.last_N = N
                    N += 1
                    first_trial_in_block = False
                    break

            # end of the block (show feedback and reinit variables for the next block)
            if N in self.settings.get_block_starts():

                self.print_to_screen(u"Adatok mentése és visszajelzés előkészítése...")

                self.person_data.flush_data_to_output(self)
                self.person_data.save_person_settings(self)

                if self.settings.experiment_type == 'reaction-time':
                    whatnow = self.show_feedback_RT(N, number_of_patterns, patternERR, responses_in_block,
                                                    accs_in_block, RT_all_list, RT_pattern_list)
                else:
                    whatnow = self.show_feedback_ET(N, RT_all_list, RT_pattern_list)

                if whatnow == 'quit':
                    if N >= 1:
                        self.last_N = N - 1

                    self.quit_presentation()

                patternERR = 0
                responses_in_block = 0

                RT_pattern_list = []
                RT_all_list = []

                accs_in_block = []

                first_trial_in_block = True

            # end of the sessions (one run of the experiment script stops at the end of the current session)
            if N == self.end_at[N - 1]:
                break

    def run(self):
        ensure_dir(os.path.join(self.workdir_path, "logs"))
        ensure_dir(os.path.join(self.workdir_path, "settings"))

        # load experiment settings if exist or ask the user to specify them
        all_settings_file_path = os.path.join(self.workdir_path, "settings", "settings")
        reminder_file_path = os.path.join(self.workdir_path, "settings", "settings_reminder.txt")
        self.settings = ExperimentSettings(all_settings_file_path, reminder_file_path)
        self.all_settings_def()

        # specify predefined dictionaries
        self.colors = {'wincolor': self.settings.asrt_background, 'linecolor': 'black',
                       'stimp': self.settings.asrt_pcolor, 'stimr': self.settings.asrt_rcolor}

        self.pressed_dict = {self.settings.key1: 1, self.settings.key2: 2,
                             self.settings.key3: 3, self.settings.key4: 4}

        # reaction-time exp: stimulus circles placed in one line
        if self.settings.experiment_type == 'reaction-time':
            self.dict_pos = {1: (float(self.settings.asrt_distance) * (-1.5), 0),
                             2: (float(self.settings.asrt_distance) * (-0.5), 0),
                             3: (float(self.settings.asrt_distance) * 0.5, 0),
                             4: (float(self.settings.asrt_distance) * 1.5, 0)}
        # eye-tracking exp: stimulus circles placed in a rectangle shape
        else:
            self.dict_pos = {1: (float(self.settings.asrt_distance) * (-0.5), float(self.settings.asrt_distance) * (-0.5)),
                             2: (float(self.settings.asrt_distance) * 0.5, float(self.settings.asrt_distance) * (-0.5)),
                             3: (float(self.settings.asrt_distance) * (-0.5), float(self.settings.asrt_distance) * 0.5),
                             4: (float(self.settings.asrt_distance) * 0.5, float(self.settings.asrt_distance) * 0.5)}

        # read instruction strings
        inst_feedback_path = os.path.join(self.workdir_path, "inst_and_feedback.txt")
        self.instructions = InstructionHelper(inst_feedback_path)
        self.instructions.read_insts_from_file()
        self.instructions.validate_instructions(self.settings)

        # find out the current subject
        self.participant_id()

        # init eye-tracker if needed
        if self.settings.experiment_type == 'eye-tracking':
            self.init_eyetracker()

        # init window
        self.monitor_settings()
        if platform.system() == "Linux":
            win_type = 'pygame'
        else:
            win_type = 'pyglet'
        with visual.Window(size=self.mymonitor.getSizePix(), color=self.colors['wincolor'], fullscr=False, monitor=self.mymonitor, units="cm", winType=win_type) as self.mywindow:
            # check frame rate
            self.frame_check()

            # show experiment screen
            self.presentation()

            # stop recoring gaze data
            if self.eye_tracker is not None:
                self.eye_tracker.unsubscribe_from(
                    tobii.EYETRACKER_GAZE_DATA, self.eye_data_callback)

            # save user data
            self.person_data.save_person_settings(self)
            self.person_data.append_to_output_file('sessionend_planned_quit')

            # show ending screen
            self.instructions.show_ending(self.mywindow, self.settings)


if __name__ == "__main__":
    thispath = os.path.split(os.path.abspath(__file__))[0]
    experiment = Experiment(thispath)
    experiment.run()
