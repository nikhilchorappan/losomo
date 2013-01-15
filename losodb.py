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
				)
		''' )       
        
	self.cursor.execute('''
		
			CREATE TABLE tweets 
				(
				tweetid integer primary key, 
				body text, 
			    latitude real not null,
				longitude real not null, 
                timestamp integer not null,				
				username text not null,
				type text,
				FOREIGN KEY(username) REFERENCES user(username)
				)
				
		            ''' )
	
	self.cursor.execute(	'''
			CREATE TABLE friends 
				(  
			    username text,
				friend text,
				FOREIGN KEY(friend) REFERENCES user(username),
				FOREIGN KEY(username) REFERENCES user(username),
				PRIMARY KEY(username,friend) 
				)
			    ''' )

        self.cursor.execute('''
			CREATE TABLE tagtiprelation 
				(  
			    tagname text,
				tweetid integer,
				tagtype text,
				FOREIGN KEY(tweetid) REFERENCES tweet(tweetid),
				FOREIGN KEY(tagname) REFERENCES tags(name),
				PRIMARY KEY(tagname,tweetid)
				)				
			    ''' )
	
	self.cursor.execute( '''CREATE  UNIQUE 
				INDEX tweetindex ON  tweets ( tweetid )''')
					
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
    return cursor
  
  def authenticate( self, username , password):
	realpassword = self.query(" select password from user where username = '" + username + "'")
	row = realpassword.fetchall()
	try:
		if row[0][0] == password :  
			return True
	except IndexError :
			return False
	return False
		 
  def getuser(self,username):    
	 data = self.query(" select * from user where username = '" + username + "'")
	 return data.fetchall()
	 
  def gettable(self,tablename):
	 data = self.query(" select * from " + tablename  ) 
	 return data.fetchall()
		 	 
	  
  def adduser(self,username,password,email):
	cursor = self.connection.cursor()
	values = ( username, password, username+ ".jpg", email,0) 
	cursor.execute(" insert into user values (?,?,?,?,?)",values)    
	self.connection.commit()

  def addtip(self,username,body,latitude,longitude,timestamp,taglist):
	cursor = self.connection.cursor()
	values = (body,laitude,longitude,timestamp,username,"tip") 
	cursor.execute(''' insert into tweets 
						values (tweetindex.NEXT,?,?,?,?)''',values)
	self.connection.commit()
	for tag in taglist:
		cursor.execute(''' insert into tagtiprelation 
			values (?,tweetindex.current,"tip")''',tag)							    
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

