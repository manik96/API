from flask import (Blueprint, Flask, flash, g, render_template, request, redirect, url_for)
from API.FileTesting import File_loader
from API.db import get_db, init_db

bp = Blueprint('loader', __name__)

@bp.route('/load', methods=('GET', 'POST'))
def load():
    #Funcion de carga
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
    #Funcion de creacion
    if request.method == 'POST':
        name = str(request.form['Nombre'])
        lname = str(request.form['Apellido'])
        nac = str(request.form['Nacionalidad'])
        date = str(request.form['FechaContrato'])
        sex = str(request.form['Sexo'])
        error = None

        if name == "":
            error = 'Nombre es un campo obligatorio'
        elif lname == "":
            error = 'Apellido es un campo obligatorio'
        elif date == "":
            error = 'Fecha de contrato es un campo obligatorio'
        elif sex == "":
            error = 'Sexo es un campo obligatorio'
        if nac == "":
            nac = "<NA>"

        print(error)
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO data (nombre, apellido, nacionalidad, fechaContrato, sexo)'
                ' VALUES (?, ?, ?, ?, ?)', (name, lname, nac, date, sex)
            )
            db.commit()
            return redirect(url_for('viewer.view'))

    return render_template('/create.html')

@bp.route('/update', methods=['GET', 'POST'])
def update():
    #Funcion de actualizado. Se usa POST por jinja
    if request.method == 'POST':

        error = None

        try:  
            idn = int(request.form['ID'])
        except ValueError:
            flash('Numero ID equivocado. Por favor ingresar un numero entero positivo')
            return render_template('/update.html')

        name = str(request.form['Nombre'])
        lname = str(request.form['Apellido'])
        nac = str(request.form['Nacionalidad'])
        date = str(request.form['FechaContrato'])
        sex = str(request.form['Sexo'])

        if idn is None or idn == "":
            error = "Se requiere el campo de ID."
        elif not isinstance(idn, int) or idn < 0:
            error = "Solo se aceptan numeros enteros positivos."

        if error is not None:
            flash(error)
        else:
            db = get_db()

            top = db.execute('SELECT MAX(id) FROM data').fetchone()

            if idn > top[0]:
                flash("El numero de ID proporcionado es mayor al indice de la base de datos.")
                return render_template('/update.html')
            
            temp = db.execute('SELECT * FROM data WHERE id=?',(idn,)).fetchone()

            if name == "":
                name = temp[1]

            if lname == "":
                lname = temp[2]

            if nac == "":
                nac = temp[3]
            
            if date == "":
                date = temp[4]

            if sex == "":
                sex = temp[5]

            db.execute(
                'UPDATE data'
                ' SET nombre=?, apellido=?, nacionalidad=?, fechaContrato=?, sexo=?'
                ' WHERE id=?',(name, lname, nac, date, sex, idn)
            )
            db.commit()

            return redirect(url_for('viewer.view'))

    return render_template('/update.html')

@bp.route('/delete', methods=['GET', 'POST'])
def delete():
    #Funcion de borrado. Se usa POST por jinja
    if request.method == 'POST':
        error = None

        try:  
            idn = int(request.form['ID'])
        except ValueError:
            flash('Numero ID equivocado. Por favor ingresar un numero entero positivo')
            return render_template('/delete.html')

        if idn < 0:
            error = 'El numero de ID debe ser un numero positivo'

        if error is not None:
            flash(error)
        else:
            db = get_db()

            number = db.execute('SELECT MAX(id) FROM data').fetchone()
            if idn > number[0]:
                flash('El numero de ID proporcionado es mayor al indice de la base de datos.')
                return render_template('/delete.html')

            db.execute(
                'DELETE FROM data'
                ' WHERE id=?',(idn,)
            )
            db.commit()

            return redirect(url_for('viewer.view'))

    return render_template('/delete.html')