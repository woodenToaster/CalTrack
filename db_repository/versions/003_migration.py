from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dailyTracker_recipes = Table('dailyTracker_recipes', post_meta,
    Column('dt_id', Integer),
    Column('recipe_id', Integer),
)

daily_tracker = Table('daily_tracker', post_meta,
    Column('dt_id', Integer, primary_key=True, nullable=False),
    Column('date', Date, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['dailyTracker_recipes'].create()
    post_meta.tables['daily_tracker'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['dailyTracker_recipes'].drop()
    post_meta.tables['daily_tracker'].drop()
