import simplejson as json
import collections
import sys
import random
import string
import copy

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
    entitlements['network'] = random.sample(['wi-fi','3g','ethernet','gprs'],noDev)
    entitlements['business_model'] = random.sample(['free','buy','rent'],noDev)
    entitlements['actions'] = random.sample(['preview','watch','watch_later'],noDev)
    return entitlements
	
def main():
    locales = json.load(open('locale.json'))['locales']
    entFile = open('entitlements.json','w')
    entFile.write('{ "entitlements" : [')
    noOfRecords = 10    
    try:
	    noOfRecords = int(sys.argv[1])
    except:
	    print 'Syntax: createEntitlements <no of records>'
    count = 0
    for x in xrange(noOfRecords):
        region = locales[random.choice(locales.keys())]
        ent = getRandEntitlements(region)
        entFile.write(json.dumps(ent))
        print json.dumps(ent,indent = '  ')
        count += 1
        if count < noOfRecords:
            entFile.write(',')
    entFile.write(']}')
    entFile.close()
	
if __name__ == '__main__':
    main()