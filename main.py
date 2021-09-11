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

import json
import threading
import time
import datetime
from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import session
from flask_session import Session
from werkzeug.utils import redirect

from custom_mongo import mongo_handler
from custom_redis import redis_handler
from custom_elastic import elastic_handler
from utils import logger
from utils import feature_pack

# logger
FLASK_LOGGER = logger.CustomLogger()

# global flask app
app = Flask(__name__)
RUNNING = False

# init dbs
REDIS_CLIENT: redis_handler.RedisHandler
MONGO_CLIENT: mongo_handler.MongoHandler
ELASTIC_CLIENT: elastic_handler.ElasticHandler

FLASK_LOGGER.log_info("Connecting to databases.")
try:
    REDIS_CLIENT = redis_handler.RedisHandler()
except Exception as e:
    FLASK_LOGGER.log_error(f"Connection failed to Redis.\n\t{e}")
try:
    MONGO_CLIENT = mongo_handler.MongoHandler()
except Exception as e:
    FLASK_LOGGER.log_error(f"Connection failed to MongoDB.\n\t{e}")
try:
    ELASTIC_CLIENT = elastic_handler.ElasticHandler()
except Exception as e:
    FLASK_LOGGER.log_error(f"Connection failed to ElasticSearch.\n\t{e}")  

# global variables
UPDATE_RATE = 10 # per second
FIRST_RUN = True
BATCH_SIZE = 1000
MOVIE_SIZE = MONGO_CLIENT.movie_get_count()

@app.route("/")
def home():
    """
    method to be called when wisiting root or '/'
    """

    featured_movies = feature_pack.get_featured_movies()

    if "username" in session:
        usr = session.get("username")
        return render_template(
            "home.html", user=usr, movies=featured_movies)
    else:
        return render_template(
            "home.html", user=None, movies=featured_movies)

