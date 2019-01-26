# pylint: disable=W0612,W0613

from flask import Flask, render_template
from flask.views import View
from flask_admin import Admin
from flask_nav.elements import *  # pylint: disable=W0401,W0614

from app.models import Account, Team
from . import account, admin, auth, index, register, team


# pylint: disable=W0106
def init_app(app: Flask):
    """ Register the views blueprint to the flask app """

    @app.errorhandler(404)
    def page_not_found(err):
        return render_template("common/404.html"), 404


    @app.errorhandler(500)
    def page_error(err):
        return render_template("common/500.html"), 500


    # Register regular routes
    routes = [
        ("/", index.IndexView.as_view("index")),
        ("/register", register.SoloRegisterView.as_view("register")),
        (
            "/quickregister",
            register.QuickRegisterView.as_view("quick_register"),
        ),
        ("/login", auth.LoginView.as_view("login")),
        ("/logout", auth.LogoutView.as_view("logout")),
        ("/reset_password", auth.ResetPasswordView.as_view("reset_password")),
        (
            "/account/updatepassword",
            auth.UpdatePasswordView.as_view("update_password"),
        ),
        ("/account", account.EditAccountView.as_view("account")),
        ("/account/team", team.TeamView.as_view("team")),
        ("/account/team/update", team.UpdateView.as_view("team_update")),
        ("/account/team/create", team.CreateView.as_view("team_create")),
        ("/account/team/add", team.AddView.as_view("team_add_member")),
        ("/account/team/leave", team.LeaveView.as_view("team_leave")),
        ("/account/team/remove", team.RemoveView.as_view("team_remove")),
        ("/teams", team.list.TeamListView.as_view("teams")),
        ("/admin/signin", admin.SignInView.as_view("sign_in")),
    ]

    [app.add_url_rule(route, view_func=view) for (route, view) in routes]

    # Setup Admin interface
    flask_admin = Admin(
        app,
        name="Admin Interface",
        template_mode="bootstrap3",
        index_view=admin.HomeView(),
    )

    flask_admin.add_view(admin.AccountManageView(Account))
    flask_admin.add_view(admin.TeamManageView(Team))
