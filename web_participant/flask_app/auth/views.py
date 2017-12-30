from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth # import Blueprint object
from ..factory import db
from ..models import Organizer, Team, Event, Participant
# from .decorators import admin_required, permission_required
from ..email import send_email
from .forms import LoginForm, RegistrationForm, PasswordRecoveryForm
import random
from shapely.geometry import Point, Polygon
import requests


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    key = current_app.config["MAPS_API_KEY"]

    url = request.url_root
    domain = url.split("//")[1]
    subdomain = domain.split(".")[0]
    event = Event.query.filter_by(subdomain=subdomain).first()

    db_polygon = event.polygon
    key = current_app.config["MAPS_API_KEY"]

    #if event.status == 1:
        #return redirect(url_for('main.index'))

    if form.validate_on_submit():

        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + form.postcode.data  + form.city.data + form.street.data + "&key=" + current_app.config["MAPS_API_KEY"]
        response = requests.get(url)
        resp_json_payload = response.json()
        coords = (resp_json_payload['results'][0]['geometry']['location']['lat'], resp_json_payload['results'][0]['geometry']['location']['lng'])
        pt = Point(coords[0], coords[1])

        # Create polygon with shapely library
        polygon_help = []
        for e in db_polygon:
            polygon_help.append((e['lat'],e['lng']))

        polygon = Polygon(polygon_help)

        current_app.logger.info(polygon.contains(pt))

        if not polygon.contains(pt):
            flash('Your address is not inside the specified area. Maybe you can use the kitchen of a friend', 'error')
            return render_template('auth/register.html', form=form, key=key)

        # Check if Polygon contains location http://stackoverflow.com/questions/32180390/find-if-point-inside-polygon-on-google-maps-using-python

        team = Team(teamname=form.teamname.data,
                    diet=form.diet.data,
                    specialties=form.specialties.data,
                    postcode=form.postcode.data,
                    city=form.city.data,
                    street=form.street.data,
                    event_id=event.id,
                    x_cord = coords[0],
                    y_cord = coords[0])

        db.session.add(team)
        db.session.commit()

        password_1 = str(random.randint(1111,9999))
        password_2 = str(random.randint(1111,9999))

        participant_1 = Participant(email=form.email_1.data,
                                    name=form.name_1.data,
                                    password=password_1,
                                    team_id=team.id)

        participant_2 = Participant(email=form.email_2.data,
                                    name=form.name_2.data,
                                    password=password_2,
                                    team_id=team.id)

        db.session.add(participant_1)
        db.session.add(participant_2)
        db.session.commit()

        #token = user.generate_confirmation_token()
        # send_email(user1.email, 'Confirm Your Account',
        #   'auth/email/confirm', user=participant_1, password=password, token=token)
        send_email(participant_1.email, 'You are in!',
                   user=participant_1, password=password_1)
        send_email(participant_2.email, 'You are in!',
                   user=participant_2, password=password_2)
        flash('Registration was successful. An email has been sent to both e-mail addresses.', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form, key=key, db_polygon=db_polygon)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Participant.query.filter_by(email=form.email.data).first()
      #if user.is_administrator == False:
       #   pass
        if user is not None and user.verify_password(form.password.data):
            current_app.logger.info("LOG USER IN")
            current_app.logger.info(user.email)
            current_app.logger.info(user.id)
            login_user(user, form.remember_me.data)
            flash('Login successful', 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.', 'error')
        #return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@auth.route('/recover_password', methods=['GET', 'POST'])
def recover_password():
    form = PasswordRecoveryForm()
    if form.validate_on_submit():
        user = Participant.query.filter_by(email=form.email.data).first()
        if user == None:
            flash('unknown e-mail address', 'error')
            return render_template('auth/password_recovery.html', form=form)
        password_new = str(random.randint(1111,9999))
        user.password = password_new
        db.session.add(user)
        db.session.commit()
        send_email(user.email, 'Your new password',
                   template='auth/email/password_recovery',
                   user=user, password=password_new)
        flash('A new password has beenesent to you by email.', 'info')
        return redirect(url_for('main.index'))
    return render_template('auth/password_recovery.html', form=form)
# @auth.before_app_request
# def before_request():
#   if current_user.is_authenticated:
#       current_user.ping()
#       if not current_user.confirmed \
#       and request.endpoint[:5] != 'auth.':
#           return redirect(url_for('auth.unconfirmed'))
#
#@auth.route('/unconfirmed')
#def unconfirmed():
#    if current_user.is_anonymous or current_user.confirmed:
#        return redirect('main.index')
#    return render_template('auth/unconfirmed.html')
#
#@auth.route('/confirm')
#@login_required
#def resend_confirmation():
#    token = current_user.generate_confirmation_token()
#    send_email(current_user.email, 'Confirm Your Account',
#               'auth/email/confirm', password="******", user=current_user, token=token)
#    flash('A new confirmation email has been sent to you by email.', 'info')
#    return redirect(url_for('main.index'))
#
#@auth.route('/confirm/<token>')
#@login_required
#def confirm(token):
#    if current_user.confirmed:
#        return redirect(url_for('main.index'))
#    if current_user.confirm(token):
#        flash('You have confirmed your account. Thanks!', 'success')
#    else:
#        flash('The confirmation link is invalid or has expired.', 'error')
#    return redirect(url_for('main.index'))
#
#@auth.route('/confirm', methods=["POST"])
#def confirmtoken():
#    form = ConfirmForm()
#    if form.validate_on_submit():
#        user = Participant.query.filter_by(email=form.email.data).first()
#        if user.confirmed:
#            flash('Your account is already confirmed.' , 'info')
#            return redirect(url_for('main.index'))
#        if user.confirm(form.token.data):
#            user.password = form.password.data
#            login_user(user,form.remember_me.data)
#            flash('You have confirmed your account and set your password. Thanks!', 'success')
#            return redirect(url_for('main.index'))
#        else:
#            flash('The confirmation link is invalid or has expired.', 'error')
#    return redirect(url_for('main.index'))


