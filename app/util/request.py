"""util.request"""

from bleach import clean
from flask import request

def get_email():
    """
    Cleans and normalizes an email from the request.form
    :return: Normalized email string.
    """
    email = request.form['email']
    return clean(email).lower()

def get_password():
    """
    Cleans and normalizes an password from the request.form
    :return: Normalized password string.
    """
    password = request.form['password']
    return password
