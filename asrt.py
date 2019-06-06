
#    ASRT script in Psychopy
#    Copyright (C) <2018>  <Emese Szegedi-Hallgató>
#                  <2018>  <Tamás Zolnai>  <zolnaitamas2000@gmail.com>

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

def ensure_dir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

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

# Ask the user to specify preparation trials' number, block length, number of blocks in an epoch
# epoch number and asrt type in the different sessions
def show_epoch_and_block_settings_dialog(numsessions):
    expstart02=gui.Dlg(title=u'Beállítások')
    expstart02.addText(u'Kísérlet felépítése ')
    expstart02.addField(u'Randomok gyakorlaskent a blokk elejen (ennyi db):', 5)
    expstart02.addField(u'Eles probak a blokkban:', 80)
    expstart02.addField(u'Blokkok szama egy epochban:', 5)
    for i in range(numsessions):
        expstart02.addField(u'Session '+str(i+1)+u' epochok szama', 5)
    for ii in range(numsessions):
        expstart02.addField(u'Session '+str(ii+1)+u' ASRT tipusa', choices=["implicit", "explicit", "noASRT"])
    returned_data = expstart02.show()
    if expstart02.OK:
        blockprepN = returned_data[0]
        blocklengthN = returned_data[1]
        block_in_epochN = returned_data[2]
        epochN = 0
        epochs = []
        asrt_types = {}
        for k in range(numsessions):
            epochN += returned_data[3+k]
            epochs.append(returned_data[3+k])
        for k in range(numsessions):
            asrt_types[k+1] = returned_data[3+numsessions+k]
    else:
        core.quit()

    epoch_block_result = {
        "blockprepN" : blockprepN,
        "blocklengthN" : blocklengthN,
        "block_in_epochN" : block_in_epochN,
        "epochN" : epochN,
        "epochs" : epochs,
        "asrt_types" : asrt_types
    }
    return epoch_block_result

# Ask the user specific infromation about the computer
# and also change display settings
def show_computer_and_display_settings_dialog(possible_colors):
    expstart0a=gui.Dlg(title=u'Beállítások')
    expstart0a.addText(u'A számítógépről...')
    expstart0a.addField(u'Hasznos kepernyo szelessege (cm)', 34.2)
    expstart0a.addField(u'Szamitogep fantazianeve (ekezet nelkul)', u'Laposka')
    expstart0a.addField(u'Kepernyofrissitesi frekvencia (Hz)', 60)
    expstart0a.addText(u'Megjelenés..')
    expstart0a.addField(u'Ingerek tavolsaga (kozeppontok kozott) (cm)', 3)
    expstart0a.addField(u'Ingerek sugara (cm)', 1)
    expstart0a.addField(u'ASRT inger szine (elsodleges, R)', choices = possible_colors, initial = "Orange")
    expstart0a.addField(u'ASRT inger szine (masodlagos, P, explicit asrtnel)', choices = possible_colors, initial = "Green")
    expstart0a.addField(u'Hatter szine', choices = possible_colors, initial = "Ivory")
    expstart0a.addField(u'Nem aktiv inger szine', choices = possible_colors, initial = "Beige")
    expstart0a.addField(u'RSI (ms)', 120)
    returned_data = expstart0a.show()
    if expstart0a.OK:
        monitor_width = returned_data[0]
        computer_name = returned_data[1]
        refreshrate = returned_data[2]
        asrt_distance = returned_data[3]
        asrt_size = returned_data[4]
        asrt_rcolor = returned_data[5]
        asrt_pcolor = returned_data[6]
        asrt_background = returned_data[7]
        asrt_circle_background = returned_data[8]
        RSI_time = float(returned_data[9])/1000
    else:
        core.quit()

    screen_and_display_settings = {
        "monitor_width" : monitor_width,
        "computer_name" : computer_name,
        "refreshrate" : refreshrate,
        "asrt_distance" : asrt_distance,
        "asrt_size" : asrt_size,
        "asrt_rcolor" : asrt_rcolor,
        "asrt_pcolor" : asrt_pcolor,
        "asrt_background" : asrt_background,
        "asrt_circle_background" : asrt_circle_background,
        "RSI_time" : RSI_time
    }
    return screen_and_display_settings

# Ask the user to specify the keys used during the experiement
# and also set options related to the displayed feedback.
def show_key_and_feedback_settings_dialog():
    expstart0b=gui.Dlg(title=u'Beállítások')
    expstart0b.addText(u'Válaszbillentyűk')
    expstart0b.addField(u'Bal szelso:', 'y')
    expstart0b.addField(u'Bal kozep', 'c')
    expstart0b.addField(u'Jobb kozep', 'b')
    expstart0b.addField(u'Jobb szelso', 'm')
    expstart0b.addField(u'Kilepes', 'q')
    expstart0b.addField(u'Figyelmeztetes pontossagra/sebessegre:', True)
    expstart0b.addText(u'Ha be van kapcsolva a figyelmeztetés, akkor...:')
    expstart0b.addField(u'Figyelmeztetes sebessegre ezen pontossag felett (%):', 93)
    expstart0b.addField(u'Figyelmeztetes sebessegre ezen pontossag felett (%):', 91)
    returned_data = expstart0b.show()
    if expstart0b.OK:
        key1 = returned_data[0]
        key2 = returned_data[1]
        key3 = returned_data[2]
        key4 = returned_data[3]
        key_quit = returned_data[4]
        whether_warning = returned_data[5]
        speed_warning = returned_data[6]
        acc_warning = returned_data[7]
    else:
        core.quit()

    key_and_feedback_settings = {
        "key1" : key1,
        "key2" : key2,
        "key3" : key3,
        "key4" : key4,
        "key_quit" : key_quit,
        "whether_warning" : whether_warning,
        "speed_warning" : speed_warning,
        "acc_warning" : acc_warning
    }
    return key_and_feedback_settings

# Ask the user to specify the subject's attributes (id, subject number, group)
def show_subject_settings_dialog(groups, dict_accents):
    warningtext = ''
    itsOK = False
    while not itsOK:
        expstart=gui.Dlg(title=u'Beállítások')
        expstart.addText('')
        expstart.addText(warningtext)
        expstart.addField(u'Nev', u"Alattomos Aladar")
        expstart.addField(u'Sorszam', "0")
        if len(groups) > 1:
            expstart.addField(u'Csoport', choices = groups)

        returned_data = expstart.show()
        if expstart.OK:
            name = returned_data[0]
            name = name.lower()
            name = name.replace(' ', '-')
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

def all_settings_def():    
    all_settings_file = shelve.open(thispath+'\\settings\\'+'settings.dat')

    try:
        groups = all_settings_file['groups']
        numsessions = all_settings_file['numsessions'] 
        blockprepN = all_settings_file['blockprepN']
        blocklengthN= all_settings_file['blocklengthN']
        block_in_epochN= all_settings_file['block_in_epochN']
        epochN = all_settings_file['epochN']
        epochs = all_settings_file['epochs']
        monitor_width = all_settings_file['monitor_width']
        computer_name = all_settings_file['computer_name']
        asrt_distance = all_settings_file['asrt_distance']
        asrt_size = all_settings_file['asrt_size']
        asrt_rcolor = all_settings_file['asrt_rcolor']
        asrt_pcolor = all_settings_file['asrt_pcolor']
        asrt_background = all_settings_file['asrt_background']
        asrt_circle_background = all_settings_file['asrt_circle_background']

        refreshrate = all_settings_file['refreshrate']
        key1 = all_settings_file['key1']
        key2 = all_settings_file['key2'] 
        key3 = all_settings_file['key3']
        key4 = all_settings_file['key4'] 
        key_quit = all_settings_file['key_quit']
        whether_warning = all_settings_file['whether_warning'] 
        speed_warning = all_settings_file['speed_warning']
        acc_warning = all_settings_file['acc_warning']
        RSI_time = all_settings_file['RSI_time']
        
        maxtrial = all_settings_file['maxtrial']
        sessionstarts = all_settings_file['sessionstarts']
        blockstarts= all_settings_file['blockstarts']
        
        asrt_types = all_settings_file["asrt_types"]

    except:
        groups = []
        possible_colors = ["AliceBlue","AntiqueWhite","Aqua","Aquamarine","Azure","Beige","Bisque","Black","BlanchedAlmond","Blue","BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGrey","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","DarkOrange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkSlateGrey","DarkTurquoise","DarkViolet","DeepPink","DeepSkyBlue","DimGray","DimGrey","DodgerBlue","FireBrick","FloralWhite","ForestGreen","Fuchsia","Gainsboro","GhostWhite","Gold","GoldenRod","Gray","Grey","Green","GreenYellow","HoneyDew","HotPink","IndianRed","Indigo","Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGrey","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray","LightSlateGrey","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen","MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive","OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue","Purple","RebeccaPurple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray","SlateGrey","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","White","WhiteSmoke","Yellow","YellowGreen"]

        numgroups = 0
        numsessions = 0
        (numgroups, numsessions) = show_basic_settings_dialog()

        groups = show_group_settings_dialog(numgroups, dict_accents)

        epoch_block_result = show_epoch_and_block_settings_dialog(numsessions)
        blockprepN = epoch_block_result["blockprepN"]
        blocklengthN = epoch_block_result["blocklengthN"]
        block_in_epochN = epoch_block_result["block_in_epochN"]
        epochN = epoch_block_result["epochN"]
        epochs = epoch_block_result["epochs"]
        asrt_types = epoch_block_result["asrt_types"]
            
        maxtrial = (blockprepN+blocklengthN)*epochN*block_in_epochN
        sessionstarts = [1]
        epochs_cumulative = []
        e_temp = 0
        for e in epochs:
            e_temp+= e
            epochs_cumulative.append(e_temp)
            
        for e in epochs_cumulative:
            sessionstarts.append(e* block_in_epochN * (blocklengthN + blockprepN) +1 )

        blockstarts = [1]
        for i in range(1, epochN*block_in_epochN+2):
            blockstarts.append(i * (blocklengthN+blockprepN)+1)
        
        computer_and_display_settings = show_computer_and_display_settings_dialog(possible_colors)
        monitor_width = computer_and_display_settings["monitor_width"]
        computer_name = computer_and_display_settings["computer_name"]
        refreshrate = computer_and_display_settings["refreshrate"]
        asrt_distance = computer_and_display_settings["asrt_distance"]
        asrt_size = computer_and_display_settings["asrt_size"]
        asrt_rcolor = computer_and_display_settings["asrt_rcolor"]
        asrt_pcolor = computer_and_display_settings["asrt_pcolor"]
        asrt_background = computer_and_display_settings["asrt_background"]
        asrt_circle_background = computer_and_display_settings["asrt_circle_background"]
        RSI_time = computer_and_display_settings["RSI_time"]
            
        key_and_feedback_settings = show_key_and_feedback_settings_dialog()
        key1 = key_and_feedback_settings["key1"]
        key2 = key_and_feedback_settings["key2"]
        key3 = key_and_feedback_settings["key3"]
        key4 = key_and_feedback_settings["key4"]
        key_quit = key_and_feedback_settings["key_quit"]
        whether_warning = key_and_feedback_settings["whether_warning"]
        speed_warning = key_and_feedback_settings["speed_warning"]
        acc_warning = key_and_feedback_settings["acc_warning"]


    all_settings_file['RSI_time'] = RSI_time
    all_settings_file['refreshrate'] = refreshrate
    all_settings_file['key1'] = key1
    all_settings_file['key2'] = key2
    all_settings_file['key3'] = key3
    all_settings_file['key4'] = key4
    all_settings_file['key_quit'] = key_quit
    all_settings_file['whether_warning'] = whether_warning
    all_settings_file['speed_warning'] = speed_warning
    all_settings_file['acc_warning'] = acc_warning

    all_settings_file['groups'] = groups
    all_settings_file['numsessions'] = numsessions
    all_settings_file['blockprepN'] = blockprepN
    all_settings_file['blocklengthN'] = blocklengthN
    all_settings_file['block_in_epochN'] = block_in_epochN
    all_settings_file['epochN'] = epochN
    all_settings_file['epochs'] = epochs

    all_settings_file['asrt_types'] = asrt_types

    all_settings_file['monitor_width'] = monitor_width
    all_settings_file['computer_name'] = computer_name
    all_settings_file['asrt_distance'] = asrt_distance
    all_settings_file['asrt_size'] = asrt_size
    all_settings_file['asrt_rcolor'] = asrt_rcolor
    all_settings_file['asrt_pcolor'] = asrt_pcolor
    all_settings_file['asrt_background'] = asrt_background
    all_settings_file['asrt_circle_background'] = asrt_circle_background
    all_settings_file['maxtrial'] = maxtrial
    all_settings_file['sessionstarts'] = sessionstarts
    all_settings_file['blockstarts'] = blockstarts

    all_settings_file.sync()
    all_settings_file.close()

    settingstxt = codecs.open(thispath+'\\settings\\settings_reminder.txt','w', encoding = 'utf-8')
    settingstxt.write(u'Beállítások \n'+
                                        '\n'+
                                        'MonitorHz: '+ '\t'+ str(refreshrate).replace('.',',')+'\n'+
                                        'Monitor Width: '+ '\t'+ str(monitor_width).replace('.',',')+'\n'+
                                        'Computer Name: '+ '\t'+ computer_name+'\n'+
                                        'Response keys: '+ '\t'+ key1+', '+ key2+', '+ key3+', '+ key4+'.'+'\n'+
                                        'Quit key: '+ '\t'+ key_quit +'\n'+
                                        'Warning (speed, accuracy): '+ '\t'+ str(whether_warning)+'\n'+
                                        'Speed warning at:'+ '\t'+ str(speed_warning)+'\n'+
                                        'Acc warning at:'+ '\t'+ str(acc_warning)+'\n'+
                                        'Groups:'+ '\t'+ str(groups)[1:-1].replace("u'", '').replace("'", '')+'\n'+
                                        'Sessions:'+ '\t'+ str(numsessions)+'\n'+
                                        'Epochs in sessions:'+ '\t'+ str(epochs)[1:-1].replace("u'", '').replace("'", '')+'\n'+
                                        'Blocks in epochs:'+ '\t'+ str(block_in_epochN)+'\n'+
                                        'Preparatory Trials/Block:'+ '\t'+ str(blockprepN)+'\n'+
                                        'Trials/Block:'+ '\t'+ str(blocklengthN)+'\n'+
                                        'RSI:'+ '\t'+ str(RSI_time).replace('.',',')+'\n'+
                                        'Asrt stim distance:'+ '\t'+ str(asrt_distance)+'\n'+
                                        'Asrt stim size:'+ '\t'+ str(asrt_size)+'\n'+
                                        'Asrt stim color (implicit):'+ '\t'+ asrt_rcolor+'\n'+
                                        'Asrt stim color (explicit, cued):'+ '\t'+ asrt_pcolor+'\n'+
                                        'Asrt stim background color:'+ '\t'+ asrt_circle_background+'\n'+
                                        'Background color:'+ '\t'+ asrt_background+'\n'+
                                        '\n'+
                                        
    u'''Az alábbi beállítások minden személyre érvényesek és irányadóak. 

    A beállítások azokra a kísérletekre vonatkoznak, amelyeket ebből a mappából,
    az itt található scripttel indítottak. Ha más beállításokat (is) szeretnél alkalmazni,
    úgy az asrt.py és az instrukciókat tartalmazó .txt fájlt másold át egy másik könyvtárba is,
    és annak a scriptnek az indításakor megadhatod a kívánt másmilyen beállításokat.

    Figyelj rá, hogy mindig abból a könyvtárból indítsd a scriptet, ahol a számodra megfelelő
    beállítások vannak elmentve.

    A settings.dat fájl kitörlésével a beállítások megváltoztathatóak; ugyanakkor a fájl
    törlése a későbbi átláthatóság miatt nem javasolt. Ha mégis a törlés mellett döntenél,
    jelen .txt fájlt előtte másold, hogy a korábbi beállításokra is emlékezhess, ha szükséges lesz.
    ''')

    settingstxt.close()
    return  groups, numsessions, blockprepN, blocklengthN, block_in_epochN, epochN, epochs, monitor_width, computer_name, asrt_distance, asrt_size, asrt_rcolor, asrt_pcolor, asrt_background, asrt_circle_background, refreshrate, key1, key2, key3, key4, key_quit, whether_warning, speed_warning, acc_warning, RSI_time, maxtrial, sessionstarts, blockstarts, asrt_types

