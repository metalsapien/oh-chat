''' This module contains the verification form for rendering. '''

from flask_wtf import FlaskForm
from wtforms import StringField, validators


class VerifyForm(FlaskForm):
    ''' Class to initialize the username field of the form '''
    username = StringField('Name', [validators.Required()])
    