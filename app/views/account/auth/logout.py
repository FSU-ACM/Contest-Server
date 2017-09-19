# views.account.auth.logout

from flask import redirect, url_for, session
from app import app

@app.route('/logout', methods=['POST','GET'])
def logout():
    try:
        del session['email']
        # del session['profile_id']
    except KeyError:
        pass

    return redirect(url_for('index'),code=302)
