# Filename: tweetset.py

import numpy as np
from losodb import *
from sgraph import sgraph
import math
import matplotlib.pyplot as plt

class tweetset:
    '''This class does all the desired work needed from a set of tweets and the associated tags'''

    def __init__(self, tweettagdict):
        '''This init function initialises the object instance'''
        self.tweettagdict = tweettagdict

    def get_user(self, sortby = None):
        '''This func returns the username based on the condition given in sortby parameter'''
        usertweetlist = []

        if sortby == 'activity':
            # here usertweetlist is a list of list count, username
            for tweettag in self.tweettagdict:
                count = 1
                # first check whether username already added in the usertweetlist if so increment count else append to the list  
                if tweettag['username'] in [usertweet[1] for usertweet in usertweetlist]:
                    for (i,usertweet) in enumerate(usertweetlist): 
                        if (tweettag['username'] == usertweet[1]): 
                            usertweetlist[i][0]+=1 
                else:
                    usertweetlist.append([count, tweettag['username']])
            usertweetlist.sort(key = lambda usertweet:usertweet[0], reverse = True)
            return usertweetlist[0][1]
         
        elif sortby == 'recent':
            # here usertweetlist is a list of list timestamp, username
            for tweettag in self.tweettagdict:
                # first check whether username already added in the usertweetlist if so update timestamp in usertweetlist else append  
                if tweettag['username'] in [usertweet[1] for usertweet in usertweetlist]:
                    for (i,usertweet) in enumerate(usertweetlist): 
                        if (tweettag['username'] == usertweet[1]): 
                            usertweetlist[i][0] = tweettag['timestamp'] 
                else:
                    usertweetlist.append([tweettag['timestamp'], tweettag['username']])
            usertweetlist.sort(key = lambda usertweet:usertweet[0], reverse = True)
            return usertweetlist[0][1]
 
        elif sortby == None:
            return self.tweettagdict[0]['username']

        else:
            print "Warning : You have entered a wrong sortby parameter in get_user() function" 


    def get_centroid(self):
        '''This function returns a dict centroid of the locations in a tweetset
        {'latitude': type real,
         'longitude': type real}'''
        centroid = dict.fromkeys(["latitude", "longitude"], 0)
        
        for tweettag in self.tweettagdict:
            centroid["latitude"]+=tweettag['latitude']
            centroid["longitude"]+=tweettag['longitude']
        centroid["latitude"]/=len(self.tweettagdict)
        centroid["longitude"]/=len(self.tweettagdict)
        return centroid    
                  
    def get_taglist(self):
        '''This function examines the tagset of tweettagdict and returns the tag & count of it's occurence as a dict '''
        tagdict = {}
        for tweettag in self.tweettagdict:
            for tag in tweettag['tagset']:
                if tag in tagdict:
                    tagdict[tag]+=1
                else:
                    tagdict[tag] = 1 
        return tagdict      
          
     
    def __tweet_distance(self,lat1, long1, lat2, long2):
        if( lat2 == None):
		print yes
	# Convert latitude and longitude to 
    	# spherical coordinates in radians.
    	degrees_to_radians = math.pi/180.0
        
    	# phi = 90 - latitude
    	phi1 = (90.0 - lat1)*degrees_to_radians
    	phi2 = (90.0 - lat2)*degrees_to_radians
        
    	# theta = longitude
    	theta1 = long1*degrees_to_radians
    	theta2 = long2*degrees_to_radians
        
    	# Compute spherical distance from spherical coordinates.
        
    	# For two locations in spherical coordinates 
    	# (1, theta, phi) and (1, theta', phi')
    	# cosine( arc length ) = 
    	#    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    	# distance = rho * arc length
    
    	cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           	math.cos(phi1)*math.cos(phi2))
        try:
          arc = math.acos( cos )
        except ValueError:
           return 0.0
    	# Since radious of the earth is 6378100 meters the distance in meter is 
    	return arc* 6378100   
	
    def getDistanceMatrix(self):
	 l =  len(self.tweettagdict)
         print l
         D = np.zeros((l,l),int)
	 for i in range(l):
             for j in range(l):    
                     D[i][j] = self.__tweet_distance(self.tweettagdict[i]['latitude'], 
                                             self.tweettagdict[i]['longitude'], 
                                             self.tweettagdict[j]['latitude'], 
                                             self.tweettagdict[j]['longitude']   )                 
         return D

    def getlatitudelist(self):
        latitudelist = []
        for tweettag in self.tweettagdict:
            latitudelist.append(tweettag['latitude'])
        return latitudelist


    def getlongitudelist(self):
        longitudelist = []
        for tweettag in self.tweettagdict:
            longitudelist.append(tweettag['longitude'])
        return longitudelist


     




def main():
   db = losoDB()
   tweettagdict = db.getpage(8.54,76.89,1.5)
   #T = tweetset(tweettagdict)
    
   #print T.get_user("activity")
   #print T.get_user("recent")   
   #print T.get_user() 
   #print T.get_centroid()
   #print T.get_taglist()


   db = losoDB()
   page = db.getpage(8,76,5)
   T = tweetset(page)      
   D =  T.getDistanceMatrix()
   p = sgraph(D).getcluster(2)
   l = []
   for i in range(2):
     l.append([])
   for i in range(len(page)):
      l[p[i]].append(page[i])

   T1 = tweetset(l[0])
   T2 = tweetset(l[1])
  
   plt.plot(T1.getlatitudelist(), T1.getlongitudelist(), 'r.')
   plt.plot(T2.getlatitudelist(), T2.getlongitudelist(), 'b.')
   plt.axis([8.48, 8.55, 76.88, 76.95]) 
   plt.show()

if __name__ == "__main__":  
    main() 


