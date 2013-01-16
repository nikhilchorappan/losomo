# -*- coding: utf-8 -*-
from flask import *
from losodb import *
from flask import request

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])

def log():
	if request.method == 'GET':
		return  render_template('login.html',error = None)    
	else:
		return valid_login( request.form['username'],request.form['password'])
 

def valid_login(username,password):
   db = losoDB()
   if db.authenticate(username,password) :
	  return render_template('tipreader.html',name = username)
   else :
	  return render_template('login.html',error = " Authentication faild" )


@app.route('/sign_up', methods=['POST','GET'])

def signup():
	if request.method == 'GET':
		return  render_template('signup.html')    
	else:
		db = losoDB()
		db.adduser( request.form['username'],
						request.form['password'],request.form['email'])													    
		return render_template('login.html',error = None) 
							 


@app.route('/tipreader', methods=['POST','GET'])

def tipreader():
	 
	if request.method == 'POST':
		db = losoDB()
		taglist = request.form['taglist'].rsplit(' ')
		db.addtip( request.form['username'], request.form['body'],
						request.form['latitude'],request.form['longitude'],
						0, taglist)													    
		return render_template('tipreader.html', name = request.form['username'] ) 
							 





@app.route('/admin/table/<table_name>')

def showtable(table_name):
	db = losoDB()
	data = db.gettable(table_name)							    
	return render_template('showtable.html',table = data) 



if __name__ == '__main__':
	app.run(debug = True)

