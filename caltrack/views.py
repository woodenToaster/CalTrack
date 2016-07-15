from datetime import datetime

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import current_user, login_required
from flask.json import jsonify
from caltrack import app, db, lm, oid
from .forms import AddIngredientForm
from .models import User, Ingredient, Tracker

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
            return redirect(url_for('today'))
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


@app.route('/add', methods=['POST', 'GET'])
def add_ingredient():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    form = AddIngredientForm(request.form)
    if request.method == 'POST' and form.validate():
        ingr = Ingredient(
            name=form.name.data.lower(),
            calories=form.calories.data,
            protein=form.protein.data,
            carbs=form.carbs.data,
            fat=form.fat.data,
            fiber=form.fiber.data,
            serving_size=form.serving_size.data,
            unit=form.unit.data
        )
        db.session.add(ingr)
        db.session.commit()
        flash('New ingredient was successfully added')
        return redirect(url_for('today'))
    return render_template('add_ingredient.html', form=form)


@login_required
@app.route('/today')
def today():
    date = datetime.today().date()
    # Try to get today's Tracker from the db
    current_tracker = Tracker.query.filter_by(date=date).first()
    if current_tracker is None:
        # Add a Tracker for today to the db
        current_tracker = Tracker(date=date)
        db.session.add(current_tracker)
        db.session.commit()
    ingredients = [x for x in current_tracker.ingredients]
    day = current_tracker.date.day
    month = current_tracker.date.month
    return render_template('today.html', ingredients=ingredients, day=day, month=month)


@app.route('/search_ingredients')
def search_ingredients():
    search = request.args.get('search[term]')
    print(search)
    results = db.session.query(Ingredient).filter(Ingredient.name.like('%{}%'.format(search))).all()
    matches = [x.name for x in results]
    print(matches)
    return jsonify(matches)
