import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

from alembic_migrations.config.autogenerate_base_metadatas import autogenerate_base_metadatas
from alembic_migrations.config.autogenerate_excluded_tables import autogenerate_excluded_tables

# Load environment variables from .env file
load_dotenv()

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Allow interpolation vars to be passed to alembic.ini from the host environment
section = config.config_ini_section
config.set_section_option(section, "DB_CONNECTION_STRING", os.environ.get("DB_CONNECTION_STRING"))

# Add your model's MetaData object here for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = autogenerate_base_metadatas

# Function to exclude database tables not managed by SQLAlchemy
def include_object(object, name, type_, reflected, compare_to):
    print(f"Processing object: name={name}, type={type_}, reflected={reflected}")
    if type_ == "table":
        if name in autogenerate_excluded_tables:
            print(f"Excluding table: {name}")
            return False
        else:
            print(f"Including table: {name}")
            return True
    return True

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
