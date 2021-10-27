from flask import Flask, make_response, request, render_template, redirect, jsonify
from random import random
import jwt
import Calc_functions as Calc_functions
import datetime
from contextlib import closing
import sqlite3

#Declare the app
flaskapp = Flask(__name__)
SECRET_KEY = "3D238B65CF6D68E4B6797BBEF4EC3"


# @component External:Guest (#guest)


# Start an app route

def newuser(username, password):
    with closing(sqlite3.connect("users.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("INSERT INTO user_info (username, password) VALUES(?,?)",(username, password,))
            connection.commit()

def verify_token(token):
    if db_token:
        decoded_token = jwt.decoded(token, SECRET_KEY, "HS256")
        with closing(sqlite3.connect("users.db")) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("SELECT * FROM user_info WHERE username=?", (decoded_token.get('username'),))
                userdata=cursor.fetchone()

        if userdata != None:
            return True
        else:
            return False
    else:
        return False


def verify_token(token):
    if token :
        decoded_token = jwt.decode(token, SECRET_KEY, "HS256")
        print (decoded_token)
        # Check whether the information in decoded token is correct or not

        return True # if info is correct otherwise return false
    else:
        return False

# @component CalcApp:Web:Server:Index (#index)
# @connects #guest to #index with HTTP-GET
@flaskapp.route('/')
def index_page():
    print(request.cookies)
    isUserLoggedIn = False

    if 'token' in request.cookies:
        isUserLoggedIn = verify_token(request.cookies['token'])

    if isUserLoggedIn:
        resp = make_response(render_template('index.html'))
        return resp
    else:
        user_id = random()
        print(f"User ID: {user_id}")
        resp = make_response(render_template('main.html'))
        resp.set_cookie('user_id', str(user_id))
        return resp

# @component CalcApp:Web:Server:Login (#login)
# @connects #guest to #login with HTTP-GET
# @threat BruteForceAttack (#bf)
@flaskapp.route('/login')
def login_page():
    return render_template('login.html')

def create_token(username, password):
    validity = datetime.datetime.utcnow() + datetime.timedelta(days=15)
    print(validity)
    token = jwt.encode({'user_id': 123154, 'username': username, 'exp': validity}, SECRET_KEY, "HS256")
    return token

# @component CalcApp:Web:Server:Logout (#logout)
# @connects #guest to #logout with HTTP-GET
@flaskapp.route('/logout')
def logout_page():
    resp=make_response(redirect('/'))
    resp.delete_cookie('token')
    return resp


@flaskapp.route('/authenticate', methods = ['POST'])
def authenticate_users():
    data = request.form
    username = data['username']
    password = data['password']
     # check whether the username and password are correct
    db_token = create_token(username, password)

    try:
        with closing(sqlite3.connect("users.db")) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("CREATE TABLE user_info (id INTEGER PRIMARY KEY, username TEXT, password TEXT);")
                connection.commit()
    except:
        pass

    with closing(sqlite3.connect("users.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM user_info WHERE username=? and password=?", (username, password,))
            udat=cursor.fetchone()
        if udat == None:
            newuser(username,password)
            db_token = create_token(username, password)
            resp = make_response(render_template('calculator.html'))
            resp.set_cookie('token', db_token)
            return resp
        else:
            db_token = create_token(username, password)
            resp = make_response(render_template('calculator.html'))
            resp.set_cookie('token', db_token)
            return resp

    resp = make_response(redirect('/calculator'))
    #resp.set_cookie("loggedIn", "True")
    resp.set_cookie('token', db_token)
    return resp


# @component CalcApp:Web:Server:Calculator (#calculator)
# @connects #guest to #calculator with HTTP-GET
@flaskapp.route('/calculator', methods = ['GET'])
def calculator_get():
    isUserLoggedIn = False

    if 'token' in request.cookies:
        isUserLoggedIn = verify_token(request.cookies['token'])

    if isUserLoggedIn:
        return render_template("calculator.html")
    else:
        return make_response(redirect("/login"))


# @component CalcApp:Web:Server:Calculate (#calculate)
# @connects #guest to #calculate with HTTP-POST
@flaskapp.route('/calculate', methods = ['POST'])
def calculate_post():
    Number_1 = request.form.get('Number_1', type = int)
    Number_2 = request.form.get('Number_2', type = int)
    Operation = request.form.get('Operation')

    result = Calc_functions.process(Number_1, Number_2, Operation)

    return str(result)

# @component CalcApp:Web:Server:Calculate (#calculate)
# @connects #guest to #calculate with HTTP-POST
@flaskapp.route('/calculate2', methods = ['POST'])
def calculate_post2():
    Number_1 = request.form.get('Number_1', type = int)
    Number_2 = request.form.get('Number_2', type = int)
    Operation = request.form.get('Operation', type = str)

    result = Calc_functions.process(Number_1, Number_2, Operation)

    print(result)
    response_data = {
        'data': result
    }
    return make_response(jsonify(response_data))

if __name__ == '__main__':
    print("This is a Secure REST API Server:")
    flaskapp.run(host="0.0.0.0", debug = True, ssl_context=('cert/cert.pem', 'cert/key.pem'))
