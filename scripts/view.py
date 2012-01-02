#!/usr/bin/python
# -*- coding: utf-8 -*-
# import needed libraries:

import sys,random,string,copy
import numpy
import pylab

DEBUG = int(sys.argv[1])


filename = "income7.csv"
warning = " something is fishy.. :-< :-/ "
title = "US Income median Statistics of state "
template = ""

from compute import *
from generate import *
from tagger import *

filein = open(filename,"r")
filesavename__ = "img"
count  = 0

xaxis = []
for i in range(27):
    xaxis.append(1984 + i)

while 1 : 
    count = count + 1
    print 
    print "Input : ",count, " Level ",
    filesavename_ = filesavename__ + str(count) + "_" 
    line = filein.readline()
    if not line : 
        break
    words  = string.split(line,",")
    location  = words[0]
    words = words[1:-1]
    words.reverse()
    sequence = []
    xcount = 0
    values = []
    org_values = []
    for item in words:
        sequence.append((xaxis[xcount],float(float(item) * 0.001)))
        values.append(float(item) * 0.001)
        org_values.append([float(item)])
        xcount = xcount + 1
    slopes = computeSlopes(sequence);
    for i in range(6):
        print 
        print "Level : ",i
        slopes_ = copy.deepcopy(slopes)
        content = merge(slopes_, i)
        #print content
        for item in generateText(content,org_values) : 
            print item
        pylab.plot(xaxis, values)
        pylab.plot(extractColumn(content,0),extractColumn(content, 1))
        pylab.xlabel('Year\n')
        pylab.ylabel('Median US Income in thousand dollars')
        pylab.title(title)
        pylab.annotate("", xy=(1980,35000), xytext=(1980,35000),arrowprops=dict(facecolor='black', shrink=0.05),
                       )
        pylab.savefig(filesavename_ + str(i) + ".png")
        pylab.close()
        pylab.clf()
