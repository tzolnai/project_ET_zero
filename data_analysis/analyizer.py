# !/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) <2019-2021>  <Tamás Zolnai>  <zolnaitamas2000@gmail.com>

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
import sys
import shutil
import time

import calc_trial_data as ctd
import validate_trial_data as vtd
import extend_data as ed
import validate_extended_data as ved
import compute_learning as cl
import validate_learning as vl
import compute_interference as ci
import validate_interference as vi
import compute_jacobi as cj
import validate_jacobi as vj
import compute_anticipatory as ca
import validate_anticipatory as va
import compute_missing_data_ratio as cmd
import compute_distance as cd
import compute_binocular_distance as cbd
import compute_extreme_RT as cert
import compute_rms as crms

def setupOutputDir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        time.sleep(.001)

    os.makedirs(dir_path)
    if not os.path.isdir(dir_path):
        print("Could not make the output folder: " + dir_path)
        exit(1)

def compute_trial_data(input_dir, output_dir):
    setupOutputDir(output_dir)

    for root, dirs, files in os.walk(input_dir):
        for subject_dir in dirs:
            if subject_dir.startswith('.'):
                continue

            print("Compute RT and anticipatory eye-movements data for subject: " + subject_dir)
            raw_data_path = os.path.join(root, subject_dir, 'subject_' + subject_dir + '__log.txt')
            RT_data_path = os.path.join(output_dir, 'subject_' + subject_dir + '__trial_log.txt')
            ctd.computeTrialData(raw_data_path, RT_data_path)

        break

