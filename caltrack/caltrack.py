import os
import sqlite3

from flask import Flask, g, render_template, request, session, url_for, redirect, abort, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update({
    'DATABASE': os.path.join(app.root_path, 'caltrack.db'),
    'SECRET_KEY': 'development key',
    'USERNAME': 'admin',
    'PASSWORD': 'default'
})

app.config.from_envvar('CALTRACK_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print("Initialized the database.")


def get_db():
    """Opens a new database connnection if there is none yet for the current
    application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_ingredients():
    db = get_db()
    cur = db.execute('select name, calories, protein, carbs, fat, fiber, serving_size from ingredients')
    ingredients = cur.fetchall()
    return render_template('show_ingredients.html', ingredients=ingredients)


@app.route('/add', methods=['POST'])
def add_ingredient():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    insert_stmt = 'insert into ingredients '
    insert_stmt += '(name, calories, protein, carbs, fat, fiber, serving_size) '
    insert_stmt += 'values (?, ?, ?, ?, ?, ?, ?)'
    db.execute(
        insert_stmt,
        [request.form['name'], request.form['calories'], request.form['protein'],
         request.form['carbs'], request.form['fat'], request.form['fiber'],
         request.form['serving_size']]
    )
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_ingredients'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_ingredients'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_ingredients'))