def get_thisperson_settings():
    
    nr_of_duplets = thisperson_settings.get('nr_of_duplets', 0)
    nr_of_triplets = thisperson_settings.get('nr_of_triplets', 0)
    nr_of_quads = thisperson_settings.get('nr_of_quads', 0)
    nr_of_quints = thisperson_settings.get('nr_of_quints', 0)
    nr_of_sexts = thisperson_settings.get('nr_of_sexts', 0)

    pr_nr_of_duplets = thisperson_settings.get('pr_nr_of_duplets', 0)
    pr_nr_of_triplets = thisperson_settings.get('pr_nr_of_triplets', 0)
    pr_nr_of_quads = thisperson_settings.get('pr_nr_of_quads', 0)
    pr_nr_of_quints = thisperson_settings.get('pr_nr_of_quints', 0)
    pr_nr_of_sexts = thisperson_settings.get('pr_nr_of_sexts', 0)

    context_freq = thisperson_settings.get('context_freq',{})
    comb_freq = thisperson_settings.get('comb_freq',{})
    pr_context_freq = thisperson_settings.get('pr_context_freq',{})
    pr_comb_freq = thisperson_settings.get('pr_comb_freq',{})

    PCodes = thisperson_settings.get('PCodes', {})                          #
    PCode_types = thisperson_settings.get('PCode_types','')        #
    stim_output_line = thisperson_settings.get('stim_output_line',0)

    stim_sessionN = thisperson_settings.get('stim_sessionN',{})
    stimepoch = thisperson_settings.get('stimepoch',{})
    stimblock = thisperson_settings.get('stimblock',{})
    stimtrial = thisperson_settings.get('stimtrial',{})

    stimlist = thisperson_settings.get('stimlist',{})
    stimpr = thisperson_settings.get('stimpr',{})
    last_N = thisperson_settings.get('last_N', 0)
    end_at = thisperson_settings.get('end_at',{})

    stim_colorN = thisperson_settings.get('stim_colorN',{})
    stim_quit = thisperson_settings.get('stim_quit',{})
    
    return nr_of_duplets, nr_of_triplets, nr_of_quads, nr_of_quints, nr_of_sexts, pr_nr_of_duplets, pr_nr_of_triplets, pr_nr_of_quads, pr_nr_of_quints, pr_nr_of_sexts, context_freq, comb_freq, pr_context_freq, pr_comb_freq, PCodes, PCode_types, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, last_N, end_at, stim_colorN, stim_quit

def which_code(session_number = 0):
    pcode_raw = PCodes[session_number]
   
    if pcode_raw == 'noPattern':
        PCode = 'noPattern'
    elif pcode_raw == '1st':
        PCode = sequences_PCode[1]
    elif pcode_raw == '2nd':
        PCode = sequences_PCode[2]
    elif pcode_raw == '3rd':
        PCode = sequences_PCode[3]
    elif pcode_raw == '4th':
        PCode = sequences_PCode[4]
    elif pcode_raw == '5th':
        PCode = sequences_PCode[5]
    elif pcode_raw == '6th':
        PCode = sequences_PCode[6]
    Pcode_str = str(PCode)
    return PCode, Pcode_str

def participant_id():
    global asrt_types, PCodes, PCode_types
    global stim_output_line
    global thisperson_settings, group, identif, subject_nr
    global stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, last_N,  end_at, stim_colorN, stim_quit, stimpr
    global context_freq, comb_freq, pr_comb_freq, pr_context_freq
    global nr_of_duplets, nr_of_triplets, nr_of_quads, nr_of_quints, nr_of_sexts
    global pr_nr_of_duplets, pr_nr_of_triplets, pr_nr_of_quads, pr_nr_of_quints, pr_nr_of_sexts
    
    subject_settings = show_subject_settings_dialog(groups, dict_accents)
    identif = subject_settings["identif"]
    subject_nr = subject_settings["subject_nr"]
    group = subject_settings["group"]
    
    p_settings_file = shelve.open(thispath+'\\settings\\participant_settings.dat')
    try:
        ids_temp = p_settings_file['ids']
    except:
        ids_temp = []
            

    if identif+'_'+str(subject_nr)+'_'+group not in ids_temp:
        ids_temp.append(identif+'_'+str(subject_nr)+'_'+group)

    p_settings_file['ids'] = ids_temp
    p_settings_file.sync()
    p_settings_file.close()

    # letezik-e mar ilyen ksz-szel beállítás?
    p_settings_file = shelve.open(thispath+'\\settings\\'+identif+'_'+str(subject_nr)+"_"+group+'.dat')

    try:
        p_settings_temp = p_settings_file['all_settings']
    except:
        p_settings_temp = {}

    try:
        thisperson_settings = p_settings_temp [identif+'_'+str(subject_nr)+'_'+group]
        letezo = 1
    except:
        letezo = 0
        
    if letezo == 1:
        nr_of_duplets, nr_of_triplets, nr_of_quads, nr_of_quints, nr_of_sexts, pr_nr_of_duplets, pr_nr_of_triplets, pr_nr_of_quads, pr_nr_of_quints, pr_nr_of_sexts, context_freq, comb_freq, pr_context_freq, pr_comb_freq, PCodes, PCode_types, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, last_N, end_at, stim_colorN, stim_quit = get_thisperson_settings()
        if last_N+1 <= maxtrial:
            expstart11=gui.Dlg(title=u'Feladat indítása...')
            expstart11.addText(u'A személy adatait beolvastam.')
            expstart11.addText(u'Folytatás innen...')
            expstart11.addText('Session: '+ str(stim_sessionN[ last_N+1]))
            expstart11.addText('Epoch: '+str(stimepoch[ last_N+1]))
            expstart11.addText('Block: '+str(stimblock[last_N+1]))
            expstart11.addText('Trial: '+str(stimtrial[last_N+1]))
            expstart11.show()
            if not expstart11.OK:
                core.quit()
                
        else:
            expstart11=gui.Dlg(title=u'Feladat indítása...')
            expstart11.addText(u'A személy adatait beolvastam.')
            expstart11.addText(u'A személy végigcsinálta a feladatot.')
            expstart11.show()
            core.quit()
                
    else:
        # no such person yet
        thisperson_settings = {}
        nr_of_duplets, nr_of_triplets, nr_of_quads, nr_of_quints, nr_of_sexts, pr_nr_of_duplets, pr_nr_of_triplets, pr_nr_of_quads, pr_nr_of_quints, pr_nr_of_sexts, context_freq, comb_freq, pr_context_freq, pr_comb_freq, PCodes, PCode_types, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, last_N, end_at, stim_colorN, stim_quit = get_thisperson_settings()
        
        expstart1=gui.Dlg(title=u'Beállítások')
        expstart1.addText('')
        for z in range(numsessions):
            if asrt_types[z+1] == "noASRT":
                expstart1.addFixedField(u'Session ' + str(z+1) + ' PCode', 'noPattern')         
            else: 
                expstart1.addField(u'Session ' + str(z+1) + ' PCode', choices = ['1st' , '2nd', '3rd', '4th', '5th', '6th'])
        
        expstart1.show()
        if expstart1.OK:
            for zz in range(numsessions):
                PCodes[zz+1] = expstart1.data[zz]
            
            for key in PCodes.values():
                if (not key in PCode_types) and (not key == 'noPattern'):
                    PCode_types += key+'='
            if '=' in PCode_types:
                PCode_types = PCode_types[:-1]
            PCode_types = PCode_types.replace('1st', "1")
            PCode_types = PCode_types.replace('2nd', "2")
            PCode_types = PCode_types.replace('3rd', "3")
            PCode_types = PCode_types.replace('4th', "4")
            PCode_types = PCode_types.replace('5th', "5")
            PCode_types = PCode_types.replace('6th', "6")
        else:
            core.quit()
            
        Nr = 0
        bln = 0
        
        # itt megnézzük, melyik számú inger melyik session része (ez amiatt kell, h sessionönként lehessen implicit/explicit/no asrt-t gyártani
        
        for y in range(1, maxtrial+1):
            for ss in range(1, len(sessionstarts)):
                if y >= sessionstarts[ss-1] and y < sessionstarts[ss]:
                    stim_sessionN[y] = ss
                    end_at[y] = sessionstarts[ss]

        for epoch in range(1,epochN+1):
            
            for block in range(1, block_in_epochN+1):
                bln += 1
                current_trial_num = 0
                
                # practice
                for practice in range(1, blockprepN+1):
                    current_trial_num += 1
                    
                    Nr += 1 
                    asrt_type = asrt_types[stim_sessionN[Nr]] 
                    PCode, Pcode_str = which_code(stim_sessionN[Nr])

                    dict_HL = {}
                    if not PCode == "noPattern":
                        dict_HL[Pcode_str[0]] = Pcode_str[1]
                        dict_HL[Pcode_str[1]] = Pcode_str[2]
                        dict_HL[Pcode_str[2]] = Pcode_str[3]
                        dict_HL[Pcode_str[3]] = Pcode_str[0]

                    current_stim = random.choice([1,2,3,4])
                    stimlist[Nr] = current_stim
                    stimpr[Nr] = "R"
                    stim_colorN[Nr] = asrt_rcolor
                    stimtrial[Nr] = current_trial_num
                    stimblock[Nr] = bln
                    stimepoch[Nr] = epoch
                 
                # real
                for real in range(1, blocklengthN+1):
                
                    current_trial_num += 1
                    Nr += 1

                    asrt_type = asrt_types[stim_sessionN[Nr]] 
                    PCode, Pcode_str = which_code(stim_sessionN[Nr])
                    
                    if blockprepN%2 == 1:
                        mod_pattern = 0
                    else:
                        mod_pattern = 1
                    
                    if current_trial_num%2 == mod_pattern and asrt_type != "noASRT":
                        current_stim = int( dict_HL[ str(stimlist[Nr-2]) ] )
                        stimpr[Nr] = "P"

                        if asrt_type == 'explicit':
                            stim_colorN[Nr] = asrt_pcolor
                        elif asrt_type == "implicit" or asrt_type == 'noASRT':
                            stim_colorN[Nr] = asrt_rcolor
                    
                    else:
                        current_stim = random.choice([1,2,3,4])
                        stim_colorN[Nr] = asrt_rcolor
                        stimpr[Nr] = "R"

                    stimlist[Nr] = current_stim
                    stimtrial[Nr] = current_trial_num
                    stimblock[Nr] = bln
                    stimepoch[Nr] = epoch

        thisperson_settings = {}
        save_personal_info()

    participanttxt = codecs.open(thispath+'\\settings\\participants_in_experiment.txt','w', encoding = 'utf-8')
    for ida in ids_temp:
        y = ida.split('_')
        for x in y:
            try:
                x=str(x)
            except:
                pass
            participanttxt.write(x+'\t')
        try:
            participanttxt.write(p_settings_temp[ida]['asrt_type']+'\t')
        except:
            participanttxt.write('\t')
        try:
            participanttxt.write(str(p_settings_temp[ida]['PCode'])+'\n')
        except:
            participanttxt.write('\n')
            
                                        
    participanttxt.close()
    return thisperson_settings, group, subject_nr, identif

