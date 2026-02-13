from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ShortUrl
from src.exceptions import SlugAlreadyExistsError


async def add_slug_to_database(
    slug: str,
    long_url: str,
    session: AsyncSession,
) -> None:
    """
    Добавляет новую запись о сокращенной ссылке в базу данных.

    Создает новый объект ShortUrl и сохраняет его в базе данных. При возникновении
    конфликта уникальности (IntegrityError) преобразует его в SlugAlreadyExistsError.

    Args:
        slug: Короткий идентификатор ссылки
        long_url: Оригинальный длинный URL
        session: Асинхронная сессия SQLAlchemy для работы с базой данных

    Raises:
        SlugAlreadyExistsError: Если запись с таким идентификатором уже существует
    """
    new_slug = ShortUrl(
        slug=slug,
        long_url=long_url,
    )
    session.add(new_slug)
    try:
        await session.commit()
    except IntegrityError:
        raise SlugAlreadyExistsError


async def get_long_url_by_slug_from_database(
    slug: str, session: AsyncSession
) -> str | None:
    """
    Получает оригинальный URL по короткому идентификатору из базы данных.

    Выполняет запрос к базе данных для поиска записи с указанным slug.
    Возвращает оригинальный URL, если запись найдена, или None, если не найдена.

    Args:
        slug: Короткий идентификатор ссылки для поиска
        session: Асинхронная сессия SQLAlchemy для выполнения запроса

    Returns:
        Оригинальный длинный URL, если запись найдена, иначе None

    Note:
        Функция использует scalar_one_or_none() для получения результата, что означает:
        - возвращает объект, если найдена ровно одна запись
        - возвращает None, если запись не найдена
        - выбрасывает исключение, если найдено более одной записи (что невозможно
          при прави��ьной настройке первичного ключа)
    """
    query = select(ShortUrl).filter_by(slug=slug)
    result = await session.execute(query)
    res: ShortUrl | None = result.scalar_one_or_none()
    return res.long_url if res is not None else None
