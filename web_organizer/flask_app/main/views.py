from flask import render_template, redirect, url_for, current_app, request, flash
from flask_login import login_required, current_user
from . import main
from ..models import Event, Team
from flask_app.auth.forms import LoginForm, RegistrationForm
from .forms import EditProfileForm
from ..factory import db
import itertools


@main.route('/')
def index():
    if current_user.is_authenticated:
        # Get all events which are organized by current organizer
        events = []
        participants = []
        for event in Event.query.all():
            current_app.logger.info("CURRENT USER {}".format(current_user.id))
            current_app.logger.info("EVENT {}".format(event.organizer_id))
            if (current_user.id == event.organizer_id):
                events.append(event)
                current_app.logger.info(len(events))
                participants.append(Event.query.join(Team).filter(Team.event_id == event.id).count())
            # current_app.logger.info("EVENT NAME {}".format(event.name))

        if len(events) == 0:
            events = None
        else:
            events = itertools.zip_longest(events, participants)
        return render_template('main/index.html', events=events)
    form = LoginForm()
    return render_template('main/landing_page.html', form=form)


@main.route('/about')
def about():
    return render_template('main/about.html')


@main.route('/logout')
@login_required
def logout():
    return redirect(url_for('auth.logout'))


@main.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    return render_template('auth/register.html', form=form)


@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = EditProfileForm(obj=current_user)

    if request.method == 'POST':
        if form.validate():
            current_user.ping()
            current_user.name = form.name.data
            current_user.email = form.email.data
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Account settings were edited successfully!", "success")
            return redirect(url_for('main.index'))
        else:
            current_app.logger.info(form.errors)
            current_app.logger.info("Form error")
            flash("Profile was not changed due to errors!", "error")
            return render_template('main/settings.html', form=form)

    return render_template('main/settings.html', form=form)
