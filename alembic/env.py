from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from models import Base
import os

config = context.config

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    DB_HOST = os.environ.get("DB_HOST", "todo-db")
    DB_PORT = os.environ.get("DB_PORT", "5432")

    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
    )

config.set_main_option("sqlalchemy.url", DATABASE_URL)
target_metadata = Base.metadata

print("DATABASE_URL =", DATABASE_URL)


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()