
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

##!/usr/bin/env python
# -*- coding: utf-8 -*-


from psychopy import visual, core, event, gui, monitors, sound, prefs
import shelve, random, codecs, os, time, matplotlib
import pyglet

from os import listdir
from os.path import isfile, join
import numbers

# This class handles all operation related to experiment settings
# These settings apply to all subjects in the specific experiment
class ExperimentSettings:

    def __init__(self, settings_file_path, reminder_file_path):
        self.numsessions = None         # number of sessions (e.g. 10)
        self.groups = None              # list of group names (e.g. ["kontrol", "kiserleti"])

        self.blockprepN = None          # number of practice trials at the beginning of the block (e.g. 10)
        self.blocklengthN = None        # number of trials in one block (e.g. 10)
        self.block_in_epochN = None     # number of blocks in one epoch (e.g. 10)
        self.epochN = None              # number of all epoch in all sessions (e.g. 12)
        self.epochs = None              # list of epoch numbers of all sessions (e.g. [1, 2] (two sessions, first session has 1 epoch, the second has 2))
        self.asrt_types = None          # list of asrt types of all sessions (e.g. ['implicit', 'explicit'] (two sessions, first session is an implicit asrt, the second one is explicit))

        self.monitor_width = None       # monitor's physical with in 'cm' (e.g. 29)
        self.computer_name = None       # am imaginary name of the computer where the experiment is run
        self.asrt_distance = None
        self.asrt_size = None
        self.asrt_rcolor = None
        self.asrt_pcolor = None
        self.asrt_background = None
        self.RSI_time = None

        self.key1 = None                # key for the first stimulus (e.g. 'z')
        self.key2 = None                # key for the second stimulus (e.g. 'v')
        self.key3 = None                # key for the third stimulus (e.g. 'b')
        self.key4 = None                # key for the fourth stimulus (e.g. 'm')
        self.key_quit = None            # key used to quit the running script (e.g. 'q')
        self.whether_warning = None     # whether display any feedback about speed and accuracy (e.g. True)
        self.speed_warning = None       # an accuracy value, warn if the current accuracy is bigger than this value (e.g. 93)
        self.acc_warning = None         # an accuracy value, warn if the current accuracy is smaller than this value (e.g. 91)

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
                self.blocklengthN= settings_file['blocklengthN']
                self.block_in_epochN= settings_file['block_in_epochN']
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
        with codecs.open(self.reminder_file_path,'w', encoding = 'utf-8') as reminder_file:
            reminder_file.write(u'Beállítások \n'+
                                '\n'+
                                'Monitor Width: '+ '\t'+ str(self.monitor_width).replace('.',',')+'\n'+
                                'Computer Name: '+ '\t'+ self.computer_name+'\n'+
                                'Response keys: '+ '\t'+ self.key1+', '+ self.key2+', '+ self.key3+', '+ self.key4+'.'+'\n'+
                                'Quit key: '+ '\t'+ self.key_quit +'\n'+
                                'Warning (speed, accuracy): '+ '\t'+ str(self.whether_warning)+'\n'+
                                'Speed warning at:'+ '\t'+ str(self.speed_warning)+'\n'+
                                'Acc warning at:'+ '\t'+ str(self.acc_warning)+'\n'+
                                'Groups:'+ '\t'+ str(self.groups)[1:-1].replace("u'", '').replace("'", '')+'\n'+
                                'Sessions:'+ '\t'+ str(self.numsessions)+'\n'+
                                'Epochs in sessions:'+ '\t'+ str(self.epochs)[1:-1].replace("u'", '').replace("'", '')+'\n'+
                                'Blocks in epochs:'+ '\t'+ str(self.block_in_epochN)+'\n'+
                                'Preparatory Trials\\Block:'+ '\t'+ str(self.blockprepN)+'\n'+
                                'Trials\\Block:'+ '\t'+ str(self.blocklengthN)+'\n'+
                                'RSI:'+ '\t'+ str(self.RSI_time).replace('.',',')+'\n'+
                                'Asrt stim distance:'+ '\t'+ str(self.asrt_distance)+'\n'+
                                'Asrt stim size:'+ '\t'+ str(self.asrt_size)+'\n'+
                                'Asrt stim color (implicit):'+ '\t'+ self.asrt_rcolor+'\n'+
                                'Asrt stim color (explicit, cued):'+ '\t'+ self.asrt_pcolor+'\n'+
                                'Background color:'+ '\t'+ self.asrt_background+'\n'+
                                '\n'+
                                'Az alábbi beállítások minden személyre érvényesek és irányadóak\n\n'+

                                'A beállítások azokra a kísérletekre vonatkoznak, amelyeket ebből a mappából,\n'+
                                'az itt található scripttel indítottak. Ha más beállításokat (is) szeretnél alkalmazni,\n'+
                                'úgy az asrt.py és az instrukciókat tartalmazó .txt fájlt másold át egy másik könyvtárba is,\n'+
                                'és annak a scriptnek az indításakor megadhatod a kívánt másmilyen beállításokat.\n\n'+

                                'Figyelj rá, hogy mindig abból a könyvtárból indítsd a scriptet, ahol a számodra megfelelő\n'+
                                'beállítások vannak elmentve.\n\n'+

                                'A settings.dat fájl kitörlésével a beállítások megváltoztathatóak; ugyanakkor a fájl\n'+
                                'törlése a későbbi átláthatóság miatt nem javasolt. Ha mégis a törlés mellett döntenél,\n'+
                                'jelen .txt fájlt előtte másold, hogy a korábbi beállításokra is emlékezhess, ha szükséges lesz.\n')

    def get_maxtrial(self):
        return (self.blockprepN + self.blocklengthN) * self.epochN * self.block_in_epochN

    def get_block_starts(self):
        if self.blockstarts == None:
            self.blockstarts = [1]
            for i in range(1, self.epochN * self.block_in_epochN + 2):
                self.blockstarts.append(i * (self.blocklengthN + self.blockprepN) + 1)

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
                self.sessionstarts.append(e * self.block_in_epochN * (self.blocklengthN + self.blockprepN) + 1)

        return self.sessionstarts

