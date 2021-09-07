"""
name: main.py
desc: main script for the website Movie Town
author: tuna cici

what does it do:
uses flask to create and handle the web application.
also initializes connection to databases. (not sure about this yet)
"""
# DURING DEVELOPMENT
# TODO: Come up with better and meaningful comments
# TODO: Clean up the code after each long session (house keeping)
# TODO: Create a basic front-end for the web. (USE TEMPLATING)
# TODO: Initialize the databases and make sure they are up and running
# TODO: Basic error handling

# AFTER DEVELOPMENT
# TODO: Look up for exploits and try to get rid of them
# TODO: More and more security measures
# TODO: Make the front-end prettier

# GENERAL TIPS FOR MYSELF
# TODO: Try to make it as fool-proof as you can

import handler

from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import session
from flask_session import Session
from werkzeug.utils import redirect

from custom_redis import redis_handler

redis_session = redis_handler.RedisHandler()

# currently on localhost
app = Flask(__name__)
app.debug = True
app.secret_key = "B4D_w0lf"
app.config['SESSION_TYPE'] = "redis"
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis_session.get_redis()

server_session = Session(app)

# variables for testing

@app.route("/")
def home():
    """
    method to be called when wisiting root or '/'
    """

    if "username" in session:
        return render_template("home.html", signed_in=True)
    else:
        return render_template("home.html", signed_in=False)

@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    """
    method to be called when wisiting '/sign-up'
    """
    if request.method == "POST":
        form = request.form
        result = handler.handle_signup(form)
        if result:
            # TODO: Inform the user about the results
            pass
        else:
            # TODO: Critical error. Handle this ASAP!
            pass
        return redirect(url_for("home"))
    else:
        return render_template("sign-up.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    method to be called when wisiting '/login'
    """
    if request.method == "POST":
        form = request.form
        result = handler.handle_login(form, session)
        print(result)
        if result == "success":
            # TODO: Inform the user about the results
            return redirect(url_for("home"))
        else:
            # TODO: Critical error. Handle this ASAP!
            return redirect(url_for("home"))
        
    else:
        return render_template("login.html")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    """
    method to be called when wisiting '/logout'
    """
    if "username" in session:
        session.pop("username")
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run()