def monitor_settings():
    screen = pyglet.window.get_platform().get_default_display().get_default_screen()
    dimension_x = screen.width
    dimension_y = screen.height

    ## Monitor beállítása
    my_monitor = monitors.Monitor('myMon')
    my_monitor.setSizePix( [dimension_x, dimension_y] ) 
    my_monitor.setWidth(monitor_width) # cm-ben
    my_monitor.saveMon()
    
    return dimension_x, dimension_y, my_monitor

def print_to_screen(mytext = u""):
    xtext.text = mytext
    xtext.draw()

def frame_check():
    # monitorral kapcsolatos informáciok
    print_to_screen(u'Adatok előkészítése folyamatban. \nEz eltarthat pár másodpercig. \nAddig semmit sem fogsz látni a képernyőn...')
    mywindow.flip()
    core.wait(2)

    frame_time, frame_sd = mywindow.getMsPerFrame(nFrames = 120) [0], mywindow.getMsPerFrame(nFrames = 120) [1]
    frame_rate = mywindow.getActualFrameRate()
    return frame_time, frame_sd, frame_rate
    
def stim_bg():
    for i in range(1,5):
        stimbg.pos = dict_pos[i]
        stimbg.draw()

def unexpectedquit():
    for l in unexp_quit:
        print_to_screen(l)
        mywindow.flip()
        tempkey = event.waitKeys(keyList= [key1, key2, key3, key4, key_quit])
        if key_quit in tempkey:
            core.quit() 

def instructions():
    for l in insts:
        print_to_screen(l)
        mywindow.flip()
        tempkey = event.waitKeys(keyList= [key1, key2, key3, key4, key_quit])
        if key_quit in tempkey:
            core.quit() 

def ending():
    for l in ending:
        print_to_screen(l)
        mywindow.flip()
        tempkey = event.waitKeys(keyList= [key1, key2, key3, key4, key_quit])
        if key_quit in tempkey:
            core.quit() 

def feedback_explicit(rt_m ="", rt_m_p = "", acc_for_p= "", acc_for_the_w= ""):

    for l in feedback_exp:
        l = l.replace('*MEANRT*', rt_m)
        l = l.replace('*MEANRTP*', rt_m_p)
        l = l.replace('*PERCACCP*', acc_for_p)
        l = l.replace('*PERCACC*', acc_for_the_w)
        
        if whether_warning is True:
            if acc_for_the_whole > speed_warning:
                l = l.replace('*SPEEDACC*', feedback_speed[0])
            elif acc_for_the_whole < acc_warning:
                l = l.replace('*SPEEDACC*', feedback_accuracy[0])
            else:
                l = l.replace('*SPEEDACC*', '')
            
        print_to_screen(l)
        mywindow.flip()
        tempkey = event.waitKeys(keyList= [key1, key2, key3, key4, key_quit])
        if key_quit in tempkey:
            return 'quit'
        else:
            return 'continue'

def feedback_implicit(rt_m = "", acc_for_the_w= ""):
    for i in feedback_imp:
        i = i.replace('*MEANRT*', rt_m)
        i = i.replace('*PERCACC*', acc_for_the_w)
        
        if whether_warning is True:
            if acc_for_the_whole > speed_warning:
                i = i.replace('*SPEEDACC*', feedback_speed[0])
            elif acc_for_the_whole < acc_warning:
                i = i.replace('*SPEEDACC*', feedback_accuracy[0])
            else:
                i = i.replace('*SPEEDACC*', '')
            
        print_to_screen(i)
        mywindow.flip()
        tempkey = event.waitKeys(keyList= [key1, key2, key3, key4, key_quit])
        if key_quit in tempkey:
            return 'quit'
        else:
            return 'continue'

def heading_to_output():
    try:
        outfile_txt = codecs.open(thispath+'\\logs\\'+group+'_'+str(subject_nr)+'_'+identif+'_log.txt', 'r', encoding = 'utf-8')
        heading = 1
        outfile_txt.close()
    except:
        heading = 0
        
    heading_list = [ 'computer_name',
                                'Group',
                                'Subject_ID',
                                'Subject_nr',
                                'asrt_type',
                                'PCode',
                                'Pcode_Types', 

                                'output_line',
                                'outputline_thisstart', #
                                'trialN_in_whole_ASRT', 
                                "trialN_in_session",
                                'trialN_thisstart',         #
                                
                                'userquit_log',
                                
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

                                'stimulus_color', #uj helyen
                                'PR', #uj helyen
                                'RT', #uj helyen
                                'error', #uj helyen 
                                'cumulative_error',  #uj helyen
                                'previous_one_accurate', #uj helyen
                                'previous_two_accurate', #uj helyen
                                'previous_three_accurate', #uj helyen
                                'previous_four_accurate', #uj helyen
                                'previous_five_accurate', #uj helyen

                                # innenmegy a duplazas meg az anyazas

                                'tripfilter',
                                'quadfilter',

                                'stimulus', 
                                'duplet',
                                'triplet',
                                'quad',
                                'quint',
                                'sext',

                                'sing_frequency',
                                "dup_frequency",
                                "trip_frequency",
                                "quad_frequency",
                                "quint_frequency",
                                "sext_frequency",
                                
                                'sing_trialprob',
                                "dup_trialprob",
                                "trip_trialprob",
                                "quad_trialprob",
                                "quint_trialprob",
                                "sext_trialprob",

                                'thisstart_sing_frequency',
                                "thisstart_dup_frequency",
                                "thisstart_trip_frequency",
                                "thisstart_quad_frequency",
                                "thisstart_quint_frequency",
                                "thisstart_sext_frequency",
                                
                                'thisstart_sing_trialprob',
                                "thisstart_dup_trialprob",
                                "thisstart_trip_trialprob",
                                "thisstart_quad_trialprob",
                                "thisstart_quint_trialprob",
                                "thisstart_sext_trialprob",
                                
                                "hand_change",

                                'abstr_dup',
                                'abstr_trip',
                                'abstr_quad',
                                'abstr_quint',
                                'abstr_sext',

                                "dir_last",
                                "dir_last_two",
                                "dir_last_three",
                                "dir_last_four",
                                "dir_last_five",

                                "relative_dir_last",
                                "relative_dir_last_two",
                                "relative_dir_last_three",
                                "relative_dir_last_four",
                                "relative_dir_last_five",

                                "relative_dir_last_up",
                                "relative_dir_last_two_up",
                                "relative_dir_last_three_up",
                                "relative_dir_last_four_up",
                                "relative_dir_last_five_up",

                                'currentTT',
                                'currentQT',
                                'currentQiT',
                                'currentST',

                                "trip_group",
                                "quad_group",
                                "quint_group",
                                "sext_group",

                                "P1_trip",
                                "P1_tripT",
                                "P1_quad",
                                "P1_quadT",
                                "P1_quint",
                                "P1_quintT",
                                "P1_sext",
                                "P1_sextT",

                                "P2_trip",
                                "P2_tripT",
                                "P2_quad",
                                "P2_quadT",
                                "P2_quint",
                                "P2_quintT",
                                "P2_sext",
                                "P2_sextT",

                                "P3_trip",
                                "P3_tripT",
                                "P3_quad",
                                "P3_quadT",
                                "P3_quint",
                                "P3_quintT",
                                "P3_sext",
                                "P3_sextT",

                                "P4_trip",
                                "P4_tripT",
                                "P4_quad",
                                "P4_quadT",
                                "P4_quint",
                                "P4_quintT",
                                "P4_sext",
                                "P4_sextT",

                                "P5_trip",
                                "P5_tripT",
                                "P5_quad",
                                "P5_quadT",
                                "P5_quint",
                                "P5_quintT",
                                "P5_sext",
                                "P5_sextT",

                                "P6_trip",
                                "P6_tripT",
                                "P6_quad",
                                "P6_quadT",
                                "P6_quint",
                                "P6_quintT",
                                "P6_sext",
                                "P6_sextT",

# ez csak erre vonatkozik

                                'stimbutton',

# innenmegy a duplazas meg az anyazas

                                'pr_tripfilter',
                                'pr_quadfilter',

                                'pr_stimulus', 
                                'pr_duplet',
                                'pr_triplet',
                                'pr_quad',
                                'pr_quint',
                                'pr_sext',

                                'pr_sing_frequency',
                                "pr_dup_frequency",
                                "pr_trip_frequency",
                                "pr_quad_frequency",
                                "pr_quint_frequency",
                                "pr_sext_frequency",
                                
                                'pr_sing_trialprob',
                                "pr_dup_trialprob",
                                "pr_trip_trialprob",
                                "pr_quad_trialprob",
                                "pr_quint_trialprob",
                                "pr_sext_trialprob",

                                'pr_thisstart_sing_frequency',
                                "pr_thisstart_dup_frequency",
                                "pr_thisstart_trip_frequency",
                                "pr_thisstart_quad_frequency",
                                "pr_thisstart_quint_frequency",
                                "pr_thisstart_sext_frequency",
                                
                                'pr_thisstart_sing_trialprob',
                                "pr_thisstart_dup_trialprob",
                                "pr_thisstart_trip_trialprob",
                                "pr_thisstart_quad_trialprob",
                                "pr_thisstart_quint_trialprob",
                                "pr_thisstart_sext_trialprob",

                                "pr_hand_change",

                                'pr_abstr_dup',
                                'pr_abstr_trip',
                                'pr_abstr_quad',
                                'pr_abstr_quint',
                                'pr_abstr_sext',

                                "pr_dir_last",
                                "pr_dir_last_two",
                                "pr_dir_last_three",
                                "pr_dir_last_four",
                                "pr_dir_last_five",

                                "pr_relative_dir_last",
                                "pr_relative_dir_last_two",
                                "pr_relative_dir_last_three",
                                "pr_relative_dir_last_four",
                                "pr_relative_dir_last_five",

                                "pr_relative_dir_last_up",
                                "pr_relative_dir_last_two_up",
                                "pr_relative_dir_last_three_up",
                                "pr_relative_dir_last_four_up",
                                "pr_relative_dir_last_five_up",

                                'pr_currentTT',
                                'pr_currentQT',
                                'pr_currentQiT',
                                'pr_currentST',

                                "pr_trip_group",
                                "pr_quad_group",
                                "pr_quint_group",
                                "pr_sext_group",


                                "pr_P1_trip",
                                "pr_P1_tripT",
                                "pr_P1_quad",
                                "pr_P1_quadT",
                                "pr_P1_quint",
                                "pr_P1_quintT",
                                "pr_P1_sext",
                                "pr_P1_sextT",

                                "pr_P2_trip",
                                "pr_P2_tripT",
                                "pr_P2_quad",
                                "pr_P2_quadT",
                                "pr_P2_quint",
                                "pr_P2_quintT",
                                "pr_P2_sext",
                                "pr_P2_sextT",

                                "pr_P3_trip",
                                "pr_P3_tripT",
                                "pr_P3_quad",
                                "pr_P3_quadT",
                                "pr_P3_quint",
                                "pr_P3_quintT",
                                "pr_P3_sext",
                                "pr_P3_sextT",

                                "pr_P4_trip",
                                "pr_P4_tripT",
                                "pr_P4_quad",
                                "pr_P4_quadT",
                                "pr_P4_quint",
                                "pr_P4_quintT",
                                "pr_P4_sext",
                                "pr_P4_sextT",

                                "pr_P5_trip",
                                "pr_P5_tripT",
                                "pr_P5_quad",
                                "pr_P5_quadT",
                                "pr_P5_quint",
                                "pr_P5_quintT",
                                "pr_P5_sext",
                                "pr_P5_sextT",

                                "pr_P6_trip",
                                "pr_P6_tripT",
                                "pr_P6_quad",
                                "pr_P6_quadT",
                                "pr_P6_quint",
                                "pr_P6_quintT",
                                "pr_P6_sext",
                                "pr_P6_sextT",

                                # ez a ketto viszonyara vonatkozik

                                'obs_pr_trip',
                                'obs_pr_quad',
                                'obs_pr_quint',
                                'obs_pr_sext',

                                'anticip_trip_moved_category',
                                'anticip_quad_moved_category',
                                'anticip_quint_moved_category',
                                'anticip_sext_moved_category',

                                'obs_pr_sing_actual_difference_freq',
                                'obs_pr_dup_actual_difference_freq',
                                'obs_pr_trip_actual_difference_freq',
                                'obs_pr_quad_actual_difference_freq',
                                'obs_pr_quint_actual_difference_freq',
                                'obs_pr_sext_actual_difference_freq',

                                'obs_pr_sing_actual_difference_prob',
                                'obs_pr_dup_actual_difference_prob',
                                'obs_pr_trip_actual_difference_prob',
                                'obs_pr_quad_actual_difference_prob',
                                'obs_pr_quint_actual_difference_prob',
                                'obs_pr_sext_actual_difference_prob',
                                
                                'thisstart_obs_pr_sing_actual_difference_freq',
                                'thisstart_obs_pr_dup_actual_difference_freq',
                                'thisstart_obs_pr_trip_actual_difference_freq',
                                'thisstart_obs_pr_quad_actual_difference_freq',
                                'thisstart_obs_pr_quint_actual_difference_freq',
                                'thisstart_obs_pr_sext_actual_difference_freq',

                                'thisstart_obs_pr_sing_actual_difference_prob',
                                'thisstart_obs_pr_dup_actual_difference_prob',
                                'thisstart_obs_pr_trip_actual_difference_prob',
                                'thisstart_obs_pr_quad_actual_difference_prob',
                                'thisstart_obs_pr_quint_actual_difference_prob',
                                'thisstart_obs_pr_sext_actual_difference_prob'
                                
                                ]
    
    abclist = ['_a_code', '_b_code', '_c_code', '_d_code', '_e_code', '_f_code' ]
    
    for mypc in range(len(PCode_types.split('='))):
        heading_list.append('anticip_type_trip' + abclist[mypc])
        heading_list.append('anticip_type_quad' + abclist[mypc])
        heading_list.append('anticip_type_quint' + abclist[mypc])
        heading_list.append('anticip_type_sext' + abclist[mypc])

    for mypc in range(len(PCode_types.split('='))):
        heading_list.append('anticip_move_trip' + abclist[mypc])
        heading_list.append('anticip_move_type_quad' + abclist[mypc])
        heading_list.append('anticip_move_type_quint' + abclist[mypc])
        heading_list.append('anticip_move_type_sext' + abclist[mypc])

    heading_list.append('quit_log')

    if heading == 0:
        outfile_txt = codecs.open(thispath+'\\logs\\'+group+'_'+str(subject_nr)+'_'+identif+'_log.txt', 'w', encoding = 'utf-8')
        for h in heading_list:
            outfile_txt.write(h+'\t')
        outfile_txt.close()

