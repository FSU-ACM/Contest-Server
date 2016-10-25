from flask import redirect, url_for, render_template, request

from app import app
from app.models import *
from signin import sign_in


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send/<string:fsuid>')
def send_mail(fsuid):
    addr = sign_in(fsuid)
    # if addr is not None:
    #     print fsuid, addr
    #     return redirect(url_for('confirm', addr=addr))
    # else:
    #     return render_template('walkin.html')
    return render_template('confirm.html', email=addr)


# @app.route('/confirm')
# def confirm():
#     email = request.args['addr']
#     return render_template('confirm.html', email=email)

@app.route('/teams')
def teams():
    teams = Team.query.all()
    return render_template('teams.html', teams=teams)
