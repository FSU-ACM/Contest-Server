from wtforms.fields.html5 import EmailField as wtf_EmailField
from wtforms import StringField as wtf_StringField

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
