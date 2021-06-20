import os
from flask import (Flask, flash, g, render_template, request, redirect, url_for)
from . import db
from . import load
from . import view


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='25530735',
        DATABASE=os.path.join(app.instance_path, 'APIdb')
    )
    app.config.from_pyfile('config.py', silent=True)

    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/')
    def home():
        return render_template('home.html')

    app.add_url_rule('/', endpoint='/')


    db.init_app(app)
    app.register_blueprint(load.bp)
    app.register_blueprint(view.bp)

    return app
