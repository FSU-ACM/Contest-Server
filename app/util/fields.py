from wtforms.fields.html5 import EmailField as wtf_EmailField
from wtforms import StringField as wtf_StringField
from wtforms import SelectMultipleField as wtf_SelectMultipleField
from wtforms import widgets

from app.models import Course
from app.util import course as course_util

class EmailField(wtf_EmailField):
    """Email field for WTForms

    This field inherits <input type="email"> from the
    wtforms.EmailField, but also will automatically convert
    all data to lowercase.

    """

    def __init__(self, *args, **kwargs):
        wtf_EmailField.__init__(self, *args, **kwargs)

    def process_formdata(self, valuelist):
        super(wtf_EmailField, self).process_formdata(valuelist)

        if valuelist and len(valuelist) >= 1:
            self.data = valuelist[0].lower()


class FSUIDField(wtf_StringField):
    """FSUID field for custom WTForms.

    This field will normalize FSUIDs to be all lowercase.

    """

    def __init__(self, *args, **kwargs):
        wtf_StringField.__init__(self, *args, **kwargs)

    def process_formdata(self, valuelist):
        super(wtf_StringField, self).process_formdata(valuelist)

        if valuelist and len(valuelist) >= 1:
            self.data = valuelist[0].lower()


class CoursesField(wtf_SelectMultipleField):
    """Courses field for custom WTForms.

    Automatically populates choices with available courses.

    """

    def __init__(self, *args, **kwargs):
        wtf_SelectMultipleField.__init__(self, *args, **kwargs)
        self.choices = course_util.get_choices()

    def pre_validate(self, *args):
        # Hacky way to avoid validation issues due to dynamic choices
        # Everything is validated on form submission anyways
        return True
