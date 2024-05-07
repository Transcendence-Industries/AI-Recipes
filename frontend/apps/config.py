"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, random, string


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Version
    VERSION = os.getenv('VERSION')

    # Set up the App SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice(string.ascii_lowercase) for i in range(32))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_ENGINE = os.getenv('DB_ENGINE', None)
    DB_USER = os.getenv('DB_USER', None)
    DB_PASSWORD = os.getenv('DB_PASSWORD', None)
    DB_HOST = os.getenv('DB_HOST', None)
    DB_PORT = os.getenv('DB_PORT', None)
    DB_NAME = os.getenv('DB_NAME', None)

    USE_SQLITE = True

    # try to set up a Relational DBMS
    if DB_ENGINE and DB_NAME and DB_USER:
        try:
            # Relational DBMS: PSQL, MySql
            SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
                DB_ENGINE,
                DB_USER,
                DB_PASSWORD,
                DB_HOST,
                DB_PORT,
                DB_NAME
            )

            USE_SQLITE = False
        except Exception as e:
            print('> Error: DBMS Exception: ' + str(e))
            print('> Fallback to SQLite ')

    if USE_SQLITE:
        # This will create a file in <app> FOLDER
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
