from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Импортируем ваши модели
from app.models import Base  # Импорт вашей базы (Base), которая содержит модели
from app.database import DATABASE_URL  # Ваша строка подключения

# Загружаем конфигурацию файла alembic.ini
config = context.config

# Чтение логгера из конфигурации файла alembic.ini
fileConfig(config.config_file_name)

# Указываем Alembic использовать вашу мета-информацию о моделях
target_metadata = Base.metadata

# Определяем URL базы данных
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline():
    """Запуск миграций в режиме оффлайн."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск миграций в режиме онлайн."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
