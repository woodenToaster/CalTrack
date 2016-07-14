from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dailyTracker_recipes = Table('dailyTracker_recipes', pre_meta,
    Column('dt_id', INTEGER),
    Column('recipe_id', INTEGER),
)

daily_tracker = Table('daily_tracker', pre_meta,
    Column('dt_id', INTEGER, primary_key=True, nullable=False),
    Column('date', DATE, nullable=False),
)

tracker = Table('tracker', post_meta,
    Column('dt_id', Integer, primary_key=True, nullable=False),
    Column('date', Date, nullable=False),
)

tracker_ingredients = Table('tracker_ingredients', post_meta,
    Column('dt_id', Integer),
    Column('ingr_id', Integer),
)

tracker_recipes = Table('tracker_recipes', post_meta,
    Column('dt_id', Integer),
    Column('recipe_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dailyTracker_recipes'].drop()
    pre_meta.tables['daily_tracker'].drop()
    post_meta.tables['tracker'].create()
    post_meta.tables['tracker_ingredients'].create()
    post_meta.tables['tracker_recipes'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dailyTracker_recipes'].create()
    pre_meta.tables['daily_tracker'].create()
    post_meta.tables['tracker'].drop()
    post_meta.tables['tracker_ingredients'].drop()
    post_meta.tables['tracker_recipes'].drop()
