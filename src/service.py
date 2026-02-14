import re

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.crud import (
    add_slug_to_database,
    get_long_url_by_slug_from_database,
)
from src.exceptions import NoLongUrlFoundError, SlugAlreadyExistsError
from src.shortener import generate_random_slug


async def generate_short_url(
    long_url: str, session: AsyncSession
) -> str:
    """
    Генерирует короткий идентификатор для длинного URL и сохраняет его в базе данных.

    Пытается создать уникальный короткий идентификатор до 5 раз при возникновении
    конфликта из-за уже существующего идентификатора.

    Args:
        long_url: Оригинальный длинный URL
        session: Асинхронная сессия SQLAlchemy для работы с базой данных

    Returns:
        Сгенерированный короткий идентификатор (slug)

    Raises:
        SlugAlreadyExistsError: Если не удалось сгенерировать уникальный идентификатор за 5 попыток
    """

    async def _generat_slug_and_add_to_db() -> str:
        slug = generate_random_slug()
        await add_slug_to_database(slug, long_url, session)
        return slug

    for attempt in range(5):
        try:
            slug = await _generat_slug_and_add_to_db()
            return slug
        except SlugAlreadyExistsError as ex:
            if attempt == 4:
                raise SlugAlreadyExistsError from ex
    return slug


async def get_url_by_slug(slug: str, session: AsyncSession) -> str:
    """
    Получает оригинальный URL по короткому идентификатору из базы данных.

    Args:
        slug: Короткий идентификатор URL
        session: Асинхронная сессия SQLAlchemy для работы с базой данных

    Returns:
        Оригинальный длинный URL

    Raises:
        NoLongUrlFoundError: Если URL с таким идентификатором не найден в базе данных
    """
    long_url = await get_long_url_by_slug_from_database(slug, session)
    if not long_url:
        raise NoLongUrlFoundError(f"No long url found for slug {slug}")
    return long_url


async def is_valid_url_regex(url: str) -> bool:
    """
    Проверяет URL с помощью регулярного выражения.

    Args:
        url (str): строка для проверки

    Returns:
        bool: True, если URL соответствует шаблону
    """
    pattern = re.compile(
        r"^https?://"  # Протокол http или https
        r"(?:www\.)?"  # Опциональный www
        r"[-a-zA-Z0-9@:%._+~#=]{1,256}"  # Доменное имя
        r"\."  # Точка перед доменом верхнего уровня
        r"[a-zA-Z0-9()]{1,6}"  # Домен верхнего уровня (2–6 символов)
        r"\b"  # Граница слова
        r"(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$",  # Путь и параметры
        re.IGNORECASE,
    )
    return bool(pattern.match(url))
