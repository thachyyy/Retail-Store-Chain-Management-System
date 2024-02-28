from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from app.core.settings import settings
from app.models.base import Base
#Import all models
from app.models.batch import *
from app.models.branch import *
from app.models.categories import *
# from app.models.contract_for_product import *
from app.models.contract import *
from app.models.customer import *
from app.models.employee import *
from app.models.import_order import *
from app.models.invoice_for_customer import *
from app.models.invoice_from_vendor import *
from app.models.order_of_batch import *
from app.models.product_of_warehouse_receipt import *
from app.models.product import *
from app.models.promotion_belong_to_branch import *
from app.models.promotion_for_order import *
from app.models.promotion import *
from app.models.purchase_order import *
from app.models.user import *
from app.models.vendor import *
from app.models.warehouse_receipt import * 

config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_db_url():
    return settings.SQLALCHEMY_DATABASE_URI


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_db_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = get_db_url()
    connectable = create_engine(url)
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