def otherseq(codenum = "1234", listfrom = []):
    
    codenum = codenum*3
    #trip
    try:
        trip_pattern = str(listfrom[-3]) + str(listfrom[-1])
        if trip_pattern in codenum:
            tripASRT = "5"
            tripASRT_type = "H"
        else:
            tripASRT = "1"
            tripASRT_type = "L"
    except:
        tripASRT= ""
        tripASRT_type = ""
        
        
    #quad 
    try:
        quad_pattern1 = str(listfrom[-4])+ str(listfrom[-2])
        quad_pattern2 = str(listfrom[-3])+ str(listfrom[-1])
        if (quad_pattern1 in codenum) or (quad_pattern2 in codenum):
            if (quad_pattern1 in codenum) and (quad_pattern2 in codenum):
                quadASRT = "2"
                quadASRT_type = "H1"
            else:
                quadASRT = "1"
                if tripASRT_type == "H":
                    quadASRT_type = "H2"
                elif tripASRT_type == "L":
                    quadASRT_type = "L"
        else:
            quadASRT = "0"
            quadASRT_type = "NA"
    except:
        quadASRT = ""
        quadASRT_type = ""
        
        
    #quint
    try:
        quint1 = str(listfrom[-5])+str(listfrom[-3])+str(listfrom[-1])
        quint2 = str(listfrom[-4])+str(listfrom[-2])
        quint_context =  str(listfrom[-5])+str(listfrom[-3])
        if (quint1 in codenum) or (quint2 in codenum):
            if (quint1 in codenum) and (quint2 in codenum):
                quintASRT = "5"
                quintASRT_type = "H1b"
            elif quint1 in codenum:
                quintASRT = "4"
                quintASRT_type = "H2"
            elif quint2 in codenum:
                quintASRT = "1"
                if (quadASRT_type == "L") and (quint_context in codenum):
                    quintASRT_type = "La"
                elif (quadASRT_type == "L"):
                    quintASRT_type = "Lb"
                elif quadASRT_type  == "H1":
                    quintASRT_type = "H1a"

        else: 
            quintASRT = "0"
            quintASRT_type = "NA"

    except:
        quintASRT = ""
        quintASRT_type = ""
    
    #sext
    try:
        sext1 = str(listfrom[-6]) + str(listfrom[-4]) + str(listfrom[-2])
        sext2 =str(listfrom[-5]) + str(listfrom[-3]) + str(listfrom[-1])
        if (sext1 in codenum) or (sext2 in codenum):
            if (sext1 in codenum) and (sext2 in codenum):
                sextASRT = "2"
                sextASRT_type = "H1b-I"
            else:
                sextASRT = "1"
                if quintASRT_type == "H1b":
                    sextASRT_type = "H1b-II"
                else:
                    sextASRT_type = quintASRT_type
        else:
            sextASRT = "0"
            sextASRT_type = "NA"
    except:
        sextASRT = ""
        sextASRT_type =""
    
    if 'noPattern' in codenum:
        tripASRT, tripASRT_type, quadASRT, quadASRT_type, quintASRT, quintASRT_type, sextASRT, sextASRT_type = "","","","","","","",""
    return tripASRT, tripASRT_type, quadASRT, quadASRT_type, quintASRT, quintASRT_type, sextASRT, sextASRT_type

def save_personal_info(mydict ={}):
    global thisperson_settings

    thisperson_settings['nr_of_duplets'] = nr_of_duplets
    thisperson_settings['nr_of_triplets'] = nr_of_triplets
    thisperson_settings['nr_of_quads'] = nr_of_quads
    thisperson_settings['nr_of_quints'] = nr_of_quints
    thisperson_settings['nr_of_sexts'] = nr_of_sexts
    
    thisperson_settings['pr_nr_of_duplets'] = pr_nr_of_duplets
    thisperson_settings['pr_nr_of_triplets'] = pr_nr_of_triplets
    thisperson_settings['pr_nr_of_quads'] = pr_nr_of_quads
    thisperson_settings['pr_nr_of_quints'] = pr_nr_of_quints
    thisperson_settings['pr_nr_of_sexts'] = pr_nr_of_sexts

    thisperson_settings['context_freq'] = context_freq
    thisperson_settings['comb_freq'] = comb_freq
    thisperson_settings['pr_context_freq'] = pr_context_freq
    thisperson_settings['pr_comb_freq'] = pr_comb_freq

    thisperson_settings[ 'PCodes' ] = PCodes
    thisperson_settings[ 'PCode_types' ] = PCode_types
    thisperson_settings[ 'stim_output_line' ] = stim_output_line

    thisperson_settings[ 'stim_sessionN' ] = stim_sessionN
    thisperson_settings[ 'stimepoch' ] = stimepoch
    thisperson_settings[ 'stimblock' ] = stimblock
    thisperson_settings[ 'stimtrial' ] = stimtrial

    thisperson_settings[ 'stimlist' ] = stimlist
    thisperson_settings[ 'stimpr' ] = stimpr
    thisperson_settings[ 'last_N' ] = last_N
    thisperson_settings[ 'end_at' ] = end_at
    thisperson_settings[ 'stim_colorN' ] = stim_colorN
    thisperson_settings[ 'stim_quit' ] = stim_quit

    p_settings_file = shelve.open(thispath+'\\settings\\'+identif+'_'+str(subject_nr)+"_"+group+'.dat')
    try:
        p_settings_temp = p_settings_file['all_settings']
    except:
        p_settings_temp = {}

    p_settings_temp[identif+'_'+str(subject_nr)+'_'+group] = thisperson_settings

    p_settings_file['all_settings'] = p_settings_temp
    p_settings_file.sync()
    p_settings_file.close()

def combos(listfrom = []):
    
    try:
        sext = listfrom[-6] * 100000 + listfrom[-5] * 10000 + listfrom[-4] * 1000 + listfrom[-3] * 100 + listfrom[-2] * 10 + listfrom[-1]
    except:
        sext = ""

    try:
        quint =  listfrom[-5] * 10000 + listfrom[-4] * 1000 + listfrom[-3] * 100 + listfrom[-2] * 10 + listfrom[-1]
    except:
        quint = ""
        
    try:
        quad = listfrom[-4] * 1000 + listfrom[-3] * 100 + listfrom[-2] * 10 + listfrom[-1]
    except:
        quad = ""

    try:
        trip = listfrom[-3] * 100 + listfrom[-2] * 10 + listfrom[-1]
    except:
        trip = ""
        
    try:
        dup = listfrom[-2] * 10 + listfrom[-1]
    except:
        dup = ""
        
    return dup, trip, quad, quint, sext
        
def previous_accuracy(listfrom = []):
    
    try:
        if listfrom[-6] + listfrom[-5] + listfrom[-4] + listfrom[-3] + listfrom[-2] == 0:
            last_five = 1
        else:
            last_five = 0
    except:
        last_five = ''

    try:
        if  listfrom[-5] + listfrom[-4] + listfrom[-3] + listfrom[-2] == 0:
            last_four = 1
        else:
            last_four = 0
    except:
        last_four = ''
        
    try:
        if  listfrom[-4] + listfrom[-3] + listfrom[-2] == 0:
            last_three = 1
        else:
            last_three = 0
    except:
        last_three = ''

    try:
        if  listfrom[-3] + listfrom[-2] == 0:
            last_two = 1
        else:
            last_two = 0
    except:
        last_two = ''
        
    try:
        if listfrom[-2] == 0:
            last_one = 1
        else:
            last_one = 0
    except:
        last_one = ''

    return last_five, last_four, last_three, last_two, last_one

def directions_def(listfrom = []):
    
    try:
        dir_one = listfrom[-1]
    except:
        dir_one = ''
        
    try:
        dir_two = listfrom[-2] + listfrom[-1]
    except:
        dir_two = ''

    try:
        dir_three = listfrom[-3] + listfrom[-2] + listfrom[-1]
    except:
        dir_three = ''

    try:
        dir_four = listfrom[-4] + listfrom[-3] + listfrom[-2] + listfrom[-1]
    except:
        dir_four = ''

    try:
        dir_five = listfrom[-5] + listfrom[-4] + listfrom[-3] + listfrom[-2] + listfrom[-1]
    except:
        dir_five = ''

    return dir_one, dir_two, dir_three, dir_four, dir_five

def reldir(howmany = 1, listfrom=[], lastdlist = []):
    prevs = lastdlist[:-1]
    to_return = ''
    try:
        for i in range(howmany): 
            if listfrom[-i-1] in (">","<"):
                if listfrom[-i-2] == 'R':
                    immediate = 0
                elif listfrom[-i-2] in (">","<"):
                    immediate = 1
                else:
                    pass
                lastd = prevs[-1]
                if lastd  == listfrom[-i-1]:
                    if immediate == 1:
                        to_return = "S" + to_return
                    elif immediate == 0:
                        to_return = "s" + to_return
                else:
                    if immediate == 1:
                        to_return = "O" + to_return
                    elif immediate == 0:
                        to_return = "o" + to_return
                        
                del prevs[-1]
            elif listfrom[-i-1] in ("R"):
                to_return = 'R'+ to_return
            else:
                to_return=""
    except:
        to_return = ""

    return to_return

def hand_changing(listfrom = [], handdict = {}):
    try:
        if handdict[listfrom[-1]] == handdict[listfrom[-2]]:
            return 'same_as_before'
        else:
            return 'different_from_prev'
    except:
        return ''

def abstract_structure(listfrom =[], howmany = 3):
    dict_abst={}
    dict_abst[ listfrom[-1] ] = 'a'
    to_return = ''
    
    try:
        for i in range(howmany-1):
            if listfrom[-2-i] not in dict_abst.keys():
                if 'b' not in dict_abst.values():
                    dict_abst[listfrom[-2-i]] = 'b'
                    to_return = 'b' + to_return
                elif 'c' not in dict_abst.values():
                    dict_abst[listfrom[-2-i]] = 'c'
                    to_return = 'c' + to_return
                elif 'd' not in dict_abst.values():
                    dict_abst[listfrom[-2-i]] = 'd'
                    to_return = 'd' + to_return
            else:
                to_return = dict_abst[listfrom[-2-i]] + to_return
        to_return = to_return + 'a'
    except:
        to_return = ''
    
    return to_return

