#initialize flask

import os
import redis

from flask import Flask
from flask_session import Session

#code pulled from Flask tutorial as needed

# create_app is the factory method
# TODO: a better explainer on Factory methods
# They're a way to provide instances of interfaces to subclasses, sorta?
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_url_path='/static')
    # __name__ is the name of the current module
    # instance_relative_config=True - Tells flask config files are relative to instance folder
    
    # Lets some default config stuff... Change 'dev' to rand
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    
    if test_config is None:
        # load instance config, if it exists, if not testing.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config if passed in
        app.config.from_mapping(test_config)

    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url('redis://:XsOh4vprLZ7SlNOPzW6j5PJp9e6AjMuk@localhost:6379')


    with app.app_context():
        from . import routes
        
        return app
    

