import datetime

from caltrack import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return "<User {}>".format(self.username)


recipes_ingredients = db.Table(
    'recipes_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.recipe_id')),
    db.Column('ingr_id', db.Integer, db.ForeignKey('ingredient.ingr_id'))
)


dailyTracker_recipes = db.Table(
    'dailyTracker_recipes',
    db.Column('dt_id', db.Integer, db.ForeignKey('dailytracker.dt_id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.recipe_id'))
)


dailyTracker_ingredients = db.Table(
    'dailyTracker_ingredients',
    db.Column('dt_id', db.Integer, db.ForeignKey('dailytracker.dt_id')),
    db.Column('ingr_id', db.Integer, db.ForeignKey('ingredient.ingr_id'))
)


class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    ingredients = db.relationship('Ingredient', secondary=recipes_ingredients,
                                  backref=db.backref('recipes', lazy='dynamic'))

    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def __repr__(self):
        return "<Recipe {}>".format(self.name)


class Ingredient(db.Model):
    ingr_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    fat = db.Column(db.Integer, nullable=False)
    fiber = db.Column(db.Integer, nullable=False)
    serving_size = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "<Ingredient {}>".format(self.name)


class DailyTracker(db.Model):
    dt_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    recipes = db.relationship('Recipe', secondary=dailyTracker_recipes,
                              backref=db.backref('daily_trackers'), lazy='dynamic')
    ingredients = db.relationship('Ingredient', secondary=dailyTracker_ingredients,
                                  backref=db.backref('daily_trackers', lazy='dynamic'))

    def __init__(self, recipes):
        self.date = datetime.date()
        self.recipes = recipes

    def __repr__(self):
        return "<DailyTracker {}".format(self.date)
