from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError

class EditProfileForm(FlaskForm):
    email = StringField('Email von Organizer', validators=[Required(), Length(1, 64),Email()])
    name = StringField('Name von Organizer', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password')
    submit = SubmitField('Change Data')
