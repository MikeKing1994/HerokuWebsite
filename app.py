from flask import Flask, render_template, request, json, send_from_directory, redirect, url_for, session, escape, Markup
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
mysql = MySQL(app)
 
# MySQL configuration and setup
app.config['MYSQL_DATABASE_USER'] = 'bdda20b2a0f5ee'
app.config['MYSQL_DATABASE_PASSWORD'] = 'f14d9eef'
app.config['MYSQL_DATABASE_DB'] = 'heroku_b00189bd70b3211'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-05.cleardb.net'
app.config['UPLOAD_FOLDER'] = 'static/Uploads'
mysql.init_app(app)
# set the secret key.  This is the secret key for the cookies, nothing to do with SQL
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def checkLogin():
    if '_email' in session:
        print('logged in as %s' % escape(session['_email']))
        return 1
    else:
        print ('You are not logged in')
        return 0


@app.route("/", methods = ['GET','POST'])
def main():
    if checkLogin():
        return render_template('index/indexLoggedIn.html', username = escape(session['_email']))
    else:
        print ('You are not logged in')
        return render_template('index/IndexLoggedOut.html')

	
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup/signupLoggedOut.html')
	
@app.route('/showSignIn')
def showSignIn():
	return render_template('signin/signinLoggedOut.html')
	
@app.route('/calculator')
def calculator():
    if checkLogin():
        return render_template('calculator/calculatorLoggedIn.html', username = escape(session['_email']))
    else:
        return render_template('calculator/calculatorLoggedOut.html')


#Downloads a file. File must be stored in /static/uploads.
@app.route('/uploads/<path:filename>')
def download_file(filename):
    #uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)
							

#This is the backend function for performing a signin, not to show the signin page.
@app.route('/signIn', methods = ['GET','POST'])
def signIn():
    try:
        #get the username and password from the form
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        
        # validate the received values
        if _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            #This is vulnerable to injection, room for improvement here.
            cursor.execute("SELECT user_username FROM tbl_user WHERE user_username = %s AND user_password = %s", [_email, _password])
            row = cursor.fetchone()
            if row:
                #if the login details are in the database, populates the cookie with the username and password
                session['_email'] = request.form['inputEmail']
                session['_password'] = request.form['inputPassword']
                return redirect(url_for('main'))
            else:
                #failed logins return you to the signin page
                return redirect(url_for('showSignIn'))
				
        else:
		    #failure to get data from the web form redirects to the signin page. Improve by showing a validation here
            return redirect(url_for('showSignIn'))
    except Exception as e:
	    return json.dumps({'error':str(e)})
	
			
#This is the backend function for performing a signup, not to show the signup page.
@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        #get the values from the web form
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createUser',(_name,_email,_password)) 
            data = cursor.fetchall()
            #len(data) will be non-zero if the proc returns an error message
            if len(data) is 0:
                conn.commit()
                return  redirect(url_for('main'))
			#Can improve by adding error handling here	
            else:
                return redirect(url_for('main'))
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return redirect(url_for('main'))
        
        
@app.route('/signOut')
def logout():
    #remove the username from the session if it's there
    session.pop('_email', None)
    return redirect(url_for('main'))
    
		
@app.route('/showToDo')
def showToDo():
    #when you first load the page you want to check if we're logged in, if not prompt sign in 
    #once signed in, display the list and also have an entry form to add to the list
    if checkLogin():
        #because you must be logged in to view this page, can get the username from the cookies
        _email = escape(session['_email'])
        print(_email)
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlstring=("SELECT id, item, entry_date FROM to_do_list WHERE user_username = '%s'" % _email) 
        cursor.execute(sqlstring)
        list = cursor.fetchall()
        #all of the handling of this list is done on the template
        return render_template('todo/toDoLoggedIn.html', username = _email, list = list)
    else:
        #the page can't be accessed without being logged in
        return render_template('todo/toDoLoggedOut.html')
        
	
