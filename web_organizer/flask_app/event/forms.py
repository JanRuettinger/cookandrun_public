from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextField, TextAreaField, IntegerField, DateField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Organizer, Event
from datetime import datetime

class CreateEventForm(FlaskForm):
    name = StringField('Name', validators=[Required(), Length(1, 64)])
    date = StringField('Date', validators=[Required()])
    city = StringField('Name', validators=[Required(), Length(1, 20)])
    postcode = StringField('Postleitzahl', validators=[Required(), Length(1, 5)])
    subdomain = StringField('Subdomain', validators=[Required(), Length(1,30)])

    def validate_subdomain(self, field):
        event = Event.query.filter_by(subdomain=field.data).first()
        # current_app.logger.info("event.name: " + event.name)
        # current_app.logger.info("self.name: " + self.name.data)
        # current_app.logger.info("event.date: " + str(event.date))
        # current_app.logger.info("self.date: " + str(datetime.strptime(self.date.data, '%b %d, %Y')))
        if event:
            raise ValidationError('Subdomain is already used.')

class UpdateEventForm(FlaskForm):
    name = StringField('Name', validators=[Required(), Length(1, 64)])
    date = StringField('Date', validators=[Required()])
    starter_time = StringField('Startzeit', validators=[Required()])
    main_time = StringField('Mainzeit', validators=[Required()])
    dessert_time = StringField('Dessertzeit', validators=[Required()])
    subdomain = StringField('Subdomain', validators=[Required()])
    afterparty_time = StringField('Afterpartyzeit', validators=[Required()])
    afterparty_address = StringField('Name', validators=[Required(), Length(1, 64)])
    afterparty_description = StringField('Afterpartybeschreibung', validators=[Required(), Length(1, 200)])

    def validate_subdomain(self, field):
        event = Event.query.filter_by(subdomain=field.data).first()
        # current_app.logger.info("event.name: " + event.name)
        # current_app.logger.info("self.name: " + self.name.data)
        # current_app.logger.info("event.date: " + str(event.date))
        # current_app.logger.info("self.date: " + str(datetime.strptime(self.date.data, '%b %d, %Y')))
        if event:
            if event.name != self.name.data and event.date != datetime.strptime(self.date.data, '%b %d, %Y'):
                raise ValidationError('Subdomain is already used.')


class MailForm(FlaskForm):
    subject = StringField('Subject', validators=[Required(), Length(1, 64)])
    content = TextAreaField('Content', validators=[Required()])


