from flask import Flask
from flask import url_for
from flask import render_template
from flask import request

from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Index Page</h1>"

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name = None):
    return render_template("hello.html", name_html=name)

@app.route("/user/<username>")
def show_user_profile(username):
    # show the user profile
    return f"Welcome back, {escape(username)}"

@app.route("/post/<int:post_id>")
def show_post(post_id):
    "show the post with the id: post_id"
    return f"Post: {escape(post_id)}"

@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    return f"Subpath: {escape(subpath)}"

with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello"))
    print(url_for("show_user_profile", username="tunacici"))
    print(url_for("show_post", post_id=45443))
    print(url_for("show_subpath", subpath="C:/Users/tunac"))
