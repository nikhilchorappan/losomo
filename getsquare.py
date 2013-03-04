import urllib2
import json


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



def getsquare(lat, lng):
    
    '''This function gets the data from foursquare API by considering a square of 800m side. We get data from this square by viewing the square as overlapping circles and calling foursquare API for the circles.Here we consider a side equivalent to 5 circles of radius 100m''' 

    newlat = lat + 0.0008983207989
    newlng = lng + 0.0009071496
    superset1 = set()
    superset2 = set()
    for i in range(5):
        for j in range(5):
            data=urllib2.urlopen('https://api.foursquare.com/v2/tips/search?ll='+ str(lat+i*0.00179836) +','+ str(lng+j*0.00179836) + '&limit='+str(100)+'&oauth_token=DJGP2ZUTS1DIPEEMQJ05KPAR0YK5RVXGJWLJIOEZORSPMUW0&v=20130227')
            data_obj = json.loads(data.read())
            set1,set2=forsquaredataextractor(data_obj)
            superset1|=set1
            superset2|=set2   
    for i in range(4):
        for j in range(4):
            data=urllib2.urlopen('https://api.foursquare.com/v2/tips/search?ll='+ str(newlat+i*0.00179836) +','+ str(newlng+j*0.00179836) + '&limit='+str(100)+'&oauth_token=DJGP2ZUTS1DIPEEMQJ05KPAR0YK5RVXGJWLJIOEZORSPMUW0&v=20130227')
            data_obj = json.loads(data.read())
            set1,set2=forsquaredataextractor(data_obj)
            superset1|=set1
            superset2|=set2 
    newlat+=0.0008983207989
    newlng+=0.0009071496
    for i in range(3):
        for j in range(3):
            data=urllib2.urlopen('https://api.foursquare.com/v2/tips/search?ll='+ str(newlat+i*0.00179836) +','+ str(newlng+j*0.00179836) + '&limit='+str(100)+'&oauth_token=DJGP2ZUTS1DIPEEMQJ05KPAR0YK5RVXGJWLJIOEZORSPMUW0&v=20130227')
            data_obj = json.loads(data.read())
            set1,set2=forsquaredataextractor(data_obj)
            superset1|=set1
            superset2|=set2 
    newlat+=0.0008983207989
    newlng+=lng + 0.0009071496
    for i in range(2):
        for j in range(2):
            data=urllib2.urlopen('https://api.foursquare.com/v2/tips/search?ll='+ str(newlat+i*0.00179836) +','+ str(newlng+j*0.00179836) + '&limit='+str(100)+'&oauth_token=DJGP2ZUTS1DIPEEMQJ05KPAR0YK5RVXGJWLJIOEZORSPMUW0&v=20130227')
            data_obj = json.loads(data.read())
            set1,set2=forsquaredataextractor(data_obj)
            superset1|=set1
            superset2|=set2
    '''
    newlat+=0.0008983207989
    newlng+=lng + 0.0009071496
    data=urllib2.urlopen('https://api.foursquare.com/v2/tips/search?ll='+ str(newlat+0.00179836) +','+ str(newlng+0.00179836) + '&limit='+str(100)+'&oauth_token=DJGP2ZUTS1DIPEEMQJ05KPAR0YK5RVXGJWLJIOEZORSPMUW0&v=20130227')
    data_obj = json.loads(data.read())
    set1,set2=forsquaredataextractor(data_obj)
    superset1|=set1
    superset2|=set2
    ''' 
    print superset1
    print superset2
            
getsquare(8.54389,76.895)            


    
