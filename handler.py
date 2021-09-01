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

import form_helper

def handle_signup(form: dict) -> str:
    result = form_helper.check_register(form)
    if result is None:
        # TODO: Register the user to the database
        pass
    else:
        # TODO: Inform the user about the error
        print(result)

def handle_login(form: dict) -> str:
    # TODO: Handle the login request
    pass