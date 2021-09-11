"""
name: handler.py
desc: handles web requests. mostly posts.
author: tuna cici

what does it do:
uses incoming forms to handle them accordingly.
currently used for login and sign-ups.
"""
# TODO: Complete login and sign-up handlings
# TODO: Establish connection to databases

# GENERAL TIPS FOR MYSELF
# TODO: Use encryption whenever possible

# global import
import time
import json
import uuid
import bcrypt
import datetime
from flask import session

# local import
import form_helper
from utils import feature_pack
from custom_mongo.mongo_handler import MongoHandler
from custom_elastic.elastic_handler import ElasticHandler

def handle_signup(db: MongoHandler, form: dict) -> str:
    # check if register form is valid
    result = form_helper.check_register(db, form)

    if result is None:
        # TODO: Register the user to the database

        # encrypt the password
        pass_hashed = bcrypt.hashpw(
            bytes(form.get("passwordOne"), encoding="utf-8"),
            bcrypt.gensalt()
        )

        # get random profile picture
        picture_path = feature_pack.get_profile_picture()

        db.user_add(
            form.get("name"),
            form.get("surname"),
            form.get("username"),
            form.get("mailAddress"),
            pass_hashed,
            picture_path
        )

        return "success"
    
    # TODO: Inform the user about the error
    return result

def handle_login(db: MongoHandler, form: dict, session: session) -> str:
    # TODO: Handle the login request
    username = form.get("username")
    password = form.get("passwordOne")

    # check if user registered
    user = db.user_get(username)
    if user is None:
        return f"could not find anyone with the username '{username}'"
        
    # check password
    valid = bcrypt.checkpw(
        bytes(password, encoding="utf8"), user.get("u_password"))
    if valid:
        session["username"] = user
        return "success"
    
    return "wrong password, try again"

def handle_search(elastic: ElasticHandler, search_str: str) -> list:
    result = elastic.search(search_str)
    return result

def handle_password_change(
    mongo: MongoHandler,
    user: dict,
    form: dict)-> str:
    # check current password
    curr_pass = user.get("u_password")
    form_pass = form.get("currentPassword")

    same = bcrypt.checkpw(bytes(form_pass, encoding="utf-8"), curr_pass)

    if not same:
        return "wrong_curr_pass"
    
    passwordOne = form.get("newPasswordOne")
    passwordTwo = form.get("newPasswordTwo")

    response = form_helper.check_password(passwordOne, passwordTwo)

    if response == "invalid_password":
        return "fail"
    elif response == "invalid_confirm":
        return "fail"
    elif response == "valid":
        user_id = user.get("u_id")
        pass_hashed = bcrypt.hashpw(
            bytes(passwordOne, encoding="utf-8"),
            bcrypt.gensalt())
        mongo.user_update_password(user_id, pass_hashed)
        return "success"

    return "fail"

def handle_watchlist_add(
    db: MongoHandler,
    id: uuid.UUID,
    movie: str) -> str:
    curr_list = db.watchlist_get(id)
    data = {
        "movie": movie,
        "data_added": str(datetime.datetime.now()),
        "watched": "no"
    }

    curr_list.append(data)

    new_list = {
        "list": [i for i in curr_list]
    }

    db.watchlist_update(id, json.dumps(new_list))
    return "success"

def handle_watchlist_remove(
    db: MongoHandler,
    id: uuid.UUID,
    movie: str) -> str:
    curr_list = db.watchlist_get(id)

    # remove the movie from the list
    removed = False
    for i in range(len(curr_list)):
        print(f"looking for: {curr_list[i]}")
        if curr_list[i].get("movie") == movie:
            curr_list.pop(i)
            removed = True
            break

    if not removed:
        return "fail"

    new_list = {
        "list": [i for i in curr_list]
    }
    
    db.watchlist_update(id, json.dumps(new_list))
    return "success"

def check_integrity(
    mongo: MongoHandler,
    elastic: ElasticHandler,
    start: int, end: int) -> bool:

    print(f"Looking between {start} and {end}")
    mongo_movies = mongo.get_range_of_movies(start, end)

    print(f"Starting check operations.")
    for i in mongo_movies:
        result = elastic.movie_get(i.get("m_id"))

        if not result:
            print(f"Indexing: {i.get('m_id')}")
            elastic.movie_add(
                i.get("m_id", "None"),
                i.get("m_imdb_id", "None"),
                i.get("m_title", "None"),
                i.get("m_year", "None"),
                i.get("m_genre", "None"),
                i.get("m_duration", 0),
                i.get("m_country", "None"),
                i.get("m_director", "None"),
                i.get("m_writer", "None"),
                i.get("m_production", "None"),
                i.get("m_actors", "None"),
                i.get("m_description", "None"),
                i.get("m_score", 0.0),
                i.get("m_poster", "None")
            )
    return True