def grouped_types (mylist = [], structure = 3):
    
    to_return= ''
    try:
        for mycode in PCode_types.split("="):
            mycode = int(mycode)
            if mylist[mycode-1][structure-3] != '':
                to_return = to_return + mylist [mycode-1][structure-3] + '-'

        if '-' in to_return:
            to_return = to_return[:-1]
    except:
        to_return=  ''
       
    return to_return

def freqs_and_probs( my_dict_stim = {}, my_dict_context = {},   stim_comb = 0, numb = 0):
    try:
        if stim_comb != '':
            to_return_freq = 100 * float( my_dict_stim.get( str(stim_comb), 1) - 1 )  /  (numb -1)
        else:
            to_return_freq = ""
    except ZeroDivisionError:
        to_return_freq = ''
    except:
        print('unhandled exception in the function freqs and probs')

    try:
        if stim_comb != '':
            to_return_prob = 100 * float( my_dict_stim.get( str(stim_comb), 1) - 1 )  /  ( my_dict_context.get(str(stim_comb)[0:-1], 1) -1)
        else:
            to_return_prob = ''
    except ZeroDivisionError:
        to_return_prob = ''
    except:
        print('unhandled exception in the function freqs and probs')

    return to_return_freq, to_return_prob

def update_occurences( mydict_whole = {}, mydict_context = {}, current_com = ''):    
    if not current_com == '':
        mydict_context [ str(current_com)[0:-1] ] = mydict_context.get(  str(current_com)[0:-1], 0) +1
        mydict_whole [ str(current_com) ] = mydict_whole.get( str(current_com), 0) +1

def whether_anticip ( type1 = '', type2 = '', mylist =[]):
    to_return = 0
    if type1 != '' and type2 != '':
        to_return = mylist.index(type2) - mylist.index(type1)
    else:
        to_return = ''
    return to_return

def difs(freq=0.0, freq_pr = 0.0, prob = 0.0, prob_pr = 0.0):
    
    to_return_freq, to_return_prob = '',''
    
    try:
        to_return_freq = str(freq_pr - freq)
    except:
        to_return_freq = ''
        

    try:
        to_return_prob = str(prob_pr - prob)
    except:
        to_return_prob = ''

    return to_return_freq, to_return_prob

