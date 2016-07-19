from flask_wtf import Form
from wtforms import StringField, BooleanField, DecimalField, SelectField, PasswordField
from wtforms.validators import DataRequired, InputRequired


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegistrationForm(Form):
    username = StringField('username', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])


class AddIngredientForm(Form):
    name = StringField('name', validators=[InputRequired()])
    calories = DecimalField('calories', validators=[InputRequired()])
    protein = DecimalField('protein', validators=[InputRequired()])
    carbs = DecimalField('carbs', validators=[InputRequired()])
    fat = DecimalField('fat', validators=[InputRequired()])
    fiber = DecimalField('fiber', validators=[InputRequired()])
    serving_size = DecimalField('serving_size', validators=[InputRequired()])
    choices = ['oz', 'cup', 'gram', 'tablespoon', 'teaspoon', 'other']
    choices = [(c, c) for c in choices]
    unit = SelectField('unit', validators=[InputRequired()], choices=choices)


class AddToTrackerForm(Form):
    name = StringField('name', validators=[InputRequired()])
