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
from werkzeug.utils import redirect

from custom_redis import redis_handler

print("hello")

# currently on localhost
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis_handler.from_url('redis://localhost:6379')

# variables for testing

@app.route("/")
def home():
    """
    method to be called when wisiting root or '/'
    """
    return render_template("home.html", signed_in = True)

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
        return redirect(url_for("home", signed_in = True), )
    else:
        return render_template("sign-up.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    method to be called when wisiting '/login'
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
        
        return redirect(url_for("home"), signed_in = True)
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run()