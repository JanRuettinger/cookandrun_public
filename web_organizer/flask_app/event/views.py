from flask import render_template, redirect, url_for, current_app, request, flash
from flask_login import login_required, current_user
from . import event
from ..models import Event, Team, Group
from .forms import CreateEventForm, UpdateEventForm, MailForm
from .helpers import draw_teams, delete_groups, \
                    change_event_status
from ..factory import db
from ..email_helper import send_email
from ..decorators import event_access_required
import json
from datetime import datetime


@event.route('/new', methods=['GET', 'POST'])
def new():
    form = CreateEventForm()
    form_action = url_for('event.new')

    if request.method == 'POST':
        if form.validate_on_submit():
            event = Event(name=form.name.data, date=form.date.data,
                          city=form.city.data, postcode=form.postcode.data,
                          subdomain=form.subdomain.data,
                          organizer_id=current_user.id)

            db.session.add(event)
            try:
                db.session.commit()
            except:
                current_app.logger.info("IN EXCEPT")
                flash("Es ist ein Fehler aufgetreten", "error")
                return render_template('event/new.html', form=form,
                                       form_action=form_action)

            flash('Event was created successfully!', 'success')
            return redirect(url_for('main.index'))
    return render_template('event/new.html', form=form, form_action=form_action)


@event_access_required
@event.route('/<id>')
def show_event(id):
    event = Event.query.filter_by(id = id).first()
    if event:
        number_teams = (Event.query.join(Team).filter(Team.event_id == event.id).count())
        if number_teams % 9 == 0 and event.status == 3:
            change_event_status(event, 4)
        lat = event.address['results'][0]['geometry']['location']['lat']
        lng = event.address['results'][0]['geometry']['location']['lng']
        db_polygon = event.polygon
        # current_app.logger.info(event.status)
        key = current_app.config["MAPS_API_KEY"]
        return render_template('event/show_event.html', event=event,
                               number_teams=number_teams, key=key, lat=lat,
                               lng=lng, db_polygon=db_polygon)
                               #,form=form, form_action=form_action)
    else:
        return redirect(url_for('main.index'))


@event_access_required
@event.route('/<id>/update_settings', methods=['GET', 'POST'])
@login_required
def update_settings(id):
    event = Event.query.filter_by(id = id).first()
    form = UpdateEventForm(obj=event)
    form_action = url_for('event.update_settings', id=event.id)

    if event is None:
        return redirect(url_for('main.index'))

    if event.status == 5 or event.status == 2 or event.status == 6:
        flash("You are not allowed to change event settings atm.", "error")
        return redirect(url_for('main.index'))

    if request.method == 'POST' and event:
        if form.validate():
            event.name = form.name.data
            event.date = datetime.strptime(form.date.data, '%b %d, %Y')
            event.starter_time = form.starter_time.data
            event.main_time = form.main_time.data
            event.dessert_time = form.dessert_time.data
            event.subdomain = form.subdomain.data
            event.afterparty_address = form.afterparty_address.data
            event.afterparty_time = form.afterparty_time.data
            event.afterparty_description = form.afterparty_description.data

            db.session.add(event)
            db.session.commit()
            change_event_status(event, 1)
            flash('Event was edited successfully!', 'success')
        else:
            flash("Event settings were not changed due to errors!", "error")
        return render_template('event/update_settings.html', event=event, form=form, form_action=form_action)

    if event:
        return render_template('event/update_settings.html', event=event, form=form, form_action=form_action)


@event_access_required
@event.route('/<id>/update_map', methods=['GET', 'POST'])
@login_required
def update_map(id):
    event = Event.query.filter_by(id = id).first()

    if event is None:
        return redirect(url_for('main.index'))

    if event.status == 5 or event.status == 2 or event.status == 6:
        flash("You are not allowed to change event settings atm.", "error")
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        # request.method == "POST"
        event.polygon = request.get_json()
        db.session.add(event)
        db.session.commit()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    if event:
        lat = event.address['results'][0]['geometry']['location']['lat']
        lng = event.address['results'][0]['geometry']['location']['lng']
        db_polygon = event.polygon
        key = current_app.config["MAPS_API_KEY"]
        return render_template('event/update_map.html', event=event, key=key, lat=lat, lng=lng, db_polygon=db_polygon)
    else:
        return redirect(url_for('main.index'))