#This is the backend function for adding an item to the to do list	
@app.route('/toDoAppend', methods = ['GET','POST'])
def toDoAppend():
    try:
        #This function needs the email of the logged in user and the item to be appended
        _email = escape(session['_email'])
        _Item = request.form['inputItem']
        # validate the received values
        if _email and _Item:
            conn = mysql.connect()
            cursor = conn.cursor()
		    #append the item to the list here:
            sqlstring=("INSERT INTO to_do_list (user_username, item, entry_date) VALUES ('%s', '%s', NOW());" % (_email , _Item))
            cursor.execute(sqlstring)
            conn.commit()
            return redirect(url_for('showToDo'))
        else:
		    #can improve by adding error handling here
            return redirect(url_for('showToDo'))
    except Exception as e:
        return redirect(url_for('showToDo'))
        

#This is the backend function for deleting an item from the to do list
@app.route('/deleteToDoItem', methods = ['GET','POST'])
def deleteToDoItem():
    #the button on the form itself returns the itemid of the item to be deleted
	itemId = request.form['delete']
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("delete from to_do_list where id = %s" , [itemId]) 
	conn.commit()
	return redirect(url_for('showToDo'))	


#These render the pages for the generic content pages
@app.route('/showContent1')
def showContent1():
	if checkLogin():
		return render_template('content/showContent1LoggedIn.html')
	else:
		return render_template('content/showContent1LoggedOut.html')
		
@app.route('/showContent2')
def showContent2():
	if checkLogin():
		return render_template('content/showContent2LoggedIn.html')
	else:
		return render_template('content/showContent2LoggedOut.html')

@app.route('/showContent3')
def showContent3():
	if checkLogin():
		return render_template('content/showContent3LoggedIn.html')
	else:
		return render_template('content/showContent3LoggedOut.html')

@app.route('/showContent4')
def showContent4():
	if checkLogin():
		return render_template('content/showContent4LoggedIn.html')
	else:
		return render_template('content/showContent4LoggedOut.html')
		
        
@app.route('/showValidationTest')
def showValidationTest():
	if checkLogin():
		return render_template('validationTest/ValidateLoggedIn.html', username = escape(session['_email']))
	else:
		return render_template('validationTest/ValidateLoggedOut.html')

        
#This function is called by the submit button on the validationTest page
@app.route('/validate', methods = ['GET','POST'])		
def validate():
    #get the three values from the form and the username from the cookies
	Field1 = request.form['Field1']
	Field2 = request.form['Field2']
	Field3 = request.form['Field3']
	_email = escape(session['_email'])
    
    #run through the validations and insert any flagged validations into validationList
	validationList = []
	if Field1 not in ['0','1']:
		validationList.append('Field 1 must be either 0 or 1')
	if Field2 is None:
		validationList.append('Field 2 cannot be left blank')
	if Field1 == Field3:
		validationList.append('Field 1 must not be equal to Field 3')
		
	if validationList ==[]:
		#insert into database and return to the page
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("insert into validationTest (user_id, DateCreated, Field1, Field2, Field3) values (%s, now(),%s,%s,%s)",[_email,Field1,Field2,Field3])
		conn.commit()
		return render_template('validationTest/ValidateLoggedIn.html')
        
##Incomplete sections
##@app.route('/showValidationReport', methods = ['GET','POST'])
##def showValidationReport():
##	if checkLogin():
##		return render_template('validationReport/ValidationReportLoggedIn.html', username = escape(session['_email']))
##	else:
##		return render_template('validationReport/ValidationReportLoggedOut.html')
##        
##		
##@app.route('/validationReport', methods = ['GET','POST'])
##def validationReport():
##	Fields = request.form.getlist('selectedList')
##	print(Fields)
##	return render_template('validationReport/ValidationReportLoggedIn.html', username = escape(session['_email']))
##		

		
if __name__ == "__main__":
    app.run()