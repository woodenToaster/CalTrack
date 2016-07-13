from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from caltrack import app, db, lm, oid
from .forms import LoginForm
from .models import User, Ingredient

# @app.route('/')
# @app.route('/index')
# @login_required
# def index():
#     user = g.user
#     return render_template('index.html', title='Home', user=user)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
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


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


# @oid.after_login
# def after_login(resp):
#     if resp.email is None or resp.email == "":
#         flash('Invalid login. Please try again.')
#         return redirect(url_for('login'))
#     user = User.query.filter_by(emial=resp.email).first()
#     if user is None:
#         username = resp.username
#         if username is None or username == "":
#             username = resp.email.split('@')[0]
#         user = User(username=username, email=resp.email)
#         db.session.add(user)
#         db.session.commit()
#     remember_me = False
#     if 'remember_me' in session:
#         remember_me = session['remember_me']
#         session.pop('remember_me', None)
#     login_user(user, remember=remember_me)
#     return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_ingredients'))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def show_ingredients():
    ingredients = Ingredient.query.all()
    return render_template('show_ingredients.html', ingredients=ingredients)


@app.route('/add', methods=['POST'])
def add_ingredient():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    insert_stmt = 'insert into ingredients '
    insert_stmt += '(name, calories, protein, carbs, fat, fiber, serving_size) '
    insert_stmt += 'values (?, ?, ?, ?, ?, ?, ?)'
    ingr = Ingredient(
        name=request.form['name'],
        calories=request.form['calories'],
        protein=request.form['protein'],
        carbs=request.form['carbs'],
        fat=request.form['fat'],
        fiber=request.form['fiber'],
        serving_size=request.form['serving_size']
    )
    db.session.add(ingr)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_ingredients'))
