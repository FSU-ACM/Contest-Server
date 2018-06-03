from flask import (flash, request)

from app.forms import EditAccount as EditAccountForm
from app.util import session as session_util
from app.views.generic import AccountFormView


class EditAccountView(AccountFormView):
    """Lets user adjust some account fields.

    Unauth'd users redirected to login.

    """

    def get_template_name(self):
        return 'form2/edit_account.html'

    def get_form(self):
        account = session_util.get_account()
        return EditAccountForm(
            first_name=account.first_name,
            last_name=account.last_name,
            fsuid=account.fsuid
        )

    def post(self):
        form = EditAccountForm(request.form)

        if form.validate():
            account = session_util.get_account()
            data = {field.name: field.data for field in form}
            del data['csrf_token']
            del data['submit']

            account.update(**data)
            account.save()

            flash('Account updated')

        return self.render_template(form=form)


