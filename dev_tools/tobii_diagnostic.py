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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>

import tobii_research as tobii

import time

# Sometimes the eyetracker is not identified for the first time
# Try until we get any data.
loop_count = 1
eye_trackers = tobii.find_all_eyetrackers()
while not eye_trackers and loop_count < 10:
    eye_trackers = tobii.find_all_eyetrackers()
    time.sleep(0.01)
    loop_count += 1

if not eye_trackers:
    print("No eye tracker device found.")
    quit()

eye_tracker = eye_trackers[0]
print("Eyetracker device basic informations:")
print("Address: " + eye_tracker.address)
print("Model: " + eye_tracker.model)
print("Name: " + eye_tracker.device_name)
print("Serial number: " + eye_tracker.serial_number)
print("Firmware version: " + eye_tracker.firmware_version)

print("")
print("Eye tracker device capabilities:")
if tobii.CAPABILITY_CAN_SET_DISPLAY_AREA in eye_tracker.device_capabilities:
    print("Eye tracker's display area is modifiable.")
else:
    print("Eye tracker's display area is not modifiable.")

if tobii.CAPABILITY_HAS_EXTERNAL_SIGNAL in eye_tracker.device_capabilities:
    print("User can get external signal from the eye tracker.")
else:
    print("User can not get external signal from the eye tracker.")

if tobii.CAPABILITY_HAS_EYE_IMAGES in eye_tracker.device_capabilities:
    print("User can get eye image from the eye tracker.")
else:
    print("User can not get eye image from the eye tracker.")


print("")
print("Eye tracker's frequency:")
print("Supported gaze output frequencies: ", end='')
index = 1
for gaze_output_frequency in eye_tracker.get_all_gaze_output_frequencies():
    if index > 1:
        print(", ", end='')
    print("{0} Hz".format(gaze_output_frequency), end='')
    index += 1

print(".")
print("Currently used gaze ouput frequency: {0} Hz.".format(eye_tracker.get_gaze_output_frequency()))

print("")
print("Eye tracking modes:")
print("Supported eye tracking modes: ", end='')
index = 1
for eye_tracking_mode in eye_tracker.get_all_eye_tracking_modes():
    if index > 1:
        print(", ", end='')
    print(eye_tracking_mode, end='')
    index += 1

print(".")
print("Currently used eye tracking mode: {0}.".format(eye_tracker.get_eye_tracking_mode()))

print("")
print("Eye tracker's track box (mm):")
track_box = eye_tracker.get_track_box()
print("Top-left position of the front side: {0}.".format(track_box.front_upper_left))
print("Top-right position of the front side: {0}.".format(track_box.front_upper_right))
print("Bottom-left position of the front side: {0}.".format(track_box.front_lower_left))
print("Bottom-right position of the front side: {0}.".format(track_box.front_lower_right))
print("Top-left position of the back side: {0}.".format(track_box.back_upper_left))
print("Top-right position of the back side: {0}.".format(track_box.back_upper_right))
print("Bottom-left position of the back side: {0}.".format(track_box.back_lower_left))
print("Bottom-right position of the back side: {0}.".format(track_box.back_lower_right))

# Helper function to write out float tupples with two decimal precision


def print_float_tupple(print_label, float_tupple):
    print(print_label, end='')
    print("(", end='')
    index = 1
    for float_value in float_tupple:
        if index > 1:
            print(", ", end='')
        print("{:0.2f}".format(float_value), end='')
        index += 1
    print(").", end='')
    print("")


print("")
print("Eye tracker's display area (mm):")
display_area = eye_tracker.get_display_area()
print_float_tupple("Top-left position: ", display_area.top_left)
print_float_tupple("Top-right position: ", display_area.top_right)
print("Display area's width: {:0.2f}".format(display_area.width))
print_float_tupple("Bottom-left position: ", display_area.bottom_left)
print_float_tupple("Bottom-right position: ", display_area.bottom_right)
print("Display area's height: {:0.2f}".format(display_area.height))
