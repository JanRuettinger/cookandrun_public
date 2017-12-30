from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth  # import Blueprint object
from ..factory import db
from ..models import Organizer
# from .decorators import admin_required, permission_required
from ..email_helper import send_email
from .forms import LoginForm, RegistrationForm, PasswordRecoveryForm
import random


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        # if not current_user.confirmed \
        # and request.endpoint[:5] != 'auth.':
        # return redirect(url_for('auth.unconfirmed'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password = str(random.randint(1111, 9999))
        organizer = Organizer(email=form.email.data, name=form.name.data, password=password)

        db.session.add(organizer)
        db.session.commit()

        send_email(organizer.email, subject='Your new Account',
         template='auth/email/account_creation', organizer=organizer, password=password)
        flash('Registration was successful!', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        organizer = Organizer.query.filter_by(email=form.email.data).first()
        if organizer is None:
            flash('Invalid username or password.', 'error')
            return render_template('main/login.html', form=form)
    if organizer and organizer.verify_password(form.password.data):
        login_user(organizer, form.remember_me.data)
        current_app.logger.info('Organizer authenticated: {}'.format(organizer.is_authenticated))
        flash('Login successful', 'success')
        return redirect(request.args.get('next') or url_for('main.index'))
    flash('Invalid username or password.', 'error')
    return render_template('auth/login.html', form=form)


@auth.route('/recover', methods=['GET', 'POST'])
def recover():
    form = PasswordRecoveryForm()
    if form.validate_on_submit():
        organizer = Organizer.query.filter_by(email=form.email.data).first()
        if organizer:
            password = str(random.randint(1111, 9999))
            organizer.password = password
            db.session.add(organizer)
            db.session.commit()
            send_email(organizer.email, subject='Password recovered',
             template= 'auth/email/recover_password', organizer=organizer, password=password)
            flash('A new password has been sent to your inbox.', 'success')
        else:
            flash('No account with this e-mail address', 'error')
        return redirect(url_for('main.index'))
    return render_template('auth/recover.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

# @auth.route('/unconfirmed')
# def unconfirmed():
#     if current_user.is_anonymous or current_user.confirmed:
#         return redirect('main.index')
#     return render_template('auth/unconfirmed.html')

# @auth.route('/confirm')
# @login_required
# def resend_confirmation():
#     token = current_user.generate_confirmation_token()
#     send_email(current_user.email, 'Confirm Your Account',
#                'auth/email/confirm', password="******", user=current_user, token=token)
#     flash('A new confirmation email has been sent to you by email.', 'info')
#     return redirect(url_for('main.index'))

# @auth.route('/confirm/<token>')
# @login_required
# def confirm(token):
#     if current_user.confirmed:
#         return redirect(url_for('main.index'))
#     if current_user.confirm(token):
#         flash('You have confirmed your account. Thanks!', 'success')
#     else:

#         flash('The confirmation link is invalid or has expired.', 'error')
#     return redirect(url_for('main.index'))

# @auth.route('/confirm', methods=["POST"])
# def confirmtoken():
#     form = ConfirmForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user.confirmed:
#             flash('Your account is already confirmed.' , 'info')
#             return redirect(url_for('main.index'))
#         if user.confirm(form.token.data):
#             user.password = form.password.data
#             login_user(user,form.remember_me.data)
#             flash('You have confirmed your account and set your password. Thanks!', 'success')
#             return redirect(url_for('main.index'))
#         else:
#             flash('The confirmation link is invalid or has expired.', 'error')
#     return redirect(url_for('main.index'))








