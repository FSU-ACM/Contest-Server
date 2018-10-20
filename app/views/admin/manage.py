from flask import flash, redirect, url_for, request, Markup

from flask_admin import AdminIndexView
from flask_admin.contrib.mongoengine import ModelView

from app.util import session as session_util

def get_team_members(view, context, model, name):
    """Returns team members as formatted links to their Account's edit view.

    """
    if model.members:
        member_list = ''
        for user in model.members:
            if user:
                member_list += "<a href='" \
                            + url_for('account.edit_view', id=user.id) \
                            + "'>" + str(user) + "</a>\n"
        return Markup(member_list)
    else:
        return ''

class HomeView(AdminIndexView):
    """Main index view for admin interface with access restriction.

    """

    def is_accessible(self):
        try:
            account = session_util.get_account()
            return account.is_admin is True
        except:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class BaseManageView(ModelView):
    """Base view containing access restriction functions.

    """

    def is_accessible(self):
        try:
            account = session_util.get_account()
            return account.is_admin is True
        except:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class AccountManageView(BaseManageView):
    """Admin view used to view and edit Accounts.

    """

    column_exclude_list = ('password',)

    column_formatters = dict(
        profile=lambda v, c, m, n: Markup("<a href='" + url_for('profile.edit_view', id=m.profile.id) + "'>Profile</a>"),
        team=lambda v, c, m, n: Markup("<a href='" + url_for('team.edit_view', id=m.team.id) + "'>" + str(m.team) + "</a>"),
    )

    def on_model_change(self, form, model, is_created):
        """Makes sure a new/edited Account's password is hashed.

        """
        if form.password.data[:6] != "pbkdf2":
            model.set_password(form.password.data)

class ProfileManageView(BaseManageView):
    """Admin view used to view and edit Profile.

    """
    pass

class TeamManageView(BaseManageView):
    """Admin view used to view and edit Teams.

    """
    column_formatters = dict(
        members=get_team_members
    )
