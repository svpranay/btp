# Operate on fields.txt and get those points where wind10 has been mentioned

import string,sys,os

filename = 'fields.txt'
filein = open(filename,'r')


while 1: 
    line  = filein.readline()
    if not line : 
        break
    words = string.split(line," ")
    try : 
        if words[3] == '"wind10M"' : 
            print words[1][1:-4] + "tab"
    except : 
        continue
