import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

"""
Конфигурация базы данных и управление подключениями.
"""

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение параметров подключения из переменных окружения
DB_TYPE = os.getenv("DB_TYPE", "postgresql")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")

# Формирование URL подключения к базе данных
DATABASE_URL = f"{DB_TYPE}+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Создание асинхронного движка SQLAlchemy для подключения к PostgreSQL
# Настройки пула подключений:
# - pool_size: 20 (основной пул подключений)
# - max_overflow: 30 (максимальное количество дополнительных подключений при высокой нагрузке)
engine = create_async_engine(
    url=DATABASE_URL,
    pool_size=20,
    max_overflow=30,
)

# Фабрика асинхронных сессий
# expire_on_commit=False означает, что объекты не будут истекать после коммита транзакции
new_session = async_sessionmaker(bind=engine, expire_on_commit=False)
