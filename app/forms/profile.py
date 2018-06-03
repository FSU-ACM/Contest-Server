from flask_mongoengine.wtf import model_form
from wtforms import widgets, SubmitField

from app.models import Profile as ProfileModel

Profile_ = model_form(
    ProfileModel,
    field_args={
        # 'dob': {
        #     'label': 'Date of Birth'
        # },
        'age': {
            'label': 'Age'
        },
        'gender': {
            'label': 'Gender',
            'widget': widgets.Select(),
            'default': ''
        },
        'race': {
            'label': 'Race',
            'widget': widgets.Select(),
            'default': ''
        },
        'food_allergies': {
            'label': 'Food Allergies?',
            'widget': widgets.TextInput()
        },
        'major': {
            'label': 'Major',
            'widget': widgets.TextInput()
        },
        'grad_year': {
            'label': 'Graduation Year'
        },
        'grad_term': {
            'label': 'Graduation Term',
            'widget': widgets.Select(),
            'default': ''
        },
        'adv_course': {
            'label': 'Furthest Core Course Taken',
            'widget': widgets.Select(),
            'default': ''
        },
        'student_status': {
            'label': 'Student Status',
            'widget': widgets.Select(),
            'default': ''
        }
    }
)

class Profile(Profile_):
    submit = SubmitField('Save')
