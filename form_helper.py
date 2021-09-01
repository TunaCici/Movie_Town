"""
name: form_helper.py
desc: helper module for checking forms
author: tuna cici

what does it do:
provides functions to validate forms.
makes sure no funny bussinnes happens.
also improves security a little bit.
"""
import re

MIN_ALLOWED_NAME = 2
MIN_ALLOWED_SURNAME = 2
MIN_ALLOWED_USERNAME = 4
MIN_ALLOWED_PASSWORD = 8

def validate_email(mail: str) -> bool:
    """
    validates email using reguler expression
    args:
        mail: mail address
    returns:
        bool: the validation
    """
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    
    if re.search(regex, mail):
        return True
    else:
        return False

def check_register(form: dict) -> str:
    """
    checks for errors in the form from sign-up page
    args:
        form: posted data from the page
    returns:
        str: if there is an error
        None: if everything is okay
    errors:
        invalid_name
        invalid_surname
        invalid_username
        invalid_mail
        invalid_password
        invalid_confirm
        invalid_accept
    """
    name = form.get("name")
    surname = form.get("surname")
    username = form.get("username")
    mailAddress = form.get("maildAddress")
    passwordOne = form.get("passwordOne")
    passwordTwo = form.get("passwordTwo")
    accept = form.get("accept")

    if name is None or len(name) < MIN_ALLOWED_NAME:
        return "invalid_name"
    if surname is None or len(surname) < MIN_ALLOWED_SURNAME:
        return "invalid_surname"
    if username is None or len(username) < MIN_ALLOWED_USERNAME:
        return "invalid_username"
    if mailAddress is None or (not validate_email(mailAddress)):
        return "invalid_mail"
    if passwordOne is None or len(passwordOne) < MIN_ALLOWED_PASSWORD:
        return "invalid_password"
    if passwordTwo is None or passwordTwo != passwordOne:
        return "invalid_confirm"
    if accept is None:
        return "invalid_accept"

    return None