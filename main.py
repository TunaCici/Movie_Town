from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from werkzeug.utils import redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        print("getting post")
        return redirect(url_for("home"))

    return render_template("sign-up.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        print("getting post")
        return redirect(url_for("home"))

    return render_template("login.html")
