from httpx import AsyncClient


async def test_generate_slug(ac: AsyncClient):  # type: ignore
    """
    Тест для генерации короткой ссылки
    """
    result = await ac.post(
        "/short_url", json={"long_url": "https://google.com"}
    )
    assert result.status_code == 200


async def test_valid_url(ac: AsyncClient):  # type: ignore
    """
    Тест для проверки валидности URL
    """
    result = await ac.post(
        "/short_url", json={"long_url": "htt:/g.com"}
    )
    assert result.status_code == 400


async def test_empty_url(ac: AsyncClient):  # type: ignore
    """
    Тест для проверки пустого URL
    """
    result = await ac.post("/short_url", json={"long_url": ""})
    assert result.status_code == 400
    assert result.json()["detail"] == "URL невалиден"


async def test_invalid_url_format(ac: AsyncClient):  # type: ignore
    """
    Тест для проверки невалидного формата URL
    """
    result = await ac.post("/short_url", json={"long_url": "not-a-url"})
    assert result.status_code == 400
    assert result.json()["detail"] == "URL невалиден"
