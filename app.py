from flask import Flask, render_template, request, json, send_from_directory, redirect, url_for, session, escape
#from flaskext.mysql import MySql
from flask_mysqldb import MySQL
from werkzeug import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
mysql = MySQL(app)
 
# MySQL configurations
app.config['MYSQL_USER'] = 'bdda20b2a0f5ee'
app.config['MYSQL_PASSWORD'] = 'f14d9eef'
app.config['MYSQL_DB'] = 'heroku_b00189bd70b3211'
app.config['MYSQL_HOST'] = 'us-cdbr-iron-east-05.cleardb.net'
app.config['UPLOAD_FOLDER'] = 'static/Uploads'
#mysql.init_app(app)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def checkLogin():
    if '_email' in session:
        print('logged in as %s' % escape(session['_email']))
        return 1
    else:
        print ('You are not logged in')
        return 0


@app.route("/")
def main():
    if checkLogin():
        return render_template('indexLoggedIn.html', username = escape(session['_email']))
    else:
        print ('You are not logged in')
        return render_template('indexLoggedOut.html')

	
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
	
@app.route('/showSignIn')
def showSignIn():
	return render_template('signin.html')
	
@app.route('/calculator')
def calculator():
    if checkLogin():
        return render_template('calculatorLoggedIn.html', username = escape(session['_email']))
    else:
        return render_template('calculatorLoggedOut.html')


@app.route('/uploads/<path:filename>')
def download_file(filename):
    #uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)
							

@app.route('/signIn', methods = ['GET','POST'])
def signIn():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        
        # validate the received values
        if _email and _password:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("SELECT user_username FROM tbl_user WHERE user_username = %s AND user_password = %s", [_email, _password])
            row = cursor.fetchone()
            if row:
                session['_email'] = request.form['inputEmail']
                session['_password'] = request.form['inputPassword']
		        #do something for a successful login here:
                return redirect(url_for('main'))
            else:
			    #do something for a failed login here, this hsould probably include email already exists, but password is wrong, etc
                return redirect(url_for('showSignIn'))
				
        else:
		    #do something for not getting the full request from the webform
            return redirect(url_for('showSignIn'))
    except Exception as e:
	    return json.dumps({'error':str(e)})
	
			
			
@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            conn = mysql.connection
            cursor = conn.cursor()
            #_hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_password)) # this was previously _hashed password
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        #cursor.close() 
        #conn.close()
        return render_template('index.html')
        
@app.route('/signOut')
def logout():
    # remove the username from the session if it's there
    session.pop('_email', None)
    return redirect(url_for('main'))
		
@app.route('/showToDo')
def showToDo():
	return render_template('ToDo.html')
	
@app.route('/toDo', methods = ['GET','POST'])
def toDo():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _email and _password:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("SELECT user_username FROM tbl_user WHERE user_username = %s AND user_password = %s", [_email, _password])
            row = cursor.fetchall()
            if row:
		        #do something for a successful login here:
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.execute("SELECT entry_date, item FROM to_do_list WHERE user_username = %s", [_email])
                items = cursor.fetchall()
                if items:
                    return 'this is your to do list: {0}'.format(items)
                else:
                    return 'error failed to collect your items'
            else:
			    #do something for a failed login here, this hsould probably include email already exists, but password is wrong, etc
                return redirect(url_for('showToDo'))
				
        else:
		    #do something for not getting the full request from the webform
            return redirect(url_for('showSignIn'))
    except Exception as e:
	    return json.dumps({'error':str(e)})


if __name__ == "__main__":
    app.run()