from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

"""
Модель данных для хранения сокращенных ссылок в базе данных.
"""


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy в приложении.
    Наследуется от DeclarativeBase для поддержки декларативного стиля определения моделей.
    """

    pass


class ShortUrl(Base):
    """
    Модель для хранения сокращенных ссылок.

    Представляет таблицу 'short_urls' в базе данных, где хранятся соответствия
    между короткими идентификаторами (slugs) и оригинальными длинными URL.

    Attributes:
        slug (str): Короткий идентификатор (первичный ключ)
        long_url (str): Оригинальный длинный URL
    """

    __tablename__ = "short_urls"

    slug: Mapped[str] = mapped_column(primary_key=True)
    long_url: Mapped[str]
