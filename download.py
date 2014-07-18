#   downloading data from hk observatory
#   http://www.hko.gov.hk/wxinfo/radars/rad_256_png/2d256radar_201407181412.png

########################################
#   imports
import datetime, time, re, os, shutil, urllib2, urllib

########################################
#   setups
root = ""

######################################
#   current
time0   = time.time()
t0   = time.localtime()
year, month, day, hour, minute, second = t0.tm_year, t0.tm_mon, t0.tm_mday, t0.tm_hour, t0.tm_min, t0.tm_sec
######################################
#   functions

def getCurrentTime():
    t0   = time.localtime()
    return t0.tm_year, t0.tm_mon, t0.tm_mday, t0.tm_hour, t0.tm_min, t0.tm_sec

def getDatetime(dY=0, dM=0, dD=0 ,dh=0, dm=0, ds=0):
    if isinstance(dY, datetime.datetime):
        T = dY
    else:
        Y, M, D, h, m, s = getCurrentTime()
        T = datetime.datetime(Y+dY,M+dM,D+dD,h+dh,m+dm,s+ds)
    return T.year, T.month, T.day, T.hour, T.minute,T.second
    
######################################
#   classes

class Charts(object):
    """
    a collection of charts
    USE:
        a = charts(name='rad256')
    """
    def __init__(self, name,  #e.g. "rad256"
                urlPattern,   # e.g. something like "http://www.hko.gov.hk/wxinfo/radars/rad_256_png/2d256radar_YYYYMMDDhhmm.png"
                 interval=12,   #unit:  minutes
                 description="",
                 ):
        #   open dataFolder
        dataFolder = name + '/'
        if not os.path.exists(dataFolder):
            os.makedirs(dataFolder)
        self.name           = name
        self.urlPattern     = urlPattern
        self.interval       = interval
        self.description    = description


    def fetch(self, days=4,reload=True):
        fileSuffix     = self.urlPattern[-3:]
        count           = 0
        dataFolder  = self.name+'/'
        for dD in range(-4,1):
            #   compute the date
            Y, M, D, h, m, s = getDatetime(dD=dD)
            print "Y, M, D, h, m, s =",Y, M, D, h, m, s
            # construct the folder
            outputFolder    = dataFolder + ("0000"+str(Y))[-4:] + ("00"+str(M))[-2:] + ("00"+str(D))[-2:] + "/"
            if not os.path.exists(outputFolder):
                os.makedirs(outputFolder)

            for minute in range(0, 1440, self.interval):
            # get the url
                url             = self.urlPattern
                Y1, M1, D1, h1, m1, s1 = getDatetime(datetime.datetime(Y,M,D,0,0,0) + datetime.timedelta(1.*minute  / 1440))
                pairs = [('YYYY', Y1), ('MM',M1), ('DD',D1), ('hh',h1), ('mm',m1)]
                for pair in pairs:
                    try:
                        ###  http://www.hko.gov.hk/wxinfo/radars/rad_256_png/2d256radar_201407151424.png
                        if pair[1]>1000:
                            url = re.sub(pair[0], str(pair[1]), url)
                        else:
                            url = re.sub(pair[0], ('00'+str(pair[1]))[-2:], url)
                    except:
                        print "no match found!", pair, url
                        continue
                #   get the output file name
                fileName = ("0000"+str(Y1))[-4:] + ("00"+str(M1))[-2:] + ("00"+str(D1))[-2:] + ("00"+str(h1))[-2:] + ("00"+str(m1))[-2:] + "." + fileSuffix
                to_path = outputFolder + self.name + "_" + fileName
                if os.path.isfile(to_path) and reload==False:
                    print to_path, ' <--- already exists!!'

                #   try to fetch the data
                try:    
                    webpage = urllib.urlretrieve(url, to_path)
                    if os.path.getsize(to_path)<2000:
                        os.remove(to_path)
                        print "file broken!", url
                        returnValue = 0.5
                    else:
                        print url, " - fetched!!!!!!!!!!"
                        returnValue=1
                        count+=1
                except:
                    print fileName, "not found!!!!"
                    returnValue = 0
                    return returnValue
        print "%d images fetched " %count + " in folder" + outputFolder
        return count




######################################################
#   main loop

def getObjects():
    
    rad256 = Charts(name="rad256",
                     urlPattern= "http://www.hko.gov.hk/wxinfo/radars/rad_256_png/2d256radar_YYYYMMDDhhmm.png",   # e.g. something like "http://www.hko.gov.hk/wxinfo/radars/rad_256_png/2d256radar_YYYYMMDDhhmm.png"
                     interval=12,   #unit:  minutes
                     description=""
                     )

    rad128 = Charts(name="rad128",
                     urlPattern= "http://www.hko.gov.hk/wxinfo/radars/rad_128_png/2d128radar_YYYYMMDDhhmm.png" ,  # e.g. something like "http://www.hko.gov.hk/wxinfo/radars/rad_128_png/2d128radar_YYYYMMDDhhmm.png"
                     interval=12,   #unit:  minutes
                     description=""
                     )
    rad064 = Charts(name="rad064",
                     urlPattern= "http://www.hko.gov.hk/wxinfo/radars/rad_064_png/2d064radar_YYYYMMDDhhmm.png" ,  # e.g. something like "http://www.hko.gov.hk/wxinfo/radars/rad_064_png/2d064radar_YYYYMMDDhhmm.png"
                     interval=12,   #unit:  minutes
                     description=""
                     )



    L=[rad256, rad128, rad064]
    return L

def main():
    L = getObjects()
    for charts in L:
        charts.fetch()
    
    
if __name__=="__main__":
    main()    