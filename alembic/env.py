import os
from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# 1. Force load environment variables right away
load_dotenv(override=True)

# 2. Import your working database engine
from app.core.database import engine as db_engine

# 3. Import Base and your models so Alembic can read the schema
from app.models.base import Base
import app.models.student
import app.models.comment
import app.models.group
import app.models.webhook

# Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Renders the URL string without masking the password to prevent NeonDB auth errors
    url = db_engine.url.render_as_string(hide_password=False)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Connect directly using your working engine, bypassing alembic.ini entirely
    with db_engine.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()