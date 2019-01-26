from flask import render_template
from flask.views import View


class IndexView(View):
    """ Just renders the homepage """

    def dispatch_request(self):
        return render_template("index/index.html")
