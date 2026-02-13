from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

"""
Конфигурация базы данных и управление подключениями.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Создание асинхронного движка SQLAlchemy для подключения к PostgreSQL
# Настройки пула подключений:
# - pool_size: 20 (основной пул подключений)
# - max_overflow: 30 (максимальное количество дополнительных подключений при высокой нагрузке)
engine = create_async_engine(
    url="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
    pool_size=20,
    max_overflow=30,
)

# Фабрика асинхронных сессий
# expire_on_commit=False означает, что объекты не будут истекать после коммита транзакции
new_session = async_sessionmaker(bind=engine, expire_on_commit=False)
