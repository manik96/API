from flask import (Blueprint, Flask, flash, g, render_template, request, redirect, url_for)
from API.FileTesting import File_loader
from API.db import get_db

bp = Blueprint('viewer', __name__)

@bp.route('/view')
def view():
    #Metodo 'GEt' usado para presentar toda la informacion actual de la base de datos
    db = get_db()
    rows = db.execute('SELECT * FROM data').fetchall()
    return render_template('view.html', rows=rows)