def presentation():
    global context_freq, comb_freq, pr_context_freq, pr_comb_freq
    global nr_of_duplets, nr_of_triplets, nr_of_quads, nr_of_quints, nr_of_sexts
    global pr_nr_of_duplets, pr_nr_of_triplets, pr_nr_of_quads, pr_nr_of_quints, pr_nr_of_sexts
    global pr_nr_of_duplets_thisstart, pr_nr_of_triplets_thisstart, pr_nr_of_quads_thisstart, pr_nr_of_quints_thisstart, pr_nr_of_sexts_thisstart
    global last_N, N, stim_output_line, thisstart_outputline
    global rt_mean, rt_mean_p, acc_for_patterns, acc_for_the_whole, last_trial_in_block
	
    
    outfile_txt = codecs.open(thispath+'\\logs\\'+group+'_'+str(subject_nr)+'_'+identif+'_log.txt', 'a+', encoding = 'utf-8')
    RSI_timer = 0.0
    startfrom = thisperson_settings.get('last_N')
    N = startfrom + 1
    thisstart_N = 1

    trial_after_quit = '0' ###########################################################################
    
     
    if (startfrom+1) in sessionstarts:
        instructions()
        
    else:
        unexpectedquit()
        trial_after_quit = 0 ######################################################################
                
    relative_directions = []
    last_hand = ""
    
    Npressed_in_block = 0
    pressed_buttons = []
    stims_in_block = []
    accs_in_block  = []
    directions_in_block = []
    pr_directions_in_block = []
    previous_direction = []
    pr_previous_direction = []
    
    asrt_type = asrt_types[stim_sessionN[N]] 
    PCode, Pcode_str = which_code(stim_sessionN[N])
    
    allACC = 0
    patternERR = 0
    number_of_patterns = 0
    
    RT_pattern_list = []
    RT_all_list = []
    
    hand_dict = {1:'left', 2:'left', 3:'right', 4:'right'}
    
    thisstart_comb_freq = {}
    thisstart_context_freq = {}
    pr_thisstart_comb_freq = {}
    pr_thisstart_context_freq = {}

    trip_type_list = ['NA','L','H']
    quad_type_list = ['NA','L', 'H1', 'H2']
    quint_type_list = ['NA','La','Lb','H1a','H1b','H2']
    sext_type_list = ['NA','La','Lb','H1a','H1b-I','H1b-II','H2']
    type_lists = [trip_type_list, quad_type_list, quint_type_list, sext_type_list]

    anticip_trip, anticip_quad, anticip_quint, anticip_sext = '','','',''

    tempy = []
    thisstart_outputline = 0
    
    nr_of_duplets_thisstart, nr_of_triplets_thisstart, nr_of_quads_thisstart, nr_of_quints_thisstart, nr_of_sexts_thisstart = 0,0,0,0,0
    pr_nr_of_duplets_thisstart, pr_nr_of_triplets_thisstart, pr_nr_of_quads_thisstart, pr_nr_of_quints_thisstart, pr_nr_of_sexts_thisstart = 0,0,0,0,0

    while True:
                    
        stim_bg()
        mywindow.flip()
        
        RSI_clock.reset()
        RSI.start( RSI_time) 
        
        try:
            session_trial_num = N - sessionstarts[stim_sessionN[N]-1] + 1
        except:
            session_trial_num = "N/A"
         
        try:
            trial_after_quit += 1
            if trial_after_quit == 6:
                trial_after_quit = "0"
        except:
            trial_after_quit = "0"
        
        
        if stimpr[N] == 'P':
            if asrt_types[stim_sessionN[N]] == 'explicit':
                stimP.fillColor =  colors['stimp']
            else:
                stimP.fillColor =  colors['stimr']
            stimP.setPos(dict_pos[stimlist[N]])
        else:
            stimR.setPos(dict_pos[stimlist[N]])
        
        RSI.complete()  
        
        cycle = 0
        allACC = 0
        
        stims_in_block.append(stimlist[N])
        
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
            press = event.waitKeys(keyList = [key1,key2,key3,key4, key_quit], timeStamped = trial_clock)
            
            stim_RT_time = time.strftime('%H:%M:%S')
            stim_RT_date = time.strftime('%d/%m/%Y')
            stimRT = press[0][1]
            
            thisstart_outputline +=1
            stim_output_line += 1
            Npressed_in_block += 1

            if cycle == 1:
                stim_first_RT = press[0][1]
            
            stimbutton = press [0][0]
            stim_RSI = RSI_timer

            if press[0][0] == key_quit:
                print_to_screen("Quit...\nSaving data...")
                mywindow.flip()
                
                if stim_output_line > 1:
                    stim_quit ='userquit'
                outfile_txt.write('userquit')
                outfile_txt.close()

                stim_output_line -= 1
                
                if N>=1:
                    last_N = N-1
                    last_session = stim_sessionN[N-1]
                    last_trial_in_block = stimtrial[N-1]
                    last_epoch = stimepoch[N-1]
                    
                save_personal_info(thisperson_settings)
                core.quit() 
            
            elif pressed_dict[press[0][0]] == stimlist[N]:                
                stimACC = 0
                accs_in_block.append(0)
                pressed_buttons.append(pressed_dict[press[0][0]])
                
                if stimACC == allACC and Npressed_in_block > 1:
                    try:
                        if (stimlist[N] > stimlist[N-1]) :
                            directions_in_block.append(">")
                            previous_direction.append(">")
                        elif (stimlist[N] < stimlist[N-1]):
                            directions_in_block.append("<")
                            previous_direction.append("<")
                        elif (stimlist[N] == stimlist[N-1]) :
                            directions_in_block.append('R')
                    except:
                        pass

                if Npressed_in_block > 1:
                    try:
                        if (pressed_buttons[-1] > pressed_buttons[-2]) :
                            pr_directions_in_block.append(">")
                            pr_previous_direction.append('>')
                        elif (pressed_buttons[-1] < pressed_buttons[-2] ) :
                            pr_directions_in_block.append("<")
                            pr_previous_direction.append('<')
                        elif (pressed_buttons[-1] == pressed_buttons[-2])  :
                            pr_directions_in_block.append('R')
                    except:
                        pass
                    
                

                if stimpr[N] == 'P':
                    number_of_patterns +=1
                    RT_pattern_list.append(stimRT)
                RT_all_list.append(stimRT)
                
            else:
                stimACC = 1
                allACC += 1
                accs_in_block.append(1)

                pressed_buttons.append(pressed_dict[press[0][0]])
                if stimpr[N] == 'P':
                    patternERR +=1
                    number_of_patterns +=1
                    RT_pattern_list.append(stimRT)
                RT_all_list.append(stimRT)

                if stimACC == allACC and Npressed_in_block > 1:
                    try:
                        if (stimlist[N] > stimlist[N-1]) :
                            directions_in_block.append(">")
                            previous_direction.append(">")
                        elif  (stimlist[N] < stimlist[N-1]):
                            directions_in_block.append("<")
                            previous_direction.append("<")
                        elif (stimlist[N] == stimlist[N-1]) :
                            directions_in_block.append('R')
                    except:
                        pass
                        
                if Npressed_in_block > 1:
                    try:
                        if (pressed_buttons[-1] > pressed_buttons[-2] ) :
                            pr_directions_in_block.append(">")
                            pr_previous_direction.append('>')
                        elif  (pressed_buttons[-1] < pressed_buttons[-2]) :
                            pr_directions_in_block.append("<")
                            pr_previous_direction.append('<')
                        elif ( pressed_buttons[-1] == pressed_buttons[-2] ) :
                            pr_directions_in_block.append('R')
                    except:
                        pass
               
            stimbuttonnr = pressed_dict[ press [0][0] ]
            stim_allACC  = allACC

            akarmi = core.Clock()

           # kiszamitjuk, mik voltak a latott/nyomott kombinaciok (ingerhatosok szintjeig)

            stim_duplet, stim_triplet, stim_quartet, stim_quintet, stim_sextet = combos(stims_in_block)
            if stim_duplet != "" and stimACC == stim_allACC:
                nr_of_duplets += 1
                nr_of_duplets_thisstart += 1
            if stim_triplet != "" and stimACC == stim_allACC:
                nr_of_triplets += 1
                nr_of_triplets_thisstart += 1
            if stim_quartet != "" and stimACC == stim_allACC:
                nr_of_quads += 1
                nr_of_quads_thisstart += 1
            if stim_quintet != ""and stimACC == stim_allACC:
                nr_of_quints += 1
                nr_of_quints_thisstart += 1
            if stim_sextet != "" and stimACC == stim_allACC:
                nr_of_sexts += 1
                nr_of_sexts_thisstart += 1

            pressed_duplet, pressed_triplet, pressed_quad, pressed_quint, pressed_sext = combos(pressed_buttons)
            if pressed_duplet != "":
                pr_nr_of_duplets += 1
                pr_nr_of_duplets_thisstart += 1
            if pressed_triplet != "":
                pr_nr_of_triplets += 1
                pr_nr_of_triplets_thisstart += 1
            if pressed_quad != "":
                pr_nr_of_quads += 1
                pr_nr_of_quads_thisstart += 1
            if pressed_quint != "":
                pr_nr_of_quints += 1
                pr_nr_of_quints_thisstart += 1
            if pressed_sext != "":
                pr_nr_of_sexts += 1
                pr_nr_of_sexts_thisstart += 1

            # eltaroljuk, hogy ezek a latott/nyomott kombinaciok (es kontextusaik) hanyadszor fordulnak elo
            
            if stimACC == 0:
                update_occurences( mydict_whole = comb_freq, mydict_context = context_freq, current_com = stimlist[N])
                update_occurences( mydict_whole = comb_freq, mydict_context = context_freq, current_com = stim_duplet)
                update_occurences( mydict_whole = comb_freq, mydict_context = context_freq, current_com = stim_triplet)
                update_occurences( mydict_whole = comb_freq, mydict_context = context_freq, current_com = stim_quartet)
                update_occurences( mydict_whole = comb_freq, mydict_context = context_freq, current_com = stim_quintet)
                update_occurences( mydict_whole = comb_freq, mydict_context = context_freq, current_com = stim_sextet)

            update_occurences( mydict_whole = pr_comb_freq, mydict_context = pr_context_freq, current_com = pressed_dict[press[0][0]])
            update_occurences( mydict_whole = pr_comb_freq, mydict_context = pr_context_freq, current_com = pressed_duplet)
            update_occurences( mydict_whole = pr_comb_freq, mydict_context = pr_context_freq, current_com = pressed_triplet)
            update_occurences( mydict_whole = pr_comb_freq, mydict_context = pr_context_freq, current_com = pressed_quad)
            update_occurences( mydict_whole = pr_comb_freq, mydict_context = pr_context_freq, current_com = pressed_quint)
            update_occurences( mydict_whole = pr_comb_freq, mydict_context = pr_context_freq, current_com = pressed_sext)

            # ugyanez erre az inditasra vonatkoztatva csak

            if stimACC == 0:
                update_occurences( mydict_whole = thisstart_comb_freq, mydict_context = thisstart_context_freq, current_com = stimlist[N])
                update_occurences( mydict_whole = thisstart_comb_freq, mydict_context = thisstart_context_freq, current_com = stim_duplet)
                update_occurences( mydict_whole = thisstart_comb_freq, mydict_context = thisstart_context_freq, current_com = stim_triplet)
                update_occurences( mydict_whole = thisstart_comb_freq, mydict_context = thisstart_context_freq, current_com = stim_quartet)
                update_occurences( mydict_whole = thisstart_comb_freq, mydict_context = thisstart_context_freq, current_com = stim_quintet)
                update_occurences( mydict_whole = thisstart_comb_freq, mydict_context = thisstart_context_freq, current_com = stim_sextet)

            update_occurences( mydict_whole = pr_thisstart_comb_freq, mydict_context = pr_thisstart_context_freq, current_com = pressed_dict[press[0][0]])
            update_occurences( mydict_whole = pr_thisstart_comb_freq, mydict_context = pr_thisstart_context_freq, current_com = pressed_duplet)
            update_occurences( mydict_whole = pr_thisstart_comb_freq, mydict_context = pr_thisstart_context_freq, current_com = pressed_triplet)
            update_occurences( mydict_whole = pr_thisstart_comb_freq, mydict_context = pr_thisstart_context_freq, current_com = pressed_quad)
            update_occurences( mydict_whole = pr_thisstart_comb_freq, mydict_context = pr_thisstart_context_freq, current_com = pressed_quint)
            update_occurences( mydict_whole = pr_thisstart_comb_freq, mydict_context = pr_thisstart_context_freq, current_com = pressed_sext)

            # kiszamoljuk, hogy akkor mi a jelenlegi freq, és mi a probability
            # minden esetben az eddigi elofordulast szamszerusitjuk, a jelenlegi nelkul
            # ehhez kell tudunk, hanyadik az inger  # N tarolja
            # es hanyadik a buttonpress # stim_output_line tárolja
           
            sing_freq, sing_prob = freqs_and_probs(         my_dict_stim = comb_freq, my_dict_context = context_freq, stim_comb = stimlist[N], numb = N)
            dup_freq, dup_prob = freqs_and_probs(          my_dict_stim = comb_freq, my_dict_context = context_freq, stim_comb = stim_duplet, numb = nr_of_duplets)
            trip_freq, trip_prob = freqs_and_probs(           my_dict_stim = comb_freq, my_dict_context = context_freq, stim_comb = stim_triplet, numb = nr_of_triplets)
            quad_freq, quad_prob = freqs_and_probs(      my_dict_stim = comb_freq, my_dict_context = context_freq, stim_comb = stim_quartet, numb = nr_of_quads)
            quint_freq, quint_prob = freqs_and_probs(      my_dict_stim = comb_freq, my_dict_context = context_freq, stim_comb = stim_quintet, numb = nr_of_quints)
            sext_freq, sext_prob = freqs_and_probs(           my_dict_stim = comb_freq, my_dict_context = context_freq, stim_comb = stim_sextet, numb = nr_of_sexts)
              
            pr_sing_freq, pr_sing_prob = freqs_and_probs(my_dict_stim = pr_comb_freq, my_dict_context = pr_context_freq, stim_comb = pressed_dict[press[0][0]], numb = stim_output_line)
            pr_dup_freq, pr_dup_prob = freqs_and_probs(my_dict_stim = pr_comb_freq, my_dict_context = pr_context_freq, stim_comb = pressed_duplet, numb = pr_nr_of_duplets)
            pr_trip_freq, pr_trip_prob = freqs_and_probs(my_dict_stim = pr_comb_freq, my_dict_context = pr_context_freq, stim_comb = pressed_triplet, numb = pr_nr_of_triplets)
            pr_quad_freq, pr_quad_prob = freqs_and_probs(my_dict_stim = pr_comb_freq, my_dict_context = pr_context_freq, stim_comb = pressed_quad, numb = pr_nr_of_quads)
            pr_quint_freq, pr_quint_prob = freqs_and_probs(my_dict_stim = pr_comb_freq, my_dict_context = pr_context_freq, stim_comb = pressed_quint, numb = pr_nr_of_quints)
            pr_sext_freq, pr_sext_prob = freqs_and_probs(my_dict_stim = pr_comb_freq, my_dict_context = pr_context_freq, stim_comb = pressed_sext, numb = pr_nr_of_sexts)
           
            
            sing_dif_freq,       sing_dif_prob =      difs(freq= sing_freq,    freq_pr =  pr_sing_freq,       prob = sing_prob,          prob_pr = pr_sing_prob)
            dup_dif_freq,        dup_dif_prob =       difs(freq=  dup_freq,    freq_pr =  pr_dup_freq,        prob = dup_prob,         prob_pr = pr_dup_prob)
            trip_dif_freq,        trip_dif_prob =        difs(freq= trip_freq,     freq_pr =  pr_trip_freq,        prob = trip_prob,          prob_pr = pr_trip_prob)
            quad_dif_freq,     quad_dif_prob =      difs(freq= quad_freq,  freq_pr =  pr_quad_freq,     prob = quad_prob,        prob_pr = pr_quad_prob)
            quint_dif_freq,     quint_dif_prob =     difs(freq= quint_freq,  freq_pr =  pr_quint_freq,     prob = quint_prob,       prob_pr = pr_quint_prob)
            sext_dif_freq,        sext_dif_prob =       difs(freq= sext_freq,    freq_pr =  pr_sext_freq,        prob = sext_prob,         prob_pr = pr_sext_prob)
                

            #ugyanez csak erre az inditasra vonatkoztatva
            
            thisstart_sing_freq, thisstart_sing_prob = freqs_and_probs(       my_dict_stim = thisstart_comb_freq, my_dict_context = thisstart_context_freq, stim_comb = stimlist[N], numb = thisstart_N) # helyett az kene, h inditas ota hanyadik
            thisstart_dup_freq, thisstart_dup_prob = freqs_and_probs(       my_dict_stim = thisstart_comb_freq, my_dict_context = thisstart_context_freq, stim_comb = stim_duplet, numb = nr_of_duplets_thisstart) # helyett az kene, h inditas ota hanyadik
            thisstart_trip_freq, thisstart_trip_prob = freqs_and_probs(        my_dict_stim = thisstart_comb_freq, my_dict_context = thisstart_context_freq, stim_comb = stim_triplet, numb = nr_of_triplets_thisstart)
            thisstart_quad_freq, thisstart_quad_prob = freqs_and_probs(   my_dict_stim = thisstart_comb_freq, my_dict_context = thisstart_context_freq, stim_comb = stim_quartet, numb = nr_of_quads_thisstart)
            thisstart_quint_freq, thisstart_quint_prob = freqs_and_probs(   my_dict_stim = thisstart_comb_freq, my_dict_context = thisstart_context_freq, stim_comb = stim_quintet, numb = nr_of_quints_thisstart)
            thisstart_sext_freq, thisstart_sext_prob = freqs_and_probs(        my_dict_stim = thisstart_comb_freq, my_dict_context = thisstart_context_freq, stim_comb = stim_sextet, numb = nr_of_sexts_thisstart)
              
            pr_thisstart_sing_freq, pr_thisstart_sing_prob = freqs_and_probs(     my_dict_stim = pr_thisstart_comb_freq, my_dict_context = pr_thisstart_context_freq, stim_comb = pressed_dict[press[0][0]], numb = thisstart_outputline)
            pr_thisstart_dup_freq, pr_thisstart_dup_prob = freqs_and_probs(     my_dict_stim = pr_thisstart_comb_freq, my_dict_context = pr_thisstart_context_freq, stim_comb = pressed_duplet, numb = pr_nr_of_duplets_thisstart)
            pr_thisstart_trip_freq, pr_thisstart_trip_prob = freqs_and_probs(      my_dict_stim = pr_thisstart_comb_freq, my_dict_context = pr_thisstart_context_freq, stim_comb = pressed_triplet, numb = pr_nr_of_triplets_thisstart)
            pr_thisstart_quad_freq, pr_thisstart_quad_prob = freqs_and_probs( my_dict_stim = pr_thisstart_comb_freq, my_dict_context = pr_thisstart_context_freq, stim_comb = pressed_quad, numb = pr_nr_of_quads_thisstart)
            pr_thisstart_quint_freq, pr_thisstart_quint_prob = freqs_and_probs(my_dict_stim = pr_thisstart_comb_freq, my_dict_context = pr_thisstart_context_freq, stim_comb = pressed_quint, numb = pr_nr_of_quints_thisstart)
            pr_thisstart_sext_freq, pr_thisstart_sext_prob = freqs_and_probs(     my_dict_stim = pr_thisstart_comb_freq, my_dict_context = pr_thisstart_context_freq, stim_comb = pressed_sext, numb = pr_nr_of_sexts_thisstart)

            thisstart_sing_dif_freq,    thisstart_sing_dif_prob =         difs(   freq= thisstart_sing_freq,   freq_pr =  pr_thisstart_sing_freq,    prob = thisstart_sing_prob,       prob_pr = pr_thisstart_sing_prob)
            thisstart_dup_dif_freq,     thisstart_dup_dif_prob =         difs(   freq= thisstart_dup_freq,    freq_pr =  pr_thisstart_dup_freq,     prob = thisstart_dup_prob,        prob_pr = pr_thisstart_dup_prob)
            thisstart_trip_dif_freq,      thisstart_trip_dif_prob =         difs(   freq= thisstart_trip_freq,    freq_pr =  pr_thisstart_trip_freq,      prob = thisstart_trip_prob,        prob_pr = pr_thisstart_trip_prob)
            thisstart_quad_dif_freq,    thisstart_quad_dif_prob =      difs(   freq= thisstart_quad_freq, freq_pr =  pr_thisstart_quad_freq,   prob = thisstart_quad_prob,     prob_pr = pr_thisstart_quad_prob)
            thisstart_quint_dif_freq,    thisstart_quint_dif_prob =     difs(   freq= thisstart_quint_freq, freq_pr =  pr_thisstart_quint_freq,   prob = thisstart_quint_prob,     prob_pr = pr_thisstart_quint_prob) 
            thisstart_sext_dif_freq,      thisstart_sext_dif_prob =        difs(   freq= thisstart_sext_freq,   freq_pr =  pr_thisstart_sext_freq,      prob = thisstart_sext_prob,       prob_pr = pr_thisstart_sext_prob)

            # ellenorizzuk hogy a megelozo trialek pontosak voltak-e

            last_five_accurate, last_four_accurate, last_three_accurate, last_two_accurate, last_one_accurate  = previous_accuracy(accs_in_block)
      
            abs1 = abstract_structure(listfrom = stims_in_block, howmany = 1)
            abs2 = abstract_structure(listfrom = stims_in_block, howmany = 2)
            abs3 = abstract_structure(listfrom = stims_in_block, howmany = 3)
            abs4 = abstract_structure(listfrom = stims_in_block, howmany = 4)
            abs5 = abstract_structure(listfrom = stims_in_block, howmany = 5)
            abs6 = abstract_structure(listfrom = stims_in_block, howmany = 6)

            pr_abs1 = abstract_structure(listfrom = pressed_buttons, howmany = 1)
            pr_abs2 = abstract_structure(listfrom = pressed_buttons, howmany = 2)
            pr_abs3 = abstract_structure(listfrom = pressed_buttons, howmany = 3)
            pr_abs4 = abstract_structure(listfrom = pressed_buttons, howmany = 4)
            pr_abs5 = abstract_structure(listfrom = pressed_buttons, howmany = 5)
            pr_abs6 = abstract_structure(listfrom = pressed_buttons, howmany = 6)

            if abs3 in ('aba','aaa'):
                tripfilter = 0
            elif abs3 == '':
                tripfilter= ''
            else:
                tripfilter = 1
                
            if abs4 in ('acba', 'dcba', 'cbba'):
                quadfilter = 1
            elif abs4 == '':
                quadfilter = ''
            else:
                quadfilter = 0
                
            if pr_abs3 in ('aba','aaa'):
                pr_tripfilter = 0
            elif pr_abs3 == '':
                pr_tripfilter= ''
            else:
                pr_tripfilter = 1
                
            if pr_abs4 in ('acba', 'dcba', 'cbba'):
                pr_quadfilter = 1
            elif pr_abs4 == '':
                pr_quadfilter = ''
            else:
                pr_quadfilter = 0


            d1, d2, d3, d4, d5 = directions_def(listfrom = directions_in_block)
            pr_d1, pr_d2, pr_d3, pr_d4, pr_d5 = directions_def(listfrom = pr_directions_in_block)
            
            rel_five     = reldir(howmany= 5, listfrom = directions_in_block, lastdlist = previous_direction)
            rel_four    = reldir(howmany= 4, listfrom = directions_in_block, lastdlist = previous_direction)
            rel_three   = reldir(howmany= 3, listfrom = directions_in_block, lastdlist = previous_direction)
            rel_two      = reldir(howmany= 2, listfrom = directions_in_block, lastdlist = previous_direction)
            rel_one      = reldir(howmany= 1, listfrom = directions_in_block, lastdlist = previous_direction)

            pr_rel_five     = reldir(howmany= 5, listfrom = pr_directions_in_block, lastdlist = pr_previous_direction)
            pr_rel_four    = reldir(howmany= 4, listfrom = pr_directions_in_block, lastdlist = pr_previous_direction)
            pr_rel_three   = reldir(howmany= 3, listfrom = pr_directions_in_block, lastdlist = pr_previous_direction)
            pr_rel_two      = reldir(howmany= 2, listfrom = pr_directions_in_block, lastdlist = pr_previous_direction)
            pr_rel_one      = reldir(howmany= 1, listfrom = pr_directions_in_block, lastdlist = pr_previous_direction)

            handchange = hand_changing(listfrom = stims_in_block, handdict = hand_dict)
            pr_handchange = hand_changing(listfrom = pressed_buttons, handdict = hand_dict)
        
            currentT, currentTT, currentQ, currentQT, currentQi, currentQiT, currenctS, currentST = otherseq(codenum = Pcode_str, listfrom = stims_in_block)
            pr_currentT, pr_currentTT, pr_currentQ, pr_currentQT, pr_currentQi, pr_currentQiT, pr_currenctS, pr_currentST = otherseq(codenum = Pcode_str, listfrom = pressed_buttons)
    
            obs_pr_trip_moved_category = whether_anticip(type1 = currentTT, type2 = pr_currentTT, mylist = trip_type_list)
            obs_pr_quad_moved_category = whether_anticip(type1 = currentQT, type2 = pr_currentQT, mylist = quad_type_list)
            obs_pr_quint_moved_category = whether_anticip(type1 = currentQiT, type2 = pr_currentQiT, mylist = quint_type_list)
            obs_pr_sext_moved_category = whether_anticip(type1 = currentST, type2 = pr_currentST, mylist = sext_type_list)
                        
            obs_pr_trip, obs_pr_quad, obs_pr_quint, obs_pr_sext = '','','',''
            if  currentTT != '' and pr_currentTT != '':
                obs_pr_trip = currentTT + '_' + pr_currentTT
            if  currentQT != '' and pr_currentQT != '':
                obs_pr_quad = currentQT + '_' + pr_currentQT
            if currentQiT != '' and pr_currentQiT != '':
                obs_pr_quint = currentQiT + '_' + pr_currentQiT
            if currentST != '' and pr_currentT != '':
                obs_pr_sext = currentST + '_' + pr_currentST
                
            P1_trip, P1_tripT, P1_quad, P1_quadT, P1_quint, P1_quintT, P1_sext, P1_sextT = otherseq(codenum = "1234", listfrom = stims_in_block)
            P2_trip, P2_tripT, P2_quad, P2_quadT, P2_quint, P2_quintT, P2_sext, P2_sextT = otherseq(codenum = "1243", listfrom = stims_in_block)
            P3_trip, P3_tripT, P3_quad, P3_quadT, P3_quint, P3_quintT, P3_sext, P3_sextT = otherseq(codenum = "1324",listfrom = stims_in_block)
            P4_trip, P4_tripT, P4_quad, P4_quadT, P4_quint, P4_quintT, P4_sext, P4_sextT = otherseq(codenum = "1342", listfrom = stims_in_block)
            P5_trip, P5_tripT, P5_quad, P5_quadT, P5_quint, P5_quintT, P5_sext, P5_sextT = otherseq(codenum = "1423", listfrom = stims_in_block)
            P6_trip, P6_tripT, P6_quad, P6_quadT, P6_quint, P6_quintT, P6_sext, P6_sextT = otherseq(codenum = "1432", listfrom = stims_in_block)

            prP1_trip, prP1_tripT, prP1_quad, prP1_quadT, prP1_quint, prP1_quintT, prP1_sext, prP1_sextT = otherseq(codenum = "1234", listfrom = pressed_buttons)
            prP2_trip, prP2_tripT, prP2_quad, prP2_quadT, prP2_quint, prP2_quintT, prP2_sext, prP2_sextT = otherseq(codenum = "1243", listfrom = pressed_buttons)
            prP3_trip, prP3_tripT, prP3_quad, prP3_quadT, prP3_quint, prP3_quintT, prP3_sext, prP3_sextT = otherseq(codenum = "1324",listfrom = pressed_buttons)
            prP4_trip, prP4_tripT, prP4_quad, prP4_quadT, prP4_quint, prP4_quintT, prP4_sext, prP4_sextT = otherseq(codenum = "1342", listfrom = pressed_buttons)
            prP5_trip, prP5_tripT, prP5_quad, prP5_quadT, prP5_quint, prP5_quintT, prP5_sext, prP5_sextT = otherseq(codenum = "1423", listfrom = pressed_buttons)
            prP6_trip, prP6_tripT, prP6_quad, prP6_quadT, prP6_quint, prP6_quintT, prP6_sext, prP6_sextT = otherseq(codenum = "1432", listfrom = pressed_buttons)
        
            temporary_typelist_current = [currentTT, currentQT, currentQiT, currentST]

            temporary_typelist = [[P1_tripT, P1_quadT, P1_quintT, P1_sextT] ,
                                                    [P2_tripT, P2_quadT, P2_quintT, P2_sextT] ,
                                                    [P3_tripT, P3_quadT, P3_quintT, P3_sextT] ,
                                                    [P4_tripT, P4_quadT, P4_quintT, P4_sextT] ,
                                                    [P5_tripT, P5_quadT, P5_quintT, P5_sextT] ,
                                                    [P6_tripT, P6_quadT, P6_quintT, P6_sextT] ]
                        
            grouped_trip = grouped_types(mylist = temporary_typelist, structure = 3)
            grouped_quad = grouped_types(mylist = temporary_typelist, structure = 4)
            grouped_quint = grouped_types(mylist = temporary_typelist, structure = 5)
            grouped_sext = grouped_types(mylist = temporary_typelist, structure = 6)

            pr_temporary_typelist = [[prP1_tripT, prP1_quadT, prP1_quintT, prP1_sextT] ,
                                                    [prP2_tripT, prP2_quadT, prP2_quintT, prP2_sextT] ,
                                                    [prP3_tripT, prP3_quadT, prP3_quintT, prP3_sextT] ,
                                                    [prP4_tripT, prP4_quadT, prP4_quintT, prP4_sextT] ,
                                                    [prP5_tripT, prP5_quadT, prP5_quintT, prP5_sextT] ,
                                                    [prP6_tripT, prP6_quadT, prP6_quintT, prP6_sextT] ]

            pr_grouped_trip = grouped_types(mylist = pr_temporary_typelist, structure = 3)
            pr_grouped_quad = grouped_types(mylist = pr_temporary_typelist, structure = 4)
            pr_grouped_quint = grouped_types(mylist = pr_temporary_typelist, structure = 5)
            pr_grouped_sext = grouped_types(mylist = pr_temporary_typelist, structure = 6)
           
            
            all_anticips = []
            all_category_moves = []
            for kod in range(6):
                allista_type = []
                allista_move = []
                for tipus in range(4):
                    if pr_temporary_typelist[kod][tipus] != '' and temporary_typelist_current[tipus] != '':
                        allista_type.append(temporary_typelist_current[tipus] + '_' + pr_temporary_typelist[kod][tipus])
                        allista_move.append(    whether_anticip (type1 = temporary_typelist_current[tipus], type2 =  pr_temporary_typelist[kod][tipus], mylist = type_lists[tipus]) )       
                    else:
                        allista_type.append('')
                        allista_move.append('')
                
                all_anticips.append(allista_type[:])
                all_category_moves.append(allista_move[:])

            relevant_anticips = []
            relevant_moves = []
            for mypcode in PCode_types.split('='):
                relevant_anticips.append(all_anticips[int(mypcode)-1])
                relevant_moves.append(all_category_moves[int(mypcode)-1])

            tempy = [computer_name,
                        group,
                        identif,
                        subject_nr,
                        asrt_type,
                        PCode,
                        PCode_types,

                        stim_output_line, 
                        thisstart_outputline,
                        N, 
                        session_trial_num,
                        thisstart_N,

                        trial_after_quit,

                        stim_sessionN[N], 
                        stimepoch[N],  
                        stimblock[N], 
                        stimtrial[N],  

                        stim_RSI, 
                        frame_rate,
                        frame_time,
                        frame_sd,
                        stim_RT_time ,
                        stim_RT_date ,

                        stim_colorN[N],
                        stimpr[N], 
                        stimRT, 
                        stimACC, 
                        stim_allACC, 
                        last_one_accurate,
                        last_two_accurate, 
                        last_three_accurate, 
                        last_four_accurate,
                        last_five_accurate,

                        # innen ism

                        tripfilter,
                        quadfilter,

                        stimlist[N], 
                        stim_duplet,
                        stim_triplet,
                        stim_quartet,
                        stim_quintet,
                        stim_sextet,

                        str(sing_freq)[:5],
                        str(dup_freq)[:5],
                        str(trip_freq)[:5],
                        str(quad_freq)[:5],
                        str(quint_freq)[:5],
                        str(sext_freq)[:5],

                        str(sing_prob)[:5],
                        str(dup_prob)[:5],
                        str(trip_prob)[:5],
                        str(quad_prob)[:5],
                        str(quint_prob)[:5],
                        str(sext_prob)[:5],

                        str(thisstart_sing_freq)[:5],
                        str(thisstart_dup_freq)[:5],
                        str(thisstart_trip_freq)[:5],
                        str(thisstart_quad_freq)[:5],
                        str(thisstart_quint_freq)[:5],
                        str(thisstart_sext_freq)[:5],

                        str(thisstart_sing_prob)[:5],
                        str(thisstart_dup_prob)[:5],
                        str(thisstart_trip_prob)[:5],
                        str(thisstart_quad_prob)[:5],
                        str(thisstart_quint_prob)[:5],
                        str(thisstart_sext_prob)[:5],


                        handchange,
                        abs2,
                        abs3,
                        abs4,
                        abs5,
                        abs6,

                        d1,
                        d2,
                        d3,
                        d4,
                        d5,

                        rel_one,
                        rel_two,
                        rel_three,
                        rel_four,
                        rel_five,

                        rel_one.upper(),
                        rel_two.upper(),
                        rel_three.upper(),
                        rel_four.upper(),
                        rel_five.upper(),
                
                        currentTT,
                        currentQT,
                        currentQiT,
                        currentST,
                        
                        grouped_trip,
                        grouped_quad,
                        grouped_quint,
                        grouped_sext,

                        P1_trip,
                        P1_tripT,
                        P1_quad,
                        P1_quadT,
                        P1_quint,
                        P1_quintT,
                        P1_sext,
                        P1_sextT,

                        P2_trip,
                        P2_tripT,
                        P2_quad,
                        P2_quadT,
                        P2_quint,
                        P2_quintT,
                        P2_sext,
                        P2_sextT,

                        P3_trip,
                        P3_tripT,
                        P3_quad,
                        P3_quadT,
                        P3_quint,
                        P3_quintT,
                        P3_sext,
                        P3_sextT,

                        P4_trip,
                        P4_tripT,
                        P4_quad,
                        P4_quadT,
                        P4_quint,
                        P4_quintT,
                        P4_sext,
                        P4_sextT,

                        P5_trip,
                        P5_tripT,
                        P5_quad,
                        P5_quadT,
                        P5_quint,
                        P5_quintT,
                        P5_sext,
                        P5_sextT,

                        P6_trip,
                        P6_tripT,
                        P6_quad,
                        P6_quadT,
                        P6_quint,
                        P6_quintT,
                        P6_sext,
                        P6_sextT,


                        # ez csak erre vonatkozik
                        stimbutton, 
                        
                        # es ide a duplazasok
                        # innen ism

                        pr_tripfilter,
                        pr_quadfilter,

                        pressed_dict[press[0][0]],  # ey mi
                        pressed_duplet,
                        pressed_triplet,
                        pressed_quad,
                        pressed_quint,
                        pressed_sext,

                        str(pr_sing_freq)[:5],
                        str(pr_dup_freq)[:5],
                        str(pr_trip_freq)[:5],
                        str(pr_quad_freq)[:5],
                        str(pr_quint_freq)[:5],
                        str(pr_sext_freq)[:5],

                        str(pr_sing_prob)[:5],
                        str(pr_dup_prob)[:5],
                        str(pr_trip_prob)[:5],
                        str(pr_quad_prob)[:5],
                        str(pr_quint_prob)[:5],
                        str(pr_sext_prob)[:5],

                        str(pr_thisstart_sing_freq)[:5],
                        str(pr_thisstart_dup_freq)[:5],
                        str(pr_thisstart_trip_freq)[:5],
                        str(pr_thisstart_quad_freq)[:5],
                        str(pr_thisstart_quint_freq)[:5],
                        str(pr_thisstart_sext_freq)[:5],

                        str(pr_thisstart_sing_prob)[:5],
                        str(pr_thisstart_dup_prob)[:5],
                        str(pr_thisstart_trip_prob)[:5],
                        str(pr_thisstart_quad_prob)[:5],
                        str(pr_thisstart_quint_prob)[:5],
                        str(pr_thisstart_sext_prob)[:5],

                        pr_handchange,
                        pr_abs2,
                        pr_abs3,
                        pr_abs4,
                        pr_abs5,
                        pr_abs6,

                        pr_d1,
                        pr_d2,
                        pr_d3,
                        pr_d4,
                        pr_d5,

                        pr_rel_one,
                        pr_rel_two,
                        pr_rel_three,
                        pr_rel_four,
                        pr_rel_five,

                        pr_rel_one.upper(),
                        pr_rel_two.upper(),
                        pr_rel_three.upper(),
                        pr_rel_four.upper(),
                        pr_rel_five.upper(),
                
                        pr_currentTT,
                        pr_currentQT,
                        pr_currentQiT,
                        pr_currentST,
                        
                        pr_grouped_trip,
                        pr_grouped_quad,
                        pr_grouped_quint,
                        pr_grouped_sext,

                        prP1_trip,
                        prP1_tripT,
                        prP1_quad,
                        prP1_quadT,
                        prP1_quint,
                        prP1_quintT,
                        prP1_sext,
                        prP1_sextT,

                        prP2_trip,
                        prP2_tripT,
                        prP2_quad,
                        prP2_quadT,
                        prP2_quint,
                        prP2_quintT,
                        prP2_sext,
                        prP2_sextT,

                        prP3_trip,
                        prP3_tripT,
                        prP3_quad,
                        prP3_quadT,
                        prP3_quint,
                        prP3_quintT,
                        prP3_sext,
                        prP3_sextT,

                        prP4_trip,
                        prP4_tripT,
                        prP4_quad,
                        prP4_quadT,
                        prP4_quint,
                        prP4_quintT,
                        prP4_sext,
                        prP4_sextT,

                        prP5_trip,
                        prP5_tripT,
                        prP5_quad,
                        prP5_quadT,
                        prP5_quint,
                        prP5_quintT,
                        prP5_sext,
                        prP5_sextT,

                        prP6_trip,
                        prP6_tripT,
                        prP6_quad,
                        prP6_quadT,
                        prP6_quint,
                        prP6_quintT,
                        prP6_sext,
                        prP6_sextT,

                        # observed es pressed viszonya

                        obs_pr_trip,
                        obs_pr_quad,
                        obs_pr_quint,
                        obs_pr_sext,
                        
                        obs_pr_trip_moved_category,
                        obs_pr_quad_moved_category,
                        obs_pr_quint_moved_category,
                        obs_pr_sext_moved_category,
                        
                        sing_dif_freq,
                        dup_dif_freq,
                        trip_dif_freq,
                        quad_dif_freq,
                        quint_dif_freq,
                        sext_dif_freq,
                        
                        sing_dif_prob,
                        dup_dif_prob,
                        trip_dif_prob,
                        quad_dif_prob,
                        quint_dif_prob,
                        sext_dif_prob,

                        thisstart_sing_dif_freq,
                        thisstart_dup_dif_freq,
                        thisstart_trip_dif_freq,
                        thisstart_quad_dif_freq,
                        thisstart_quint_dif_freq,
                        thisstart_sext_dif_freq,
                        
                        thisstart_sing_dif_prob,
                        thisstart_dup_dif_prob,
                        thisstart_trip_dif_prob,
                        thisstart_quad_dif_prob,
                        thisstart_quint_dif_prob,
                        thisstart_sext_dif_prob ]

            for relevant in relevant_anticips:
                for k in range(4):
                    tempy.append(relevant[k])
                    
            for relevant in relevant_moves:
                for k in range(4):
                    tempy.append(relevant[k])
                                    
            outfile_txt.write('\n')
            for t in tempy:
                try:
                    t = str(t)
                    t = t.replace('.',',')
                    outfile_txt.write(t+'\t')
                except:
                    outfile_txt.write(t+'\t')
            
            if stimACC== 0:
                last_N = N
                last_session = stim_sessionN[N]
                last_trial_in_block = stimtrial[N]
                last_epoch = stimepoch[N]
                N += 1
                thisstart_N += 1

                break
            
        print (akarmi.getTime())

        if N in blockstarts: # n+1 volt
            
            print_to_screen(u"Adatok mentése és visszajelzés előkészítése...")
            mywindow.flip()

