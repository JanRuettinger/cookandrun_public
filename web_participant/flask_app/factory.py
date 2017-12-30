from flask import Flask, request
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

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    #app.config.from_pyfile('config.py')


    mail.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Configure logging
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
    # handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    # handler.setLevel(app.config['LOGGING_LEVEL'])
    # formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    # handler.setFormatter(formatter)
    # app.logger.addHandler(handler)
    @app.errorhandler(404)
    def page_not_found(error):
        return 'This route does not exist {}'.format(request.url), 404

    return app
