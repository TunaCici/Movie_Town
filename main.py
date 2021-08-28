from flask import Flask
from flask import url_for
from flask import render_template
from flask import request

from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("hello.html")
