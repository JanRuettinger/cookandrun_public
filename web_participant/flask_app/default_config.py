import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Amazon Web Services credentials
    AWS_ACCESS_KEY_ID = '...'
    AWS_SECRET_ACCESS_KEY = '...'

    # Amazon Simple Email Service
    SES_REGION_NAME = 'us-west-2'  # change to match your region
    SES_EMAIL_SOURCE = '...'

    MAPS_API_KEY = '...'
    JSON_AS_ASCII = False

    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'flask.log'
    LOGGING_LEVEL = logging.DEBUG



class DevelopmentConfig(Config):
    SECRET_KEY = 'developmentkey'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'flask.log'
    LOGGING_LEVEL = logging.DEBUG
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://cookandrun:testtest@postgres:5432/cookandrun'

class TestingConfig(Config):
    DEBUG = False
    SECRET_KEY = "prod key"
    SQLALCHEMY_DATABASE_URI = ''

config = {
        'development': DevelopmentConfig,
        'production': TestingConfig,
        'default': DevelopmentConfig
        }