#            # random, implicit
            try:
                acc_for_patterns = 100*float( number_of_patterns - patternERR) / number_of_patterns
                acc_for_patterns_str = str(acc_for_patterns)[0:5].replace('.',',') + ' %'
            except:
                acc_for_patterns = "N/A"
                acc_for_patterns_str = "N/A"

            try:
                acc_for_the_whole = 100*float( Npressed_in_block - sum(accs_in_block)) / Npressed_in_block
                acc_for_the_whole_str = str(acc_for_the_whole)[0:5].replace('.',',') + ' %'  # ezzel nem kezdek semmit latszolag
                
            except:
                acc_for_the_whole = 'N/A'
                acc_for_the_whole_str = 'N/A'
            
            try:
                rt_mean = float( sum(RT_all_list)) / len(RT_all_list)
                rt_mean_str = str(rt_mean)[:5].replace('.',',')
            except:
                rt_mean = 'N/A'
                rt_mean_str = 'N/A'
                
            try:
                rt_mean_p =  float( sum(RT_pattern_list)) / len(RT_pattern_list)
                rt_mean_p_str = str(rt_mean_p)[:5].replace('.',',')
            except:
                rt_mean_p = 'N/A'
                rt_mean_p = 'N/A'


            if asrt_types[stim_sessionN[N-1]] == 'explicit':
                whatnow = feedback_explicit(rt_m = rt_mean_str, rt_m_p = rt_mean_p_str, acc_for_p = acc_for_patterns_str, acc_for_the_w = acc_for_the_whole_str )
            else:
                whatnow = feedback_implicit(rt_mean_str, acc_for_the_whole_str)

            if whatnow == 'continue':
                pass
            elif whatnow == 'quit':
                print_to_screen("Quit...\nSaving data...")
                mywindow.flip()
                
                if stim_output_line > 1:
                    stim_quit ='userquit'
                outfile_txt.write('userquit')
                outfile_txt.close()
                
                if N>=1:
                    last_N = N-1
                    last_session = stim_sessionN[N-1]
                    last_trial_in_block = stimtrial[N-1]
                    last_epoch = stimepoch[N-1]
                    
                save_personal_info(thisperson_settings)
                core.quit() 
            else:
                print('wtf')
                
            patternERR = 0
            allACC = 0
            Npressed_in_block = 0
            
            RT_pattern_list = []
            RT_all_list = []
            
            stims_in_block = []
            pressed_buttons  = []
            
            accs_in_block  = []
            
            directions_in_block = []
            pr_directions_in_block = []
            previous_direction = []
            pr_previous_direction = []

        if N  == end_at[N-1]:
            break
    outfile_txt.close()