@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    """
    method to be called when wisiting '/sign-up'
    """
    if "username" in session:
        FLASK_LOGGER.log_warning(f"Already logged in.")
        return redirect(url_for("home"))

    elif request.method == "POST":
        form = request.form
        result = handler.handle_signup(MONGO_CLIENT, form)
        if result:
            # TODO: Inform the user about the results
            FLASK_LOGGER.log_info("Successfuly registered.")
            handler.handle_login(MONGO_CLIENT, form, session)
        else:
            # TODO: Critical error. Handle this ASAP!
            FLASK_LOGGER.log_warning(f"Failed to register. ({result})")
            pass
        return redirect(url_for("home"))
    
    return render_template("sign-up.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    method to be called when wisiting '/login'
    """
    if "username" in session:
        FLASK_LOGGER.log_warning(f"Already logged in.")

    elif request.method == "POST":
        form = request.form
        result = handler.handle_login(MONGO_CLIENT, form, session)
        if result == "success":
            # successfully logged in
            FLASK_LOGGER.log_info(
                f"User: {form.get('username')} successfully logged in.")
            return redirect(url_for("home"))
        
        # login failed
        FLASK_LOGGER.log_warning(
            f"User: {form.get('username')} failed to log in. ({result})")
        return redirect(url_for("home"))
        
    return render_template("login.html")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    """
    method to be called when wisiting '/logout'
    """
    if "username" in session:
        FLASK_LOGGER.log_info(
            f"User: {session.get('u_username')} logged out.")
        session.pop("username")
        return redirect(url_for("home"))
    
    return redirect(url_for("home"))

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    """
    method to be called when wisiting '/profile'
    """
    if "username" in session:
        usr = session.get("username")
        return render_template(
            "profile_base.html", user=usr, welcoming=feature_pack.get_str_time())
    
    return redirect(url_for("login"))

@app.route("/profile-panel", methods=['POST'])
def profil_panel():
    """
    method to be called when posting to '/profile-panel'
    """
    if "username" in session:
        usr = session.get("username")
        operation = request.form.get("request")

        if operation == "load_information":
            rendered = render_template("profile_information.html", user=usr)

            data = {
                "result": "success",
                "data": rendered
            }

            return json.dumps(data)

        elif operation == "load_password":
            rendered = render_template("profile_password.html")

            data = {
                "result": "success",
                "data": rendered
            }

            return json.dumps(data)

    return json.dumps({"result": "fail"})

@app.route("/password", methods=['POST'])
def password():
    """
    method to be called when posting to '/password'
    """
    if "username" in session:
        usr = session.get("username")
        if request.form.get("request") == "change":
            form = request.form
            result = handler.handle_password_change(MONGO_CLIENT, usr, form)

            if result == "success":
                session.pop("username")
                return json.dumps({"result": result})

            return json.dumps({"result": "fail"})
    
    return json.dumps({"result": "fail"})

@app.route("/search", methods=['GET', 'POST'])
def search():
    """
    method to be called when wisiting '/profile'
    """
    if "username" in session:
        usr = session.get("username")

        return render_template("search.html", user=usr)
    
    return redirect(url_for("login"))

@app.route("/process-search", methods=['POST'])
def process_search():
    """
    method to be called by jQuery to process search strings
    """
    if "username" in session:
        search_str = request.form.get("search_str")
        if search_str:
            results = handler.handle_search(ELASTIC_CLIENT, search_str)
            result_size = len(results)

            movie_cards = []
            for i in range(len(results)):
                movie_cards.append(
                    render_template("movie_card.html", movie=results[i], job="add", number=i)
                )

            data = {
                "result": "success",
                "result_size": result_size,
                "data": movie_cards         
            }

            return json.dumps(data)

        else:
            return json.dumps({"result": "empty"})
    return json.dumps({"result": "fail"})

@app.route("/watchlist", methods=['GET', 'POST'])
def watchlist():
    """
    method to be called when visiting '/watchlist'
    """
    if "username" in session:
        usr = session.get("username")
        return render_template("watchlist.html", user=usr)

    return redirect(url_for("home"))

@app.route("/process-watchlist", methods=['POST'])
def process_watchlist():
    """
    method to be called when posting to '/process-watchlist'
    """
    if "username" in session:
        usr = session.get("username")
        operation = request.form.get("request")

        if operation == "add":
            result = handler.handle_watchlist_add(
                MONGO_CLIENT, usr.get("u_id"), request.form.get("target"))
            if result == "success":
                return json.dumps({"result": "success"})
            return json.dumps({"result": "fail"})
        elif operation == "load":
            # get watchlist of the user
            movie_ids = MONGO_CLIENT.watchlist_get(usr.get("u_id"))
            if len(movie_ids) == 0:
                return json.dumps({"result": "empty"})

            # get the movies from their id
            movies = []
            for i in movie_ids:
                movie = ELASTIC_CLIENT.movie_get(i.get("movie"))
                if movie:
                    movies.append(movie)

            # render the movie cards
            movie_cards = []
            for i in range(len(movies)):
                movie_cards.append(
                    render_template("movie_card.html", movie=movies[i], job="remove", number=i)
                )
            
            # send them to AJAX
            data = {
                "result": "success",
                "result_size": len(movie_cards),
                "data": movie_cards
            }

            return json.dumps(data)
        elif operation == "remove":
            result = handler.handle_watchlist_remove(
                MONGO_CLIENT, usr.get("u_id"), request.form.get('target')
            )
            if result == "success":
                return json.dumps({"result": "success"})
            return json.dumps({"result": "fail"})
    
    return json.dumps({"result": "fail"})

def watchdog():
    """
    monitors the website and dbs after app.run() is called.
    """
    global FIRST_RUN
    time.sleep(1)
    last_run = time.perf_counter()
    integrity_start_idx = 0
    integrity_end_idx = 0
    integrity_check_stop = True

    while RUNNING:
        curr_run = time.perf_counter()
        delta = curr_run - last_run
        if (1 / UPDATE_RATE) <= delta:
            # TODO: write the code here
            if FIRST_RUN:
                # TODO: to be executed on the first run 
                # redis_c.reset() # reset session data
                FIRST_RUN = False

            # obtain integrity between mongo and elastic
            if integrity_check_stop:
                integrity_start_idx = 0
            else:
                if MOVIE_SIZE - integrity_start_idx < BATCH_SIZE:
                    integrity_end_idx = MOVIE_SIZE
                    integrity_check_stop = True
                else:
                    integrity_end_idx = integrity_start_idx + BATCH_SIZE

                handler.check_integrity(
                    MONGO_CLIENT, ELASTIC_CLIENT,
                    integrity_start_idx, integrity_end_idx
                )
                integrity_start_idx += BATCH_SIZE
            last_run = time.perf_counter()


if __name__ == "__main__":
    # check dbs
    if not REDIS_CLIENT.runnig():
        FLASK_LOGGER.log_error("Redis client is not running. Aborting.")

    if not MONGO_CLIENT.running():
        FLASK_LOGGER.log_error("Mongo client is not running. Aborting.")
    
    if not ELASTIC_CLIENT.running():
        FLASK_LOGGER.log_error("Elastic client is not running. Aborting.")

    FLASK_LOGGER.log_info("Successfully connected to DBs.")

    app.debug = False
    app.secret_key = "B4D_w0lf"
    app.config['SESSION_TYPE'] = "redis"
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = REDIS_CLIENT.get_redis()
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=8)
    server_session = Session(app)

    # reset the session before start

    FLASK_LOGGER.log_info("Starting")
    try:
        t_watchdog = threading.Thread(target=watchdog)
        t_watchdog.start()

        RUNNING = True
        app.run()
        RUNNING = False

        t_watchdog.join()
    except Exception as e:
        FLASK_LOGGER.log_error(f"Something went wrong. Aborting.\n\t{e}")
        exit(-1)
    FLASK_LOGGER.log_info("What a successful run! Goob job.")