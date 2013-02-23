# Filename: tweetanalyser.py

from losodb import *

class tweetanalyser:
    '''This class does all the desired work needed from a set of tweets and the associated tags'''

    def __init__(self, tweettaglist):
        '''This init function initialises the object instance'''
        # tweettaglist is a list in the order username, tweet, timestamp, location, tags
        self.tweettaglist = tweettaglist

    def get_user(self, sortby = None):
        '''This func returns the username based on the condition given in sortby parameter'''
        usertweetlist = []

        if sortby == 'activity':
            for tweettag in self.tweettaglist:
                count = 1
                # first check whether username already added in the usertweetlist if so increment count else append to the list  
                if tweettag[0] in [x[1] for x in usertweetlist]:
                    for (i,x) in enumerate(usertweetlist): 
                        if (tweettag[0] == x[1]): 
                            usertweetlist[i][0]+=1 
                else:
                    usertweetlist.append([count, tweettag[0]])
            usertweetlist.sort(key = lambda x:x[0], reverse = True)
            return usertweetlist[0][1]
 


def main():
   db = losoDB()
   tweettaglist = db.gettweettaglist()
   T = tweetanalyser(tweettaglist)
   print T.get_user("activity")      


if __name__ == "__main__":  
    main() 


