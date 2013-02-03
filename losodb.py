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
			    username text primary key,
				password text not null,
				photourl text not null,
				email text not null,
				log integer
				)		      ''' )       
        
			self.cursor.execute('''
		
			CREATE TABLE tweets 
				(
				tweetid integer primary key autoincrement, 
				body text not null, 
			        latitude real not null,
				longitude real not null, 
                                timestamp integer not null,				
				username text not null,
				type text,
				FOREIGN KEY(username) REFERENCES user(username)
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
		 	 	  
  def adduser(self,username,password,email):
	values = ( username, password, username+ ".jpg", email,0) 
	self.query(" insert into user values (?,?,?,?,?)",values)    

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
	                     username =  ? and type = ? ''',values)
	return tweetid[0][0]

  def addtip(self,username,body,latitude,longitude,timestamp,taglist):
	values = (body,latitude,longitude,timestamp,username,"tip") 
	self.query(''' insert into tweets (  body , latitude, longitude ,
						timestamp , username , type)
						values (?,?,?,?,?,?)''',values)
	tweetid = self.gettweetid(values)
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
         
  def gettaglist(self):	
    taglist = self.query('''select tagname from tag''')
    return taglist	   
             
	   	     
if __name__ == "__main__":
  db = losoDB()
  print db.search(["bus"])
