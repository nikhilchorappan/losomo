import os
import sqlite3 
from config import *

class losoDB():
  
  def __init__(self):
    """ 
     This function takes a path name as input  default path name
     and returns the connection object that connected to database ,this function
     will raise error if the given path does not exist. If the database is creating
     for the first time it also sets its initial setings such as creating required tables 
    """
    DBpath = default_DBpath 
    if not (  os.path.exists(os.path.dirname(DBpath))):
       raise IOError('Default database path %s to create losomo database does not exist'%os.path.dirname(DBpath))  	
     
    if not (os.path.exists(DBpath) ):      # no database is created yet . 
      try:
           self.connection = sqlite3.connect(DBpath)
      except sqlite3.OperationalError:
           raise IOError(' Cannot create a losomo database file at %s ' %DBpath )
      else :    
			#______ initial setings________#
			self.cursor = self.connection.cursor() 
			self.cursor.execute('''create table CachedList( title text )''' )
        
			self.cursor.execute('''
			CREATE TABLE user 
				(  
                                userid integer primary key,
			        firstname text not null,
                                lastname text,
                                gender text, 
				password text not null,
				photourl text not null,
				email text not null
				)		      ''' )       
        
			self.cursor.execute('''
		
			CREATE TABLE tweets 
				(
				tweetid integer primary key autoincrement, 
				body text not null, 
			        latitude real not null,
				longitude real not null, 
                                timestamp integer not null,				
				userid text not null,
				type text,
				FOREIGN KEY(userid) REFERENCES user(userid)
				)             ''' )	
				
			self.cursor.execute('''
			CREATE TABLE tag 
				(  
				tagid integer primary key autoincrement,
			        tagname text unique not null
				
			     )            ''' )
	
			self.cursor.execute('''
			CREATE TABLE tagtiprelation 
				(  
			        tagid integer,
				tweetid integer,
				tagtype text,
				FOREIGN KEY(tagid) REFERENCES tag(tagid)
				FOREIGN KEY(tweetid) REFERENCES tweets(tweetid),
				PRIMARY KEY(tagid,tweetid)
				)				
			                        ''' )
	
			self.cursor.execute( '''CREATE  UNIQUE 
				INDEX tweetindex ON  tweets ( tweetid )''')
				
			self.cursor.execute( '''CREATE  UNIQUE 
				          INDEX tagindex ON  tag ( tagid )''')
					
			self.connection.commit()
    else :
      try :
        self.connection = sqlite3.connect(DBpath)
      except sqlite3.OperationalError:
          raise IOError(' Unable to open a database file at %s'%DBpath) 
          

  def query(self,query,values = None ):
    cursor = self.connection.cursor()
    if values :
		cursor.execute(query,values)		
    else :
		cursor.execute(query)    
    self.connection.commit()
    return cursor.fetchall()
 
  
  def authenticate( self, username , password):
	realpassword = self.query(" select password from user where username = ? ",[username])
	try:
		if realpassword[0][0] == password :  
			return True
	except IndexError :
			return False
	return False
		 
  def getuser(self,username):    
	 return self.query(" select * from user where username = ?",[username])	 
	 
  def gettable(self,tablename):
	 return  self.query(" select * from " + tablename ) 
		 	 	  
  def adduserset(self,userset):
      for usertuple in userset: 
          try:
	      self.query(" insert into user values (?,?,?,?,?,?,?)",usertuple)    
          except Exception:
              pass     

  def gettagid(self,tag):
	tagid = self.query(" select tagid from tag where tagname = ?",[tag])

	try: 
		return tagid[0][0]
	except IndexError :
		self.query(" insert into tag ( tagname ) values ( ?)",[tag])
		tagid = self.query(" select tagid from tag where tagname = ?",[tag])
		return tagid[0][0]

   
  def gettweetid(self,values):
	tweetid = self.query(''' select tweetid from tweets where 
	                     body = ? and latitude = ? and
	                     longitude = ? and timestamp = ? and
	                     userid =  ? and type = ? ''',values)
	return tweetid[0][0]

  def addtip(self, tweetset):
      from topia.termextract import extract
      from topia.termextract import tag
      tagger = tag.Tagger()
      tagger.initialize()
      extractor = extract.TermExtractor(tagger)
      extractor.filter = extract.permissiveFilter

      extractor = extract.TermExtractor()
      extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=2)   
      for tweettuple in tweetset:
          tweettuple += ("tip",)
	  self.query(''' insert into tweets (  body , latitude, longitude ,
						timestamp , userid , type)
						values (?,?,?,?,?,?)''',tweettuple)
          tagextractor = extractor(tweettuple[0])
          for tag in tagextractor:
              taglist = tag[0][0]
          print taglist
	  tweetid = self.gettweetid(tweettuple)
	  for tag in taglist:
              tagid = self.gettagid(tag)
	      self.query(''' insert into tagtiprelation 
			values (?,?,"tip")''',(tagid,tweetid))							    
      self.connection.commit()	
	   
  def search(self,taglist = None ,username = None,latitude = None,longitude = None):
    tweetlist = []
    for tag in taglist:
      tweetlist.append( self.query( '''
					select username , body ,tweets.tweetid from tweets ,tagtiprelation ,tag
					where tweets.tweetid = tagtiprelation.tweetid and
				    tag.tagid = tagtiprelation.tagid 
				    and tag.tagname  = ? ''',[tag]) )
    tweettaglist = []
    for tweet in tweetlist[0]:
      taglist = self.query('''select tagname from tag,tagtiprelation
                                   where tag.tagid = tagtiprelation.tagid and 
                                    tagtiprelation.tweetid = ?''',[tweet[-1]] )
      tweettaglist.append(tuple(list( tweet[0:-1]) +taglist ))     
    return tweettaglist	
    
  def gethomedata(self,taglist = None ,username = None,latitude = None,longitude = None):
    tweetlist  = self.query("select username, body,tweetid from tweets")
    tweettaglist = []
    for tweet in tweetlist :
      taglist = self.query('''select tagname from tag,tagtiprelation
                                   where tag.tagid = tagtiprelation.tagid and 
                                    tagtiprelation.tweetid = ?''',[tweet[-1]] )    
      tweettaglist.append(tuple(list( tweet[0:-1]) +taglist ))
    return tweettaglist      
         
  def gettweettaglist(self,taglist = None ,username = None,latitude = None,longitude = None):
    tweetlist  = self.query("select username, body, timestamp, latitude, longitude, tweetid from tweets")
    tweettaglist = []
    for tweet in tweetlist :
      taglist = self.query('''select tagname from tag,tagtiprelation
                                   where tag.tagid = tagtiprelation.tagid and 
                                    tagtiprelation.tweetid = ?''',[tweet[-1]] )    
      tweettaglist.append(tuple(list( tweet[0:-1]) +taglist ))
    return tweettaglist 

  def gettaglist(self):	
    taglist = self.query('''select tagname from tag''')
    return taglist	   


  def getpage(self,clat,clong, width ):
    ''' getpage function returns all tweets and its associated data
        within an area. The area is called page which always will be in the shape of a square
        clat and clong gives the latitude and longitude of the centroid of the square.
        and width gives its side leangth. It returns the data as a list of dictionry
        where each dictionary have following contents

       tweetdict = { 'id' : type integer tweetid
                     'body' : type string tweetbody
                     'latitude' :  type real 
                     'longitude' : type real
                     'timestamp' : type integer
                     'username'  : type text username who wrote that tweet
                     'type' : type text ( "tip","notification ",etc)
                     'tagset' : type set ( set of tags belongs to that tweet)}


        ''' 

    radius = width/2
    tweettuplelist  = self.query('''select * from tweets 
                               where latitude between {0} and {1} and 
                               longitude between {2} 
                               and {3} '''.format(clat-radius, clat+radius, clong-radius, clong+radius))
    tweetdictlist = []
    for tweettuple in tweettuplelist :
       tagtuplelist = self.query('''select tagname from tag,tagtiprelation
                                   where tag.tagid = tagtiprelation.tagid and 
                                    tagtiprelation.tweetid = ?''',[tweettuple[0]] )
       taglist = []
       for tagtuple in tagtuplelist:
          taglist.append(tagtuple[0])
       tagset=set(taglist)
       tweetdict = { 'id' : tweettuple[0],
                     'body' : tweettuple[1],
                     'latitude' : tweettuple[2],
                     'longitude' : tweettuple[3],
                     'timestamp' : tweettuple[4],
                     'username' : tweettuple[5],
                     'type' : tweettuple[6],
                     'tagset' : tagset }
 
       tweetdictlist.append(tweetdict)
    return tweetdictlist              
	   	     
if __name__ == "__main__":
  db = losoDB()
  body = " this is for cheking"
  timestamp = 0
  username = "nikhil"
  
  values = (body,None,None,timestamp,username,"tip")
  # print db.query(''' insert into tweets (  body , latitude, longitude ,
  #  						timestamp , username , type)
  #						values (?,?,?,?,?,?)''',values)
  lats =  db.query(''' select longitude from tweets''')
  #print lats
  l = db.getpage(8,76,5)
  print l
 # print l[0]

  #for l in lats:
   # if l>0 :
    #     print l[0].real
