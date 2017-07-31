# app.views

from flask import render_template
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


from . import admin
from . import nav
from . import views
from . import account
from . import register
