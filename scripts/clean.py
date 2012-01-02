import string,os,sys

filename1 = 'waves.txt'
filename2 = 'ParseTuples.txt'

filein1 = open(filename1,'r')


dump = filein1.readline()


def joinAll(loc):
    l = []
    filein2 = open(filename2,'r')    
    dump = filein2.readline()
    while 1 :
        line = filein2.readline()
        if not line :
            break
        words = string.split(line,',')
        if loc == words[0][1:-1] :
            l.append(line)
    return l


previous_line = filein1.readline()
prev = string.split(previous_line,' ')
l = []
while 1 : 
    
    current_line = filein1.readline()
    if not current_line : 
        break
    curr = string.split(current_line,' ')
    if curr[0] != prev[0] :
        
        #print prev
        l.append(prev)
        # search for it now and print , next will be next
        print
        loc = prev[0][1:prev[0].find('tab')] + 'prn'
        l1 = joinAll(loc) # my custom function
        if l1 :
            for item in l : 
                for i in item : 
                    print i, 
            l = []
            for item in l1 : 
                print item,
        l=[]
        prev = curr 
    #print prev
    l.append(prev)
    prev = curr

        
