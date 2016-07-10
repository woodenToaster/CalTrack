from caltrack import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return "<User {}>".format(self.username)

recipes_ingredients = db.Table(
    'recipes_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.recipe_id')),
    db.Column('ingr_id', db.Integer, db.ForeignKey('ingredient.ingr_id'))
)


class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    ingredients = db.relationship(
        'Ingredient',
        secondary=recipes_ingredients,
        backref='recipes'
    )

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
    recipes = db.relationship('Recipe', secondary=recipes_ingredients)

    def __repr__(self):
        return "<Ingredient {}>".format(self.name)
