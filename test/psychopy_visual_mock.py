#    Copyright (C) <2018>  <Tamás Zolnai>    <zolnaitamas2000@gmail.com>

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

#!\\usr\\bin\\env python
# -*- coding: utf-8 -*-

from psychopy import visual, event

listOfDrawings = []

# override visual methods, to check the drawing objects without actually drawing
def __RectangleDraw(rectangle):
    rect_copy = Rect()
    rect_copy.pos = rectangle.pos
    rect_copy.width = rectangle.width
    rect_copy.height = rectangle.height
    rect_copy.fillColor = rectangle.fillColor
    listOfDrawings.append(rect_copy)

visual.Rect.draw = __RectangleDraw

def __CircleDraw(circle):
    circle_copy = Circle()
    circle_copy.radius = circle.radius
    circle_copy.pos = circle.pos
    circle_copy.fillColor = circle.fillColor
    circle_copy.lineColor = circle.lineColor
    listOfDrawings.append(circle_copy)

visual.Circle.draw = __CircleDraw

def __LineDraw(line):
    line_copy = Line()
    line_copy.start = line.start
    line_copy.end = line.end
    line_copy.lineWidth = line.lineWidth
    line_copy.lineColor = line.lineColor
    listOfDrawings.append(line_copy)

visual.Line.draw = __LineDraw

def __TextStimDraw(textStim):
    test_stim_copy = TextStim()
    test_stim_copy.height = textStim.height
    test_stim_copy.pos = textStim.pos
    test_stim_copy.color = textStim.color
    test_stim_copy.text = textStim.text
    listOfDrawings.append(test_stim_copy)

visual.TextStim.draw = __TextStimDraw

def __PolygonDraw(polygon):
    polygon_copy = Polygon()
    polygon_copy.fillColor = polygon.fillColor
    polygon_copy.lineColor = polygon.lineColor
    polygon_copy.pos = polygon.pos
    polygon_copy.radius = polygon.radius
    polygon_copy.lineWidth = polygon.lineWidth
    polygon_copy.ori = polygon.ori
    listOfDrawings.append(polygon_copy)

visual.Polygon.draw = __PolygonDraw

def __WindowFlip(window):
    pass

visual.Window.flip = __WindowFlip

returnKeyList = []

def GetKeys(keyList, modifiers = False, timeStamped = False):
    global returnKeyList
    if len(returnKeyList) > 0:
        if returnKeyList[0] in keyList:
            returnKey = returnKeyList[0]
            returnKeyList = returnKeyList[1:]
            return returnKey
    elif len(keyList) > 0:
        return keyList[0]

event.getKeys = GetKeys

class Rect:

    def __init__(self):
        pos = None
        width = None
        height = None
        fillColor = None

class Circle:

    def __init__(self):
        pos = None
        radius = None
        fillColor = None
        lineColor = None

class Line:

    def __init__(self):
        start = None
        end = None
        lineWidth = None
        lineColor = None

class TextStim:

    def __init__(self):
        pos = None
        height = None
        color = None
        text = None

class Polygon:

    def __init__(self):
        fillColor = None
        lineColor = None
        pos = None
        lineWidth = None
        radius = None
        ori = None


class PsychoPyVisualMock:

    def __init__(self):

        global listOfDrawings
        listOfDrawings = []

    def getListOfDrawings(self):
        return listOfDrawings

    def clear(self):
        listOfDrawings = []

    def setReturnKeyList(self, keyList):
        global returnKeyList
        returnKeyList = keyList