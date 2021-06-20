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