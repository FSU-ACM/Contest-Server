from flask_mongoengine.wtf import model_form
from wtforms import widgets
from app.models import Profile as ProfileModel

Profile = model_form(
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
            'widget': widgets.Select()
        },
        'race': {
            'label': 'Race',
            'widget': widgets.Select()
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
            'widget': widgets.Select()
        },
        'adv_course': {
            'label': 'Furthest Core Course Taken',
            'widget': widgets.Select()
        },
        'student_status': {
            'label': 'Student Status',
            'widget': widgets.Select()
        },
    }
)
