from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from database import Base, engine  # Sizning loyihangizdagi to'g'ri import

# target_metadata ni to'g'ri sozlash
target_metadata = Base.metadata

# Alembic Config ob'ekti
config = context.config

# Loglarni sozlash
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Migratsiya funksiyalari

def run_migrations_offline() -> None:
    """Offline rejimida migratsiyalarni bajarish."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Online rejimida migratsiyalarni bajarish."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Offline yoki Online rejimiga qarab mos funksiyani chaqirish
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
