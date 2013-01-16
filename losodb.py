# -*- coding: utf-8 -*-
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
				password text,
				photourl text,
				email text,
				log integer
				)		      ''' )       
        
			self.cursor.execute('''
		
			CREATE TABLE tweets 
				(
				tweetid integer primary key autoincrement, 
				body text, 
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
			    tagname text unique
				
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
          

  def query(self,query):
    cursor = self.connection.cursor() 
    cursor.execute(query)    
    self.connection.commit()
    return cursor.fetchall()
  
  def authenticate( self, username , password):
	realpassword = self.query(" select password from user where username = '" + username + "'")
	try:
		if realpassword[0][0] == password :  
			return True
	except IndexError :
			return False
	return False
		 
  def getuser(self,username):    
	 return self.query(" select * from user where username = '" + username + "'")	 
	 
  def gettable(self,tablename):
	 return  self.query(" select * from " + tablename  ) 
		 	 	  
  def adduser(self,username,password,email):
	cursor = self.connection.cursor()
	values = ( username, password, username+ ".jpg", email,0) 
	cursor.execute(" insert into user values (?,?,?,?,?)",values)    
	self.connection.commit()

  def gettagid(self,tag):
	tagid = self.query(" select tagid from tag where tagname = " + tag)
	try: 
		return tagid[0][0]
	except IndexError :
		self.query(" insert into tag values ( " + tag +")" )

   
  def gettweetid(self,values):
	tweetid = self.query(''' select tweetid from tweet where 
	                     body = value[0] and latitude = value[1] and
	                     longitude = value[2] and timestamp = value[3] and
	                     username =  value[4]''')
	return tweetid[0][0]

  def addtip(self,username,body,latitude,longitude,timestamp,taglist):
	cursor = self.connection.cursor()
	values = (body,latitude,longitude,timestamp,username,"tip") 
	cursor.execute(''' insert into tweets 
						values (?,?,?,?,?,?)''',values)
	self.connection.commit()
	tweetid = self.gettweetid(values)
	
	for tag in taglist:
		tagid = self.gettagid(tag)
		cursor.execute(''' insert into tagtiprelation 
			values (?,?,"tip")''',tagid,tweetid)							    
	self.connection.commit()	
	   
	   
	   
	   
	     
if __name__ == "__main__":
  db = losoDB()
  print db.getuser("*")
  # db.query(''' insert into user values ("sebin","sebin","sebin","sebin7@gmail.com",0) ''')
 
   #c= db.query( ''' select * from user ''') 
   #for row in c :
   #  print row
   #if( db.userauthentication("nikhil","nikhil") ):
	#   print " true "
   #else :
	#   print " false"

