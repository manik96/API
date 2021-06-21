#Este archivo contiene los principales metodos del programa
from flask import (Blueprint, Flask, flash, g, render_template, request, redirect, url_for)
from API.FileTesting import File_loader
from API.db import get_db, init_db

bp = Blueprint('loader', __name__)

@bp.route('/load', methods=('GET', 'POST'))
def load():
    #Metodo utilizado para cargar los datos del archivo
    if request.method == 'POST':
        path = request.form['Absolute Path']
        error = None

        spath = str(path)
        state = File_loader(spath)

        if isinstance(state, str):
            error = state

        if error is None:
            db = get_db()
            #Asegurar que se inserta a una nueva tabla
            init_db()
            for row in state.itertuples(index=False, name=None):
                name, lname, nac, date, sex = row
                db.execute(
                    'INSERT INTO data (nombre, apellido, nacionalidad, fechaContrato, sexo) VALUES (?, ?, ?, ?, ?)',
                    (name, lname, str(nac), str(date.date()), sex)
                )
            db.commit()
            return redirect(url_for('viewer.view'))

        #Mostrar al usario cualquier error ocurrido durante el proceso
        flash(error)

    return render_template('/load.html')

@bp.route('/create', methods=('GET', 'POST'))
def create():
    #Metodo para la creacion de nuevos elementos en la tabla
    if request.method == 'POST':
        name = str(request.form['Nombre'])
        lname = str(request.form['Apellido'])
        nac = str(request.form['Nacionalidad'])
        date = str(request.form['FechaContrato'])
        sex = str(request.form['Sexo'])
        error = None

        #Solo el campo de nacionalidad puede estar vacio
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
    #Metodo para actualizar elementos en la tabla
    #Debido a contricciones de html forms se usa method='POST' y no method='PUT'
    if request.method == 'POST':

        error = None
        #Asegurar que se ingresa un elemento valido (int)
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

            #Corroborar que el numero proporcionado no sea mayor al indice de la tabla
            top = db.execute('SELECT MAX(id) FROM data').fetchone()
            if idn > top[0]:
                flash("El numero de ID proporcionado es mayor al indice de la base de datos.")
                return render_template('/update.html')

            #Para evitar la perdida de informacion asigna los valores existentes antes de insertar en la tabla
            temp = db.execute('SELECT * FROM data WHERE id=?',(idn,)).fetchone()
            if temp is not None:
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
    #Metodo para borrar filas de la tabla
    #Debido a contricciones de html forms se usa method='POST' y no method='DELETE'
    if request.method == 'POST':
        error = None

        #Asegurar que se ingresa un elemento valido (int)
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

            #Confirmar que el numero ingresado no sea mayor al indice de la tabla
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