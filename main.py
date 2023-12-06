import json

from flask import Flask, render_template, url_for, redirect, request, flash, session, jsonify
from werkzeug.security import generate_password_hash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'This is a secret key for sr cloud application.'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'srcloud_db'

mysql = MySQL(app)





@app.route('/')
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        result = cursor.fetchone()
        # print(result)
        if result:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            # session['id'] = result[0]
            session['username'] = result['username']
            session['password'] = result['password']
            # Redirect to home page
            # flash('Welcome You Logged In Successfully!', 'login_success')
            return redirect(url_for('index'))
        else:
            # Account doesnt exist or username/password incorrect
            flash('Please enter valid credentials', 'login_warning')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account Email already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('sign_up.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])

def profile():
    return render_template('profile.html')


@app.route('/index/')
def index():
    if 'username' in session:
        return render_template('index.html')


@app.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        username = session['username']
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Verify the current password
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and user['password'] == current_password:
            if new_password == confirm_password:
                # Update the password
                cur = mysql.connection.cursor()
                cur.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username,))
                mysql.connection.commit()
                cur.close()
                flash('Password updated successfully!', 'password_success')
                return redirect(url_for('index'))
            else:
                flash('New password and confirm password do not match!', 'password_unmatch')
                return redirect(url_for('index'))
        else:
            return 'Invalid username or password!'

    return render_template('change_password.html')


@app.route('/getreport/', methods=['GET'])
def get_data():
    fromdate = request.args.get('fromdate')
    todate = request.args.get('todate')


    # app.config['MYSQL_DB'] = 'rfid_config_db'


    cur = mysql.connection.cursor()
    query = "SELECT * FROM rfid_config_db.rfid_tag_tbl WHERE date_time >= %s AND date_time <= %s"
    # query = "SELECT * FROM rfid_config_db.rfid_tag_tbl WHERE BETWEEN date_time = %s AND date_time = %s"
    values = (fromdate, todate)
    cur.execute(query, values)
    data = cur.fetchall()
    # print(data)
    # cur.close()
    jsondata = json.dumps(data)
    # print(jsondata)
    return jsondata



if __name__ == '__main__':
    app.run()
