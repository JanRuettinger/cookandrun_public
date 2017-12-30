from werkzeug.security import generate_password_hash, check_password_hash
from .factory import db
from flask_login import UserMixin, AnonymousUserMixin
from .factory import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
from sqlalchemy import orm
import bleach
import requests
import json


class Organizer(UserMixin, db.Model):
    __tablename__ = 'organizers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Organizer, self).__init__(**kwargs)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def get_events(self):
        pass

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Organizer %r>' % self.email


class Participant(UserMixin, db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'))

    # Relationships
    team = db.relationship("Team", back_populates="members")

    def __init__(self, **kwargs):
        super(Participant, self).__init__(**kwargs)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.email

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(64))
    diet = db.Column(db.String(64))  # normal, vegetarian, vegan
    specialties = db.Column(db.Text())  # e.g. allergic to bananas
    postcode = db.Column(db.String(16))
    city = db.Column(db.String(64))
    street = db.Column(db.String(128))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    x_cord = db.Column(db.Float)
    y_cord = db.Column(db.Float)

    group_id = db.Column(db.Integer, db.ForeignKey('groups.id',
        ondelete='CASCADE'))

    host_1_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'))
    host_2_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'))
    host_3_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'))

    # Relationships
    members = db.relationship('Participant', back_populates="team", passive_deletes=True)
    #group = db.relationship("Group", back_populates="teams", foreign_keys=[group_id])


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('organizers.id'))

    # general
    name = db.Column(db.String(64))
    subdomain = db.Column(db.String(64), unique=True)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    _address = db.Column(db.Text(), default="")
    _polygon = db.Column(db.Text(), default="")
    status = db.Column(db.Integer, default=0)

    #status
    # 0 = registration closed, organizer setups everything up (default status)
    # 1 = registration open, but teams don't know their hosts yet
    # 2 = registration closed, teams can now see their hosts
    # 3 = event officially startet, no special features yet

    # timetable
    starter_time = db.Column(db.String(20))
    main_time = db.Column(db.String(20))
    dessert_time = db.Column(db.String(20))

    # afterparty
    afterparty_flag = db.Column(db.Boolean(), default=True)
    afterparty_time = db.Column(db.String(20))
    afterparty_address = db.Column(db.String(140))
    afterparty_description = db.Column(db.String(140))


    def __init__(self, city, postcode, **kwargs):
        super(Event, self).__init__(**kwargs)
        self.postcode = postcode
        self.city = city
        #self.subdomain = city.lower()

        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + self.postcode  + self.city + "&key=" + current_app.config["MAPS_API_KEY"]
        response = requests.get(url)
        resp_json_payload = response.json()
        self.address = resp_json_payload
        # print(resp_json_payload['results'][0]['geometry']['location'])

    @orm.reconstructor
    def init_on_load(self):
        for attr in self.address['results'][0]['address_components']:
            #current_app.logger.info(attr['types'])
            if 'locality' in attr['types']:
                self.city = attr['long_name']
                #current_app.logger.info(attr['long_name'])

    @property
    def address(self):
        if not self._address:
            return {}
        return json.loads(self._address)

    @address.setter
    def address(self, value):
        self._address = json.dumps(value)

    @property
    def polygon(self):
        if not self._polygon:
            return {}
        return json.loads(self._polygon)

    @polygon.setter
    def polygon(self, value):
        self._polygon = json.dumps(value)



