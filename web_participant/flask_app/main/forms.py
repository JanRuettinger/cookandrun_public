from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Participant

class EditProfileForm(FlaskForm):
    teamname = StringField('Teamname', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    email = StringField('Email von Teilnehmer', validators=[Required(), Length(1, 64),Email()])
    name = StringField('Teilnehmer 1', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][ A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots, spaces or underscores')])
    password = PasswordField('Password', validators=[Length(0, 14)])

    #location = StringField('Addresse von unserer Küche', validators=[Required(), Length(1, 64)])
    diet = RadioField('Ernährungsweise', choices=[('1', 'Vegetarier'), ('2', 'Veganer'), ('3', 'Alles')], validators=[Required()])

#    specialties = StringField('Specialties', validators=[Length(1, 64)])
    submit = SubmitField('Change Data')
