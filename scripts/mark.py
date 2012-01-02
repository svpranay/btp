
import string,sys,os

filename1 = './../data/extracts3.txt'
#filename2 = 'waves.txt'
filein1 = open(filename1,'r')
#filein2 = open(filename2,'r')

#all_marked = []
speed_descriptors = ['increasing','decreasing','easing','freshening','rising']

data = []
tuples = []
print_detail = 0

def markIfReported(data,tuples):
    reported = {}
    for line in  tuples : 
        words = string.split(line,',')
    #print words[14]
        descriptions = string.split(words[14][1:-1],' ')
        flag = 0
        for w in descriptions :
            if w in speed_descriptors : 
                flag = 1 
        if flag == 1 : 
        #print words[14]
        # describing the speed of wind10
            s = int(words[1][1:-1])
            time = int(words[4])
        #print s,time
            for item in data :
            #"10May2001_02.tab" 11/5/2001 19:00:00 "11/18" "ENE" 8 3 AM
            #print item
                words2 = string.split(item,' ')
                curr_section = int(words2[6])
                curr_timestamp = words2[3][1:-1]
                curr_ts = string.split(curr_timestamp,'/')
                #print curr_ts
                curr_time = int(curr_ts[1])
                if s == curr_section : 
                    # currently look for exact match
                    if time == curr_time : 
                        reported[item] = 1 
            # handle the case where 24 and 0
                else : 
                    if s == curr_section - 1 : 
                        if time  == 24 and curr_time == 0 : 
                            reported[item] = 1 
                    if s == curr_section + 1 : 
                        if time  == 0 and curr_time == 24 : 
                            reported[item] = 1 
    
    print
    if print_detail : 
        for item in data : 
            if item in reported : 
                w_ = string.split(item,' ')
            #print w_[5] + " 1"
                print w_[3] + " " + w_[5] + "\tReported"
            else :
                w_ = string.split(item,' ')
            #print w_[5] + " 0"
                print w_[3] + " " + w_[5] 
        for item in tuples : 
        #print item[:-1]
            words = string.split(item,',')
            print words[4] + "\t" + words[6] + "\t" + words[7] + "\t" + words[13] + " " + words[14] + " " + words[15] + " " + words[16]
    else : 
        # print in less detail 
        for item in data : 
            if item in reported : 
                w_ = string.split(item,' ')
                print w_[5] + " 1"
            else :
                w_ = string.split(item,' ')
                print w_[5] + " 0"

while 1: 
    line  = filein1.readline()
    if not line : 
        break
    if line == '\n' and len(data) == 0 and len(tuples) == 0 : 
        continue # skip empty lines between cases.
    if line == '\n' : 
        markIfReported(data,tuples)
        data = []
        tuples = []
        continue
    words = string.split(line,',')
    if len(words) == 1 : 
        data.append(line)
    else :
        tuples.append(line)


