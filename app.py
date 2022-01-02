from flask import Flask, redirect
from flask import render_template
from flask import request
from flask import session
from bson.json_util import loads, dumps
from flask import make_response

import database as db
import authentication
import logging

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b'hsaldkfj213'
app.env = "development"

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

@app.route('/',  methods=['post', 'get'])
def index():
    if "user" in session.keys():
        return render_template('logged_in.html', userinput = loads(session["user"]))
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")    
        password = request.form.get("password")
        fullname = request.form.get("fullname")
        userinput = {'username': username, 'email': email, 'password': password, 'fullname': fullname}
        if (db.check_user(username)):
            return render_template('index.html', invalid=True)
        else: 
            db.create_user(userinput)
            session["user"] = dumps(userinput)
            app.logger.info('%s', "authenticated")
            return render_template('logged_in.html', userinput = userinput)
    return render_template('index.html', invalid=False)

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')

@app.route('/organizations')
def orgs():

    organizations = db.get_orgs()
    return render_template('orgs.html', page="Organizations", organizations=organizations)

@app.route('/orgdetails')
def orgdetails():
    code = request.args.get('code', '')
    organization = db.get_org(int(code))

    return render_template('organization_details.html', organization=organization)

@app.route('/profile', methods=['post', 'get'])
def profile():
    if "user" in session.keys():
        if request.method == "POST":
            fullname = loads(session["user"])
            fullname = fullname["fullname"]
            username = request.form.get("username")
            email = request.form.get("email")    
            password = request.form.get("password")
            userinput = {'username': username, 'email': email, 'password': password, 'fullname': fullname}
            db.update_user(email,fullname,username,password)
            session["user"] = dumps(userinput)
        return render_template('profile.html', userinput = loads(session["user"]))
       

    if request.method == "POST":
        email = request.form.get("email")    
        password = request.form.get("password")
        if db.check_email(email):
            userinput = authentication.login(email, password)
            if (userinput):
                session["user"] = dumps(userinput)
                return render_template('logged_in.html', userinput = userinput)
            else:
                return render_template('login.html', invalid=True)
        else: 
            return render_template('login.html', invalid=True)
    
    return render_template("login.html",invalid=False)
 