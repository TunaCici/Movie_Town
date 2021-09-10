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
import uuid
import bcrypt
from flask import session

# local import
import form_helper
from custom_mongo.mongo_handler import MongoHandler
from custom_elastic.elastic_handler import ElasticHandler

def handle_signup(form: dict, db: MongoHandler) -> str:
    # check if register form is valid
    result = form_helper.check_register(form)

    if result is None:
        # TODO: Register the user to the database

        # encrypt the password
        pass_hashed = bcrypt.hashpw(
            bytes(form.get("passwordOne"), encoding="utf-8"),
            bcrypt.gensalt()
        )

        # create uuid for the user
        unq_id = uuid.uuid4()

        db.user_add(
            unq_id,
            form.get("name"),
            form.get("surname"),
            form.get("username"),
            form.get("maildAddress"),
            pass_hashed
        )

        return "success"
    
    # TODO: Inform the user about the error
    return result

def handle_login(form: dict, db: MongoHandler, session: session) -> str:
    # TODO: Handle the login request
    username = form.get("username")
    password = form.get("passwordOne")

    # check if user registered
    user = db.user_get(username)
    if user is None:
        return "fail"
        
    # check password
    valid = bcrypt.checkpw(
        bytes(password, encoding="utf8"), user.get("u_password"))
    if valid:
        session["username"] = user
        return "success"
    
    return "fail"

def check_integrity(
    mongo: MongoHandler,
    elastic: ElasticHandler,
    start: int, end: int) -> bool:

    mongo_movies = mongo.get_range_of_movies(start, end)

    for i in mongo_movies:
        result = elastic.movie_get(i.get("m_id"))
        if not result:
            print(f"Indexing: {i.get('m_id')}")
            elastic.movie_add(
                i.get("m_id"),
                i.get("m_imdb_id"),
                i.get("m_title"),
                i.get("m_year"),
                i.get("m_genre"),
                i.get("m_duration"),
                i.get("m_country"),
                i.get("m_director"),
                i.get("m_writer"),
                i.get("m_production"),
                i.get("m_actors"),
                i.get("m_description"),
                i.get("m_score"),
                i.get("m_poster")
            )
    
    return True