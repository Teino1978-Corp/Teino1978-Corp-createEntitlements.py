import simplejson as json
import requests
import threading
import sys
import properties
import collections
import random
esURL = 'http://' + properties.host + ':' + properties.port + '/' + properties.index + '/' + properties.type

def updateData(data,movie_id):
    URL = (esURL + '/%s' + '/_update')%movie_id    
    headers = {'Accept': 'application/json'}
    print data
    r = requests.post(URL,data=data,headers=headers)
    print r.text,r.url 
 
def main(): 
    try:
        entFile = open(sys.argv[1],'r')
    except:
        print 'syntax: updateData <entitlements_file> [no. of records]'
        sys.exit(0) 
    ent = json.load(entFile,object_pairs_hook=collections.OrderedDict)['entitlements']
    count = 1
    try :
        noOfRecords = sys.argv[2]
    except:
        noOfRecords = json.loads(requests.get(esURL+'/_count').text)['count']
    print 'No. of records to be inserted: ',noOfRecords
    import pdb;pdb.set_trace()
    resp = requests.get( esURL+ '/_search?size=%s&_source=_id'%str(noOfRecords) )
    resp = json.loads(resp.text)['hits']['hits']
    ids = [x['_id'] for x in resp]
    for id in ids:
        movie = {'doc' : {'entitlements' :  random.choice(ent)}}
        t = threading.Thread(updateData(json.dumps(movie),id))
        t.start()
        count += 1
        if count > int(noOfRecords) :
            print "Inserted records"
            break
            
if __name__ == '__main__' :
    main()