# some constants and dictionaries

thispath = '\\'.join( os.path.realpath(__file__).split('\\')[:-1])
dict_accents = {u'á':u'a',u'é':u'e',u'í':u'i',u'ó':u'o',u'ő':u'o',u'ö':u'o',u'ú':u'u',u'ű':u'u',u'ü':u'u'}

sequences_PCode = { 1 : 1234, 2 : 1243, 3 : 1324, 4 : 1342, 5 : 1423, 6 : 1432 }
sequence_highs = {}
sequence_highs_long = {}
for i in [1,2,3,4,5,6]:
    temp = []
    for k in [1,2,3,4]:
        temp.append(str(sequences_PCode[i])[0]+str(k)+str(sequences_PCode[i])[1])
        temp.append(str(sequences_PCode[i])[1]+str(k)+str(sequences_PCode[i])[2])
        temp.append(str(sequences_PCode[i])[2]+str(k)+str(sequences_PCode[i])[3])
        temp.append(str(sequences_PCode[i])[3]+str(k)+str(sequences_PCode[i])[0])
    sequence_highs[i] = temp[:]
    sequence_highs_long[sequences_PCode[i]] = temp[:]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# vezerles
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main():
    global groups, numsessions, blockprepN, blocklengthN, block_in_epochN, epochN, epochs, monitor_width, computer_name, asrt_distance, asrt_size, asrt_rcolor, asrt_pcolor, asrt_background, asrt_circle_background, refreshrate, key1, key2, key3, key4, key_quit, whether_warning, speed_warning, acc_warning, RSI_time, maxtrial, sessionstarts, blockstarts, asrt_types
    global colors
    global insts, feedback_exp, feedback_imp, feedback_speed, feedback_accuracy, ending, unexp_quit
    global thisperson_settings, group, subject_nr, identif
    global nr_of_duplets, nr_of_triplets, nr_of_quads, nr_of_quints, nr_of_sexts, pr_nr_of_duplets, pr_nr_of_triplets, pr_nr_of_quads, pr_nr_of_quints, pr_nr_of_sexts, context_freq, comb_freq, pr_context_freq, pr_comb_freq, PCodes, PCode_types, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, last_N, end_at, stim_colorN, stim_quit
    global mywindow, xtext, pressed_dict, RSI, RSI_clock, trial_clock, dict_pos
    global stimbg, stimP, stimR, stim_pressed
    global frame_time, frame_sd, frame_rate

    ensure_dir(os.path.join(thispath, "logs"))
    ensure_dir(os.path.join(thispath, "settings"))
    groups, numsessions, blockprepN, blocklengthN, block_in_epochN, epochN, epochs, monitor_width, computer_name, asrt_distance, asrt_size, asrt_rcolor, asrt_pcolor, asrt_background, asrt_circle_background, refreshrate, key1, key2, key3, key4, key_quit, whether_warning, speed_warning, acc_warning, RSI_time, maxtrial, sessionstarts, blockstarts, asrt_types = all_settings_def()
    dimension_x, dimension_y, my_monitor = monitor_settings()

    colors = { 'wincolor' : asrt_background, 'linecolor':'black', 'stimp':asrt_pcolor, 'stimr':asrt_rcolor}

    inst_feedback_path = os.path.join(thispath, "inst_and_feedback.txt")
    insts, feedback_exp, feedback_imp, feedback_speed, feedback_accuracy, ending, unexp_quit = read_instructions(inst_feedback_path)

    thisperson_settings, group, subject_nr, identif = participant_id()
    nr_of_duplets, nr_of_triplets, nr_of_quads, nr_of_quints, nr_of_sexts, pr_nr_of_duplets, pr_nr_of_triplets, pr_nr_of_quads, pr_nr_of_quints, pr_nr_of_sexts, context_freq, comb_freq, pr_context_freq, pr_comb_freq, PCodes, PCode_types, stim_output_line, stim_sessionN, stimepoch, stimblock, stimtrial, stimlist, stimpr, last_N, end_at, stim_colorN, stim_quit = get_thisperson_settings()

    # Ablak és ingerek felépítése az ismert beállítások szerint
    mywindow = visual.Window (size = (dimension_x, dimension_y), color = colors['wincolor'], fullscr = False, monitor = my_monitor, units = "cm")

    xtext = visual.TextStim(mywindow, text = u"", units = "cm", height = 0.6, color = "black")

    pressed_dict ={key1:1,key2:2,key3:3,key4:4}

    RSI = core.StaticPeriod(screenHz=refreshrate)
    RSI_clock = core.Clock()
    trial_clock = core.Clock()

    dict_pos = { 1:  ( float(asrt_distance)*(-1.5), 0),
                 2:  ( float(asrt_distance)*(-0.5), 0),
                 3:  ( float(asrt_distance)*  0.5,   0),
                 4:  ( float(asrt_distance)*  1.5,   0) }

    stimbg = visual.Circle( win = mywindow, radius = 1, units = "cm", fillColor = None, lineColor = colors['linecolor'])
    stimP = visual.Circle( win = mywindow, radius = asrt_size, units = "cm", fillColor = colors['stimp'], lineColor = colors['linecolor'], pos = dict_pos[1])
    stimR = visual.Circle( win = mywindow, radius = asrt_size, units = "cm", fillColor = colors['stimr'], lineColor = colors['linecolor'], pos = dict_pos[1])
    stim_pressed = visual.Circle( win = mywindow, radius = asrt_size, units = "cm", fillColor = 'gray', lineColor = colors['linecolor'], lineWidth = 3, pos = dict_pos[1])


    frame_time, frame_sd, frame_rate = frame_check()

    heading_to_output()

    presentation()
    save_personal_info(thisperson_settings)

    outfile_txt = codecs.open(thispath+'\\logs\\'+group+'_'+str(subject_nr)+'_'+identif+'_log.txt', 'a+', encoding = 'utf-8')
    outfile_txt.write('sessionend_planned_quit')
    outfile_txt.close()

    ending()

if __name__ == "__main__":
    main()

