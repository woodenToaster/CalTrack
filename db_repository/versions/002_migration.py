from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
recipe = Table('recipe', post_meta,
    Column('recipe_id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=120), nullable=False),
)

recipes_ingredients = Table('recipes_ingredients', post_meta,
    Column('recipe_id', Integer),
    Column('ingr_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['recipe'].create()
    post_meta.tables['recipes_ingredients'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['recipe'].drop()
    post_meta.tables['recipes_ingredients'].drop()
