from faker import Faker
import click
import random

from flask_app.models import Organizer, Participant, Event, Team
from flask_app.factory import db
from flask import current_app
import requests


@click.option('--num_teams', default=36, help='Number of teams')
def populate_db(num_teams):
    """Populates the database with seed data."""
    fake = Faker()
    streets = ["Sebastianstrasse 12a",
               "Akazienweg 2",
               "Alfred-Mehl-Straße 3",
               "Am Brucker Bahnhof 7",
               "Am Brucker Seela 1",
               "Am Heiligenholz 2",
               "Am Pestalozziring 3",
               "Am Weichselgarten 4",
               "Am Winkelfeld 5",
               "Am Wolfsmantel 6",
               "An der Autobahn 3",
               "An der Lauseiche 2",
               "An der Wied 1",
               "Anna-Goes-Straße 10",
               "Anna-Wüstling-Weg 2",
               "Anschützstraße 3",
               "Bachfeldstraße 3",
               "Badergasse 4",
               "Bahnstraße 5",
               "Baumschulenweg 6",
               "Bauvereinsstraße 2",
               "Bienenweg 3",
               "Birkenweg 1",
               "Bonhoefferweg 2",
               "Herbstwiesenweg 3",
               "Herzogenauracher Damm 3",
               "Heuweg 3",
               "Hohlgasse 3",
               "Hollerweg 3",
               "Holzschuherring 3",
               "Huberweg 3",
               "Hummelweg 3",
               "Hutgraben 3",
               "Im Gäßla 3",
               "In der Zeil 3",
               "Jenaer Straße 3",
               "Judengasse 3",
               "Juragasse 3"]

    o1 = Organizer(email="demo@organizer.com", name="Jan",
                          password="demo")
    db.session.add(o1)
    db.session.commit()

    event =  Event(name="Laufgelage", postcode="91052", city="Erlangen", organizer_id=o1.id)
    db.session.add(event)
    db.session.commit()

    for i in range(num_teams-1):
        postcode = "91058"
        city = "erlangen"
        street = streets[i]

        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + \
                postcode  + city + street + "&key=" + current_app.config["MAPS_API_KEY"]
        response = requests.get(url)
        resp_json_payload = response.json()
        try:
            coords = (resp_json_payload['results'][0]['geometry']['location']['lat'], resp_json_payload['results'][0]['geometry']['location']['lng'])
        except:
            print(street)

        team = Team(teamname=fake.user_name(),
                    diet=random.randint(0,2),
                    postcode=postcode,
                    city=city,
                    street=street,
                    x_cord = coords[0],
                    y_cord = coords[1],
                    event_id=event.id)

        db.session.add(team)
        db.session.commit()

        password_1 = str(random.randint(1111,9999))
        password_2 = str(random.randint(1111,9999))

        participant_1 = Participant(email=fake.email(),
                                    name=fake.name(),
                                    password=password_1,
                                    team_id=team.id)

        participant_2 = Participant(email=fake.email(),
                                    name=fake.name(),
                                    password=password_2,
                                    team_id=team.id)

        db.session.add(participant_1)
        db.session.add(participant_2)
        db.session.commit()

    # Demo account
    postcode = "91058"
    city = "erlangen"
    street = "Enggleis 6"

    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + \
            postcode  + city + street + "&key=" + current_app.config["MAPS_API_KEY"]
    response = requests.get(url)
    resp_json_payload = response.json()
    try:
        coords = (resp_json_payload['results'][0]['geometry']['location']['lat'], resp_json_payload['results'][0]['geometry']['location']['lng'])
    except:
        print(street)

    team = Team(teamname="Demo",
                diet=random.randint(0,2),
                postcode=postcode,
                city=city,
                street=street,
                x_cord = coords[0],
                y_cord = coords[1],
                event_id=event.id)

    db.session.add(team)
    db.session.commit()

    password_1 = "demo"
    password_2 = "demo"

    participant_1 = Participant(email="demo@participant.com",
                                name=fake.name(),
                                password=password_1,
                                team_id=team.id)

    participant_2 = Participant(email="demo2@participant.com",
                                name=fake.name(),
                                password=password_2,
                                team_id=team.id)

    db.session.add(participant_1)
    db.session.add(participant_2)
    db.session.commit()

    print("Demo-Organizer:  demo@organizer.com Pw: demo")
    print("Demo-Participant: demo@participant.com Pw: demo")


def create_db():
    """Creates the database."""
    db.create_all()


def drop_db():
    """Drops the database."""
    if click.confirm('Are you sure?', abort=True):
        db.drop_all()


def recreate_db():
    """Same as running drop_db() and create_db()."""
    drop_db()
    create_db()


@click.option('--event_id',  help='You can see the event id in the browser or\
                                   look it up in the database')
def populate_event(event_id):
    fake = Faker()
    event = Event.query.filter_by(id=event_id).first()
    postcodes = ["91058"]
    streets = ["Sebastianstrasse12a",
               "Akazienweg 2",
               "Alfred-Mehl-Straße 3",
               "Am Brucker Bahnhof 7",
               "Am Brucker Seela 1",
               "Am Heiligenholz 2",
               "Am Pestalozziring 3",
               "Am Weichselgarten 4",
               "Am Winkelfeld 5",
               "Am Wolfsmantel 6",
               "An der Autobahn 3",
               "An der Lauseiche 2",
               "An der Wied 1",
               "Anna-Goes-Straße 10",
               "Anna-Wüstling-Weg 2",
               "Anschützstraße 3",
               "Bachfeldstraße 3",
               "Badergasse 4",
               "Bahnstraße 5",
               "Baumschulenweg 6",
               "Bauvereinsstraße 2",
               "Bienenweg 3",
               "Birkenweg 1",
               "Bonhoefferweg 2",
               "Herbstwiesenweg 3",
               "Herzogenauracher Damm 3",
               "Heuweg 3",
               "Hohlgasse 3",
               "Hollerweg 3",
               "Holzschuherring 3",
               "Huberweg 3",
               "Hummelweg 3",
               "Hutgraben 3",
               "Im Gäßla 3",
               "In der Zeil 3",
               "Jenaer Straße 3",
               "Judengasse 3",
               "Juragasse 3"]

    for i in range(36):

        postcode = postcodes[0]
        city="erlangen"
        street=streets[i]

        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + \
                postcode  + city + street + "&key=" + current_app.config["MAPS_API_KEY"]
        response = requests.get(url)
        resp_json_payload = response.json()
        #print(street)
        try:
            coords = (resp_json_payload['results'][0]['geometry']['location']['lat'], resp_json_payload['results'][0]['geometry']['location']['lng'])
            #print(coords)
        except:
            #print(resp_json_payload['results'])
            print(street)

        team = Team(teamname=fake.user_name(),
                    diet=random.randint(0,2),
                    postcode=postcode,
                    city=city,
                    street=street,
                    x_cord = coords[0],
                    y_cord = coords[1],
                    event_id=event.id)

        db.session.add(team)
        db.session.commit()

        password_1 = str(random.randint(1111,9999))
        password_2 = str(random.randint(1111,9999))

        participant_1 = Participant(email=fake.email(),
                                    name=fake.name(),
                                    password=password_1,
                                    team_id=team.id)

        participant_2 = Participant(email=fake.email(),
                                    name=fake.name(),
                                    password=password_2,
                                    team_id=team.id)

        db.session.add(participant_1)
        db.session.add(participant_2)
        db.session.commit()
