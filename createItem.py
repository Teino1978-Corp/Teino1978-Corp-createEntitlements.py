import simplejson as json
import collections
import sys
import random
import string
import copy


def getRandString(size):
    lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(size)]
    return "".join(lst)
    
    
def getRandAwards(year) :
    no = random.randint(1,3)
    ret = []
    for x in range(no) :
        awards = collections.OrderedDict()
        awardType = random.choice( ['golden globe', 'oscar', 'grammy'] )
        cat = random.choice( ['won' , 'nominated'] )
        awards['type'] = awardType
        awards[cat] = random.randint(1950,year)
        ret.append(awards)
    return ret

def getRandEntitlements(region):
    entitlements = collections.OrderedDict()
    entitlements['enabled'] = '1'
    entitlements['format'] = random.choice(['mkv','mov','flv','divx','xvid'])
    entitlements['region'] = region
    entitlements['devices'] = []
    entitlements['network'] = []
    entitlements['business_model'] = []
    entitlements['actions'] = []
    noDev = random.randint(1,3)
    entitlements['devices'] = random.sample(['desktop','android','iOS','TV'],noDev)
    entitlements['network'] = random.sample(['wi-fi','3g','ethernet','LTE','gprs','lte'],noDev)
    entitlements['business_model'] = random.sample(['free','buy','rent'],noDev)
    entitlements['actions'] = random.sample(['preview','watch','watch_later'],noDev)
    return entitlements
    
def putData(data,movie_id):
    URL = "http://localhost:9200/catalog/mediaitem/%s"%movie_id    
    headers = {'Accept': 'application/json'}
    r = requests.post(URL,data=data,headers=headers)
    print r.text,r.url 

jsonFile = open(sys.argv[1])
movies = json.load(jsonFile,object_pairs_hook=collections.OrderedDict)
locales = json.load(open('locale.json'))['locales']
record = collections.OrderedDict()
print "{ 'movies':"
print '['
noOfrecords = 0
for movie in movies['movies']:
    record = movie
    record['enabled'] = '1'
    record['locale'] = random.choice(locales.keys())
    record['region'] = locales[record['locale']]
    record['contentId'] = getRandString(3)
    record['contentGroupID'] = getRandString(3)
    record['contentGroupType'] = 'movie'
    record['tenantId'] = getRandString(3)
    record['regionId'] = getRandString(3)
    metadata = collections.OrderedDict()
    metadata['basicInfo'] = collections.OrderedDict()
    metadata['basicInfo']['countryOfOrigin'] = None
    metadata['basicInfo']['episodeCount'] = None
    metadata['basicInfo']['seasonCount'] = None
    metadata['basicInfo']['totalEpisodeCount'] = None
    metadata['basicInfo']['airDates'] = None
    metadata['production'] = collections.OrderedDict()
    metadata['production']['studios'] = random.choice(['Warner Bros','Walt Disney Pictures', 'Universal Pictures', 'Columbia Pictures', '20th Century Fox', 'Paramount Pictures'])
    metadata['production']['runtime'] = ":".join([str(random.randint(1,3)),str(random.randint(0,59)),str(random.randint(0,59))])
    metadata['production']['MPAARating'] = random.uniform(1.0,5.0)
    metadata['production']['internationalRating'] = random.uniform(1.0,5.0)
    metadata['production']['budget'] = '$' + str(random.randint(1,300))+' million'
    metadata['castFacts'] = []
    metadata['castDetails'] = []
    for cast in movie['contributions'] :
       castFacts = collections.OrderedDict()
       castDetails = collections.OrderedDict()
       castFacts['name'] = cast['contributor']['title']
       castFacts['birthdate'] = '-'.join( [str(random.randint(1950,1994)),str(random.randint(1,12)),str(random.randint(1,28)) ] ) 
       castFacts['birthPlace'] = locales[random.choice(locales.keys())]
       castFacts['nationality'] = castFacts['birthPlace']
       metadata['castFacts'].append(castFacts)
       castDetails['name'] = cast['contributor']['title']
       castDetails['awards'] = getRandAwards(record['year'])
       castDetails['biography'] = None
       castDetails['fbLink'] = 'facebook.com/' + 'xyz'
       metadata['castDetails'].append(castDetails)
    metadata['castVolume'] = collections.OrderedDict()
    metadata['castVolume']['top500'] = None
    metadata['castVolume'] ['top5000'] = None
    metadata['socialMedia'] = collections.OrderedDict()
    metadata['socialMedia']['website'] = 'xyz.com'
    metadata['socialMedia']['fbLink'] = 'facebook.com/xyz'
    metadata['socialMedia']['twiltterHandle'] = '#xyz'
    metadata['awards'] = getRandAwards(record['year'])
    metadata['boxOffice'] = collections.OrderedDict()
    randInt = random.randint(10,200)
    metadata['boxOffice']['boxOfficeUSA'] = str(randInt) + 'million'
    metadata['boxOffice']['boxOfficeGlobal'] = str(randInt + 30) + 'million'
    metadata['boxOffice']['dlaBoxOffice'] = str(randInt - 10) + 'million' 
    metadata['keywords'] = [movie['title'],movie['contributions'][0]['contributor']['title']]
    metadata['timeCode'] = collections.OrderedDict()
    randHrs= random.randint(1,3)
    randMin = random.randint(2,59)
    randSec = random.randint(0,59)
    metadata['timeCode']['studioRuntime'] = str(randHrs) + ':' + str(randMin+2) + ':'  + str(randSec)
    metadata['timeCode']['actualRuntime'] = str(randHrs) + ':' + str(randMin) + ':'  + str(randSec)
    metadata['timeCode']['titleSeqStart'] = '00:02:00'
    metadata['timeCode']['titleSeqEnd'] = '00:02:30'
    metadata['timeCode']['titleFrameTimeCode'] = None
    metadata['timeCode']['endCreditsStartTime'] = str(randHrs) + ':' + str(randMin-2) + ':'  + str(randSec)
    metadata['timeCode']['endCreditsEndTime'] = str(randHrs) + ':' + str(randMin-1) + ':'  + str(randSec)
    metadata['timeCode']["adInsertionBlocks"] = ["00:10:00","00:30:00","1:30:00","2:00:00"]
    record['metadata'] = metadata
    record['entitlements'] = getRandEntitlements('US')
    print json.dumps(record,indent='  ')  
	noOfrecords  += 1
    if 	noOfrecords < len(movies) -1 :
        print ','
print ']\n}'
