import urllib2
import json



def fromapi( latitude , longitude ,limit ):
	data=urllib2.urlopen('''https://api.foursquare.com/v2/tips/search?ll={0},{1}&limit={2}&oauth_token=DJGP2ZUTS1DIPEEMQJ05KPAR0YK5RVXGJWLJIOEZORSPMUW0&v=20130227'''.format(latitude,longitude,limit))

	data_obj = json.loads(data.read())
	for data in data_obj["response"]["tips"]:
   	   print data["text"]
	return data_obj




def forsquaredataextractor(data_obj):
    ''' This function organises data_obj given by foursquare API into two sets user & tweet. User set is a list of tuples (userid, firstName, lastName, gender, password, photourl, email) and tweet set is a list of tuples (body, latitude, longitude, timestamp, userid)'''

    set1 = set() 
    set2 = set()

    for data in data_obj["response"]["tips"]:
        try:
            set1.add((data["user"]["id"], data["user"]["firstName"], data["user"]["lastName"], data["user"]["gender"], "password", data["user"]["firstName"]+".jpg", data["user"]["firstName"]+"@gmail.com"))
            set2.add((data["text"], data["venue"]["location"]["lat"], data["venue"]["location"]["lng"], data["createdAt"], data["user"]["id"], 'tip'))
        except KeyError:
            set1.add((data["user"]["id"], data["user"]["firstName"], None, data["user"]["gender"], "password", "user.jpg", "user@gmail.com"))
            set2.add((data["text"], data["venue"]["location"]["lat"], data["venue"]["location"]["lng"], data["createdAt"], data["user"]["id"], 'tip'))
    return set1,set2



def getsquare(latitude,longitude,width = 1000):
        lateq200 = 0.0008983207989 *2
	longeq200 = 0.0009071496   *2
	newlat = latitude + 0.0008983207989
        newlong = longitude + 0.0009071496
        
        n = (width/200) +1
        superset_user = set([])
        superset_tweets = set([])  
	for i in range(n):
	  for j in range(n):
		data_obj = fromapi(latitude+(i*lateq200) , longitude +(j*longeq200) ,100)
	  	userset,tweetset =  forsquaredataextractor(data_obj)
                superset_user = superset_user | userset
                superset_tweets = superset_tweets |tweetset
	
        for i in range(n-1):
	  for j in range(n-1):
		data_obj = fromapi(latitude+(i*lateq200) , longitude +(j*longeq200) ,100)
	  	userset,tweetset =  forsquaredataextractor(data_obj)
                superset_user = superset_user | userset
                superset_tweets = superset_tweets |tweetset
		
        print superset_user 
        print superset_tweets  
        return superset_user , superset_tweets


def feedtrivandram(lat = 8.82,lon =76.6, n = 35):
     	
      for i in range(n):
	for j in range(n):
	    userset,tweetset = getsquare(lat+(i*lateq1000),lon+(i*longeq1000),1000)
            adduserset(userset)
	    addtweetset(tweetset)



        
getsquare(8.54389,76.895,1000)
            



    
