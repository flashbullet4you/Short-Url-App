from httpx import AsyncClient


async def test_generate_slug(ac: AsyncClient):
    result = await ac.post("/short_url", json={"long_url": "https://google.com"})
    assert result.status_code == 200


async def test_valid_url(ac: AsyncClient):
    result = await ac.post("/short_url", json={"long_url": "htt:/g.com"})
    assert result.status_code == 400


async def test_empty_url(ac: AsyncClient):
    result = await ac.post("/short_url", json={"long_url": ""})
    assert result.status_code == 400
    assert result.json()["detail"] == "URL невалиден"


async def test_invalid_url_format(ac: AsyncClient):
    result = await ac.post("/short_url", json={"long_url": "not-a-url"})
    assert result.status_code == 400
    assert result.json()["detail"] == "URL невалиден"