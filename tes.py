# -*- coding: utf-8 -*-
from flask import *
from cache1 import *
from flask import request


app = Flask(__name__)

@app.route('/hom')

def hello_world():
   db = losoDB()
   c = db.query( ''' select * from CachedList ''')
   lis = []
   for row in c:
     lis.append(row)
   return lis[7]
   
def valid_login(latitude,longitude):
   db = losoDB()
   c= db.query( ''' select * from CachedList ''')
   #execute("insert into %s 
	#  values ( ?,?,?,?,?,?,?,?,?,?,?
	 # ,?,?,?,? )" %os.path.dirname(row[0]).replace('/','_'), crow)
                     
                     
                     
   lis = []
   for row in c:
     lis.append(row)
   #if name == lis[7][0] :
    #  return render_template('login.html',name= None)
  
  #else :
   return render_template('home.html',name= latitude + " & " + longitude)

   
@app.route('/login', methods=['POST','GET'])

def log():
    return render_template('login.html')

@app.route('/home',methods = ['POST','GET'])

def login():
  
  if request.method == 'GET':
    return  render_template('home.html',name = 'Nikhil')
    
  else:
    return valid_login( request.form['latitude'],request.form['longitude'])
    

if __name__ == '__main__':
	app.run(debug = True)
	#app.run(host = '0.0.0.0')
