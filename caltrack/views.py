from datetime import datetime

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import current_user, login_required
from flask.json import jsonify
from caltrack import app, db, lm, oid
from .forms import AddIngredientForm
from .models import User, Ingredient, Tracker


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


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_ingredients'))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/add_ingredient', methods=['POST', 'GET'])
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
    return render_template(
        'today.html',
        ingredients=ingredients,
        day=day,
        month=month,
        totals=current_tracker.get_totals()
    )


@app.route('/search_ingredients')
def search_ingredients():
    search = request.args.get('search[term]')
    print(search)
    results = db.session.query(Ingredient).filter(Ingredient.name.like('%{}%'.format(search))).all()
    matches = [x.name for x in results]
    print(matches)
    return jsonify(matches)


@app.route('/add_to_tracker', methods=['POST'])
def add_to_tracker():
    name = request.form['name']
    ingr = Ingredient.query.filter_by(name=name).first()
    if ingr:
        # Add to today's Tracker
        date = datetime.today().date()
        current_tracker = Tracker.query.filter_by(date=date).first()
        if current_tracker is None:
            raise Exception("Tracker for {} doesn't exist".format(date))
        else:
            current_tracker.ingredients.append(ingr)
            db.session.commit()
            return redirect(url_for('today'))
    else:
        # Add to database and today's tracker
        return redirect(url_for('add_ingredient'))
