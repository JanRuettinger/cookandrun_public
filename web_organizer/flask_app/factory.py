from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .default_config import config
import logging

db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

from .commands import create_db, drop_db, populate_db, recreate_db,\
                      populate_event


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    #app.config.from_pyfile('config.py')
    #app.jinja_env.trim_blocks = True
    #app.jinja_env.lstrip_blocks = True

    mail.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .core import core as core_blueprint
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .event import event as event_blueprint

    app.register_blueprint(core_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(event_blueprint, url_prefix='/event')
    register_commands(app)

    # Configure logging
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
    # handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    # handler.setLevel(app.config['LOGGING_LEVEL'])
    # formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    # handler.setFormatter(formatter)
    # app.logger.addHandler(handler)

    return app

def register_commands(app):
    """Register custom commands for the Flask CLI."""
    for command in [create_db, drop_db, populate_db, recreate_db,
            populate_event]:
        app.cli.command()(command)
