import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    #Establece una conexion a la base de datos
    if 'database' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    #Finaliza la conexion a la base de datos
    db = g.pop('database', None)

    if db is not None:
        db.close()

def init_db():
    #Inizializa la base de datos bajo el esquema dado
    #print("Instanciando base de datos.")
    db = get_db()

    with current_app.open_resource('dbscheme.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Limpia la data existente y crea nuevas tablas"""
    init_db()
    click.echo('Base de datos instanciada')

def init_app(app):
    #Establece como limpiar la base de datos y añade un nuevo comando para flask
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)