@event_access_required
@event.route('/<id>/open_registration', methods=["GET"])
def open_registration(id):
    event = Event.query.filter_by(id=id).first()

    if event is None:
        return redirect(url_for('main.index'))

    if event.status == 0:
        flash("You are not allowed to open the resgistration atm.", "error")
        return redirect(url_for('main.index'))

    change_event_status(event, 2)  # status = 2 reg open
    flash('Registration is now open!', 'success')
    return redirect(url_for('event.show_event', id=event.id))


@event_access_required
@event.route('/<id>/close_registration', methods=["GET"])
def close_registration(id):
    event = Event.query.filter_by(id=id).first()

    if event is None:
        return redirect(url_for('main.index'))

    if event.status == 0 or event.status == 1:
        flash("You are not allowed to close the resgistration atm.", "error")
        return redirect(url_for('main.index'))

    change_event_status(event, 3)
    flash('Registration is now closed!', 'success')
    return redirect(url_for('event.show_event', id=event.id))


@event_access_required
@event.route('/<id>/show_map', methods=['GET'])
def show_map(id):
    event = Event.query.filter_by(id = id).first()

    if event is None:
        return redirect(url_for('main.index'))

    if event.status == 0 or event.status == 1:
        flash("You can't to request the map atm.", "error")
        return redirect(url_for('main.index'))

    lat = event.address['results'][0]['geometry']['location']['lat']
    lng = event.address['results'][0]['geometry']['location']['lng']
    teams = Team.query.filter_by(event_id=event.id).all()
    number_groups = int(len(teams)/9)
    key = current_app.config["MAPS_API_KEY"]

    if event.status <= 4: # before draw
        teams_javascript  = []
        for t in teams:
            teams_javascript.append(t.id)
            teams_javascript.append(t.x_cord)
            teams_javascript.append(t.y_cord)
            teams_javascript.append(1)

        return render_template('event/show_map.html', teams=teams_javascript, lat=lat,
                               lng=lng, key=key, status = event.status)
    else: # after draw
        teams_javascript  = []
        for t in teams:
            teams_javascript.append(t.id)
            teams_javascript.append(t.x_cord)
            teams_javascript.append(t.y_cord)
            teams_javascript.append(t.group_id % number_groups)

        return render_template('event/show_map.html', teams=teams_javascript, lat=lat,
                               lng=lng, key=key, status = event.status)


