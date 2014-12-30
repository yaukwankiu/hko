# from source /CWB/ folder to target /CWB/ folder

#source = "d:/CWB/" ; target = "f:/CWB/"
source = "c:/yaukwankiu/HKO/" ; target = "g:/HKO/"

dryRun = False
#keys=["charts",'fcst', 'hs1', 'hsao','hq', 'qpf', 'rainfall', "satellite", 'sco', "sea", "temper", "s0",'uvi',]
#keys=['charts2']
keys=['']
nokeys = ['allinone', '.git', '.py', '.pyc', '.md', ]
sinceTime = '201401130'
#sinceTime =''

print "keys:", keys
print "nokeys:", nokeys
print "transferring:", source, "->", target
print 'since time:', sinceTime
print "sleeping 3 seconds"
import time
time.sleep(3)

#key1 = "hs1"
#nokey='charts2'

import os
import shutil
import time

L   = os.listdir(source)
for nokey in nokeys:
    L = [v for v in L if not (nokey in v)]
    L = [v for v in L if os.path.isdir(v)]

L1  = []
for key in keys:
    L1.extend([v+"/" for v in L if key in v])
L= L1
print "L:", '\t'.join(L)
print "sleeping 2 seconds"
time.sleep(2)

for typeFolder in L:
    print "\n--------------------------\ntransferring", typeFolder
    L2 = os.listdir(source + typeFolder)   
    #print L2 #debug
    print "L2[0]:",  L2[0], 
    if os.path.isdir(source+typeFolder+L2[0]):
        print "is a directory"
        L2 = [v + "/" for v in L2 if not ('.git' in v) and v>=sinceTime]
    else:
        print "is not a directory"
        L2 = [v for v in L2 if not ('.git' in v) and v>=sinceTime]
    if os.path.isdir(source+typeFolder+L2[0]):
        for dateFolder in L2:
            print '\n............\ntransferring', dateFolder
            if '.git' in dateFolder:
                continue # /.git/     folder
            if dateFolder[0] not in ['1','2']:
                continue  #doesn't start with a date
            L3 = os.listdir(source+typeFolder+dateFolder)
            if L3 == []:
                continue
            else:
                for fileName in L3:
                    #if '.git' in fileName:
                    #    continue # /.git/     folder
                    if os.path.exists(target+typeFolder+dateFolder+fileName):
                        pass
                        #print "target exists!"
                    else:
                        print source + typeFolder  + dateFolder  + fileName , 
                        print "->",
                        print target + typeFolder
                        if not dryRun:
                            if not os.path.exists(target+typeFolder+dateFolder):
                                os.makedirs(target+typeFolder+dateFolder)
                            shutil.copyfile( source + typeFolder  + dateFolder  + fileName,  target + typeFolder  + dateFolder  + fileName )
    else:
        for fileName in L2:
        #if '.git' in fileName:
        #    continue # /.git/     folder
            if os.path.exists(target+typeFolder+fileName):
                pass
                #print "target exists!"
            else:
                print source + typeFolder  + fileName , 
                print "->",
                print target + typeFolder
                if not dryRun:
                    if not os.path.exists(target+typeFolder):
                        os.makedirs(target+typeFolder)
                    shutil.copyfile( source + typeFolder  + fileName,  target + typeFolder  +  fileName )
                            