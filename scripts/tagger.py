#!/usr/bin/python
# -*- coding: utf-8 -*-
# import needed libraries:
import sys,random,string,copy
import numpy
import pylab
from compute import  *

def findSpikes(points):
    # (alpha, beta)
    spiketext = ""
    line = linearRegression(points)
    alpha = line[0]
    beta  = line[1]
    #print line
    for i in range(len(points)):
        yprime = beta * points[i][0] + alpha 
        y = points[i][1]
        diff = yprime - y
        spikeflag = 0
        if diff < 0 : 
            diff = diff * -1
            spikeflag = 1
        #print item[0], y , diff
        diffpercent = (diff * 100.0)/y
        check_adjacent_values = adjacentCheck(i, points, beta, alpha ,1 )
        if diffpercent > spikepercent and check_adjacent_values : 
            print
            if spikeflag : 
                print "A SPIKE observerd " , "@",points[i][0]
                spiketext = spiketext + "A spike is observed at " + str(points[i][0])
                
                # remove the spike
                # compute the slope i-1,i+1 
                # and join
                #the below code doesn't handle two step peaks and hence creates problems.
                #points[i][1] = (points[i-1][1] + points[i+1][1] )/ 2
                #newslope = (points[i+1][1] - points[i-1][1]) / (points[i+1][0] - points[i-1][0])
                #points[i][2] = newslope
                #points[i-1][2] = newslope                
                return spiketext
            else : 
                spiketext = spiketext + "A dip is observed at " + str(points[i][0])
                # remove the spike
                #points[i][1] = (points[i-1][1] + points[i+1][1] )/ 2
                #newslope = (points[i+1][1] - points[i-1][1]) / (points[i+1][0] - points[i-1][0])
                #points[i][2] = newslope
                #points[i-1][2] = newslope                
                print "DIP observerd " , "@",points[i][0]
            print
    return spiketext

def adjacentCheck(index, data_points, beta, alpha , width) : 
    if index + width >= len(data_points):
        return 0
    prev_yprime = beta * data_points[index - width][0] + alpha 
    next_yprime = beta * data_points[index + width][0] + alpha 
    prev_y = data_points[index - width][1]
    next_y = data_points[index + width][1]
    prev_diff = prev_yprime - prev_y
    next_diff = next_yprime - next_y
    prev_diffpercent = (prev_diff * 100.0)/prev_y
    next_diffpercent = (next_diff * 100.0)/next_y
    if prev_diffpercent < spikepercent and next_diffpercent < spikepercent :
        return 1
    else :
        if width == 1 : 
            return adjacentCheck(index, data_points, beta, alpha, 2 )
        else : 
            return 0
