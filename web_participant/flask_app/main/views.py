from flask import render_template, redirect, url_for, current_app, request, flash
from flask_login import login_required, current_user
from . import main
from ..models import Event, Team
from flask_app.auth.forms import LoginForm, RegistrationForm
from .forms import EditProfileForm
from .helpers import seed_participants, delete_participants
from ..factory import db
from ..decorators import dispatch


@main.route('/')
@dispatch
def index():
    current_app.logger.info("In index")
    url = request.url_root
    domain = url.split("//")[1]
    subdomain = domain.split(".")[0]
    event = Event.query.filter_by(subdomain=subdomain).first()
    if current_user.is_authenticated:

        # Check if event is started ie people can see their plan for the night
        # Create plan
            # - address of Starter_Host
            # - address of Main_Host
            # - address of Dessert_Host

        team = Team.query.get(current_user.team_id)
        current_app.logger.info('EIGENES TEAM: {}'.format(team.teamname))

        if event.status < 5:
            return render_template('index.html', event=event)
        else:
            diet_to_word = {'1': "No special diet", '2': "Vegetarian", '3': "Vegan"}
            if team.host_1_id != current_user.team_id:
                host_1 = Team.query.get(team.host_1_id)
            else:
                host_1 = -1
                guests = Team.query.filter_by(host_1_id = host_1).all()
                diet = max([g.diet for g in guests])

            if team.host_2_id != current_user.team_id:
                host_2 = Team.query.get(team.host_2_id)
            else:
                host_2 = -1
                guests = Team.query.filter_by(host_2_id = host_2).all()
                diet = max([g.diet for g in guests])

            if team.host_3_id != current_user.team_id:
                host_3 = Team.query.get(team.host_3_id)
            else:
                host_3 = -1
                guests = Team.query.filter_by(host_3_id=team.id).all()
                diet = max([g.diet for g in guests])


            return render_template('index.html', event=event, host_1=host_1,
                    host_2=host_2, host_3=host_3, diet=diet_to_word[diet])
    else:
        form = LoginForm()
        lat = event.address['results'][0]['geometry']['location']['lat']
        lng = event.address['results'][0]['geometry']['location']['lng']
        db_polygon = event.polygon
        key = current_app.config["MAPS_API_KEY"]
        current_app.logger.info(current_user.is_authenticated)
        current_app.logger.info("User not authenticated")
        return render_template('landing_page.html', event=event, form=form, key=key, lat=lat, lng=lng, db_polygon=db_polygon)

@main.route('/fail')
def fail():
    return render_template('fail.html')

@main.route('/contact')
def contact():
    current_app.logger.info("In contact function")
    return render_template('contact.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/logout')
@login_required
def logout():
    return redirect(url_for('auth.logout'))

@main.route('/register')
def register():

    url = request.url_root
    domain = url.split("//")[1]
    subdomain = domain.split(".")[0]
    event = Event.query.filter_by(subdomain=subdomain).first()

    if event.status == "registration closed":
        flash("Sorry, registration is already closed.")
        return redirect(url_for('main.index'))

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    return render_template('auth/register.html', form=form)

@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = EditProfileForm()

    if request.method == 'POST':
        if form.validate():
            current_user.ping()
            current_user.name = form.name.data
            current_user.email = form.email.data
            current_user.team.diet = form.diet.data
            if len(form.password.data) >= 0:
                current_user.password = form.password.data

            db.session.add(current_user)
            db.session.commit()
            flash("Profile was edited successfully!", 'success')
            return redirect(url_for('main.index'))
        else:
            current_app.logger.info(form.errors)
            flash("Profile was not changed due to errors!", 'error')
    return render_template('settings.html', form=form)

@main.route('/seed/<count>')
@dispatch
def seed(count):

    url = request.url_root
    domain = url.split("//")[1]
    subdomain = domain.split(".")[0]
    event = Event.query.filter_by(subdomain=subdomain).first()
    form = LoginForm()
    lat = event.address['results'][0]['geometry']['location']['lat']
    lng = event.address['results'][0]['geometry']['location']['lng']
    db_polygon = event.polygon
    key = current_app.config["MAPS_API_KEY"]

    seed_participants(event.id, count=int(count))

    return render_template('landing_page.html', event=event, form=form, key=key, lat=lat, lng=lng, db_polygon=db_polygon, status=event.status)

@main.route('/delete')
@dispatch
def delete():
    url = request.url_root
    domain = url.split("//")[1]
    subdomain = domain.split(".")[0]
    event = Event.query.filter_by(subdomain=subdomain).first()
    # form = LoginForm()
    # lat = event.address['results'][0]['geometry']['location']['lat']
    # lng = event.address['results'][0]['geometry']['location']['lng']
    # db_polygon = event.polygon
    # key = current_app.config["MAPS_API_KEY"]

    #current_app.logger.info('DELETE')

    delete_participants(event.id)

    return redirect(url_for('main.index'))

    #return render_template('landing_page.html', event=event, form=form, key=key, lat=lat, lng=lng, db_polygon=db_polygon, status=event.status)

