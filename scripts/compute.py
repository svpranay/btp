#!/usr/bin/python
# -*- coding: utf-8 -*-
# import needed libraries:

DEBUG = 0
INFINITE = 10000000
TOLERANCE = 0.999999
points_count = 27
divisions = 5
spikepercent = 20

# The index indicates max and min in the column of index
# returns [[ min, loc] , [ max, loc] ] 
def minmax(data_points, index):
    minimum = [ INFINITE , 0]
    maximum = [(-1) * INFINITE, 0]
    length = len(data_points)
    for i in range(length):
       if data_points[i][index] < minimum[0] : 
           minimum[0] = data_points[i][index]
           minimum[1] = i
           continue
       if data_points[i][index] > maximum[0] : 
           maximum[0] = data_points[i][index]
           maximum[1] = i
    return [minimum, maximum]


#values is a tuple of 
# coordinate points in xy plane
# values are sorted on x corodinates
def computeSlopes(values):
    slopes = []
    previous = values[0]
    previous_slope = 0
    for item in values[1:] :
        ty = (item[1] - previous[1]) 
        tx = item[0] - previous[0]
        if tx == 0 : 
            tx = 0.00001  # infinite slope
        tslope = float(ty) / (float(tx) )
        previous_slope = tslope
        #print previous[0],previous[1],tslope
        slopes.append([previous[0],previous[1],tslope]);
        previous = item
    slopes.append([previous[0],previous[1],previous_slope]) # assume previous slope since no data
    return slopes



# Input : percent to summarise 0-4.
def merge(slopes, level):
    #print "Merging the values...len ",len(slopes)
    #print slopes
    level  = level * 20
    zero_flag = 0
    if level != 0 : 
        zero_flag = 2
    remove_points = ((level * len(slopes)) / 100) - zero_flag
    #print "Total points to remove " , remove_points
    for i in range(remove_points):
        prev = slopes[0]
        min_diff = INFINITE
        min_diff_index = 0
        count = 0
        for item in slopes[1:-1]:
            count = count + 1
            diff = abs(prev[2] - item[2])
            if diff < min_diff : 
                min_diff_index = count
                min_diff = diff
        #print "Index to cut ", min_diff_index, "From : ",slopes
        ty = slopes[min_diff_index+1][1] - slopes[min_diff_index-1][1] 
        tx = slopes[min_diff_index+1][0] - slopes[min_diff_index-1][0] 
        slopes[min_diff_index-1][2] = float(ty)/tx
        if DEBUG : 
            print "Removing index ",min_diff_index,slopes[min_diff_index]
            print slopes
        slopes = slopes[:min_diff_index] + slopes[min_diff_index+1:]

        #print "After cut", len(slopes)
        #print slopes
    #print "Final lenght ",len(slopes)
    # the last slope must be equal to the previous 
    # since we do not have the data to compute it.
    slopes[-1][2] = slopes[-2][2]
    return slopes

def enumerate(slopes, result):
    if len(slopes) == 1 : 
        result.append([slopes[0][0], slopes[0][1], slopes[0][2]])
        return result
    else : 
        if DEBUG : 
            print "Generating...."
            print slopes[0][0]
        partial_result = expand(slopes[0],slopes[1])
        if not partial_result : 
            partial_result.append(slopes[0])
        if DEBUG :
            print partial_result
        return enumerate(slopes[1:], result + partial_result)

def expand(s1, s2) :
    m = s1[2]
    y1 = s1[1]
    y2 = s2[1]
    l = [s1]
    count = s1[0]
    while 1 : 
        #print "Enumerate while loop...",m
        if (abs(l[-1][1] - y2) < TOLERANCE) and m >= 0  : 
            return l[:-1]
        if l[-1][1] >= y2  and m >= 0  : 
            return l[:-1]
        if (abs(y2 - l[-1][1]) < TOLERANCE) and m < 0  : 
            return l[:-1]
        if l[-1][1] <= y2  and m < 0  : 
            return l[:-1]
        else : 
            count = count + 1
            t = [ count, l[-1][1] + m , m]
            l.append( t )

"""    count = (y2 - y1) / m 
    print count
    print "y1, y2, m, count",y1,y2,m, int(count)
    l = []
    for i in range(count): 
        print i
        l.append( y1 + (i * m))
    return l
"""

   
def linearRegression(points):
    #print "Lin Reg ",points
    xmean = 0
    ymean = 0
    for item in points : 
        xmean = xmean + item[0]
        ymean = ymean + item[1]
    xmean = float(xmean) / len(points)
    ymean = float(ymean) / len(points)
    #print xmean , ymean
    # compute beta
    denom = 0.0
    beta = 0.0
    for item in points : 
        beta = beta + (item[0] - xmean) * (float(item[1]) - ymean);
        denom = denom + (item[0] - xmean) * (item[0] - xmean)
    beta = beta/denom
    #print "Slope ", beta
    # compute alpha
    alpha = ymean - (beta * xmean)
    #print "Alpha " , alpha
    return (alpha,beta)

# a utility function
def extractColumn(points,index):
    newlist = []
    for item in points : 
        newlist.append(item[index])
    return newlist


#slopes is sorted on x-axis
def computeAverage(slopes):
    averageslope = 0 
    count = 0
    for item in slopes : 
        count = count + 1
        averageslope = averageslope + item[2]
    if count == 0 :
        print "Error "
        return 100;
    return averageslope/float(count)

def countInflectionPoints(slopes):
    #print "Inflectino ponits.."
    #print slopes
    count = 0
    prev = slopes[0][2]
    for item in slopes[1:] :
        if prev * item[2] < 0 :
            count = count + 1
        prev = item[2]
    #print "Count ",count
    return count

