'''
app.py contains all of the server application
this is where you'll find all of the get/post request handlers
the socket event handlers are inside of socket_routes.py
'''

from flask import Flask, render_template, request, abort, url_for, jsonify, redirect
from flask_socketio import SocketIO
import db
import secrets
import base64
import os
from models import User
from flask import session
from sqlalchemy.orm import Session
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

# import logging

# this turns off Flask Logging, uncomment this to turn off Logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__)

# secret key used to sign the session cookie
app.config['SECRET_KEY'] = secrets.token_hex()
load_dotenv()  # This loads the variables from .env into the environment
COMMON_HMAC_KEY = os.getenv('COMMON_HMAC_KEY')
print(COMMON_HMAC_KEY)


socketio = SocketIO(app)

# don't remove this!!
import socket_routes

# index page
@app.route("/")
def index():
    return render_template("index.jinja")

# login page
@app.route("/login")
def login():    
    return render_template("login.jinja")

# handles a post request when the user clicks the log in button
@app.route("/login/user", methods=["POST"])
def login_user():
    if not request.is_json:
        abort(404)

    username = request.json.get("username")
    password = request.json.get("password")

    user =  db.get_user(username)
    if user is None:
        return "Error: User does not exist!"

    if user.password != password:
        return "Error: Password does not match!"
    
    # Reset the session for each new login
    session.clear()
    session['username'] = username  # Correctly setting the username in the session
    session['role'] = user.role
    # return jsonify({"success": True, "url": url_for('home', username=username)})

    return url_for('home', username=request.json.get("username"))

# handles a get request to the signup page
@app.route("/signup")
def signup():
    return render_template("signup.jinja")

# handles a post request when the user clicks the signup button
@app.route("/signup/user", methods=["POST"])
def signup_user():
    if not request.is_json:
        return jsonify({"success": False, "error": "Invalid request"}), 400

    data = request.get_json()
    print(f"Received signup data: {data}")

    username = request.json.get("username")
    password = request.json.get("password")
    public_key = request.json.get("publicKey")
    role = request.json.get("role")
    if public_key is None:
        print("Public key is missing from the data.")
    # print(f"Received public key for {username}: {public_key}")  # Debug log

    if db.get_user(username) is None:
        db.insert_user(username, password, public_key, role)
        session['username'] = username  # Set up user session
        session['role'] = role
        return jsonify({"success": True, "url": url_for('home', username=username), "hmac_key": COMMON_HMAC_KEY})
    else:
        return jsonify({"success": False, "error": "User already exists!"})


# handler when a "404" error happens
@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.jinja'), 404

# home page, where the messaging app is
@app.route("/home")
def home():
    # if request.args.get("username") is None:
    #     abort(404)
    # return render_template("home.jinja", username=request.args.get("username"))
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if the user is not in session
    username = session['username']
    role = session['role']
    return render_template("home.jinja", username=username, role=role)

@app.route("/api/get_public_key/<username>", methods=['GET'])
def get_public_key(username):
    user = db.get_user(username)
    if user and user.public_key:
        return jsonify(publicKey=user.public_key)
    else:
        return jsonify(error="User or public key not found"), 404
    
@app.route("/api/get_hmac_key")
def get_hmac_key():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401  # Ensuring user is logged in
    
    # Optionally add more checks for further security, e.g., user roles

    # Send the HMAC key securely
    return jsonify({"hmac_key": COMMON_HMAC_KEY})

@app.route('/knowledge-repository')
def knowledge_repository():
    return render_template('knowledge_repository.jinja')

@app.route("/profile/<username>")
def profile(username):
    user = db.get_user(username)
    if user is None:
        return render_template('404.jinja'), 404
    return render_template("profile.jinja", user=user)

if __name__ == '__main__':
    socketio.run(app)