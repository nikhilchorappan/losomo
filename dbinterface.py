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
     for the first time it also sets its initial setings such as creating table such as CachedList 
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
			CREATE TABLE comments 
				(  
			        userid integer,
				tweetid integer,
				body text,
				FOREIGN KEY(tweetid) REFERENCES tweet(tweetid),
				FOREIGN KEY(userid) REFERENCES user(userid)
				)
	    ''' )

	self.cursor.execute('''
			CREATE TABLE graph 
				( 
				tag1 text,
			        tag2 text,
				count integer not null,
				FOREIGN KEY(tag1) REFERENCES tag(name),
				FOREIGN KEY(tag2) REFERENCES tag(name),
				PRIMARY KEY(tag1,tag2) 
				)
	    ''' )

	self.cursor.execute('''
			CREATE TABLE action 
			      ( 
			      username text not null,
			      tipid integer not null,
			      FOREIGN KEY(username) REFERENCES user(username),
			      FOREIGN KEY(tipid) REFERENCES tips(id),
			      PRIMARY KEY(username,tipid) 
			      )
		    ''' )


	self.cursor.execute( '''
			        CREATE TABLE tags ( name text primary key,
					   count integer not null
					 )
			      ''')




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
               #return conn.cursor()
      except sqlite3.OperationalError:
          raise IOError(' Unable to open a database file at %s'%DBpath) 
          

  def query(self,query):
    self.cursor = self.connection.cursor() 
    self.cursor.execute(query)    
    self.connection.commit()
    return self.cursor
    
     
  
if __name__ == "__main__":
   db = losoDB()
   #db.query(''' insert into CachedList values ("colin") ''')
   c= db.query( ''' select * from CachedList ''') 
   for row in c :
     print row