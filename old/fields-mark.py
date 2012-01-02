# Operate on fields.txt and get those points where wind10 has been mentioned

import string,sys,os

filename1 = 'reported.txt'
filename2 = 'waves.txt'
filein1 = open(filename1,'r')
filein2 = open(filename2,'r')

all_marked = []

while 1: 
    line  = filein1.readline()
    if not line : 
        break
    all_marked.append(line[:-1])

while 1: 
    line  = filein2.readline()
    if not line : 
        break
    words = string.split(line," ")
    try : 
        if words[0][1:-1] in all_marked : 
            print line[:-1] + " " + "1"
        else :
            print line[:-1] + " " + "0"
    except : 
        continue
