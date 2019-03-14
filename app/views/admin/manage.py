from flask import flash, redirect, url_for, request, Markup

from flask_admin import AdminIndexView
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.form.fields import Select2Field

from app.models.Account import Account
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
            return account.is_admin == True
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
            return account.is_admin == True
        except:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class AccountManageView(BaseManageView):
    """Admin view used to view and edit Accounts.

    """

    column_exclude_list = ('password',)
    column_searchable_list = ('email', 'fsuid', 'first_name', 'last_name',)
    column_default_sort = ('email', False)
    column_filters = ('signin',)

    column_formatters = dict(
        team=lambda v, c, m, n: Markup("<a href='" + url_for('team.edit_view', id=m.team.id) + "'>" + str(m.team) + "</a>") if m.team else "",
    )

    def on_model_change(self, form, model, is_created):
        """Makes sure a new/edited Account's password is hashed.

        """
        if form.password.data[:6] != "pbkdf2":
            model.set_password(form.password.data)

class TeamManageView(BaseManageView):
    """Admin view used to view and edit Teams.

    """

    column_searchable_list = ('team_name',)
    column_default_sort = ('team_name', False)
    column_filters = ('division',)

    column_formatters = dict(
        members=get_team_members
    )

class CourseManageView(BaseManageView):
    """Admin view used to add and edit extra credit Courses.

    """

    column_list = ('name', 'professor_name', 'professor_email', 'division', 'num_students',)
    column_default_sort = ('name', False)
    column_searchable_list = ('name', 'professor_name', 'professor_email',)
    column_editable_list = ('name', 'professor_name', 'division')
    column_display_pk = True

    def scaffold_form(self):
        """Replaces Division field with a Select field in the edit form.

        """
        
        form = super().scaffold_form()
        form.division = Select2Field('Division', coerce=int, choices=[(1, "Upper"), (2, "Lower")])
        return form


    def scaffold_list_form(self, widget=None, validators=None):
        """Replaces Division field with a Select field in the editable column.
        
        """

        form_class = super().scaffold_list_form(widget=widget, validators=validators)
        form_class.division = Select2Field('Division', coerce=int, choices=[(1, "Upper"), (2, "Lower")])
        return form_class


    def on_model_delete(self, model):
        """Removes all references to deleted course to avoid dangling
        references.

        """

        Account.objects(courses=model).update(pull__courses=model)
