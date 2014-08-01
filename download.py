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

def getDatetime(dD=0 ,dh=0, dm=0, ds=0):

    if isinstance(dD, datetime.datetime):   # fail-safe
        T = dD
    else:
        Y, M, D, h, m, s = getCurrentTime()
        dT = datetime.timedelta(dD + 1./24 * dh + 1./1440 * dm + 1./86400*ds)
        T = datetime.datetime(Y,M,D,h,m,s)
        T   += dT
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
                 useDoubleDigitYear=False,
                 ):
        #   open dataFolder
        dataFolder = name + '/'
        self.name           = name
        self.urlPattern     = urlPattern
        self.interval       = interval
        self.description    = description
        self.timed          =timed
        self.useDoubleDigitYear= useDoubleDigitYear

        if not os.path.exists(dataFolder):
            os.makedirs(dataFolder)
        if not os.path.exists(dataFolder+'readme.txt'):
            open(dataFolder+'readme.txt','w').write(description)


    def fetch(self, days=3,reload=False, *args, **kwargs):
        days= int(days)
        fileSuffix     = self.urlPattern[-3:]
        count           = 0
        dataFolder  = self.name+'/'
        if not self.timed:
            return self.fetchSingle()
        else:
            for dD in range(-days+1,1):  # if days=3:  the day before(-2), yesterday(-1), today(0)
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
                    if self.useDoubleDigitYear:
                        pairs = [('YY', Y1%100), ('MM',M1), ('DD',D1), ('hh',h1), ('mm',m1)]
                    else:
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
                    else:
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
                            #return returnValue
            print "%d images fetched " %count + " in folder" + outputFolder
            return count


    def fetchSingle(self, *args, **kwargs):
        url = self.urlPattern
        fileSuffix     = url[-3:]
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

    def readme(self, toSaveToFile=False, saveMode='a'):
        description = self.description
        readmeString = description + '\n'
        urls = re.findall(r'http.+htm', description)
        for url in urls:
            x = urllib2.urlopen(url).read()
            #<meta name="Description" content="Animated Photo at Cheung Chau Sacred Heart School " />
            readmeString += re.findall(r'(?<=\<meta name\=\"Description\" content\=\").+(?=\" \/\>)', x)[0] + '\n'
        print readmeString
        if toSaveToFile:
            open(root + self.name + '/readme.txt', saveMode).write(readmeString)
        return readmeString
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
    photoNameList = ['lfs', 'wlp', 'kfb','tpk', 'sk2', 'tlc', 'klt', 'hk2', 'hko', 'swh', 'gsi', 'cp1', 'slw', 'dnl', 'pe2', 'cch', 'wgl', 'wl2', 'lam', 'cce']
    photoList  = []
    for p in photoNameList:
        photo  = Charts(name=p,
                       #urlPattern='http://www.hko.gov.hk/wxinfo/aws/hko_mica/%s/latest_%s.jpg' %(p.lower(), p.upper()),
                       # http://www.hko.gov.hk/wxinfo/aws/hko_mica/wlp/imgWLP_140718_1445.jpg
                       
                       urlPattern='http://www.hko.gov.hk/wxinfo/aws/hko_mica/%s/img%s_YYMMDD_hhmm.jpg' %(p.lower(), p.upper()),
                       timed = True,
                       interval=5,
                       description = "http://www.hko.gov.hk/wxinfo/ts/webcam/ani_%s_photo_e.htm" %p.upper(),
                       useDoubleDigitYear=True
                       )
        photoList.append(photo)

                    
    L0=[rad256, rad128, rad064, rad3d040]

    L1=[tempehk,humidehk,miniehk, tempehk, maxiehk_1,grassehk,   windehk,  gustehk , gustehk ,  visehk ,  preehk, vismape  ]
    return L0 + L1 + photoList

def main(key1="", *args, **kwargs):
    L = getObjects()
    L = [v for v in L if key1 in v.name]
    print '\n'.join([v.name for v in L])
    time.sleep(2)
    for charts in L:
        charts.fetch(*args, **kwargs)
    
    
if __name__=="__main__":
    if len(sys.argv)>1:
        key1 = sys.argv[1]
        print 'key1=',key1
    if len(sys.argv)>2:
        days = sys.argv[2]
        print 'Number. of days fetched=' , days
    print "sleeping 2 seconds"
    time.sleep(2)
    main(*sys.argv[1:])    
