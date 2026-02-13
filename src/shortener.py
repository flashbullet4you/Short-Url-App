import string
from secrets import choice

"""
Модуль для генерации коротких идентификаторов (slugs) для сокращения ссылок.
"""


# Алфавит для генерации коротких идентификаторов (буквы и цифры)
ALPHABET: str = string.ascii_letters + string.digits


def generate_random_slug() -> str:
    """
    Генерирует случайный 6-символьный короткий идентификатор.

    Использует криптографически безопасный генератор случайных чисел (secrets.choice)
    для выбора символов из алфавита, включающего заглавные и строчные буквы латинского
    алфавита, а также цифры (0-9).

    Returns:
        Случайно сгенерированный 6-символьный строковый идентификатор

    Example:
        >>> generate_random_slug()
        'aB3x9Z'
        >>> generate_random_slug()
        'mK7p2Q'
    """
    slug = ""
    for _ in range(6):
        slug += choice(ALPHABET)
    return slug