class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    starter_1_host = db.Column(db.Integer, db.ForeignKey('teams.id', name='1', ondelete='CASCADE'))
    starter_1_guest_1 = db.Column(db.Integer, db.ForeignKey('teams.id', name='2', ondelete='CASCADE'))
    starter_1_guest_2 = db.Column(db.Integer, db.ForeignKey('teams.id', name='3', ondelete='CASCADE'))

    starter_2_host = db.Column(db.Integer, db.ForeignKey('teams.id', name='4', ondelete='CASCADE'))
    starter_2_guest_1 = db.Column(db.Integer, db.ForeignKey('teams.id', name='5', ondelete='CASCADE'))
    starter_2_guest_2 = db.Column(db.Integer, db.ForeignKey('teams.id', name='6', ondelete='CASCADE'))

    starter_3_host = db.Column(db.Integer, db.ForeignKey('teams.id', name='7', ondelete='CASCADE'))
    starter_3_guest_1 = db.Column(db.Integer, db.ForeignKey('teams.id', name='8', ondelete='CASCADE'))
    starter_3_guest_2 = db.Column(db.Integer, db.ForeignKey('teams.id', name='9', ondelete='CASCADE'))

    main_1_host = db.Column(db.Integer, db.ForeignKey('teams.id', name='10', ondelete='CASCADE'))
    main_1_guest_1 = db.Column(db.Integer, db.ForeignKey('teams.id', name='11', ondelete='CASCADE'))
    main_1_guest_2 = db.Column(db.Integer, db.ForeignKey('teams.id', name='12', ondelete='CASCADE'))

    main_2_host = db.Column(db.Integer, db.ForeignKey('teams.id', name='13', ondelete='CASCADE'))
    main_2_guest_1 = db.Column(db.Integer, db.ForeignKey('teams.id', name='14', ondelete='CASCADE'))
    main_2_guest_2 = db.Column(db.Integer, db.ForeignKey('teams.id', name='15', ondelete='CASCADE'))

    main_3_host = db.Column(db.Integer, db.ForeignKey('teams.id', name='16', ondelete='CASCADE'))
    main_3_guest_1 = db.Column(db.Integer, db.ForeignKey('teams.id', name='17', ondelete='CASCADE'))
    main_3_guest_2 = db.Column(db.Integer, db.ForeignKey('teams.id', name='18', ondelete='CASCADE'))

    dessert_1_host = db.Column(db.Integer, db.ForeignKey('teams.id', name='19', ondelete='CASCADE'))
    dessert_1_guest_1 = db.Column(db.Integer, db.ForeignKey('teams.id', name='20', ondelete='CASCADE'))
    dessert_1_guest_2 = db.Column(db.Integer, db.ForeignKey('teams.id', name='21', ondelete='CASCADE'))

    dessert_2_host = db.Column(db.Integer, db.ForeignKey('teams.id', name='22', ondelete='CASCADE'))
    dessert_2_guest_1 = db.Column(db.Integer, db.ForeignKey('teams.id', name='23', ondelete='CASCADE'))
    dessert_2_guest_2 = db.Column(db.Integer, db.ForeignKey('teams.id', name='24', ondelete='CASCADE'))

    dessert_3_host = db.Column(db.Integer, db.ForeignKey('teams.id', name='25', ondelete='CASCADE'))
    dessert_3_guest_1 = db.Column(db.Integer, db.ForeignKey('teams.id', name='26', ondelete='CASCADE'))
    dessert_3_guest_2 = db.Column(db.Integer, db.ForeignKey('teams.id', name='27', ondelete='CASCADE'))

    #Relationships
    # teams = db.relationship('Team', back_populates="group", foreign_keys=[starter_1_id, starter_2_id, starter_3_id, main_1_id, main_2_id, main_3_id, dessert_1_id, dessert_2_id, dessert_3_id])
    #teams = db.relationship('Team', back_populates="group", foreign_keys=lambda: Team.group_id)

    def __init__(self, **kwargs):
        super(Group, self).__init__(**kwargs)


# DONT TOUCH

@login_manager.user_loader
def load_user(participant_id):
    try:
        return Participant.query.get(participant_id)
    except:
        return None


class AnonymousOrganizer(AnonymousUserMixin):
    pass


class AnonymousParticipant(AnonymousUserMixin):
    name = "ANON"
    pass


login_manager.anonymous_user = AnonymousParticipant