def validate_trial_data(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for subject_dir in dirs:
            if subject_dir.startswith('.'):
                continue

            print("Validate RT and anticipatory eye-movements data for subject: " + subject_dir)
            raw_data_path = os.path.join(root, subject_dir, 'subject_' + subject_dir + '__log.txt')
            RT_data_path = os.path.join(output_dir, 'subject_' + subject_dir + '__trial_log.txt')
            vtd.validateTrialData(raw_data_path, RT_data_path)

        break

def extend_trial_data(input_dir, output_dir):
    setupOutputDir(output_dir)

    for root, dirs, files in os.walk(input_dir):
        for file in files:

            input_file = os.path.join(input_dir, file)
            output_file = os.path.join(output_dir, os.path.splitext(file)[0] + '_extended.txt')
            ed.extendTrialData(input_file, output_file)

        break

def validate_extended_trial_data(input_dir):

    for root, dirs, files in os.walk(input_dir):
        for file in files:

            input_file = os.path.join(input_dir, file)
            ved.validateExtendedTrialData(input_file)

        break

def compute_implicit_learning(input_dir, output_dir):
    setupOutputDir(output_dir)

    output_file = os.path.join(output_dir, 'implicit_learning.txt')
    cl.computeImplicitLearning(input_dir, output_file)

def validate_implicit_learning(input_dir, output_dir):

    output_file = os.path.join(output_dir, 'implicit_learning.txt')
    vl.validateImplicitLearning(input_dir, output_file)

def compute_sequence_learning(input_dir, output_dir):
    setupOutputDir(output_dir)

    output_file = os.path.join(output_dir, 'sequence_learning.txt')
    cl.computeSequenceLearning(input_dir, output_file)

def validate_sequence_learning(input_dir, output_dir):

    output_file = os.path.join(output_dir, 'sequence_learning.txt')
    vl.validateSequenceLearning(input_dir, output_file)

def compute_statistical_learning(input_dir, output_dir):
    setupOutputDir(output_dir)

    output_file = os.path.join(output_dir, 'statistical_learning.txt')
    cl.computeStatisticalLearning(input_dir, output_file)

def validate_statistical_learning(input_dir, output_dir):

    output_file = os.path.join(output_dir, 'statistical_learning.txt')
    vl.validateStatisticalLearning(input_dir, output_file)

def compute_interference_data(input_dir, output_dir):
    setupOutputDir(output_dir)

    output_file = os.path.join(output_dir, 'interference.txt')
    ci.computeInterferenceData(input_dir, output_file)

def validate_interference_data(input_dir, output_dir):
    output_file = os.path.join(output_dir, 'interference.txt')
    vi.validateInterferenceData(input_dir, output_file)

def compute_jacobi_data(input_dir, output_dir):
    setupOutputDir(output_dir)

    output_file = os.path.join(output_dir, 'jacobi_results.txt')
    cj.computeJacobiTestData(input_dir, output_file)

def validate_jacobi_data(input_dir, output_dir):
    output_file = os.path.join(output_dir, 'jacobi_results.txt')
    vj.validateJacobiTestData(input_dir, output_file)

def compute_jacobi_filter(input_dir, output_dir):
    output_file = os.path.join(output_dir, 'jacobi_filter.txt')
    cj.computeJacobiFilterCriteria(input_dir, output_file)

def compute_anticipatory_data(input_dir, output_dir):
    setupOutputDir(output_dir)

    output_file = os.path.join(output_dir, 'anticipatory_data.txt')
    ca.computeAnticipatoryData(input_dir, output_file)

def validate_anticipatory_data(input_dir, output_dir):

    output_file = os.path.join(output_dir, 'anticipatory_data.txt')
    va.validateAnticipatoryData(input_dir, output_file)

def compute_missing_data_ratio(input_dir, output_dir, jacobi = False):
    setupOutputDir(output_dir)

    output_file = os.path.join(output_dir, 'missing_data_ratio.txt')
    cmd.computeMissingDataRatio(input_dir, output_file, jacobi)

def compute_distance(input_dir, output_dir, jacobi = False):
    setupOutputDir(output_dir)

    output_file = os.path.join(output_dir, 'distance_data.txt')
    cd.computeDistance(input_dir, output_file, jacobi)

def compute_binocular_distance(input_dir, output_dir, jacobi = False):
    setupOutputDir(output_dir)

    output_file = os.path.join(output_dir, 'RMS(E2E)_data.txt')
    cbd.computeBinocularDistance(input_dir, output_file, jacobi)

def compute_extreme_RT(input_dir, output_dir):
    setupOutputDir(output_dir)

    output_file = os.path.join(output_dir, 'extreme_RT_averages.txt')
    cert.computeExtremeRTAverages(input_dir, output_file)

def compute_RMS(input_dir, output_dir, jacobi = False):
    setupOutputDir(output_dir)

    output_file = os.path.join(output_dir, 'RMS(S2S)_data.txt')
    crms.computeRMS(input_dir, output_file, jacobi)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You need to specify an input folder for raw data files.")
        exit(1)

    if not os.path.isdir(sys.argv[1]):
        print("The passed first parameter should be a valid directory path: " + sys.argv[1])
        exit(1)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    trial_data_dir = os.path.join(script_dir, 'data', 'trial_data')

    compute_trial_data(sys.argv[1], trial_data_dir)

    # validate_trial_data(sys.argv[1], trial_data_dir)
    
    extended_trial_data_dir = os.path.join(script_dir, 'data', 'trial_data_extended')

    extend_trial_data(trial_data_dir, extended_trial_data_dir)
    
    # validate_extended_trial_data(extended_trial_data_dir)

    implicit_learning_dir = os.path.join(script_dir, 'data', 'implicit_learning')

    compute_implicit_learning(extended_trial_data_dir, implicit_learning_dir)

    # validate_implicit_learning(extended_trial_data_dir, implicit_learning_dir)

    interference_dir = os.path.join(script_dir, 'data', 'interference')

    compute_interference_data(extended_trial_data_dir, interference_dir)

    # validate_interference_data(extended_trial_data_dir, interference_dir)

    # jacobi_result_dir = os.path.join(script_dir, 'data', 'jacobi_test')

    # compute_jacobi_data(sys.argv[1], jacobi_result_dir)

    # validate_jacobi_data(sys.argv[1], jacobi_result_dir)

    # compute_jacobi_filter(sys.argv[1], jacobi_result_dir)

    anticipatory_dir = os.path.join(script_dir, 'data', 'anticipatory_movements')

    compute_anticipatory_data(extended_trial_data_dir, anticipatory_dir)

    #validate_anticipatory_data(extended_trial_data_dir, anticipatory_dir)

    missing_data_dir = os.path.join(script_dir, 'data', 'missing_data')

    compute_missing_data_ratio(sys.argv[1], missing_data_dir)

    #jacobi_missing_data_dir = os.path.join(script_dir, 'data', 'jacobi_missing_data')

    #compute_missing_data_ratio(sys.argv[1], jacobi_missing_data_dir, True)

    distance_dir = os.path.join(script_dir, 'data', 'distance_data')

    compute_distance(sys.argv[1], distance_dir)

    #jacobi_distance_dir = os.path.join(script_dir, 'data', 'jacobi_distance_data')

    #compute_distance(sys.argv[1], jacobi_distance_dir, True)

    binocular_distance_dir = os.path.join(script_dir, 'data', 'binocular_distance_data')

    compute_binocular_distance(sys.argv[1], binocular_distance_dir)

    #jacobi_binocular_distance_dir = os.path.join(script_dir, 'data', 'jacobi_binocular_distance_data')

    #compute_binocular_distance(sys.argv[1], jacobi_binocular_distance_dir, True)

    RMS_dir = os.path.join(script_dir, 'data', 'RMS')

    compute_RMS(sys.argv[1], RMS_dir)

    #jacobi_RMS_dir = os.path.join(script_dir, 'data', 'jacobi_RMS')

    #compute_RMS(sys.argv[1], jacobi_RMS_dir, True)