from flask import render_template, redirect, url_for
from flask.views import MethodView
from flask_wtf import FlaskForm

from app.util import session as session_util
from app.util.errors import UnauthorizedUserError


class FormView(MethodView):
    """Abstract parent class to all form-based views.

    Most of this project consist of forms for users (contest participants) to
    complete plus the validation and subsequent processing for those forms. As
    such, we define this class to easily wrap form display and processing
    logic.

    To this end, this class requires an authentication step where we validate
    the user's permission to view the given form. If the user is unauthorized,
    we redirect them to the appropriate location. To achieve this, the class
    implements the method `redirect_unauthorized` to send a user back where
    they belong. This can be overridden for custom redirection. This step is
    inserted into the parent MethodView's `dispatch_request` method, so we
    can process the authentication step before the dispatch. All subsequent
    children must provide an implementation of this method.

    Inheritors of this class must define:

        -   A form for this data.
        -   A template in which to render the form.
        -   Implementations of the authorization methods `authorize` and
            `redirect_unauthorized`.

    """

    def dispatch_request(self, *args, **kwargs):
        try:
            self.perform_authorization(*args, **kwargs)
            return super().dispatch_request(*args, **kwargs)
        except UnauthorizedUserError:
            return self.redirect_unauthorized()

    def perform_authorization(self, *args, **kwargs):
        if not self.authorize(*args, **kwargs):
            raise UnauthorizedUserError()

    def authorize(self, *args, **kwargs):
        raise NotImplementedError()

    def redirect_unauthorized(self):
        raise NotImplementedError()

    def get_template_name(self) -> str:
        raise NotImplementedError()

    def get_form(self) -> FlaskForm:
        raise NotImplementedError()

    def render_template(self, **kwargs):
        """ Renders the view's template with the form. """
        form = kwargs.get('form') or self.get_form()
        return render_template(self.get_template_name(), form=form, **kwargs)

    def get(self):
        """ Default behavior is just to render the form. This method can be
            overwritten for additional behavior which can then call super(),
            or can juse call the self.render_template method. """
        return self.render_template()

    def post(self):
        """ This method should be overwritten to handle form-parsing logic
            on a per-view basis. """
        raise NotImplementedError()


# pylint: disable=W0223
class AccountFormView(FormView):
    def authorize(self, *args, **kwargs):
        return session_util.is_auth()

    def redirect_unauthorized(self):
        return redirect(url_for("login"))

    def render_template(self, **kwargs):
        account = session_util.get_account()
        return super().render_template(account=account, **kwargs)