# Class for handle instruction strings (reading from file, storing and displaying)
class InstructionHelper:

    def __init__(self, instructions_file_path):
        self.insts = []                 # instructions in the beginning of the experiment
        self.feedback_exp = []          # feedback for the subject about speed and accuracy in the explicit asrt case
        self.feedback_imp = []          # feedback for the subject about speed and accuracy in the explicit asrt case
        self.feedback_speed = []        # speed feedback line embedded into feedback_imp / feedback_exp
        self.feedback_accuracy = []     # accuracy feedback line embedded into feedback_imp / feedback_exp
        self.ending = []                # message in the end of the experiment
        self.unexp_quit = []            # shown message when continuing sessions after the previous data recoding was quited

        self.instructions_file_path = instructions_file_path

    # Be aware of that line endings are preserved during reading instructions
    def read_insts_from_file(self):
        try:
            with codecs.open(self.instructions_file_path, 'r', encoding = 'utf-8') as inst_feedback:
                all_inst_feedback = inst_feedback.read().split('***')
        except:
            all_inst_feedback=[]

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

    # Display given string in the given window
    def __print_to_screen(self, mytext, mywindow):
        text_stim = visual.TextStim(mywindow, text = mytext, units = 'cm', height = 0.6, color = 'black')
        text_stim.draw()

    # Display simple instructions on the screen
    def __show_message(self, instruction_list, mywindow, expriment_settings):
        # There can be more instructions to display successively
        for inst in instruction_list:
            self.__print_to_screen(inst, mywindow)
            mywindow.flip()
            tempkey = event.waitKeys(keyList= [expriment_settings.key1, expriment_settings.key2, expriment_settings.key3, expriment_settings.key4, expriment_settings.key_quit])
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
            tempkey = event.waitKeys(keyList= [expriment_settings.key1, expriment_settings.key2, expriment_settings.key3, expriment_settings.key4, expriment_settings.key_quit])
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
            tempkey = event.waitKeys(keyList= [expriment_settings.key1, expriment_settings.key2, expriment_settings.key3, expriment_settings.key4, expriment_settings.key_quit])
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

    def load_person_settings(self):
        try:
            with shelve.open(self.all_settings_file_path, 'r') as this_person_settings:

                PCodes = this_person_settings['PCodes']
                stim_output_line = this_person_settings['stim_output_line']

                stim_sessionN = this_person_settings['stim_sessionN']
                stimepoch = this_person_settings['stimepoch']
                stimblock = this_person_settings['stimblock']
                stimtrial = this_person_settings['stimtrial']

                stimlist = this_person_settings['stimlist']
                stimpr = this_person_settings['stimpr']
                last_N = this_person_settings['last_N']
                end_at = this_person_settings['end_at']

                stim_colorN = this_person_settings['stim_colorN']
        except:
            PCodes = {}
            stim_output_line = 0
            stim_sessionN = {}
            stimepoch = {}
            stimblock = {}
            stimtrial = {}
            stimlist = {}
            stimpr = {}
            last_N = 0
            end_at = {}
            stim_colorN = {}

        return PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, last_N, end_at, stim_colorN

    def save_person_settings(self, PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, last_N, end_at, stim_colorN):
        with shelve.open(self.all_settings_file_path, 'n') as this_person_settings:
            this_person_settings[ 'PCodes' ] = PCodes
            this_person_settings[ 'stim_output_line' ] = stim_output_line

            this_person_settings[ 'stim_sessionN' ] = stim_sessionN
            this_person_settings[ 'stimepoch' ] = stimepoch
            this_person_settings[ 'stimblock' ] = stimblock
            this_person_settings[ 'stimtrial' ] = stimtrial

            this_person_settings[ 'stimlist' ] = stimlist
            this_person_settings[ 'stimpr' ] = stimpr
            this_person_settings[ 'last_N' ] = last_N
            this_person_settings[ 'end_at' ] = end_at
            this_person_settings[ 'stim_colorN' ] = stim_colorN

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

        with codecs.open(self.subject_list_file_path, 'w', encoding = 'utf-8') as subject_list_file:
            for id in all_IDs:
                id_segmented = id.replace('_', '\t', 2)
                subject_list_file.write(id_segmented)
                subject_list_file.write('\n')

    def append_to_output_file(self, string_to_append):
        if not os.path.isfile(self.output_file_path):
            with codecs.open(self.output_file_path, 'w', encoding = 'utf-8') as output_file:
                self.add_heading_to_output(output_file)
                output_file.write(string_to_append)
        else:
            with codecs.open(self.output_file_path, 'a+', encoding = 'utf-8') as output_file:
                output_file.write(string_to_append)

    def write_data_to_output(self, computer_name, group, identif, subject_nr, asrt_type, PCode, stim_output_line,
                             session, epoch, block, trial, stim_RSI, frame_rate, frame_time, frame_sd, stim_RT_time,
                             stim_RT_date, stim_color, stimpr, stimRT, stimACC, stimulus, stimbutton):
        output_data = [ computer_name,
                        group,
                        identif,
                        subject_nr,
                        asrt_type,
                        PCode,

                        stim_output_line,

                        session,
                        epoch,
                        block,
                        trial,

                        stim_RSI,
                        frame_rate,
                        frame_time,
                        frame_sd,
                        stim_RT_time,
                        stim_RT_date,

                        stim_color,
                        stimpr,
                        stimRT,
                        stimACC,

                        stimulus,
                        stimbutton]
        output = "\n"
        for data in output_data:
            if isinstance(data, numbers.Number):
                data = str(data)
                data = data.replace('.',',')
            else:
                data = str(data)
            output += data + '\t'
        self.append_to_output_file(output)

    def add_heading_to_output(self, output_file):
        heading_list = [ 'computer_name',
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

def ensure_dir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

### Settings dialogs

# Ask the user to specify the number of groups and the number of sessions
def show_basic_settings_dialog(expriment_settings):
    settings_dialog = gui.Dlg(title=u'Beállítások')
    settings_dialog.addText(u'Még nincsenek beállítások mentve ehhez a kísérlethez...')
    settings_dialog.addText(u'A logfile optimalizálása érdekében kérjük add meg, hányféle csoporttal tervezed az adatfelvételt.')
    settings_dialog.addField(u'Kiserleti + Kontrollcsoportok szama osszesen', 2)
    settings_dialog.addText(u'Hány ülés (session) lesz a kísérletben?')
    settings_dialog.addField(u'Ulesek szama', 2)
    returned_data = settings_dialog.show()
    if settings_dialog.OK:
        expriment_settings.numsessions = returned_data[1]
        return returned_data[0]
    else:
        core.quit()

# Ask the user to specify the name of the groups
# Returns the list of group names
def show_group_settings_dialog(numgroups, dict_accents, expriment_settings):

    if numgroups>1:
        expriment_settings.groups = []
        settings_dialog = gui.Dlg(title=u'Beállítások')
        settings_dialog.addText(u'A csoportok megnevezése a következő (pl. kísérleti, kontroll, ....) ')
        for i in range(numgroups):
            settings_dialog.addField(u'Csoport '+str(i+1))
        returned_data = settings_dialog.show()
        if settings_dialog.OK:
            for ii in returned_data:
                ii = ii.lower()
                ii = ii.replace(' ', '_')
                ii = ii.replace('-', '_')
                for accent in dict_accents.keys():
                    ii = ii.replace(accent, dict_accents[accent])
                expriment_settings.groups.append(ii)
        else:
            core.quit()
    else:
        expriment_settings.groups = ['nincsenek csoportok']

# Ask the user to specify preparation trials' number, block length, number of blocks in an epoch
# epoch number and asrt type in the different sessions
def show_epoch_and_block_settings_dialog(expriment_settings):
    settings_dialog = gui.Dlg(title=u'Beállítások')
    settings_dialog.addText(u'Kísérlet felépítése ')
    settings_dialog.addField(u'Randomok gyakorlaskent a blokk elejen (ennyi db):', 5)
    settings_dialog.addField(u'Eles probak a blokkban:', 80)
    settings_dialog.addField(u'Blokkok szama egy epochban:', 5)
    for i in range(expriment_settings.numsessions):
        settings_dialog.addField(u'Session '+str(i+1)+u' epochok szama', 5)
    for i in range(expriment_settings.numsessions):
        settings_dialog.addField(u'Session '+str(i+1)+u' ASRT tipusa', choices=["implicit", "explicit", "noASRT"])
    returned_data = settings_dialog.show()
    if settings_dialog.OK:
        expriment_settings.blockprepN = returned_data[0]
        expriment_settings.blocklengthN = returned_data[1]
        expriment_settings.block_in_epochN = returned_data[2]
        expriment_settings.epochN = 0
        expriment_settings.epochs = []
        expriment_settings.asrt_types = {}
        for k in range(expriment_settings.numsessions):
            expriment_settings.epochN += returned_data[3+k]
            expriment_settings.epochs.append(returned_data[3+k])
        for k in range(expriment_settings.numsessions):
            expriment_settings.asrt_types[k+1] = returned_data[3+expriment_settings.numsessions+k]
    else:
        core.quit()

# Ask the user specific infromation about the computer
# and also change display settings
def show_computer_and_display_settings_dialog(possible_colors, expriment_settings):
    settings_dialog = gui.Dlg(title=u'Beállítások')
    settings_dialog.addText(u'A számítógépről...')
    settings_dialog.addField(u'Hasznos kepernyo szelessege (cm)', 34.2)
    settings_dialog.addField(u'Szamitogep fantazianeve (ekezet nelkul)', u'Laposka')
    settings_dialog.addText(u'Megjelenés..')
    settings_dialog.addField(u'Ingerek tavolsaga (kozeppontok kozott) (cm)', 3)
    settings_dialog.addField(u'Ingerek sugara (cm)', 1)
    settings_dialog.addField(u'ASRT inger szine (elsodleges, R)', choices = possible_colors, initial = "Orange")
    settings_dialog.addField(u'ASRT inger szine (masodlagos, P, explicit asrtnel)', choices = possible_colors, initial = "Green")
    settings_dialog.addField(u'Hatter szine', choices = possible_colors, initial = "Ivory")
    settings_dialog.addField(u'RSI (ms)', 120)
    returned_data = settings_dialog.show()
    if settings_dialog.OK:
        expriment_settings.monitor_width = returned_data[0]
        expriment_settings.computer_name = returned_data[1]
        expriment_settings.asrt_distance = returned_data[2]
        expriment_settings.asrt_size = returned_data[3]
        expriment_settings.asrt_rcolor = returned_data[4]
        expriment_settings.asrt_pcolor = returned_data[5]
        expriment_settings.asrt_background = returned_data[6]
        expriment_settings.RSI_time = float(returned_data[7])/1000
    else:
        core.quit()

# Ask the user to specify the keys used during the experiement
# and also set options related to the displayed feedback.
def show_key_and_feedback_settings_dialog(expriment_settings):
    settings_dialog = gui.Dlg(title=u'Beállítások')
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
        expriment_settings.key1 = returned_data[0]
        expriment_settings.key2 = returned_data[1]
        expriment_settings.key3 = returned_data[2]
        expriment_settings.key4 = returned_data[3]
        expriment_settings.key_quit = returned_data[4]
        expriment_settings.whether_warning = returned_data[5]
        expriment_settings.speed_warning = returned_data[6]
        expriment_settings.acc_warning = returned_data[7]
    else:
        core.quit()

# Ask the user to specify the subject's attributes (name, subject number, group)
def show_subject_settings_dialog(groups, dict_accents):
    warningtext = ''
    itsOK = False
    while not itsOK:
        settings_dialog = gui.Dlg(title=u'Beállítások')
        settings_dialog.addText('')
        settings_dialog.addText(warningtext, color='Red')
        settings_dialog.addField(u'Nev', u"Alattomos Aladar")
        settings_dialog.addField(u'Sorszam', "0")
        if len(groups) > 1:
            settings_dialog.addField(u'Csoport', choices = groups)

        returned_data = settings_dialog.show()
        if settings_dialog.OK:
            name = returned_data[0]
            name = name.lower()
            name = name.replace(' ', '-')
            name = name.replace('_', '-')
            for accent in dict_accents.keys():
                name = name.replace(accent, dict_accents[accent])

            subject_number = returned_data[1]
            if len(groups) > 1:
                group = returned_data[2]
            else:
                group = ""

            try:
                subject_number = int(subject_number)
                if subject_number >= 0:
                    itsOK = 1
                else:
                    warningtext = u'Pozitív egész számot adj meg a sorszámhoz!'

            except:
                warningtext = u'Pozitív egész számot adj meg a sorszámhoz!'

        else:
            core.quit()

    subject_settings = {
        "identif" : name,
        "subject_nr" : subject_number,
        "group" : group
    }
    return subject_settings

def show_subject_PCodes_dialog(experiment_settings):
    settings_dialog = gui.Dlg(title=u'Beállítások')
    settings_dialog.addText('')
    for z in range(experiment_settings.numsessions):
        if experiment_settings.asrt_types[z+1] == "noASRT":
            settings_dialog.addFixedField(u'Session ' + str(z+1) + ' PCode', 'noPattern')
        else:
            settings_dialog.addField(u'Session ' + str(z+1) + ' PCode', choices = ['1st - 1234' , '2nd - 1243', '3rd - 1324', '4th - 1342', '5th - 1423', '6th - 1432'])

    returned_data = settings_dialog.show()
    if settings_dialog.OK:
        PCodes = {}

        for zz in range(experiment_settings.numsessions):
            PCodes[zz+1] = returned_data[zz]

        return PCodes
    else:
        core.quit()

def show_subject_continuation_dialog(stim_sessionN, stimepoch, stimblock, stimtrial, last_N, experiment_settings):
    if last_N + 1 <= experiment_settings.get_maxtrial():
        expstart11=gui.Dlg(title=u'Feladat indítása...')
        expstart11.addText(u'A személy adatait beolvastam.')
        expstart11.addText(u'Folytatás innen...')
        expstart11.addText('Session: '+ str(stim_sessionN[last_N + 1]))
        expstart11.addText('Epoch: '+str(stimepoch[last_N + 1]))
        expstart11.addText('Block: '+str(stimblock[last_N + 1]))
        expstart11.addText('Trial: '+str(stimtrial[last_N + 1]))
        expstart11.show()
        if not expstart11.OK:
            core.quit()
    else:
        expstart11=gui.Dlg(title=u'Feladat indítása...')
        expstart11.addText(u'A személy adatait beolvastam.')
        expstart11.addText(u'A személy végigcsinálta a feladatot.')
        expstart11.show()
        core.quit()

def all_settings_def(experiment_settings, dict_accents):

    try:
        # check whether the settings file is in place
        experiment_settings.read_from_file()

    # if there is no settings file, we ask the user to specfiy the settings
    except:
        possible_colors = ["AliceBlue","AntiqueWhite","Aqua","Aquamarine","Azure","Beige","Bisque","Black","BlanchedAlmond","Blue","BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGrey","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","DarkOrange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkSlateGrey","DarkTurquoise","DarkViolet","DeepPink","DeepSkyBlue","DimGray","DimGrey","DodgerBlue","FireBrick","FloralWhite","ForestGreen","Fuchsia","Gainsboro","GhostWhite","Gold","GoldenRod","Gray","Grey","Green","GreenYellow","HoneyDew","HotPink","IndianRed","Indigo","Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGrey","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray","LightSlateGrey","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen","MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive","OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue","Purple","RebeccaPurple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray","SlateGrey","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","White","WhiteSmoke","Yellow","YellowGreen"]

        # get the number of groups and number of sessions
        numgroups = show_basic_settings_dialog(experiment_settings)

        # get the group names from the user
        show_group_settings_dialog(numgroups, dict_accents, experiment_settings)

        # get epoch and block settings (block number, trial number, epoch number, etc)
        epoch_block_result = show_epoch_and_block_settings_dialog(experiment_settings)
            
        # get montior / computer settings, and also options about displaying (stimulus size, stimulus distance, etc)
        show_computer_and_display_settings_dialog(possible_colors, experiment_settings)

        # get keyboard settings (reaction keys and quit key) and also feedback settings (accuracy and speed feedback, etc)
        show_key_and_feedback_settings_dialog(experiment_settings)

        # save the settings sepcifed by the user in the different dialogs
        experiment_settings.write_to_file()

        # write out a text file with the experiment settings data, so the user can check settings in a human readable form
        experiment_settings.write_out_reminder()

def which_code(session_number, PCodes):
    pcode_raw = PCodes[session_number]
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

def calculate_stim_properties(stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, experiment_settings):
    all_trial_Nr = 0
    block_num = 0

    sessionsstarts = experiment_settings.get_session_starts()
    for trial_num in range(1, experiment_settings.get_maxtrial()+1):
        for session_num in range(1, len(sessionsstarts)):
            if trial_num >= sessionsstarts[session_num-1] and trial_num < sessionsstarts[session_num]:
                stim_sessionN[trial_num] = session_num
                end_at[trial_num] = sessionsstarts[session_num]

    for epoch in range(1,experiment_settings.epochN+1):

        for block in range(1, experiment_settings.block_in_epochN+1):
            block_num += 1
            current_trial_num = 0

            # practice
            for practice in range(1, experiment_settings.blockprepN+1):
                current_trial_num += 1

                all_trial_Nr += 1
                asrt_type = experiment_settings.asrt_types[stim_sessionN[all_trial_Nr]]

                current_stim = random.choice([1,2,3,4])
                stimlist[all_trial_Nr] = current_stim
                stimpr[all_trial_Nr] = "R"
                stim_colorN[all_trial_Nr] = experiment_settings.asrt_rcolor
                stimtrial[all_trial_Nr] = current_trial_num
                stimblock[all_trial_Nr] = block_num
                stimepoch[all_trial_Nr] = epoch

            # real
            for real in range(1, experiment_settings.blocklengthN+1):

                current_trial_num += 1
                all_trial_Nr += 1

                asrt_type = experiment_settings.asrt_types[stim_sessionN[all_trial_Nr]]
                PCode = which_code(stim_sessionN[all_trial_Nr], PCodes)

                dict_HL = {}
                if not PCode == "noPattern":
                    dict_HL[PCode[0]] = PCode[1]
                    dict_HL[PCode[1]] = PCode[2]
                    dict_HL[PCode[2]] = PCode[3]
                    dict_HL[PCode[3]] = PCode[0]

                if experiment_settings.blockprepN%2 == 1:
                    mod_pattern = 0
                else:
                    mod_pattern = 1

                if current_trial_num%2 == mod_pattern and asrt_type != "noASRT":
                    if all_trial_Nr > 2:
                        current_stim = int( dict_HL[ str(stimlist[all_trial_Nr-2]) ] )
                    else:
                        current_stim = random.choice([1,2,3,4]) # first pattern stim is random
                    stimpr[all_trial_Nr] = "P"

                    if asrt_type == 'explicit':
                        stim_colorN[all_trial_Nr] = experiment_settings.asrt_pcolor
                    elif asrt_type == "implicit" or asrt_type == 'noASRT':
                        stim_colorN[all_trial_Nr] = experiment_settings.asrt_rcolor
                else:
                    current_stim = random.choice([1,2,3,4])
                    stim_colorN[all_trial_Nr] = experiment_settings.asrt_rcolor
                    stimpr[all_trial_Nr] = "R"

                stimlist[all_trial_Nr] = current_stim
                stimtrial[all_trial_Nr] = current_trial_num
                stimblock[all_trial_Nr] = block_num
                stimepoch[all_trial_Nr] = epoch

def participant_id(thispath, exp_settings, dict_accents):
    subject_settings = show_subject_settings_dialog(exp_settings.groups, dict_accents)
    identif = subject_settings["identif"]
    subject_nr = subject_settings["subject_nr"]
    group = subject_settings["group"]

    subject_id = identif + '_' + str(subject_nr) + '_' + group
    all_settings_file_path = os.path.join(thispath, "settings", subject_id)
    all_IDs_file_path = os.path.join(thispath, "settings", "participant_settings")
    subject_list_file_path = os.path.join(thispath, "settings", "participants_in_experiment.txt")
    output_file_path =  os.path.join(thispath, "logs", subject_id + '_log.txt')
    person_data_handler = PersonDataHandler(subject_id,  all_settings_file_path, all_IDs_file_path, subject_list_file_path, output_file_path)

    person_data_handler.update_subject_IDs_files()

    PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, last_N, end_at, stim_colorN = person_data_handler.load_person_settings()
        
    if last_N > 0:
        show_subject_continuation_dialog(stim_sessionN, stimepoch, stimblock, stimtrial, last_N, exp_settings)

    else:
        PCodes = show_subject_PCodes_dialog(exp_settings)
            
        calculate_stim_properties(stim_sessionN, end_at, stimepoch, stimblock, stimtrial, stimlist, stim_colorN, stimpr, PCodes, exp_settings)

        person_data_handler.save_person_settings(PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, last_N, end_at, stim_colorN)

    return group, subject_nr, identif, person_data_handler, PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, last_N,  end_at, stim_colorN, stimpr

def monitor_settings():
    screen = pyglet.window.get_platform().get_default_display().get_default_screen()

    ## Monitor beállítása
    my_monitor = monitors.Monitor('myMon')
    my_monitor.setSizePix( [screen.width, screen.height] )
    my_monitor.setWidth(exp_settings.monitor_width) # cm-ben
    my_monitor.saveMon()

    return my_monitor

def print_to_screen(mywindow, mytext):
    xtext = visual.TextStim(mywindow, text = mytext, units = "cm", height = 0.6, color = "black")
    xtext.draw()

def frame_check(mywindow):
    # monitorral kapcsolatos informáciok
    print_to_screen(mywindow, u'Adatok előkészítése folyamatban. \nEz eltarthat pár másodpercig. \nAddig semmit sem fogsz látni a képernyőn...')
    mywindow.flip()
    core.wait(2)

    ms_per_frame = mywindow.getMsPerFrame(nFrames = 120)
    frame_time = ms_per_frame[0]
    frame_sd = ms_per_frame[1]
    frame_rate = mywindow.getActualFrameRate()
    return frame_time, frame_sd, frame_rate
    
def stim_bg():
    stimbg = visual.Circle( win = mywindow, radius = 1, units = "cm", fillColor = None, lineColor = colors['linecolor'])
    for i in range(1,5):
        stimbg.pos = dict_pos[i]
        stimbg.draw()

def show_feedback(number_of_patterns, patternERR, Npressed_in_block, accs_in_block, RT_all_list,
                  RT_pattern_list, stim_sessionN, N, exp_settings, instruction_helper, mywindow):

    try:
        acc_for_the_whole = 100*float( Npressed_in_block - sum(accs_in_block)) / Npressed_in_block
        acc_for_the_whole_str = str(acc_for_the_whole)[0:5].replace('.',',')

    except:
        acc_for_the_whole = 0
        acc_for_the_whole_str = 'N/A'

    try:
        rt_mean = float( sum(RT_all_list)) / len(RT_all_list)
        rt_mean_str = str(rt_mean)[:5].replace('.',',')
    except:
        rt_mean_str = 'N/A'

    if exp_settings.asrt_types[stim_sessionN[N-1]] == 'explicit':

        try:
            rt_mean_p =  float( sum(RT_pattern_list)) / len(RT_pattern_list)
            rt_mean_p_str = str(rt_mean_p)[:5].replace('.',',')
        except:
            rt_mean_p_str = 'N/A'

        try:
            acc_for_patterns = 100*float( number_of_patterns - patternERR) / number_of_patterns
            acc_for_patterns_str = str(acc_for_patterns)[0:5].replace('.',',')
        except:
            acc_for_patterns_str = 'N/A'

        whatnow = instruction_helper.feedback_explicit(rt_mean_str, rt_mean_p_str, acc_for_patterns_str, acc_for_the_whole, acc_for_the_whole_str, mywindow, exp_settings)
    else:
        whatnow = instruction_helper.feedback_implicit(rt_mean_str, acc_for_the_whole, acc_for_the_whole_str, mywindow, exp_settings)

    return whatnow

def presentation():
    global last_N, stim_output_line
	
    # Init circle stimulus
    stimP = visual.Circle( win = mywindow, radius = exp_settings.asrt_size, units = "cm", fillColor = colors['stimp'], lineColor = colors['linecolor'], pos = dict_pos[1])
    stimR = visual.Circle( win = mywindow, radius = exp_settings.asrt_size, units = "cm", fillColor = colors['stimr'], lineColor = colors['linecolor'], pos = dict_pos[1])

    RSI_timer = 0.0
    N = last_N + 1
    
    # Show instructions or continuation message
    if N in exp_settings.get_session_starts():
        instruction_helper.show_instructions(mywindow, exp_settings)
        
    else:
        instruction_helper.show_unexp_quit(mywindow, exp_settings)
    
    Npressed_in_block = 0
    accs_in_block  = []
    
    asrt_type = exp_settings.asrt_types[stim_sessionN[N]]
    PCode = which_code(stim_sessionN[N], PCodes)
    
    allACC = 0
    patternERR = 0
    number_of_patterns = 0
    
    RT_pattern_list = []
    RT_all_list = []

    tempy = []

    RSI = core.StaticPeriod(screenHz=frame_rate)
    RSI_clock = core.Clock()
    trial_clock = core.Clock()

    while True:
                    
        stim_bg()
        mywindow.flip()
        
        RSI_clock.reset()
        RSI.start( exp_settings.RSI_time)
        
        if stimpr[N] == 'P':
            if exp_settings.asrt_types[stim_sessionN[N]] == 'explicit':
                stimP.fillColor =  colors['stimp']
            else:
                stimP.fillColor =  colors['stimr']
            stimP.setPos(dict_pos[stimlist[N]])
        else:
            stimR.setPos(dict_pos[stimlist[N]])
        
        RSI.complete()  
        
        cycle = 0
        allACC = 0
        
        while True:
            cycle += 1
            stim_bg()
            
            if stimpr[N] == 'P':
                stimP.draw()
            else:
                stimR.draw()
            mywindow.flip()
            
            if cycle == 1:
                RSI_timer = RSI_clock.getTime()

            trial_clock.reset()
            press = event.waitKeys(keyList = [exp_settings.key1,exp_settings.key2,exp_settings.key3,exp_settings.key4, exp_settings.key_quit], timeStamped = trial_clock)
            
            stim_RT_time = time.strftime('%H:%M:%S')
            stim_RT_date = time.strftime('%d/%m/%Y')
            stimRT = press[0][1]

            stim_output_line += 1
            Npressed_in_block += 1

            if cycle == 1:
                stim_first_RT = press[0][1]
            
            stimbutton = press [0][0]
            stim_RSI = RSI_timer

            if press[0][0] == exp_settings.key_quit:
                print_to_screen(mywindow, "Quit...\nSaving data...")
                mywindow.flip()

                person_data_handler.append_to_output_file('userquit')

                stim_output_line -= 1
                
                if N>=1:
                    last_N = N-1
                    
                person_data_handler.save_person_settings(PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, last_N, end_at, stim_colorN)
                core.quit() 
            
            elif pressed_dict[press[0][0]] == stimlist[N]:                
                stimACC = 0
                accs_in_block.append(0)

                if stimpr[N] == 'P':
                    number_of_patterns +=1
                    RT_pattern_list.append(stimRT)
                RT_all_list.append(stimRT)
                
            else:
                stimACC = 1
                allACC += 1
                accs_in_block.append(1)

                if stimpr[N] == 'P':
                    patternERR +=1
                    number_of_patterns +=1
                    RT_pattern_list.append(stimRT)
                RT_all_list.append(stimRT)
            stim_allACC  = allACC
            
            person_data_handler.write_data_to_output(exp_settings.computer_name, group, identif, subject_nr, asrt_type, PCode, stim_output_line,
                                                    stim_sessionN[N], stimepoch[N], stimblock[N], stimtrial[N], stim_RSI, frame_rate, frame_time,
                                                    frame_sd, stim_RT_time, stim_RT_date, stim_colorN[N], stimpr[N], stimRT, stimACC, stimlist[N], stimbutton)

            if stimACC== 0:
                last_N = N
                N += 1

                break
            
        if N in exp_settings.get_block_starts(): # n+1 volt
            
            print_to_screen(mywindow, u"Adatok mentése és visszajelzés előkészítése...")
            mywindow.flip()
            
            whatnow = show_feedback(number_of_patterns, patternERR, Npressed_in_block, accs_in_block, RT_all_list,
                                    RT_pattern_list, stim_sessionN, N, exp_settings, instruction_helper, mywindow)

            if whatnow == 'quit':
                print_to_screen(mywindow, "Quit...\nSaving data...")
                mywindow.flip()
                
                person_data_handler.append_to_output_file('userquit')
                
                if N>=1:
                    last_N = N-1
                    
                person_data_handler.save_person_settings(PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, last_N, end_at, stim_colorN)
                core.quit() 
            elif whatnow != 'continue':
                print('wtf')
                
            patternERR = 0
            allACC = 0
            Npressed_in_block = 0
            
            RT_pattern_list = []
            RT_all_list = []
            
            accs_in_block  = []

        if N  == end_at[N-1]:
            break

# some constants and dictionaries

thispath = os.path.split(os.path.abspath(__file__))[0]
dict_accents = {u'á':u'a',u'é':u'e',u'í':u'i',u'ó':u'o',u'ő':u'o',u'ö':u'o',u'ú':u'u',u'ű':u'u',u'ü':u'u'}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# vezerles
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main():
    global colors
    global group, subject_nr, identif
    global PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, last_N, end_at, stim_colorN
    global mywindow, pressed_dict, dict_pos
    global frame_time, frame_sd, frame_rate
    global exp_settings, instruction_helper
    global person_data_handler

    ensure_dir(os.path.join(thispath, "logs"))
    ensure_dir(os.path.join(thispath, "settings"))

    all_settings_file_path = os.path.join(thispath, "settings", "settings")
    reminder_file_path = os.path.join(thispath, "settings", "settings_reminder.txt")
    exp_settings = ExperimentSettings(all_settings_file_path, reminder_file_path)
    all_settings_def(exp_settings, dict_accents)

    my_monitor = monitor_settings()

    colors = { 'wincolor' : exp_settings.asrt_background, 'linecolor':'black', 'stimp':exp_settings.asrt_pcolor, 'stimr':exp_settings.asrt_rcolor}

    inst_feedback_path = os.path.join(thispath, "inst_and_feedback.txt")
    instruction_helper = InstructionHelper(inst_feedback_path)
    instruction_helper.read_insts_from_file()

    group, subject_nr, identif, person_data_handler, PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, last_N,  end_at, stim_colorN, stimpr = participant_id(thispath, exp_settings, dict_accents)

    # Ablak és ingerek felépítése az ismert beállítások szerint
    mywindow = visual.Window (size = my_monitor.getSizePix(), color = colors['wincolor'], fullscr = False, monitor = my_monitor, units = "cm")

    pressed_dict ={exp_settings.key1:1,exp_settings.key2:2,exp_settings.key3:3,exp_settings.key4:4}

    frame_time, frame_sd, frame_rate = frame_check(mywindow)


    dict_pos = { 1:  ( float(exp_settings.asrt_distance)*(-1.5), 0),
                 2:  ( float(exp_settings.asrt_distance)*(-0.5), 0),
                 3:  ( float(exp_settings.asrt_distance)*  0.5,   0),
                 4:  ( float(exp_settings.asrt_distance)*  1.5,   0) }


    presentation()
    person_data_handler.save_person_settings(PCodes, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, last_N, end_at, stim_colorN)

    person_data_handler.append_to_output_file('sessionend_planned_quit')

    instruction_helper.show_ending(mywindow, exp_settings)

if __name__ == "__main__":
    main()

