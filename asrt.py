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
import threading
import copy

try:
    import tobii_research as tobii
    g_tobii_available = True
except:
    g_tobii_available = False

g_blocks_in_feedback = 5


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

    def __init__(self, settings_file_path, reminder_file_path, project_ET_zero=False):
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
        # global epoch number -> asrt type mapping (e.g. {1 : 'implicit', 2 : 'explicit'} - (two epochs, first epoch is an implicit asrt, the second one is explicit))
        self.asrt_types = None

        # monitor's physical width in 'cm' (e.g. 29)
        self.monitor_width = None
        # an imaginary name of the computer where the experiment is run (e.g. Laposka)
        self.computer_name = None
        # distance of the neighbour stimulus circles in cm (center to center distance)
        self.asrt_distance = None
        # radius of the stimulus circle in cm (e.g. 1)
        self.asrt_size = None
        # fill color of the random stimulus or all stimulus in case of implicit asrt (e.g. "Orange")
        self.asrt_rcolor = None
        # fill color of the "pattern" stimulus in case of explicit asrt (e.g. "Orange")
        self.asrt_pcolor = None
        # background color behind the stimulus circles  (e.g. "Ivory")
        self.asrt_background = None
        # response-to-next-stimulus time in millisecond (e.g. 120)
        self.RSI_time = None

        # AOI (area of interest) is a suqare with the same origin as the stimuli, this size means the size of this square's side
        self.AOI_size = None
        # count of samples used to identify fixation on the stimulus
        self.stim_fixation_threshold = None
        # count of samples used to identify fixation on fixation cross on an instruction screen
        self.instruction_fixation_threshold = None
        # dispersion threshold in cm
        self.dispersion_threshold = None

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

        self.project_ET_zero = project_ET_zero
        self.validation_trialN = 20

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
                self.asrt_rcolor = settings_file['asrt_rcolor']
                self.asrt_pcolor = settings_file['asrt_pcolor']
                self.asrt_background = settings_file['asrt_background']
                self.RSI_time = settings_file['RSI_time']

                if self.experiment_type == 'eye-tracking':
                    self.AOI_size = settings_file['AOI_size']
                    self.stim_fixation_threshold = settings_file['stim_fixation_threshold']
                    self.instruction_fixation_threshold = settings_file['instruction_fixation_threshold']
                    self.dispersion_threshold = settings_file['dispersion_threshold']

                if self.experiment_type == 'reaction-time':
                    self.key1 = settings_file['key1']
                    self.key2 = settings_file['key2']
                    self.key3 = settings_file['key3']
                    self.key4 = settings_file['key4']
                    self.key_quit = settings_file['key_quit']
                    self.whether_warning = settings_file['whether_warning']
                    self.speed_warning = settings_file['speed_warning']
                    self.acc_warning = settings_file['acc_warning']
                elif self.experiment_type == 'eye-tracking':
                    self.key_quit = 'q'
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
            settings_file['asrt_rcolor'] = self.asrt_rcolor
            settings_file['asrt_pcolor'] = self.asrt_pcolor
            settings_file['asrt_background'] = self.asrt_background
            settings_file['RSI_time'] = self.RSI_time

            if self.experiment_type == 'eye-tracking':
                settings_file['AOI_size'] = self.AOI_size
                settings_file['stim_fixation_threshold'] = self.stim_fixation_threshold
                settings_file['instruction_fixation_threshold'] = self.instruction_fixation_threshold
                settings_file['dispersion_threshold'] = self.dispersion_threshold

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
                            'Asrt stim distance:' + '\t' + str(self.asrt_distance).replace('.', ',') + '\n' +
                            'Asrt stim size:' + '\t' + str(self.asrt_size).replace('.', ',') + '\n' +
                            'Asrt stim color (implicit):' + '\t' + self.asrt_rcolor + '\n' +
                            'Asrt stim color (explicit, cued):' + '\t' + self.asrt_pcolor + '\n' +
                            'Background color:' + '\t' + self.asrt_background + '\n')

            if self.experiment_type == 'eye-tracking':
                reminder += str('AOI size:' + '\t' + str(self.AOI_size).replace('.', ',') + '\n' +
                                'Fixation threshold for stimulus:' + '\t' + str(self.stim_fixation_threshold) + '\n' +
                                'Fixation threshold for instructions:' + '\t' + str(self.instruction_fixation_threshold) + '\n' +
                                'Dispersion threshold:' + '\t' + str(self.dispersion_threshold).replace('.', ',') + '\n')

            reminder += str('\n' +
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

        if self.project_ET_zero:
            return ((self.blockprepN + self.blocklengthN) * self.epochN * self.block_in_epochN) + (self.validation_trialN * self.numsessions)
        else:  # keep original code here
            return (self.blockprepN + self.blocklengthN) * self.epochN * self.block_in_epochN

    def get_block_starts(self):
        """Return with a list of numbers indicating the first trials of the different blocks."""

        if self.project_ET_zero:
            if self.blockstarts == None:
                self.blockstarts = [1]

                sessions_starts = self.get_session_starts()
                for i in range(len(sessions_starts) - 1):
                    start = sessions_starts[i]
                    self.blockstarts.append(start + self.validation_trialN)
                    for j in range(1, self.epochs[i] * self.block_in_epochN + 1):
                        self.blockstarts.append(
                            start + self.validation_trialN + j * (self.blocklengthN + self.blockprepN))

                    if i == len(sessions_starts) - 2:
                        self.blockstarts.append(
                            start + self.validation_trialN + (self.epochs[i] * self.block_in_epochN + 1) * (self.blocklengthN + self.blockprepN))

        else:  # keep original code here
            if self.blockstarts == None:
                self.blockstarts = [1]
                for i in range(1, self.epochN * self.block_in_epochN + 2):
                    self.blockstarts.append(
                        i * (self.blocklengthN + self.blockprepN) + 1)

        return self.blockstarts

    def get_session_starts(self):
        """Return with a list of numbers indicating the first trials of the different sessions."""

        if self.project_ET_zero:
            if self.sessionstarts == None:
                self.sessionstarts = [1]
                epochs_cumulative = []
                e_temp = 0
                for e in self.epochs:
                    e_temp += e
                    epochs_cumulative.append(e_temp)

                session = 0
                for e in epochs_cumulative:
                    session += 1
                    self.sessionstarts.append(
                        e * self.block_in_epochN * (self.blocklengthN + self.blockprepN) + 1 + (session * self.validation_trialN))
        else:  # keep original code here
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
            return [self.key_quit]
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
                    print("For running the eye-tracking version of the experiment,"
                          " we need tobii_research module to be installed!")
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
            settings_dialog.addField(u'Session ' + str(i + 1) + u' kezdő random epochok száma', 1)
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
            epoch_number = 0
            for k in range(self.numsessions):
                random_epochs = returned_data[3 + self.numsessions + k]
                epoch_in_session = 0
                for i in range(self.epochs[k]):
                    epoch_number += 1
                    epoch_in_session += 1
                    if epoch_in_session <= random_epochs:
                        self.asrt_types[epoch_number] = "noASRT"
                    else:
                        self.asrt_types[epoch_number] = returned_data[3 + (2 * self.numsessions) + k]
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
            settings_dialog.addField(u'Ingerek tavolsaga (kozeppontok kozott) (cm)', 3.0)
        else:  # 'eye-tracking'
            settings_dialog.addField(u'Ingerek tavolsaga (kozeppontok kozott) (cm)', 10.0)

        settings_dialog.addField(u'Ingerek sugara (cm)', 1.0)

        settings_dialog.addField(u'ASRT inger szine (elsodleges, R)',
                                 choices=possible_colors, initial="Orange")
        settings_dialog.addField(
            u'ASRT inger szine (masodlagos, P, explicit asrtnel)', choices=possible_colors, initial="Green")
        settings_dialog.addField(u'Hatter szine', choices=possible_colors, initial="Ivory")

        if self.experiment_type == 'reaction-time':
            settings_dialog.addField(u'RSI (ms)', 120)
        else:  # 'eye-tracking'
            settings_dialog.addField(u'RSI (ms)', 500)

        if self.experiment_type == 'eye-tracking':
            settings_dialog.addText(u'Eye-tracking paraméterek...')
            settings_dialog.addField(u'AOI négyzetek oldahossza (cm):', 3.0)
            settings_dialog.addField(u'Stimulusnál használt fixációs küszöbérték (mintavételek száma):', 12)
            settings_dialog.addField(u'Instrukcióknál használt fixációs küszöbérték (mintavételek száma):', 36)
            settings_dialog.addField(u'Diszperzió küszöbérték (cm):', 2.0)

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

            if self.experiment_type == 'eye-tracking':
                self.AOI_size = returned_data[8]
                self.stim_fixation_threshold = returned_data[9]
                self.instruction_fixation_threshold = returned_data[10]
                self.dispersion_threshold = returned_data[11]

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
        settings_dialog.addField(u'Figyelmeztetes pontosságra ezen pontossag alatt (%):', 91)
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
        if settings.experiment_type == 'reaction-time':
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

        text_stim = visual.TextStim(mywindow, text=mytext, units='cm', height=0.8, wrapWidth=20, color='black')
        text_stim.draw()
        mywindow.flip()

    def __show_message(self, instruction_list, experiment):
        """Display simple instructions on the screen."""

        # There can be more instructions to display successively
        for inst in instruction_list:
            if experiment.settings.experiment_type == 'reaction-time':
                self.__print_to_screen(inst, experiment.mywindow)
                tempkey = event.waitKeys(keyList=experiment.settings.get_key_list())
                if experiment.settings.key_quit in tempkey:
                    core.quit()
            else:  # 'eye-tracking'
                experiment.fixation_cross.draw()
                self.__print_to_screen(inst, experiment.mywindow)
                core.wait(2.0)
                response = experiment.wait_for_eye_response([experiment.fixation_cross_pos], experiment.settings.instruction_fixation_threshold)
                if response == -1:
                    core.quit()

    def show_instructions(self, experiment):
        self.__show_message(self.insts, experiment)

    def show_unexp_quit(self, experiment):
        self.__show_message(self.unexp_quit, experiment)

    def show_ending(self, experiment):
        if experiment.settings.experiment_type == 'reaction-time':
            self.__show_message(self.ending, experiment)
        else:
            self.__print_to_screen(self.ending[0], experiment.mywindow)
            core.wait(2.0)

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

    def feedback_ET(self, experiment):
        """Display feedback screen in the end of the block.

           For eye tracking we display the last five blocks' avarage reaction times.
        """
        feedback = "Most pihenhetsz egy kicsit.\n\n"
        feedback += "Az előző blokkokban mért átlagos reakcióidők:\n\n"
        blocknumber = experiment.stimblock[experiment.last_N] - min(4, len(experiment.last_block_RTs) - 1)
        for rt in experiment.last_block_RTs[-g_blocks_in_feedback:]:
            feedback += str(blocknumber) + ". blokk: " + rt + " másodperc.\n\n"
            blocknumber += 1

        self.__print_to_screen(feedback, experiment.mywindow)

    def feedback_ET_validation(self, experiment, extreme_RT_count):
        """Display feedback screen in the end of validation block.
        """
        feedback = "A teszt blokknak vége. Szólj a kísérletvezetőnek!\n\n"
        feedback += "A blokkban mért extrém reakciódidők száma: " + str(extreme_RT_count) + ".\n\n"
        feedback += "Kísérletvezető: folytatás (c) vagy újrakalibráció (r)." + "\n"

        self.__print_to_screen(feedback, experiment.mywindow)

        tempkey = event.waitKeys(keyList=['c', 'r', 'q'])
        if 'r' in tempkey or 'q' in tempkey:
            return 'quit'
        else:
            return 'continue'


class PersonDataHandler:
    """Class for handle subject related settings and data."""

    def __init__(self, subject_id, all_settings_file_path, all_IDs_file_path, subject_list_file_path, output_file_path,
                 output_file_type, jacobi_output_file_path, jacobi_ET_output_file_path):
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
        # output text files for the measured data during jacobi test
        self.jacobi_ET_output_file_path = jacobi_ET_output_file_path
        self.jacobi_output_file_path = jacobi_output_file_path
        # output buffer used to store data during jacobi test
        self.jacobi_output_data_buffer = []

    def load_person_settings(self, experiment):
        """Open settings file of the current subject and read the current state."""

        try:
            with shelve.open(self.all_settings_file_path, 'r') as this_person_settings:

                experiment.PCodes = this_person_settings['PCodes']
                experiment.subject_age = this_person_settings['subject_age']
                experiment.subject_sex = this_person_settings['subject_sex']
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
            experiment.subject_age = None
            experiment.subject_sex = None
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
            this_person_settings['subject_sex'] = experiment.subject_sex
            this_person_settings['subject_age'] = experiment.subject_age
            this_person_settings['stim_output_line'] = experiment.stim_output_line

            this_person_settings['stim_sessionN'] = experiment.stim_sessionN
            this_person_settings['stimepoch'] = experiment.stimepoch
            this_person_settings['stimblock'] = experiment.stimblock
            this_person_settings['stimtrial'] = experiment.stimtrial

            this_person_settings['stimlist'] = experiment.stimlist
            this_person_settings['stimpr'] = experiment.stimpr
            this_person_settings['last_N'] = experiment.last_N
            this_person_settings['end_at'] = experiment.end_at

    def update_all_subject_attributes_files(self, subject_sex, subject_age, subject_PCodes):
        """Add the new subject's attributes into the list of all subject data and save it into file.
           Also generate a text file with the list of all subjects participating in the experiment.
        """

        all_IDs = []
        with shelve.open(self.all_IDs_file_path) as all_subject_file:
            try:
                all_IDs = all_subject_file['ids']
            except:
                all_IDs = []

            if self.subject_id not in all_IDs:
                all_IDs.append(self.subject_id)
                all_subject_file['ids'] = all_IDs
                all_subject_file[self.subject_id] = [subject_sex, subject_age, subject_PCodes]

        with shelve.open(self.all_IDs_file_path, 'r') as all_subject_file:
            with codecs.open(self.subject_list_file_path, 'w', encoding='utf-8') as subject_list_file:
                subject_list_IO = StringIO()
                # write header
                subject_list_IO.write('subject_id\tsubject_group\tsubject_sex\tsubject_age\tsubject_PCodes\n')

                # write subject data
                for id in all_IDs:
                    id_segmented = id[len("subject_"):]
                    id_segmented = id_segmented.replace('_', '\t', 1)
                    subject_list_IO.write(id_segmented)
                    subject_list_IO.write('\t')
                    subject_list_IO.write(all_subject_file[id][0])
                    subject_list_IO.write('\t')
                    subject_list_IO.write(all_subject_file[id][1])
                    subject_list_IO.write('\t')
                    subject_list_IO.write(str(all_subject_file[id][2]))
                    subject_list_IO.write('\n')

                subject_list_file.write(subject_list_IO.getvalue())
                subject_list_IO.close()

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

    def flush_RT_data_to_output(self, experiment):
        """ Write out the ouptut date of the current trial into the output text file (reaction-time exp. type)."""
        assert self.output_file_type == 'reaction-time'

        output_buffer = StringIO()
        for data in self.output_data_buffer:
            N = data[0]
            epoch = experiment.stimepoch[N]
            PCode = experiment.which_code(epoch)
            asrt_type = experiment.settings.asrt_types[epoch]
            trial_type_high_low = experiment.calulate_trial_type_high_low(N)

            output_data = [experiment.settings.computer_name,
                           experiment.subject_group,
                           experiment.subject_number,
                           experiment.subject_sex,
                           experiment.subject_age,
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
                           trial_type_high_low,
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
                        'subject_number',
                        'subject_sex',
                        'subject_age',
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
                        'trial_type_pr',
                        'triplet_type_hl',
                        'RT',
                        'error',
                        'stimulus',
                        'response',
                        'quit_log']

        for h in heading_list:
            output_file.write(h + '\t')

    def flush_ET_data_to_output(self, experiment):
        """ Write out the ouptut data of the current trial into the output text file (eye-tracking exp. type)."""
        assert self.output_file_type == 'eye-tracking'

        output_buffer = StringIO()
        max_trial = experiment.settings.get_maxtrial()
        data_len = len(self.output_data_buffer)
        for data in self.output_data_buffer:

            N = data[0] + 1
            if N > max_trial:
                break
            epoch = experiment.stimepoch[N]
            PCode = experiment.which_code(epoch)
            asrt_type = experiment.settings.asrt_types[epoch]
            if experiment.stimpr[N] == 'pattern':
                if experiment.settings.asrt_types[epoch] == 'explicit':
                    stimcolor = experiment.colors['stimp']
                else:
                    stimcolor = experiment.colors['stimr']
            else:
                stimcolor = experiment.colors['stimr']

            trial_type_high_low = experiment.calulate_trial_type_high_low(N)
            left_gaze_data_ADCS = data[3]['left_gaze_point_on_display_area']
            right_gaze_data_ADCS = data[3]['right_gaze_point_on_display_area']
            left_eye_distance = data[3]['left_gaze_origin_in_user_coordinate_system'][2]
            right_eye_distance = data[3]['right_gaze_origin_in_user_coordinate_system'][2]
            left_gaze_validity = bool(data[3]['left_gaze_point_validity'])
            right_gaze_validity = bool(data[3]['right_gaze_point_validity'])

            if left_gaze_validity:
                left_gaze_data_PCMCS = experiment.ADCS_to_PCMCS(left_gaze_data_ADCS)
            else:
                left_gaze_data_PCMCS = (float('nan'), float('nan'))

            if right_gaze_validity:
                right_gaze_data_PCMCS = experiment.ADCS_to_PCMCS(right_gaze_data_ADCS)
            else:
                right_gaze_data_PCMCS = (float('nan'), float('nan'))

            left_pupil_diameter = data[3]['left_pupil_diameter']
            right_pupil_diameter = data[3]['right_pupil_diameter']
            left_pupil_validity = bool(data[3]['left_pupil_validity'])
            right_pupil_validity = bool(data[3]['right_pupil_validity'])

            output_data = [experiment.settings.computer_name,
                           experiment.mymonitor.getSizePix()[0],
                           experiment.mymonitor.getSizePix()[1],
                           experiment.subject_group,
                           experiment.subject_number,
                           experiment.subject_sex,
                           experiment.subject_age,
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
                           trial_type_high_low,
                           experiment.stimlist[N],
                           data[2],
                           left_gaze_data_ADCS[0],
                           left_gaze_data_ADCS[1],
                           right_gaze_data_ADCS[0],
                           right_gaze_data_ADCS[1],
                           left_gaze_data_PCMCS[0],
                           left_gaze_data_PCMCS[1],
                           right_gaze_data_PCMCS[0],
                           right_gaze_data_PCMCS[1],
                           left_eye_distance,
                           right_eye_distance,
                           left_gaze_validity,
                           right_gaze_validity,
                           left_pupil_diameter,
                           right_pupil_diameter,
                           left_pupil_validity,
                           right_pupil_validity,
                           data[4],
                           experiment.dict_pos[1][0],
                           experiment.dict_pos[1][1],
                           experiment.dict_pos[2][0],
                           experiment.dict_pos[2][1],
                           experiment.dict_pos[3][0],
                           experiment.dict_pos[3][1],
                           experiment.dict_pos[4][0],
                           experiment.dict_pos[4][1]]

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
        # make sure we don't get more data here durig writing it out
        assert data_len == len(self.output_data_buffer)
        self.output_data_buffer.clear()

    def add_ET_heading_to_output(self, output_file):
        """Add the first line to the ouput with the names of the different variables (eye-tracking exp. type)."""
        assert self.output_file_type == 'eye-tracking'

        heading_list = ['computer_name',
                        'monitor_width_pixel',
                        'monitor_height_pixel',
                        'subject_group',
                        'subject_number',
                        'subject_sex',
                        'subject_age',
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
                        'trial_type_pr',
                        'triplet_type_hl',
                        'stimulus',
                        'trial_phase',
                        'left_gaze_data_X_ADCS',
                        'left_gaze_data_Y_ADCS',
                        'right_gaze_data_X_ADCS',
                        'right_gaze_data_Y_ADCS',
                        'left_gaze_data_X_PCMCS',
                        'left_gaze_data_Y_PCMCS',
                        'right_gaze_data_X_PCMCS',
                        'right_gaze_data_Y_PCMCS',
                        'left_eye_distance',
                        'right_eye_distance',
                        'left_gaze_validity',
                        'right_gaze_validity',
                        'left_pupil_diameter',
                        'right_pupil_diameter',
                        'left_pupil_validity',
                        'right_pupil_validity',
                        'gaze_data_time_stamp',
                        'stimulus_1_position_X_PCMCS',
                        'stimulus_1_position_Y_PCMCS',
                        'stimulus_2_position_X_PCMCS',
                        'stimulus_2_position_Y_PCMCS',
                        'stimulus_3_position_X_PCMCS',
                        'stimulus_3_position_Y_PCMCS',
                        'stimulus_4_position_X_PCMCS',
                        'stimulus_4_position_Y_PCMCS',
                        'quit_log']

        for h in heading_list:
            output_file.write(h + '\t')

    def flush_jacobi_ET_data_to_output(self, experiment):
        """ Write out the ouptut data of the current trial into the output text file (eye-tracking exp. type)."""
        assert(self.output_file_type == 'eye-tracking')
        assert(experiment.settings.epochN >= 2)

        output_buffer = StringIO()
        data_len = len(self.output_data_buffer)
        for data in self.output_data_buffer:

            if data[1] == 0 or data[2] == 0:
                continue
            epoch = 2
            PCode = experiment.which_code(epoch)
            asrt_type = experiment.settings.asrt_types[epoch]

            left_gaze_data_ADCS = data[4]['left_gaze_point_on_display_area']
            right_gaze_data_ADCS = data[4]['right_gaze_point_on_display_area']
            left_eye_distance = data[4]['left_gaze_origin_in_user_coordinate_system'][2]
            right_eye_distance = data[4]['right_gaze_origin_in_user_coordinate_system'][2]
            left_gaze_validity = bool(data[4]['left_gaze_point_validity'])
            right_gaze_validity = bool(data[4]['right_gaze_point_validity'])

            if left_gaze_validity:
                left_gaze_data_PCMCS = experiment.ADCS_to_PCMCS(left_gaze_data_ADCS)
            else:
                left_gaze_data_PCMCS = (float('nan'), float('nan'))

            if right_gaze_validity:
                right_gaze_data_PCMCS = experiment.ADCS_to_PCMCS(right_gaze_data_ADCS)
            else:
                right_gaze_data_PCMCS = (float('nan'), float('nan'))

            left_pupil_diameter = data[4]['left_pupil_diameter']
            right_pupil_diameter = data[4]['right_pupil_diameter']
            left_pupil_validity = bool(data[4]['left_pupil_validity'])
            right_pupil_validity = bool(data[4]['right_pupil_validity'])

            output_data = [experiment.settings.computer_name,
                           experiment.mymonitor.getSizePix()[0],
                           experiment.mymonitor.getSizePix()[1],
                           experiment.subject_group,
                           experiment.subject_number,
                           experiment.subject_sex,
                           experiment.subject_age,
                           asrt_type,
                           PCode,

                           data[0],
                           data[1],
                           data[2],

                           experiment.frame_rate,
                           experiment.frame_time,
                           experiment.frame_sd,

                           data[3],
                           left_gaze_data_ADCS[0],
                           left_gaze_data_ADCS[1],
                           right_gaze_data_ADCS[0],
                           right_gaze_data_ADCS[1],
                           left_gaze_data_PCMCS[0],
                           left_gaze_data_PCMCS[1],
                           right_gaze_data_PCMCS[0],
                           right_gaze_data_PCMCS[1],
                           left_eye_distance,
                           right_eye_distance,
                           left_gaze_validity,
                           right_gaze_validity,
                           left_pupil_diameter,
                           right_pupil_diameter,
                           left_pupil_validity,
                           right_pupil_validity,
                           data[5],
                           experiment.dict_pos[1][0],
                           experiment.dict_pos[1][1],
                           experiment.dict_pos[2][0],
                           experiment.dict_pos[2][1],
                           experiment.dict_pos[3][0],
                           experiment.dict_pos[3][1],
                           experiment.dict_pos[4][0],
                           experiment.dict_pos[4][1]]

            output_buffer.write("\n")
            for data in output_data:
                if isinstance(data, numbers.Number):
                    data = str(data)
                    data = data.replace('.', ',')
                else:
                    data = str(data)
                output_buffer.write(data + '\t')

        with codecs.open(self.jacobi_ET_output_file_path, 'w', encoding='utf-8') as output_file:
            self.add_jacobi_ET_heading_to_output(output_file)
            output_file.write(output_buffer.getvalue())

        output_buffer.close()
        # make sure we don't get more data here durig writing it out
        assert data_len == len(self.output_data_buffer)
        self.output_data_buffer.clear()

    def add_jacobi_ET_heading_to_output(self, output_file):
        """Add the first line to the ouput with the names of the different variables (eye-tracking exp. type)."""
        assert self.output_file_type == 'eye-tracking'

        heading_list = ['computer_name',
                        'monitor_width_pixel',
                        'monitor_height_pixel',
                        'subject_group',
                        'subject_number',
                        'subject_sex',
                        'subject_age',
                        'asrt_type',
                        'PCode',

                        'test_type',
                        'run',
                        'trial',

                        'frame_rate',
                        'frame_time',
                        'frame_sd',

                        'trial_phase',
                        'left_gaze_data_X_ADCS',
                        'left_gaze_data_Y_ADCS',
                        'right_gaze_data_X_ADCS',
                        'right_gaze_data_Y_ADCS',
                        'left_gaze_data_X_PCMCS',
                        'left_gaze_data_Y_PCMCS',
                        'right_gaze_data_X_PCMCS',
                        'right_gaze_data_Y_PCMCS',
                        'left_eye_distance',
                        'right_eye_distance',
                        'left_gaze_validity',
                        'right_gaze_validity',
                        'left_pupil_diameter',
                        'right_pupil_diameter',
                        'left_pupil_validity',
                        'right_pupil_validity',
                        'gaze_data_time_stamp',
                        'stimulus_1_position_X_PCMCS',
                        'stimulus_1_position_Y_PCMCS',
                        'stimulus_2_position_X_PCMCS',
                        'stimulus_2_position_Y_PCMCS',
                        'stimulus_3_position_X_PCMCS',
                        'stimulus_3_position_Y_PCMCS',
                        'stimulus_4_position_X_PCMCS',
                        'stimulus_4_position_Y_PCMCS']

        for h in heading_list:
            output_file.write(h + '\t')

    def add_jacobi_heading_to_output(self, output_file):
        """Add the first line to the ouput with the names of the different variables (eye-tracking exp. type)."""
        assert self.output_file_type == 'eye-tracking'

        heading_list = ['computer_name',
                        'monitor_width_pixel',
                        'monitor_height_pixel',
                        'subject_group',
                        'subject_number',
                        'subject_sex',
                        'subject_age',
                        'asrt_type',
                        'PCode',

                        'test_type',
                        'run',
                        'trial',

                        'frame_rate',
                        'frame_time',
                        'frame_sd',

                        'response']

        for h in heading_list:
            output_file.write(h + '\t')

    def flush_jacobi_data_to_output(self, experiment):
        """ Write out the ouptut data of the current trial into the output text file (eye-tracking exp. type)."""
        assert(self.output_file_type == 'eye-tracking')
        assert(experiment.settings.epochN >= 2)

        output_buffer = StringIO()
        for data in self.jacobi_output_data_buffer:

            if data[1] == 0 or data[2] == 0:
                continue
            epoch = 2
            PCode = experiment.which_code(epoch)
            asrt_type = experiment.settings.asrt_types[epoch]

            output_data = [experiment.settings.computer_name,
                           experiment.mymonitor.getSizePix()[0],
                           experiment.mymonitor.getSizePix()[1],
                           experiment.subject_group,
                           experiment.subject_number,
                           experiment.subject_sex,
                           experiment.subject_age,
                           asrt_type,
                           PCode,

                           data[0],
                           data[1],
                           data[2],

                           experiment.frame_rate,
                           experiment.frame_time,
                           experiment.frame_sd,

                           data[3]]

            output_buffer.write("\n")
            for data in output_data:
                if isinstance(data, numbers.Number):
                    data = str(data)
                    data = data.replace('.', ',')
                else:
                    data = str(data)
                output_buffer.write(data + '\t')

        with codecs.open(self.jacobi_output_file_path, 'w', encoding='utf-8') as output_file:
            self.add_jacobi_heading_to_output(output_file)
            output_file.write(output_buffer.getvalue())

        output_buffer.close()
        self.jacobi_output_data_buffer.clear()


class Experiment:
    """ Class for running the ASRT experiment."""

    def __init__(self, workdir_path, project_ET_zero=False):
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
        self.current_sampling_window = None
        self.last_block_RTs = []

        self.fixation_cross_pos = None
        self.fixation_cross = None

        self.shared_data_lock = threading.Lock()
        self.main_loop_lock = threading.Lock()

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
        # sex of the subject (e.g. male, female, other)
        self.subject_sex = None
        # age of the subject (e.g. 23 (years))
        self.subject_age = None

        # a dictionary of pcodes for the different epochs (e.g. {1 : '1st - 1234', 2 : '5th - 1423'})
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
        # global trial number -> pattern or random stimulus mapping (e. g.{1 : 'pattern', 2 : 'random', 3 : 'pattern', 4 : 'random'} - two sessions with two trials in each)
        self.stimpr = None
        # number of the last trial (it is 0 in the beggining and it is always equal with the last displayed stimulus's serial number
        self.last_N = None
        # this variable has a meaning during presentation, showing the phase of displaying the current stimulus
        # possible values: "before_stimulus", "stimulus_on_screen", "after_reaction"
        self.trial_phase = None
        # this variable has a meaning during presentation, last measured RSI
        self.last_RSI = None

        self.project_ET_zero = project_ET_zero

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

    def show_subject_identification_dialog(self):
        """Ask the user to specify the subject's attributes (name, subject number, group)."""

        warningtext = ''
        itsOK = False
        while not itsOK:
            settings_dialog = gui.Dlg(title=u'Beállítások')
            settings_dialog.addText(warningtext, color='Red')
            settings_dialog.addField(u'Ksz. sorszáma', "0")
            if len(self.settings.groups) > 1:
                settings_dialog.addField(u'Csoport', choices=self.settings.groups)

            returned_data = settings_dialog.show()
            if settings_dialog.OK:
                subject_number = returned_data[0]
                try:
                    subject_number = int(subject_number)
                    if subject_number >= 0:
                        itsOK = True
                        self.subject_number = subject_number
                    else:
                        warningtext = u'Pozitív egész számot adj meg a sorszámhoz!'
                        continue

                except:
                    warningtext = u'Pozitív egész számot adj meg a sorszámhoz!'
                    continue

                if len(self.settings.groups) > 1:
                    self.subject_group = returned_data[1]
                else:
                    self.subject_group = ""
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
            expstart11.addText(u'A jacobi teszt maradt hátra.')
            expstart11.show()

    def show_subject_attributes_dialog(self):
        """Select pattern sequences for the different sessions for the current subject."""

        # Use a custom dialog for our specific experiment
        if self.project_ET_zero:

            settings_dialog = gui.Dlg(title=u'Beállítások')
            settings_dialog.addText('')
            settings_dialog.addField(u'Nem', choices=["férfi", "nő", "más"])
            settings_dialog.addField(u'Életkor', "25")
            settings_dialog.addField(u'Első PCode', choices=['1st', '2nd', '3rd', '4th', '5th', '6th'])
            settings_dialog.addField(u'Második PCode', choices=['1st', '2nd', '3rd', '4th', '5th', '6th'])

            returned_data = settings_dialog.show()
            if settings_dialog.OK:
                self.PCodes = {}

                subject_sex = returned_data[0]
                subject_age = returned_data[1]
                for i in range(self.settings.epochN):
                    if self.settings.asrt_types[i + 1] == 'noASRT':
                        PCode = 'noPattern'
                    elif i == self.settings.epochs[0] + 1:
                        PCode = returned_data[3]
                    else:
                        PCode = returned_data[2]
                    if PCode == '1st':
                        self.PCodes[i + 1] = '1st - 1234'
                    elif PCode == '2nd':
                        self.PCodes[i + 1] = '2nd - 1243'
                    elif PCode == '3rd':
                        self.PCodes[i + 1] = '3rd - 1324'
                    elif PCode == '4th':
                        self.PCodes[i + 1] = '4th - 1342'
                    elif PCode == '5th':
                        self.PCodes[i + 1] = '5th - 1423'
                    elif PCode == '6th':
                        self.PCodes[i + 1] = '6th - 1432'
                    else:
                        self.PCodes[i + 1] = 'noPattern'

                if subject_sex == "férfi":
                    self.subject_sex = "male"
                elif subject_sex == "nő":
                    self.subject_sex = "female"
                else:
                    self.subject_sex = "other"

                try:
                    subject_age = int(subject_age)
                    self.subject_age = str(subject_age)
                except:
                    core.quit()
                return self.PCodes
            else:
                core.quit()
        else:  # keep the original / more general code here
            settings_dialog = gui.Dlg(title=u'Beállítások')
            settings_dialog.addText('')
            settings_dialog.addField(u'Nem', choices=["férfi", "nő", "más"])
            settings_dialog.addField(u'Életkor', "25")

            epoch_number = 0
            for i in range(self.settings.numsessions):
                for j in range(self.settings.epochs[i]):
                    epoch_number += 1
                    if self.settings.asrt_types[epoch_number] == "noASRT":
                        settings_dialog.addFixedField(u'Epoch ' + str(epoch_number) + ' PCode', 'noPattern')
                    else:
                        settings_dialog.addField(u'Epoch ' + str(epoch_number) + ' PCode', choices=[
                            '1st', '2nd', '3rd', '4th', '5th', '6th'])

            returned_data = settings_dialog.show()
            if settings_dialog.OK:
                self.PCodes = {}

                subject_sex = returned_data[0]
                subject_age = returned_data[1]
                for i in range(epoch_number):
                    PCode = returned_data[i + 2]
                    if PCode == '1st':
                        self.PCodes[i + 1] = '1st - 1234'
                    elif PCode == '2nd':
                        self.PCodes[i + 1] = '2nd - 1243'
                    elif PCode == '3rd':
                        self.PCodes[i + 1] = '3rd - 1324'
                    elif PCode == '4th':
                        self.PCodes[i + 1] = '4th - 1342'
                    elif PCode == '5th':
                        self.PCodes[i + 1] = '5th - 1423'
                    elif PCode == '6th':
                        self.PCodes[i + 1] = '6th - 1432'
                    else:
                        self.PCodes[i + 1] = 'noPattern'

                index = self.settings.numsessions

                if subject_sex == "férfi":
                    self.subject_sex = "male"
                elif subject_sex == "nő":
                    self.subject_sex = "female"
                else:
                    self.subject_sex = "other"

                try:
                    subject_age = int(subject_age)
                    self.subject_age = str(subject_age)
                except:
                    core.quit()
                return self.PCodes
            else:
                core.quit()

    def which_code(self, epoch_number):
        """Convert sessions pattern code to a raw code containing only the series of stimulus numbers."""

        pcode_raw = self.PCodes[epoch_number]
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

    def next_stim(self, epoch_number, stimulus):
        PCode = self.which_code(epoch_number)
        assert PCode != "noPattern"

        dict_next_stimulus = {}
        dict_next_stimulus[PCode[0]] = PCode[1]
        dict_next_stimulus[PCode[1]] = PCode[2]
        dict_next_stimulus[PCode[2]] = PCode[3]
        dict_next_stimulus[PCode[3]] = PCode[0]
        return int(dict_next_stimulus[str(stimulus)])

    def calulate_trial_type_high_low(self, N):
        epoch = self.stimepoch[N]
        PCode = self.which_code(epoch)
        if PCode == "noPattern" or self.stimtrial[N] < 3 or N < 3:
            return "none"
        elif self.next_stim(epoch, self.stimlist[N - 2]) == self.stimlist[N]:
            return "high"
        else:
            return "low"

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

            if self.project_ET_zero:
                if all_trial_Nr + 1 in sessionsstarts:
                    current_trial_num = 0

                    for i in range(self.settings.validation_trialN):
                        current_trial_num += 1

                        all_trial_Nr += 1
                        asrt_type = self.settings.asrt_types[epoch]

                        current_stim = random.choice([1, 2, 3, 4])
                        self.stimlist[all_trial_Nr] = current_stim
                        self.stimpr[all_trial_Nr] = "random"
                        self.stimtrial[all_trial_Nr] = current_trial_num
                        self.stimblock[all_trial_Nr] = 0
                        self.stimepoch[all_trial_Nr] = epoch

            for block in range(1, self.settings.block_in_epochN + 1):
                block_num += 1
                current_trial_num = 0

                # practice
                for practice in range(1, self.settings.blockprepN + 1):
                    current_trial_num += 1

                    all_trial_Nr += 1
                    asrt_type = self.settings.asrt_types[epoch]

                    current_stim = random.choice([1, 2, 3, 4])
                    self.stimlist[all_trial_Nr] = current_stim
                    self.stimpr[all_trial_Nr] = "random"
                    self.stimtrial[all_trial_Nr] = current_trial_num
                    self.stimblock[all_trial_Nr] = block_num
                    self.stimepoch[all_trial_Nr] = epoch

                # real
                for real in range(1, self.settings.blocklengthN + 1):

                    current_trial_num += 1
                    all_trial_Nr += 1

                    asrt_type = self.settings.asrt_types[epoch]

                    if self.settings.blockprepN % 2 == 1:
                        mod_pattern = 0
                    else:
                        mod_pattern = 1

                    if current_trial_num % 2 == mod_pattern and asrt_type != "noASRT":
                        if current_trial_num > 2:
                            current_stim = self.next_stim(epoch, self.stimlist[all_trial_Nr - 2])
                            self.stimpr[all_trial_Nr] = "pattern"
                        else:
                            # first pattern stim is random
                            current_stim = random.choice([1, 2, 3, 4])
                            self.stimpr[all_trial_Nr] = "random"
                    else:
                        current_stim = random.choice([1, 2, 3, 4])
                        self.stimpr[all_trial_Nr] = "random"

                    self.stimlist[all_trial_Nr] = current_stim
                    self.stimtrial[all_trial_Nr] = current_trial_num
                    self.stimblock[all_trial_Nr] = block_num
                    self.stimepoch[all_trial_Nr] = epoch

    def participant_id(self):
        """Find out the current subject and read subject settings / progress if he/she already has any data."""

        self.show_subject_identification_dialog()

        # unique subject ID
        subject_id = 'subject_' + str(self.subject_number) + '_' + self.subject_group

        # init subject data handler with the rigth file paths
        all_settings_file_path = os.path.join(self.workdir_path, "subject_settings", subject_id)
        all_IDs_file_path = os.path.join(self.workdir_path, "subject_settings", "participant_settings")
        subject_list_file_path = os.path.join(self.workdir_path, "subject_settings",
                                              "participants_in_experiment.txt")
        output_file_path = os.path.join(self.workdir_path, "logs", subject_id + '_log.txt')
        jacobi_output_file_path = os.path.join(self.workdir_path, "logs", subject_id + '_jacobi_log.txt')
        jacobi_ET_output_file_path = os.path.join(self.workdir_path, "logs", subject_id + '_jacobi_ET_log.txt')
        self.person_data = PersonDataHandler(subject_id, all_settings_file_path,
                                             all_IDs_file_path, subject_list_file_path,
                                             output_file_path, self.settings.experiment_type,
                                             jacobi_output_file_path, jacobi_ET_output_file_path)

        # try to load settings and progress for the given subject ID
        self.person_data.load_person_settings(self)

        if bool(self.PCodes):
            # the current subject already started the experiment
            self.show_subject_continuation_dialog()
        # we have a new subject
        else:
            # ask about the pattern codes used in the different sessions
            self.show_subject_attributes_dialog()
            # update participant attribute files
            self.person_data.update_all_subject_attributes_files(self.subject_sex, self.subject_age, self.PCodes)
            # calculate stimulus properties for the experiment
            self.calculate_stim_properties()
            # save data of the new subject
            self.person_data.save_person_settings(self)

    def init_eyetracker(self):
        allTrackers = tobii.find_all_eyetrackers()
        if not allTrackers:
            self.print_to_screen("Eye-tracker eszköz keresése...")

        # Sometimes the eyetracker is not identified for the first time. Try more times.
        loopCount = 1
        while not allTrackers and loopCount < 200:
            allTrackers = tobii.find_all_eyetrackers()
            core.wait(0.05)
            loopCount += 1

        if len(allTrackers) < 1:
            self.print_to_screen("Nem találtam semmilyen eye-tracker eszközt!")
            core.wait(3.0)
            core.quit()

        self.eye_tracker = allTrackers[0]

    def eye_data_callback(self, origGazeData):
        self.eye_data_callback_gen(origGazeData, False)

    def eye_data_callback_jacobi(self, origGazeData):
        self.eye_data_callback_gen(origGazeData, True)

    def eye_data_callback_gen(self, origGazeData, jacobi=False):
        gazeData = copy.deepcopy(origGazeData)
        time_stamp = tobii.get_system_time_stamp()
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

        with self.shared_data_lock:
            if x_coord != None and y_coord != None:
                self.gaze_data_list.append((x_coord, y_coord))
            else:
                self.gaze_data_list.append((None, None))

            if len(self.gaze_data_list) > self.current_sampling_window:
                self.gaze_data_list.pop(0)
                assert len(self.gaze_data_list) == self.current_sampling_window

            if jacobi:
                self.person_data.output_data_buffer.append([self.jacobi_test_phase, self.jacobi_run,
                                                            self.jacobi_trial, self.jacobi_trial_phase, gazeData, time_stamp])
            else:
                self.person_data.output_data_buffer.append([self.last_N, self.last_RSI, self.trial_phase, gazeData, time_stamp])

        if self.main_loop_lock.locked():
            self.main_loop_lock.release()

    def point_is_in_rectangle(self, point, rect_center, rect_size):
        if abs(point[0] - rect_center[0]) <= rect_size / 2.0 and abs(point[1] - rect_center[1]) <= rect_size / 2.0:
            return True
        else:
            return False

    def ADCS_to_PCMCS(self, pos_ADCS):
        ''' Convert position from tobii active display coordinate system (ADCS) to PsychoPy coordinate system with cm unit (PCMCS).

            Active display coordinate system: http://developer.tobiipro.com/commonconcepts/coordinatesystems.html
            PsychoPy coordinate system with cm unit: https://www.psychopy.org/general/units.html        
        '''
        aspect_ratio = self.mymonitor.getSizePix()[1] / self.mymonitor.getSizePix()[0]
        monitor_width_cm = self.settings.monitor_width
        monitor_height_cm = monitor_width_cm * aspect_ratio

        # shift origin from top-left to center
        shift_x = monitor_width_cm / 2
        shift_y = monitor_height_cm / 2

        # scale coordinates from normalized coordinates to cm unit coordinates
        # we also mirror the y coordinates
        pos_PCMCS = ((pos_ADCS[0] * monitor_width_cm) - shift_x,
                     ((pos_ADCS[1] * monitor_height_cm) - shift_y) * - 1)
        return pos_PCMCS

    def distance_ADCS_to_PCMCS(self, distance_ADCS):
        ''' Convert distance from tobii active display coordinate system (ADCS) to PsychoPy coordinate system with cm unit (PCMCS).

            Active display coordinate system: http://developer.tobiipro.com/commonconcepts/coordinatesystems.html
            PsychoPy coordinate system with cm unit: https://www.psychopy.org/general/units.html        
        '''
        aspect_ratio = self.mymonitor.getSizePix()[1] / self.mymonitor.getSizePix()[0]
        monitor_width_cm = self.settings.monitor_width
        monitor_height_cm = monitor_width_cm * aspect_ratio

        # scale coordinates from normalized coordinates to cm unit coordinates
        distance_PCMCS = (distance_ADCS[0] * monitor_width_cm,
                          distance_ADCS[1] * monitor_height_cm)
        return distance_PCMCS

    def linear_interpolation(self, gaze_data_list, invalid_index):
        # Do we have an actual invalid data here?
        assert (gaze_data_list[invalid_index][0] == None or gaze_data_list[invalid_index][1] == None)

        # Find first valid data before the missing data sample
        valid_before = invalid_index - 1
        while (valid_before >= 0 and
               (gaze_data_list[valid_before][0] == None or gaze_data_list[valid_before][1] == None)):
            valid_before -= 1

        if valid_before < 0:
            return None

        # Find first valid data after the missing data sample
        valid_after = invalid_index + 1
        while (valid_after < len(gaze_data_list) and
               (gaze_data_list[valid_after][0] == None or gaze_data_list[valid_after][1] == None)):
            valid_after += 1

        if valid_after >= len(gaze_data_list):
            return None

        # We calulate distances in sample count
        full_distance = valid_after - valid_before
        before_distance = invalid_index - valid_before
        after_distance = valid_after - invalid_index
        before_scale_factor = after_distance / full_distance
        after_scale_factor = before_distance / full_distance

        new_x = (gaze_data_list[valid_before][0] * before_scale_factor +
                 gaze_data_list[valid_after][0] * after_scale_factor)
        new_y = (gaze_data_list[valid_before][1] * before_scale_factor +
                 gaze_data_list[valid_after][1] * after_scale_factor)

        return (new_x, new_y)

    def wait_for_eye_response(self, expected_eye_pos_list, fixation_threshold):
        assert (len(expected_eye_pos_list) == 1 or len(expected_eye_pos_list) == 4)

        while (True):
            if 'q' in event.getKeys():
                if self.main_loop_lock.locked():
                    self.main_loop_lock.release()
                return -1

            self.main_loop_lock.acquire()

            with self.shared_data_lock:
                if len(self.gaze_data_list) < fixation_threshold:
                    continue

                last_item = self.gaze_data_list[-1]

                # calculate avarage and max distance
                count = 0
                sum_x = 0
                sum_y = 0
                max_x = -10.0
                max_y = -10.0
                min_x = 10.0
                min_y = 10.0
                count = 0
                invalid_count = 0
                for i in range(len(self.gaze_data_list)):
                    pos_x = self.gaze_data_list[i][0]
                    pos_y = self.gaze_data_list[i][1]

                    # We interpolate the invalid data lineary
                    if pos_x == None or pos_y == None:
                        invalid_count += 1
                        interpolated_data = self.linear_interpolation(self.gaze_data_list, i)
                        if interpolated_data == None:
                            break
                        else:
                            pos_x = interpolated_data[0]
                            pos_y = interpolated_data[1]

                    if pos_x != None and pos_y != None:
                        sum_x += pos_x
                        sum_y += pos_y
                        max_x = max(max_x, pos_x)
                        max_y = max(max_y, pos_y)
                        min_x = min(min_x, pos_x)
                        min_y = min(min_y, pos_y)
                        count += 1

                    if count >= fixation_threshold:
                        break

                    if invalid_count > fixation_threshold * 0.334:
                        break

                # We have too many invalid data (we allow maximum 33.3333% to be invalid)
                if invalid_count > fixation_threshold * 0.334:
                    continue

                # Do we have engough data for a fixation?
                if count < fixation_threshold:
                    continue

                # Is the eye data within the given dispersion?
                dispersion_vector_norm = ((max_x - min_x), (max_y - min_y))
                dispersion_vector_cm = self.distance_ADCS_to_PCMCS(dispersion_vector_norm)
                dispersion_cm = dispersion_vector_cm[0] + dispersion_vector_cm[1]
                if dispersion_cm > self.settings.dispersion_threshold:
                    continue

                # Calculate fixation position
                avg_pos_norm = (sum_x / fixation_threshold, sum_y / fixation_threshold)
                avg_pos_cm = self.ADCS_to_PCMCS(avg_pos_norm)

                for i in range(len(expected_eye_pos_list)):
                    if self.point_is_in_rectangle(avg_pos_cm, expected_eye_pos_list[i], self.settings.AOI_size):
                        if self.main_loop_lock.locked():
                            self.main_loop_lock.release()
                        return i + 1

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

        xtext = visual.TextStim(self.mywindow, text=mytext, units="cm", height=0.8, wrapWidth=20, color="black")
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

        if self.settings.asrt_types[self.stimepoch[N - 1]] == 'explicit':

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

    def show_feedback_ET(self, RT_all_list, end_of_session):
        """ Display feedback in the end of the blocks, showing some data about reaction time."""

        rt_mean = float(sum(RT_all_list)) / len(RT_all_list)
        rt_mean_str = str(rt_mean)[:5].replace('.', ',')
        self.last_block_RTs.append(rt_mean_str)

        whatnow = self.instructions.feedback_ET(self)

        # wait some time
        core.wait(10.0)

        if not end_of_session:
            self.fixation_cross.draw()
            self.print_to_screen("A következő blokkra lépéshez néz a keresztre!")
            response = self.wait_for_eye_response([self.fixation_cross_pos], self.settings.instruction_fixation_threshold)
            if response == -1:
                return 'quit'
            else:
                return 'continue'

        return 'continue'

    def show_feedback_ET_validation(self, RT_all_list, end_of_session):
        """ Display feedback in the end of the blocks, showing some data about reaction time."""

        extreme_RT_count = 0
        for rt in RT_all_list:
            if rt > 1.0:  # 1 sec
                extreme_RT_count += 1

        whatnow = self.instructions.feedback_ET_validation(self, extreme_RT_count)

        if whatnow == 'quit':
            return 'quit'

        if not end_of_session:
            self.fixation_cross.draw()
            self.print_to_screen("A következő blokkra lépéshez néz a keresztre!")
            response = self.wait_for_eye_response([self.fixation_cross_pos], self.settings.instruction_fixation_threshold)
            if response == -1:
                return 'quit'
            else:
                return 'continue'

        return 'continue'

    def wait_for_response(self, expected_response, response_clock):
        if self.settings.experiment_type == 'reaction-time':
            press = event.waitKeys(keyList=self.settings.get_key_list(),
                                   timeStamped=response_clock)
            if press[0][0] == 'q':
                return (-1, press[0][1])
            return (self.pressed_dict[press[0][0]], press[0][1])
        # for ET version we wait for getting the right response (there is no wrong answer)
        else:
            response = self.wait_for_eye_response([self.dict_pos[expected_response]], self.settings.stim_fixation_threshold)
            # this RT is not precise, but good enough to give a feedback for the subject
            if response == 1:
                return (expected_response, response_clock.getTime())
            else:
                return (-1, response_clock.getTime())

    def quit_presentation(self):
        self.print_to_screen("Kilépés...\nAdatok mentése...")

        if self.eye_tracker is not None:
            self.eye_tracker.unsubscribe_from(tobii.EYETRACKER_GAZE_DATA, self.eye_data_callback)

        self.person_data.append_to_output_file('userquit')
        core.wait(3.0)
        core.quit()

    def presentation(self):
        """The real experiment happens here. This method displays the stimulus window and records the reactions."""

        # init presented objects
        stimP = visual.Circle(win=self.mywindow, radius=self.settings.asrt_size, units="cm",
                              fillColor=self.colors['stimp'], lineColor=self.colors['linecolor'], pos=self.dict_pos[1])
        stimR = visual.Circle(win=self.mywindow, radius=self.settings.asrt_size, units="cm",
                              fillColor=self.colors['stimr'], lineColor=self.colors['linecolor'], pos=self.dict_pos[1])
        stimbg = visual.Circle(win=self.mywindow, radius=self.settings.asrt_size, units="cm",
                               fillColor=None, lineColor=self.colors['linecolor'])
        if self.settings.experiment_type == 'eye-tracking':
            # place the fixation cross to the bottom-right corner of the screen
            aspect_ratio = self.mymonitor.getSizePix()[1] / self.mymonitor.getSizePix()[0]
            monitor_width_cm = self.settings.monitor_width
            monitor_height_cm = monitor_width_cm * aspect_ratio
            self.fixation_cross_pos = (monitor_width_cm / 2 - 3, -(monitor_height_cm / 2 - 3))
            self.fixation_cross = visual.TextStim(win=self.mywindow, text="+", height=3, units="cm", color='black', pos=self.fixation_cross_pos)

        stim_RSI = 0.0
        N = self.last_N + 1

        responses_in_block = 0
        accs_in_block = []

        patternERR = 0
        number_of_patterns = 0

        RT_pattern_list = []
        RT_all_list = []

        RSI = core.StaticPeriod(screenHz=self.frame_rate)
        RSI_clock = core.Clock()
        trial_clock = core.Clock()

        first_trial_in_block = True

        self.trial_phase = "before_stimulus"
        self.last_RSI = -1

        # start recording gaze data
        if self.eye_tracker is not None:
            self.current_sampling_window = self.settings.instruction_fixation_threshold
            self.eye_tracker.subscribe_to(tobii.EYETRACKER_GAZE_DATA, self.eye_data_callback, as_dictionary=True)

        # show instructions or continuation message
        if N in self.settings.get_session_starts():
            self.instructions.show_instructions(self)

        else:
            self.instructions.show_unexp_quit(self)

        RSI.start(self.settings.RSI_time)
        while True:
            # four empty circles where the actual stimulus can be placed
            self.stim_bg(stimbg)
            self.mywindow.flip()
            with self.shared_data_lock:
                if self.eye_tracker is not None:
                    self.current_sampling_window = self.settings.stim_fixation_threshold
                    self.gaze_data_list.clear()
                self.last_N = N - 1
                self.trial_phase = "before_stimulus"
                self.last_RSI = -1

            # set the actual stimulus' position and fill color
            if self.stimpr[N] == 'pattern':
                if self.settings.asrt_types[self.stimepoch[N]] == 'explicit':
                    stimP.fillColor = self.colors['stimp']
                else:
                    stimP.fillColor = self.colors['stimr']
                stimcolor = stimP.fillColor
                stimP.setPos(self.dict_pos[self.stimlist[N]])
            else:
                stimcolor = self.colors['stimr']
                stimR.setPos(self.dict_pos[self.stimlist[N]])

            # wait before the next stimulus to have the set RSI
            RSI.complete()

            cycle = 0

            while True:
                cycle += 1
                self.stim_bg(stimbg)

                # display the actual stimulus
                if self.stimpr[N] == 'pattern':
                    stimP.draw()
                else:
                    stimR.draw()
                self.mywindow.flip()

                # we measure the actual RSI
                if cycle == 1:
                    if first_trial_in_block:
                        stim_RSI = 0.0
                    else:
                        stim_RSI = RSI_clock.getTime()

                with self.shared_data_lock:
                    self.trial_phase = "stimulus_on_screen"
                    self.last_RSI = stim_RSI

                if cycle == 1:
                    trial_clock.reset()
                (response, time_stamp) = self.wait_for_response(self.stimlist[N], trial_clock)

                with self.shared_data_lock:
                    self.trial_phase = "after_reaction"

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
                        with self.shared_data_lock:
                            self.last_N = N - 1

                    self.quit_presentation()

                # right response
                elif response == self.stimlist[N]:
                    stimACC = 0
                    accs_in_block.append(0)

                    if self.stimpr[N] == 'pattern':
                        number_of_patterns += 1
                        RT_pattern_list.append(stimRT)
                    RT_all_list.append(stimRT)

                # wrong response -> let's wait for the next response
                else:
                    stimACC = 1
                    accs_in_block.append(1)

                    if self.stimpr[N] == 'pattern':
                        patternERR += 1
                        number_of_patterns += 1
                        RT_pattern_list.append(stimRT)
                    RT_all_list.append(stimRT)

                # save data of the last trial (for ET we save data for every sample)
                if self.settings.experiment_type == 'reaction-time':
                    self.person_data.output_data_buffer.append([N, stim_RSI, stim_RT_time, stim_RT_date,
                                                                stimRT, stimACC, response, stimcolor, self.stim_output_line])

                if stimACC == 0:
                    N += 1
                    first_trial_in_block = False
                    break

            # end of the block (show feedback and reinit variables for the next block)
            if N in self.settings.get_block_starts():

                self.print_to_screen(u"Adatok mentése és visszajelzés előkészítése...")
                with self.shared_data_lock:
                    self.last_N = N - 1
                    self.trial_phase = "before_stimulus"
                    self.last_RSI = -1
                    if self.eye_tracker is not None:
                        self.current_sampling_window = self.settings.instruction_fixation_threshold
                        self.gaze_data_list.clear()

                if self.settings.experiment_type == 'reaction-time':
                    self.person_data.flush_RT_data_to_output(self)
                else:
                    # stop registering more eye-tracking data
                    self.eye_tracker.unsubscribe_from(tobii.EYETRACKER_GAZE_DATA, self.eye_data_callback)
                    self.person_data.flush_ET_data_to_output(self)
                    # continue eye-tracking
                    self.eye_tracker.subscribe_to(tobii.EYETRACKER_GAZE_DATA, self.eye_data_callback, as_dictionary=True)

                if self.project_ET_zero:
                    validation_block = self.stimblock[self.last_N - 1] == 0
                    if validation_block:
                        whatnow = self.show_feedback_ET_validation(RT_all_list, N == self.end_at[N - 1])
                        if whatnow == 'quit':
                            index = self.settings.get_block_starts().index(N)
                            self.last_N = self.settings.get_block_starts()[index - 1] - 1
                    self.person_data.save_person_settings(self)
                    if not validation_block:
                        whatnow = self.show_feedback_ET(RT_all_list, N == self.end_at[N - 1])

                else:  # keep original code
                    self.person_data.save_person_settings(self)
                    if self.settings.experiment_type == 'reaction-time':
                        whatnow = self.show_feedback_RT(N, number_of_patterns, patternERR, responses_in_block,
                                                        accs_in_block, RT_all_list, RT_pattern_list)
                    else:
                        whatnow = self.show_feedback_ET(RT_all_list, N == self.end_at[N - 1])

                if whatnow == 'quit':
                    if N >= 1:
                        with self.shared_data_lock:
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
                # stop recoring gaze data
                if self.eye_tracker is not None:
                    self.eye_tracker.unsubscribe_from(tobii.EYETRACKER_GAZE_DATA, self.eye_data_callback)
                break

    def jacobi_ET_presentation(self):
        """Doing jacobi method for checking the implicit learning."""

        # It's meant to be used only for implicit experiments.
        assert('explicit' not in self.settings.asrt_types.values())

        # init presented objects
        stimR = visual.Circle(win=self.mywindow, radius=self.settings.asrt_size, units="cm",
                              fillColor=self.colors['stimr'], lineColor=self.colors['linecolor'], pos=self.dict_pos[1])
        stimbg = visual.Circle(win=self.mywindow, radius=self.settings.asrt_size, units="cm",
                               fillColor=None, lineColor=self.colors['linecolor'])

        # place the fixation cross to the bottom-right corner of the screen
        aspect_ratio = self.mymonitor.getSizePix()[1] / self.mymonitor.getSizePix()[0]
        monitor_width_cm = self.settings.monitor_width
        monitor_height_cm = monitor_width_cm * aspect_ratio
        self.fixation_cross_pos = (monitor_width_cm / 2 - 3, -(monitor_height_cm / 2 - 3))
        self.fixation_cross = visual.TextStim(win=self.mywindow, text="+", height=3, units="cm", color='black', pos=self.fixation_cross_pos)

        # start recording gaze data
        self.jacobi_run = 0
        self.jacobi_trial = 0
        self.jacobi_trial_phase = 'none'
        self.jacobi_test_phase = 'none'
        self.person_data.output_data_buffer.clear()
        self.person_data.jacobi_output_data_buffer.clear()
        self.current_sampling_window = self.settings.instruction_fixation_threshold
        self.eye_tracker.subscribe_to(tobii.EYETRACKER_GAZE_DATA, self.eye_data_callback_jacobi, as_dictionary=True)

        # show initial message
        jacobi_inst = "A következőkben az lesz a feladatot, hogy a tekinteteddel jelöld ki az egyes köröket.\n\n"
        jacobi_inst += "Egy kör kékre vált, ha sikerült kijelölni.\n\n"
        jacobi_inst += "Ha egy üres helyre nézel a kijelölés törlődik, így kétszer egymás után ki tudod jelülni ugyanazt a kört.\n\n"
        jacobi_inst += "A gyakorlás megkezdéséhez néz a keresztre!\n\n"
        self.fixation_cross.draw()
        self.print_to_screen(jacobi_inst)
        self.wait_for_eye_response([self.fixation_cross_pos], self.settings.instruction_fixation_threshold)

        with self.shared_data_lock:
            self.current_sampling_window = self.settings.stim_fixation_threshold
            self.gaze_data_list.clear()

        # first practice (select two circles)
        instruction_text = "Jelöld ki először a bal felső, majd a jobb felső kört!\n\n"
        self.draw_jacobi_screen(instruction_text)
        self.wait_for_eye_response([self.dict_pos[1]], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text, 1)
        core.wait(0.5)
        self.wait_for_leave_pos(self.dict_pos[1], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text)
        self.wait_for_eye_response([self.dict_pos[2]], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text, 2)
        core.wait(2.0)

        # second practice
        instruction_text = "Jelöld ki rendre a bal felső, a jobb felső, a bal alsó, majd a jobb alsó köröket!\n\n"
        self.draw_jacobi_screen(instruction_text)
        self.wait_for_eye_response([self.dict_pos[1]], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text, 1)
        core.wait(0.5)
        self.wait_for_leave_pos(self.dict_pos[1], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text)
        self.wait_for_eye_response([self.dict_pos[2]], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text, 2)
        core.wait(0.5)
        self.wait_for_leave_pos(self.dict_pos[2], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text)
        self.wait_for_eye_response([self.dict_pos[3]], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text, 3)
        core.wait(0.5)
        self.wait_for_leave_pos(self.dict_pos[4], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text)
        self.wait_for_eye_response([self.dict_pos[4]], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text, 4)
        core.wait(2.0)

        # third practice
        instruction_text = "Jelöld ki kétszer a bal felső kört, majd egyszer a jobb felsőt, végül kétszer a bal alsó kört!\n\n"
        self.draw_jacobi_screen(instruction_text)
        self.wait_for_eye_response([self.dict_pos[1]], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text, 1)
        core.wait(0.5)
        self.wait_for_leave_pos(self.dict_pos[1], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text)
        self.wait_for_eye_response([self.dict_pos[1]], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text, 1)
        core.wait(0.5)
        self.wait_for_leave_pos(self.dict_pos[1], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text)
        self.wait_for_eye_response([self.dict_pos[2]], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text, 2)
        core.wait(0.5)
        self.wait_for_leave_pos(self.dict_pos[2], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text)
        self.wait_for_eye_response([self.dict_pos[3]], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text, 3)
        core.wait(0.5)
        self.wait_for_leave_pos(self.dict_pos[3], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text)
        self.wait_for_eye_response([self.dict_pos[3]], self.settings.stim_fixation_threshold)
        self.draw_jacobi_screen(instruction_text, 3)
        core.wait(2.0)

        with self.shared_data_lock:
            self.current_sampling_window = self.settings.instruction_fixation_threshold
            self.gaze_data_list.clear()

        # inclusion test
        jacobi_inst = "Vége a gyakorlásnak.\n\n"
        jacobi_inst += "A következő feladat az lesz, hogy próbáld meg olyan sorrendben kijelölni a köröket, amely sorrendben a kísérlet első felében megjelentek.\n\n"
        jacobi_inst += "A feladat elkezdéséhez néz a keresztre!\n\n"
        self.fixation_cross.draw()
        self.print_to_screen(jacobi_inst)
        self.wait_for_eye_response([self.fixation_cross_pos], self.settings.instruction_fixation_threshold)

        self.jacobi_test_phase = 'inclusion'
        self.run_jacobi_test()

        # exclusion test
        jacobi_warn = "FIGYELEM! Most változik a feladatot!\n\n"
        warningtext = visual.TextStim(self.mywindow, text=jacobi_warn, units="cm", height=0.8, wrapWidth=20, color="red", pos=(0, 4))
        warningtext.draw()

        with self.shared_data_lock:
            self.current_sampling_window = self.settings.instruction_fixation_threshold
            self.gaze_data_list.clear()
        jacobi_inst = "Az előzőekhez képest most az lesz a feladatot, hogy MÁS sorrendben jelöld ki a köröket, amely sorrendben a kísérlet első felében megjelentek.\n\n"
        jacobi_inst += "A feladat elkezdéséhez néz a keresztre!\n\n"
        self.fixation_cross.draw()
        self.print_to_screen(jacobi_inst)
        self.wait_for_eye_response([self.fixation_cross_pos], self.settings.instruction_fixation_threshold)

        self.jacobi_test_phase = 'exclusion'
        self.run_jacobi_test()

        # stop registering more eye-tracking data
        self.eye_tracker.unsubscribe_from(tobii.EYETRACKER_GAZE_DATA, self.eye_data_callback_jacobi)
        self.person_data.flush_jacobi_data_to_output(self)
        self.person_data.flush_jacobi_ET_data_to_output(self)

    def draw_jacobi_screen(self, text='', active_stimulus=-1):
        assert(active_stimulus == -1 or active_stimulus in range(1, 5))

        ypos = self.settings.asrt_distance / 2.0 + 3.0
        if text != '':
            instruction = visual.TextStim(self.mywindow, text=text, units='cm', height=0.8, wrapWidth=20, color='black', pos=(0, ypos))
            instruction.draw()

        stimbg = visual.Circle(win=self.mywindow, radius=self.settings.asrt_size, units="cm",
                               fillColor=None, lineColor=self.colors['linecolor'])
        self.stim_bg(stimbg)

        if active_stimulus != -1:
            stim_circle = visual.Circle(win=self.mywindow, radius=self.settings.asrt_size, units="cm",
                                        fillColor=self.colors['stimr'], lineColor=self.colors['linecolor'], pos=self.dict_pos[active_stimulus])
            stim_circle.draw()

        self.mywindow.flip()

    def run_jacobi_test(self):
        with self.shared_data_lock:
            self.current_sampling_window = self.settings.stim_fixation_threshold
            self.gaze_data_list.clear()
        eye_pos_list = [self.dict_pos[1], self.dict_pos[2], self.dict_pos[3], self.dict_pos[4]]
        run_count = 4

        for j in range(run_count):
            run_size = 24
            for i in range(run_size):
                self.draw_jacobi_screen()
                with self.shared_data_lock:
                    self.jacobi_run = j + 1
                    self.jacobi_trial = i + 1
                    self.jacobi_trial_phase = "before_reaction"

                response = self.wait_for_eye_response(eye_pos_list, self.settings.stim_fixation_threshold)
                self.draw_jacobi_screen("", response)

                with self.shared_data_lock:
                    self.jacobi_trial_phase = "after_reaction"

                self.person_data.jacobi_output_data_buffer.append([self.jacobi_test_phase, self.jacobi_run, self.jacobi_trial, response])

                core.wait(0.5)
                self.wait_for_leave_pos(self.dict_pos[response], self.settings.stim_fixation_threshold)

                with self.shared_data_lock:
                    self.jacobi_trial_phase = "after_AOI_left"

            # end of run
            if j < run_count - 1:
                jacobi_inst = "Most pihenhetsz egy kicsit.\n\n"
                self.print_to_screen(jacobi_inst)

                with self.shared_data_lock:
                    self.current_sampling_window = self.settings.instruction_fixation_threshold
                    self.gaze_data_list.clear()

                core.wait(5.0)

                jacobi_inst = "A feladat folytatásához néz a keresztre!\n\n"
                self.fixation_cross.draw()
                self.print_to_screen(jacobi_inst)
                self.wait_for_eye_response([self.fixation_cross_pos], self.settings.instruction_fixation_threshold)

                with self.shared_data_lock:
                    self.current_sampling_window = self.settings.stim_fixation_threshold
                    self.gaze_data_list.clear()

    def wait_for_leave_pos(self, expected_eye_pos, fixation_threshold):

        while (True):
            if 'q' in event.getKeys():
                if self.main_loop_lock.locked():
                    self.main_loop_lock.release()
                return -1

            self.main_loop_lock.acquire()

            with self.shared_data_lock:
                if len(self.gaze_data_list) < fixation_threshold:
                    continue

                count = 0
                invalid_count = 0
                outside_eye_pos = True
                for i in range(len(self.gaze_data_list)):
                    pos_x = self.gaze_data_list[i][0]
                    pos_y = self.gaze_data_list[i][1]

                    # We interpolate the invalid data lineary
                    if pos_x == None or pos_y == None:
                        invalid_count += 1
                        interpolated_data = self.linear_interpolation(self.gaze_data_list, i)
                        if interpolated_data == None:
                            break
                        else:
                            pos_x = interpolated_data[0]
                            pos_y = interpolated_data[1]

                    if pos_x != None and pos_y != None:
                        count += 1
                        pos_norm = (pos_x, pos_y)
                        pos_cm = self.ADCS_to_PCMCS(pos_norm)
                        if self.point_is_in_rectangle(pos_cm, expected_eye_pos, self.settings.AOI_size):
                            outside_eye_pos = False

                    if count >= fixation_threshold:
                        break

                    if invalid_count > fixation_threshold * 0.334:
                        break

                # We have too many invalid data (we allow maximum 33.3333% to be invalid)
                if invalid_count > fixation_threshold * 0.334:
                    continue

                # Do we have engough data for a decision?
                if count == fixation_threshold and outside_eye_pos:
                    if self.main_loop_lock.locked():
                        self.main_loop_lock.release()
                    return 1

    def run(self, full_screen=True, mouse_visible=False, window_gammaErrorPolicy='raise'):
        ensure_dir(os.path.join(self.workdir_path, "logs"))
        ensure_dir(os.path.join(self.workdir_path, "settings"))
        ensure_dir(os.path.join(self.workdir_path, "subject_settings"))

        # load experiment settings if exist or ask the user to specify them
        all_settings_file_path = os.path.join(self.workdir_path, "settings", "settings")
        reminder_file_path = os.path.join(self.workdir_path, "settings", "settings_reminder.txt")
        self.settings = ExperimentSettings(all_settings_file_path, reminder_file_path, self.project_ET_zero)
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
            self.dict_pos = {1: (float(self.settings.asrt_distance) * (-0.5), float(self.settings.asrt_distance) * 0.5),
                             2: (float(self.settings.asrt_distance) * 0.5, float(self.settings.asrt_distance) * 0.5),
                             3: (float(self.settings.asrt_distance) * (-0.5), float(self.settings.asrt_distance) * (-0.5)),
                             4: (float(self.settings.asrt_distance) * 0.5, float(self.settings.asrt_distance) * (-0.5))}

        # read instruction strings
        inst_feedback_path = os.path.join(self.workdir_path, "inst_and_feedback.txt")
        self.instructions = InstructionHelper(inst_feedback_path)
        self.instructions.read_insts_from_file()
        self.instructions.validate_instructions(self.settings)

        # find out the current subject
        self.participant_id()

        # init window
        self.monitor_settings()
        with visual.Window(size=self.mymonitor.getSizePix(), color=self.colors['wincolor'], fullscr=full_screen,
                           monitor=self.mymonitor, units="cm", gammaErrorPolicy=window_gammaErrorPolicy) as self.mywindow:
            self.mywindow.mouseVisible = mouse_visible

            # call explicit activate here to make sure the exp window has the focus.
            self.mywindow.winHandle.activate()

            # init eye-tracker if needed
            if self.settings.experiment_type == 'eye-tracking':
                self.init_eyetracker()

            # check frame rate
            self.frame_check()

            if self.last_N + 1 <= self.settings.get_maxtrial():
                # show experiment screen
                self.presentation()

                # save user data
                self.person_data.save_person_settings(self)
                self.person_data.append_to_output_file('sessionend_planned_quit')
            else:
                self.jacobi_ET_presentation()

            # show ending screen
            self.instructions.show_ending(self)

if __name__ == "__main__":
    thispath = os.path.split(os.path.abspath(__file__))[0]
    experiment = Experiment(thispath, True)
    experiment.run()
