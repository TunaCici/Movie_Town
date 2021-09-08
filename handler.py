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
from utils import logger
from custom_mongo.mongo_handler import MongoHandler

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
