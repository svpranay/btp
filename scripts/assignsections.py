# -*- coding: utf-8 -*-
import os,sys,string
filename= './../data/extracts.txt'
filein= open(filename,'r')
line = filein.readline()
#
#am forecast
#2 6 - 0 
#3 0 - 0 
#4 0 - 0
#5 - later
#
#pm forecast
#2 15(18) - 6 
#3 6 - 0
#4 0 - 0 
#5 - later

nextflag = 1

issue_date = 0
today_date = 0
while 1 : 
    line = filein.readline()
    if not line : 
        break
    words = string.split(line,',')
    if len(words) == 1 : 
        try : 
            if nextflag == 0 :
                if pm_flag == 0 :
                    words2 = string.split(line,' ')
                    time = words2[3][1:-1]
                    ws = string.split(time,'/')
                    today_date = int(ws[0])
                    section = today_date - issue_date + 2 
                    print line[:-1] + ' ' + str(section) + prev
                else : 
                    words2 = string.split(line,' ')
                    time = words2[3][1:-1]
                    ws = string.split(time,'/')
                    today_date = int(ws[0])
                    gap = today_date - issue_date
                    #print gap,line
                    if gap == 0 : 
                        print line[:-1] + ' 2' + prev
                    elif gap  == 1 : 
                        if int(ws[1]) <= 6 : 
                            print line[:-1] + ' 2' +   prev
                        else : 
                            print line[:-1] + ' 3' +   prev
                    elif gap == 2 : 
                        print line[:-1] + ' 4'   + prev
                    else : 
                        print line[:-1] + ' 5'   + prev
            else :
                print # for a gap between two data points
                words2 = string.split(line,' ')
                time = words2[3][1:-1]
                ws = string.split(time,'/')
                if int(ws[1]) < 12 :
                    #prev = " AM"  
                    prev = ""
                    pm_flag  = 0
                    issue_date = int(ws[0])
                    today_date = int(ws[0])
                    #print line[:-1] + prev,
                    section = today_date - issue_date + 2 
                    print line[:-1] + ' ' + str(section) + prev
                else : 
                    #prev = " PM"  
                    prev=""
                    pm_flag = 1
                    issue_date = int(ws[0])
                    today_date = int(ws[0])
                    print line[:-1] + ' 2' +  prev
                    #print line[:-1] + prev ,                    
        except : 
            continue
        nextflag = 0
    else : # parse tuple
        pm_flag = 0
        nextflag = 1
        print  line,


