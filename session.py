from flask import Flask, session, redirect, url_for, escape, request, render_template
from werkzeug import secure_filename


app = Flask(__name__)


@app.route('/login')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':	
		f = request.files['the_file']
		f.save('/var/www/uploads/uploaded_file.jpg')
                return "file saved<br>"
        return render_template('photo.html')



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('upload_file'))
    return render_template('log.html')



@app.route('/sign_up', methods=['GET', 'POST'])
def sign_in():
     if request.method == 'POST':
        session['username'] = request.form['username']
	return redirect(url_for('index'))
     return render_template('signup.html') 	



@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
# set the secret key. keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__=="__main__":
    app.run(debug=True)
