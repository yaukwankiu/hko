#   downloading data from hk observatory
#   http://www.hko.gov.hk/wxinfo/radars/rad_256_png/2d256radar_201407181412.png

########################################
#   imports
import datetime, time, re, os, sys, shutil, urllib2, urllib

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
                 timed=True,
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
        if not timed:
            return self.fetchSingle()
        else:
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


    def fetchSingle(self):
        url = self.urlPattern
        outputFolder = self.name + '/'
        Y, M, D, h, m, s = getCurrentTime()
        fileName = ("0000"+str(Y))[-4:] + ("00"+str(M))[-2:] + ("00"+str(D))[-2:] + ("00"+str(h))[-2:] + ("00"+str(m))[-2:] + "." + fileSuffix
        to_path = outputFolder + self.name + "_" + fileName
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
######################################################
#   main loop

def getObjects():
    ### timed   #########
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

    rad3d040 =  Charts(name="rad3d040",
                     urlPattern= "http://www.hko.gov.hk/wxinfo/radars/rad3d_040_png/3d040radar_YYYYMMDDhhmm.png" ,  # e.g. something like "http://www.hko.gov.hk/wxinfo/radars/rad_064_png/2d064radar_YYYYMMDDhhmm.png"
                     interval=30,   #unit:  minutes
                     description="",
                     )


    rfmap =  Charts(name="rfmap",
                     urlPattern= "http://www.hko.gov.hk/wxinfo/rainfall/rfmapYYYYMMDDhhmme.png" ,  # e.g. something like "http://www.hko.gov.hk/wxinfo/radars/rad_064_png/2d064radar_YYYYMMDDhhmm.png"
                     interval=60,   #unit:  minutes
                     description="Rainfall for the past hour",
                     )

    rfmap24hrs =  Charts(name="rfmap24hrs",
                     urlPattern= "http://www.hko.gov.hk/wxinfo/rainfall/rfmap24hrs1700e.png" ,  # e.g. something like "http://www.hko.gov.hk/wxinfo/radars/rad_064_png/2d064radar_YYYYMMDDhhmm.png"
                     interval=60,   #unit:  minutes
                     description="Rainfall for the past 24 hours",
                     )


    ### untimed ############
    tempehk = Charts(name='tempehk',
                    urlPattern='http://www.hko.gov.hk/wxinfo/ts/temp/tempehk.png',
                    timed = False,
                    description = "Air Temperature Hong Kong",
                    )


    humidehk = Charts(name='humidehk',
                    urlPattern='http://www.hko.gov.hk/wxinfo/ts/temp/humidehk.png',
                    timed = False,
                    description = "Relative Humidity",
                    )

    miniehk = Charts(name='miniehk',
                    urlPattern='http://www.hko.gov.hk/wxinfo/ts/temp/miniehk.png',
                    timed = False,
                    description = "Minimum Air Temperature Recorded since 00:00",
                    )

    tempehk = Charts(name='tempehk',
                    urlPattern='http://www.hko.gov.hk/wxinfo/ts/temp/tempehk.png',
                    timed = False,
                    description = "Air Temperature Hong Kong"
                    )

    maxiehk_1 = Charts(name='maxiehk_1',
                    urlPattern='http://www.hko.gov.hk/wxinfo/ts/temp/maxiehk-1.png',
                    timed = False,
                    description = "Yesterday's Max Air Temperature"
                    )

    grassehk = Charts(name='grassehk',
                    urlPattern='http://www.hko.gov.hk/wxinfo/ts/grass/grassehk.png',
                    timed = False,
                    description = "Grass Temperature"
                    )


    windehk = Charts(name='windehk',
                    urlPattern='http://www.hko.gov.hk/wxinfo/ts/windehk.png',
                    timed = False,
                    description = "Mean Wind Speed in 10 minutes"
                    )


    gustehk = Charts(name='gustehk',
                    urlPattern='http://www.hko.gov.hk/wxinfo/ts/windgust/gustehk.png',
                    timed = False,
                    description = "Maximum Gust in 10 minutes"
                    )

    visehk = Charts(name='visehk',
                    urlPattern='http://www.hko.gov.hk/wxinfo/ts/vis/visehk.png',
                    timed = False,
                    description = "Mean Visibility in 10 Minutes"
                    )

    preehk = Charts(name='preehk',
                    urlPattern='http://www.hko.gov.hk/wxinfo/ts/pre/preehk.png',
                    timed = False,
                    description = "MSL (mean sea level?) Pressure (hPa)"
                    )

    vismape = Charts(name='vismape',
                    urlPattern='http://www.hko.gov.hk/vis/e_png/vismape.png',
                    timed = False,
                    description = "Visibility Reports"
                    )



    ### photos#######
       
                    
    L0=[rad256, rad128, rad064, rad3d040]

    L1=[tempehk,humidehk,miniehk, tempehk, maxiehk_1,grassehk,   windehk,  gustehk , gustehk ,  visehk ,  preehk, vismape  ]
    return L0+L1

def main(key1=""):
    L = getObjects()
    L = [v for v in L if key1 in v.name]
    print '\n'.join([v.name for v in L])
    time.sleep(2)
    for charts in L:
        charts.fetch()
    
    
if __name__=="__main__":
    key1 = sys.argv[1]
    print 'key1=',key1
    main(key1=key1)    