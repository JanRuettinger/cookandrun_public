from functools import wraps
from flask import g, request, redirect, url_for, render_template, current_app, flash
from flask_login import current_user
from .models import Event
from .main import main
from .factory import db

# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if current_user.is_administrator():
#             return f(*args, **kwargs)
#         else:
#             return redirect(url_for('main.index'))
#     return decorated_function

def event_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        event_id = kwargs['id']
        event = Event.query.filter_by(id = event_id).first()
        if event is not None and event.organizer_id == current_user.id:
            return f(*args, **kwargs)
        else:
            flash("You don't have access to this event!", "error")
            return redirect(url_for('main.index'))
    return decorated_function
