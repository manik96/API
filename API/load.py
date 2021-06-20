from flask import (Blueprint, Flask, flash, g, render_template, request, redirect, url_for)
from API.FileTesting import File_loader
from API.db import get_db, init_db

bp = Blueprint('loader', __name__)

@bp.route('/load', methods=('GET', 'POST'))
def load():
    if request.method == 'POST':
        path = request.form['Absolute Path']
        error = None

        spath = str(path)
        state = File_loader(spath)

        if isinstance(state, str):
            error = state

        if error is None:
            db = get_db()
            init_db()
            for row in state.itertuples(index=False, name=None):
                name, lname, nac, date, sex = row
                db.execute(
                    'INSERT INTO data (nombre, apellido, nacionalidad, fechaContrato, sexo) VALUES (?, ?, ?, ?, ?)',
                    (name, lname, str(nac), str(date.date()), sex)
                )
            db.commit()
            return redirect(url_for('viewer.view'))

        flash(error)
        print(error)

    return render_template('/load.html')

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['Nombre']
        lname = request.form['Apellido']
        nac = request.form['Nacionalidad']
        date = request.form['Fecha de Contrato']
        sex = request.form['Sexo']
        error = None

        if not name:
            error = 'Nombre es un campo obligatorio'
        elif not lname:
            error = 'Apellido es un campo obligatorio'
        elif not nac:
            nac = "<NA>"
        elif not date:
            error = 'Fecha de contrato es un campo obligatorio'
        elif not sex:
            error = 'Sexo es un campo obligatorio'

        if error is not None:
            flash(error)
        else:
            name = str(name)
            lname = str(lname)
            nac = str(nac)
            date = str(date)
            sex = str(sex)
            
            db = get_db()
            db.execute(
                'INSERT INTO data (nombre, apellido, nacionalidad, fechaContrato, sexo)'
                ' VALUES (?, ?, ?, ?, ?)', (name, lname, nac, date, sex)
            )
            db.commit()
            return redirect(url_for('viewer.view'))

    return render_template('/create.html')