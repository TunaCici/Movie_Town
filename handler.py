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

import uuid
import bcrypt
import form_helper

from custom_mongo import mongo_handler
from utils import logger

HANDLER_LOGGER = logger.CustomLogger()
MONGO_HANDLER = mongo_handler.MongoHandler()

def handle_signup(form: dict) -> str:
    result = form_helper.check_register(form)
    if result is None:
        # TODO: Register the user to the database
        HANDLER_LOGGER.log_info("Form validated. Registering the user.")
        
        # encrypt the password
        pass_hashed = bcrypt.hashpw(
            bytes(form.get("passwordOne"), encoding="utf-8"),
            bcrypt.gensalt()
        )

        # create uuid for the user
        unq_id = uuid.uuid4()

        MONGO_HANDLER.user_add(
            unq_id,
            form.get("name"),
            form.get("surname"),
            form.get("username"),
            form.get("maildAddress"),
            pass_hashed
        )
        HANDLER_LOGGER.log_info("User registered.")
        return "success"
    else:
        # TODO: Inform the user about the error
        HANDLER_LOGGER.log_warning("Invalid form.")
        return "fail"

def handle_login(form: dict) -> str:
    # TODO: Handle the login request
    pass