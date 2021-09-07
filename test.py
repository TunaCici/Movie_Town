import flask

app = flask.Flask(__name__)
app.run()

@app.route("/")
def home():
    """
    method to be called when wisiting root or '/'
    """
    return "hello"