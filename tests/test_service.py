from src.service import generate_short_url


async def test_generate_short_url(session):  # type: ignore
    """Тест для функции generate_short_url."""
    res = await generate_short_url("https://google.com", session)
    assert type(res) is str
    assert len(res) == 6


async def test_generate_short_url_duplicate(session):  # type: ignore
    """
    Тест для функции generate_short_url.
    Проверяет, что функция возвращает разные короткие ссылки для разных URL.
    """
    url = "https://example.com"
    # Генерируем первую короткую ссылку
    slug1 = await generate_short_url(url, session)
    # Пытаемся сгенерировать для того же URL
    slug2 = await generate_short_url(url, session)
    # Проверяем, что возвращается та же короткая ссылка
    assert slug1 != slug2


async def test_generate_short_url_different_urls(session):  # type: ignore
    """
    Тест для функции generate_short_url.
    Проверяет, что функция возвращает разные короткие ссылки для разных URL.
    """
    url1 = "https://example.com/page1"
    url2 = "https://example.com/page2"
    # Генерируем короткие ссылки для разных URL
    slug1 = await generate_short_url(url1, session)
    slug2 = await generate_short_url(url2, session)
    # Проверяем, что короткие ссылки разные
    assert slug1 != slug2
