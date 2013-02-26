# Filename: tweetset.py

from losodb import *

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
       

def main():
   db = losoDB()
   tweettagdict = db.getpage(8.54,76.89,1.5)
   T = tweetset(tweettagdict)
   print T.get_user("activity")
   print T.get_user("recent")   
   print T.get_user() 
   print T.get_centroid()
   print T.get_taglist()

if __name__ == "__main__":  
    main() 


