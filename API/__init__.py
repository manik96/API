import os
from flask import (Flask, flash, g, render_template, request, redirect, url_for)
from . import db
from . import load
from . import view


def create_app(test_config=None):
    #Inicializar y configurar la app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=b'\tZun\xf2b\x87\xa9\x13<)0\x1cw\xb5~',
        DATABASE=os.path.join(app.instance_path, 'APIdb')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    #Asegurarse de que el directorio 'instance' exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #Pagina de inicio del programa
    @app.route('/')
    def home():
        return render_template('home.html')

    #Registro de 'Blueprints', reglas de conexion
    app.add_url_rule('/', endpoint='/')
    db.init_app(app)
    app.register_blueprint(load.bp)
    app.register_blueprint(view.bp)

    return app
