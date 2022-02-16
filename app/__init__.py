#initialize flask

import os

from flask import Flask

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


    with app.app_context():
        from . import routes
        
        return app
    

