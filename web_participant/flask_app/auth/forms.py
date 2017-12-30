from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextField, TextAreaField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Participant, Team, Event
from flask import request, current_app
from ..factory import db

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

class PasswordRecoveryForm(FlaskForm):
    email = StringField('E-Mail', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    email_1 = StringField('Email von Teilnehmer 1', validators=[Required(), Length(1, 64),Email()])
    email_2 = StringField('Email von Teilnehmer 2', validators=[Required(), Length(1, 64),Email()])
    name_1 = StringField('Teilnehmer 1', validators=[
        Required(), Length(1, 64), Regexp('^[a-zA-Z\s]*$', 0, 'Only letters (no special characters) are allowed')])
    name_2 = StringField('Teilnehmer 2', validators=[
        Required(), Length(1, 64), Regexp('^[a-zA-Z\s]*$', 0, 'Only letters (no special characters) are allowed')])

    teamname = StringField('Teamname', validators=[
        Required(), Length(1, 64), Regexp('^[a-zA-Z]*$', 0, 'Only letters (no special characters) are allowed')])

    city = StringField('City', validators=[Required(), Length(1, 64), Regexp('^[a-zA-Z\s]*$', 0, 'Only letters (no special characters) are allowed')])
    postcode = StringField('Postcode', validators=[Required(), Length(4,8), Regexp('^[0-9]*$', 0, 'Only numbers are allowed')])

    street = StringField('Street', validators=[Required(), Length(1, 64), Regexp('^[-.A-Za-z0-9 _]*[-.A-Za-z0-9][-.A-Za-z0-9 _]*$', 0, 'Only letters (no special characters) and numbers are allowed')])

    diet = RadioField('Ernährungsweise', choices=[('1', 'Vegetarier'),('2', 'Veganer'), ('3', 'Alles')], validators=[Required()])

    specialties = TextField('Specialties', validators=[Length(0,200), Regexp('^[a-zA-Z\s]*$', 0, 'Only letters (no special characters) are allowed')])
    submit = SubmitField('Register')

    def validate_email_1(self, field):
        # Check if any participant in this particular event is already using the entered email address.
        url = request.url_root
        domain = url.split("//")[1]
        subdomain = domain.split(".")[0]
        event = Event.query.filter_by(subdomain=subdomain).first()

        participants = Participant.query.filter_by(email=field.data).all()
        for p in participants:
            if p.team.event_id == event.id:
                raise ValidationError('Email already registered for this event.')

    def validate_email_2(self, field):
        # Check if any participant in this particular event is already using the entered email address.
        url = request.url_root
        domain = url.split("//")[1]
        subdomain = domain.split(".")[0]
        event = Event.query.filter_by(subdomain=subdomain).first()

        participants = Participant.query.filter_by(email=field.data).all()
        for p in participants:
            if p.team.event_id == event.id:
                raise ValidationError('Email already registered for this event.')
