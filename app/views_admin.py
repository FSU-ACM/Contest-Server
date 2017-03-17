# /views_admin.py

from flask import redirect, url_for, render_template, request, session

from app import app, basic_auth


@app.route('/signin', methods=['POST', 'GET'])
@basic_auth.required
def sign_in():

    error, success = None, None

    if request.method == 'POST':


    return render_template('/admin/signin.html', error=error, success=success)
