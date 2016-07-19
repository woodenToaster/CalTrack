import ingredients_db

from caltrack.models import Ingredient

from caltrack import db


def populate_ingredients():
    for ingredient in ingredients_db.ingredients:
        ingr = Ingredient(**ingredient)
        db.session.add(ingr)
        db.session.commit()


def main():
    populate_ingredients()


if __name__ == '__main__':
    main()
