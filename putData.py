import simplejson as json
import requests
import threading
import sys
import collections
#from updateData import updateData
import properties
esURL = 'http://' + properties.host + ':' + properties.port + '/' + properties.index + '/' + properties.type

def putData(data,movie_id):
    URL = (esURL + "/%s")%movie_id    
    headers = {'Accept': 'application/json'}
    r = requests.post(URL,data=data,headers=headers)
    print r.text,r.url 
   
try:
    movieFile = open(sys.argv[1],'r')
except:
    print 'syntax: putData <MoviesFileName> [no. of records]'
    sys.exit(0) 
movies = json.load(movieFile)
print len(movies)
count = 1
try :
    noOfRecords = sys.argv[2]
except:
    noOfRecords = len(movies)
print "No. of records to be inserted: ",noOfRecords
for movie in movies:
    t = threading.Thread(putData(json.dumps(movie),movie['guid']))
    t.start()
    count += 1
    if count > int(noOfRecords) :
        print "Inserted records"
        break