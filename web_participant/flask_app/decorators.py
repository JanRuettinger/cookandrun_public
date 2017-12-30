from functools import wraps
from flask import g, request, redirect, url_for, render_template, current_app
from flask_login import current_user
from .models import Event
from .main import main

def dispatch(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        url = request.url_root
        domain = url.split("//")[1]
        subdomain = domain.split(".")[0]
        event = Event.query.filter_by(subdomain=subdomain).first()
        print(url)
        print(subdomain)
        current_app.logger.info("Decorator:  {}, {}".format(url, subdomain))

        if event is not None:
            return f(*args, **kwargs)
        else:
           return redirect(url_for('main.fail'))

    return decorated_function
