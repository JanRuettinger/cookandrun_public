from ..factory import db
from ..models import Organizer, Team, Event, Participant, Group
from flask import current_app


def seed_participants(event_id, count=1):
    from sqlalchemy.exc import IntegrityError
    from random import seed
    import forgery_py
    import random

    # Role.insert_roles()
    # o1 = Organizer(email="info@janruettinger.com",
    #          name="Jan",
    #          password="test")
    # e1 = Event(name="Laufgelage", postcode="91058", city="Erlangen", organizer_id=o1.id)
    # e2 = Event(name="Laufgelage", postcode="91052", city="Erlangen", organizer_id=o1.id)

    # db.session.add(o1)
    # db.session.add(e1)
    # db.session.add(e2)

    streets = ["Sebastianstrasse", "Am Bach", "Vogelherd", "Turmhügelweg"]

    seed()
    for i in range(count):
        streetnumber = str(random.randint(1,18))
        street = random.randint(0,3)
        team = Team(teamname=forgery_py.name.company_name(), specialties=forgery_py.lorem_ipsum.word(), diet=str(random.randint(1,3)), postcode="91058", city="Erlangen", street=streets[street] + " " + streetnumber, event_id=event_id)

        try:
            db.session.add(team)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        p_1 = Participant(email=forgery_py.internet.email_address(),
                         name=forgery_py.name.full_name(),
                         team_id=team.id,
                         password= "1111")

        p_2 = Participant(email=forgery_py.internet.email_address(),
                         name=forgery_py.name.full_name(),
                         team_id=team.id,
                         password= "1111")

        try:
            db.session.add(p_1)
            db.session.add(p_2)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def delete_participants(event_id):
    event = Event.query.filter_by(id = event_id).first()
    teams = Team.query.filter_by(event_id = event.id).all()
    #current_app.logger.info("Team members of Team 0:")
    #current_app.logger.info(teams[0].members)

    for t in teams:
        # current_app.logger.info("Team Members: ")
        # current_app.logger.info(t.members)
        # current_app.logger.info(t.members[0].email)
        db.session.delete(t)
        #db.session.delete(t.members[1])
        #db.session.delete(t)

    db.session.commit()

def group_teams(event_id):
    event = Event.query.filter_by(id = event_id).first()
    teams = Team.query.filter_by(event_id = event.id).all()

    number_of_groups = len(teams)/9
    for i in number_of_groups:
        g = Group(event_id=event_id)
        for n in range(8):
            teams[n+i].group_id = g.id
        db.session.add(g)
        db.session.commit()


def order_group(group_id):
    group = Group.query.filter_by(id = group_id).first()
    teams = Team.query.filter_by(group_id = group.id).all()

    # Starter1    Starter2   Starter3
    # 0,1,2       3,4,5     6,7,8

    # Main1       Main2     Main3
    # 1,3,6       4,2,8     7,0,5

    # Dessert1    Dessert2  Dessert3
    # 2,3,7       4,0,6     8,1,5

    group.starter_1_host = teams[0]
    group.starter_1_guest_1 = teams[1]
    group.starter_1_guest_1 = teams[2]

    group.starter_2_host = teams[3]
    group.starter_2_guest_1 = teams[4]
    group.starter_2_guest_1 = teams[5]

    group.starter_3_host = teams[6]
    group.starter_3_guest_1 = teams[7]
    group.starter_3_guest_1 = teams[8]

    group.main_1_host = teams[1]
    group.main_1_guest_1 = teams[3]
    group.main_1_guest_2 = teams[6]

    group.main_2_host = teams[4]
    group.main_2_guest_1 = teams[2]
    group.main_2_guest_2 = teams[8]

    group.main_3_host = teams[7]
    group.main_3_guest_1 = teams[0]
    group.main_3_guest_2 = teams[5]

    group.dessert_1_host = teams[2]
    group.dessert_1_guest_1 = teams[3]
    group.dessert_1_guest_2 = teams[7]

    group.dessert_2_host = teams[4]
    group.dessert_2_guest_1 = teams[0]
    group.dessert_2_guest_2 = teams[6]

    group.dessert_3_host = teams[8]
    group.dessert_3_guest_1 = teams[1]
    group.dessert_3_guest_2 = teams[5]

    db.session.commit()


