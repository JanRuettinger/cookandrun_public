from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextField, TextAreaField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Organizer

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

class PasswordRecoveryForm(FlaskForm):
    email = StringField('E-Mail', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email = StringField('Email Adresse', validators=[Required(), Length(1, 64),Email()])

    name = StringField('Name', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots, underscores and spaces')])

    # Output message for Email() validator.
    def validate_email(self, field):
        if Organizer.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
