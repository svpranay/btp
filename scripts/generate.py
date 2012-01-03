#!/usr/bin/python
# -*- coding: utf-8 -*-
# import needed libraries:
import sys,random,string
import numpy
import pylab
from compute import *
from tagger import *

def action(slope):
    if slope < 0.1 and slope > -0.1: 
        return "nearly constant"
    elif slope > 0 :
        #return "increasing"
        return adjective(slope) + "increasing"
    else :
        positiveslope = -1 * float(slope)
        #return  "decreasing"
        return adjective(positiveslope) + "decreasing"
    
def adjective(slope):
    if slope > 0.1 and slope < 0.5 : 
        return " slowly "
    elif slope > 0.5 and slope < 1500 : # domain dependent 
        return " steadily "
    else : 
        return " steeply "

def checkFluctuation(points, i):
    # remove fluctuations and add a single item
    index = i
    prev = points[i][2]
    average_sum = prev
    while 1 :
        if index == len(points) - 1:
            break
        index = index + 1
        curr = points[index][2]
        if curr * prev < 0 and points[index][0] == points[index-1][0] + 1: 
            average_sum = average_sum + curr 
            prev = curr
        else : 
            break
    index = index - 1 
    if index - i >= 3 : 
        if average_sum > 0 : 
            points[i].append('f')
            points[i].append("fluctuating with an overall rise")
            points[i].append(index-i)
        else:
            points[i].append('f')
            points[i].append("fluctuating with an overall fall")
            points[i].append(index-i)
    
def catchFluctuations(points):
    for i in range(points):
        checkFluctuation(points,i)

def summarize_(points, i):
    #print "summarize ", points[i][0] , i
    index = i
    prev = points[i][2]
    if points[i][2] > 0 : 
        text = action(points[i][2]) + " from " + str(points[i][0]) 
    else : 
        text = action(points[i][2]) + " from " + str(points[i][0]) 
    text_ = text
    while 1 :
        if index == len(points) - 1:
            break
        index = index + 1
        curr = points[index][2]
        if curr * prev > 0 : 
            # same sign 
            if  prev > 0 : 
                # rising 
                text = text + " then, "
                if prev < curr : 
                    text = text + " raising faster from the year " + str(points[index][0]) 
                else : 
                    text = text + " raising slower from the year " + str(points[index][0]) 
            else : 
                # falling 
                if prev < curr : 
                    text = text + " falling slower from the year " + str(points[index][0]) 
                else : 
                    text = text + " falling faster from the year " + str(points[index][0]) 
            prev = curr
        else : 
            break
    index = index - 1
    points[i].append('id')
    points[i].append(text)
    points[i].append(index-i) 
    # prepare a summarized text and store it
#commented below to avoid little variation.
#    if index < 3  :
#        points[i].append('id')
#        points[i].append(text)
#        points[i].append(index - i)
#    else : 
#        points[i].append('id')
#        points[i].append(text_ + " with little variation ")
#        points[i].append(index - i)
#uncomment above to have "little variation"
    #print "skip ",index- i
    return index  + 1
    
def summarize(points):
    t = 0
    while t < len(points)-1 : 
        t = summarize_(points,t)

def insertMinmax(points, real_values):
    l = minmax(real_values, 0)
    l[0][1] = l[0][1] + points[0][0]
    l[1][1] = l[1][1] + points[0][0]
    #print "Min max"
    #print l
    #l[0][0] - min value
    #l[0][1] - min value loc 
    #l[1][0] - max value
    #l[1][1] - max value loc 
    iprime = -1
    for i in range(len(points)-1):
        #i = i_ + 1
        if points[i][0] <= l[1][1] and points[i+1][0] > l[1][1] : 
            points[i].append("minmax")
            points[i].append("It attains maximum at " + str(l[1][1]) + " with value of " + str(l[1][0]) )
            if i == iprime : 
                # already minmax added
                points[i][len(points[i])-1] = points[i][len(points[i])-1] + " and maximum at " + str(l[1][1]) + " with value of " + str(l[1][0])
            iprime = i
        if points[i][0] <= l[0][1] and points[i+1][0] > l[0][1] : 
            points[i].append("minmax")
            points[i].append("It attains minimum at " + str(l[0][1]) + " with value of " + str(l[0][0]) )
            if i == iprime : 
                points[i][len(points[i])-1] = points[i][len(points[i])-1] + " and minimum at " + str(l[0][1]) + " with value of " + str(l[0][0])
            iprime = i

def generateText(points, real_values):
    text = []
    for i in range(len(points)-4) :
        checkFluctuation(points, i)
    summarize(points)
    insertMinmax(points,real_values)
    #print points
    i = -1
    while i < len(points) -2 :
        i = i + 1
        curr = points[i]
        next = points[i+1]
        if len(points[i]) > 3 : 
            if points[i][3] == 'f' : 
                # fluctuating..
                text.append("It " + points[i][4]+ " from " + str(curr[0]) + " until " + str(curr[0] + points[i][5]) + " " )
                #print points[i]
                if "minmax" in points[i] : 
                    text.append(points[i][points[i].index("minmax") + 1])
                i  = i + points[i][5] - 1
                continue
            if points[i][3] == 'id' : 
                # fluctuating..
                text.append("It " + points[i][4] + " until the year " + str(points[i+points[i][5] + 1][0]))
                #print points[i]
                if "minmax" in points[i] : 
                    text.append(points[i][points[i].index("minmax") + 1])
                i  = i + points[i][5]
                continue
        if curr[0] == next[0] - 1: 
            # single year 
            text.append(" In " + str(curr[0]) + " it " +  action(points[i][2]) + ".")
            #print points[i]
            if "minmax" in points[i] : 
                text.append(points[i][points[i].index("minmax") + 1])
        else : 
            text.append(" From " + str(curr[0]) +  " to " + str(next[0]) + " it " + action(points[i][2])  + ".")
            #print points[i]
            if "minmax" in points[i] : 
                text.append(points[i][points[i].index("minmax") + 1])
    return text