@event_access_required
@event.route('/<id>/teams')
def show_teams(id):
    event = Event.query.filter_by(id=id).first()

    if event is None:
        return redirect(url_for('main.index'))

    if event.status <= 4:
        flash("You need to draw the teams first.", "error")
        return redirect(url_for('main.index'))

    groups = Group.query.filter_by(event_id=event.id).all()
    groups_with_names = []
    for g in groups:
        #groups_with_names.append(g.id)
        t1 = Team.query.filter_by(id=g.starter_1_host).first().teamname
        t2 = Team.query.filter_by(id=g.starter_1_guest_1).first().teamname
        t3 = Team.query.filter_by(id=g.starter_1_guest_2).first().teamname
        t4 = Team.query.filter_by(id=g.starter_2_host).first().teamname
        t5 = Team.query.filter_by(id=g.starter_2_guest_1).first().teamname
        t6 = Team.query.filter_by(id=g.starter_2_guest_2).first().teamname
        t7 = Team.query.filter_by(id=g.starter_3_host).first().teamname
        t8 = Team.query.filter_by(id=g.starter_3_guest_1).first().teamname
        t9 = Team.query.filter_by(id=g.starter_3_guest_2).first().teamname

        t10 = Team.query.filter_by(id=g.main_1_host).first().teamname
        t11 = Team.query.filter_by(id=g.main_1_guest_1).first().teamname
        t12 = Team.query.filter_by(id=g.main_1_guest_2).first().teamname
        t13 = Team.query.filter_by(id=g.main_2_host).first().teamname
        t14 = Team.query.filter_by(id=g.main_2_guest_1).first().teamname
        t15 = Team.query.filter_by(id=g.main_2_guest_2).first().teamname
        t16 = Team.query.filter_by(id=g.main_3_host).first().teamname
        t17 = Team.query.filter_by(id=g.main_3_guest_1).first().teamname
        t18 = Team.query.filter_by(id=g.main_3_guest_2).first().teamname

        t19 = Team.query.filter_by(id=g.dessert_1_host).first().teamname
        t20 = Team.query.filter_by(id=g.dessert_1_guest_1).first().teamname
        t21 = Team.query.filter_by(id=g.dessert_1_guest_2).first().teamname
        t22 = Team.query.filter_by(id=g.dessert_2_host).first().teamname
        t23 = Team.query.filter_by(id=g.dessert_2_guest_1).first().teamname
        t24 = Team.query.filter_by(id=g.dessert_2_guest_2).first().teamname
        t25 = Team.query.filter_by(id=g.dessert_3_host).first().teamname
        t26 = Team.query.filter_by(id=g.dessert_3_guest_1).first().teamname
        t27 = Team.query.filter_by(id=g.dessert_3_guest_2).first().teamname

        groups_with_names.append([t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,\
                                  t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,\
                                  t23,t24,t25,t26,t27])

    return render_template('event/show_teams.html', event=event,
                           groups=groups_with_names)


@event_access_required
@event.route('/<id>/draw')
def draw(id):
    event = Event.query.filter_by(id=id).first()

    if event is None:
        return redirect(url_for('main.index'))

    if event.status != 4:
        flash("You are not allowed to draw atm.", "error")
        return redirect(url_for('main.index'))

    draw_teams(event)
    change_event_status(event, 5)
    flash('Draw is finished!', 'success')
    return redirect(url_for('event.show_teams', id=id))


@event_access_required
@event.route('/<id>/start')
def start(id):
    event = Event.query.filter_by(id = id).first()

    if event is None:
        return redirect(url_for('main.index'))

    if event.status != 5:
        flash("You are not allowed to start the event atm.", "error")
        return redirect(url_for('main.index'))

    change_event_status(event, 6)

    # Send out email to all participants
    teams = Team.query.filter_by(event_id=event.id).all()
    for t in teams:
        part_1 = t.members[0]
        part_2 = t.members[1]
        send_email(part_1.email, subject='Your event plan', template='event/email/event_start',
                event=event)
        send_email(part_2.email, subject='Your event plan', template='event/email/event_start',
                event=event)
    flash('Event is now started!', 'success')
    return redirect(url_for('event.show_event', id=event.id))
    # Send out emails to all participants


@event_access_required
@event.route('/<id>/delete')
def delete(id):
    event = Event.query.filter_by(id = id).first()
    #change_event_status(event, 5)

    if event is None:
        return redirect(url_for('main.index'))

    teams = Team.query.filter_by(event_id = event.id).all()

    for t in teams:
        # current_app.logger.info("Team Members: ")
        # current_app.logger.info(t.members)
        # current_app.logger.info(t.members[0].email)
        #db.session.delete(t.members[0])
        #db.session.delete(t.members[1])
        db.session.delete(t)

    db.session.commit()
    db.session.delete(event)
    db.session.commit()

    return redirect(url_for('main.index'))


#@event.route('/<id>/mail')
#def send_mail(id):
#    event = Event.query.filter_by(id=id).first()
#    form = MailForm()
#    form_action = url_for('event.send_mail', id=event.id)
#
#    #if request.method == 'POST':
#    #    pass
#    #     # for team in teams:
#    #         send_email(team.email, 'Your new Account', 'auth/email/account_creation', organizer=organizer)
#    #if request.method == 'GET':
#    return render_template('event/mail.html', form=form, form_action=form_action)
#    #     # erstelle form
