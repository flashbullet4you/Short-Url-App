# Импорты стандартной библиотеки Python
import os
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

# Импорты FastAPI и зависимостей
from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

# Импорты SQLAlchemy для работы с базой данных
from sqlalchemy.ext.asyncio import AsyncSession

# Импорты компонентов приложения
from src.database.db import engine, new_session
from src.database.models import Base
from src.exceptions import (
    NoLongUrlFoundError,
    SlugAlreadyExistsError,
)
from src.service import (
    generate_short_url,
    get_url_by_slug,
    is_valid_url_regex,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Асинхронный контекстный менеджер для жизненного цикла приложения.

    Создает все таблицы в базе данных при запуске приложения и очищает ресурсы при завершении.

    Args:
        app: Экземпляр FastAPI приложения

    Yields:
        None: Генерирует управление обратно приложению на время его работы
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтируем папку со статикой
frontend_dir = os.path.join(os.path.dirname(__name__), "static")

if os.path.exists(frontend_dir):
    app.mount(
        "/",
        StaticFiles(directory=frontend_dir, html=True),
        name="static",
    )
else:

    @app.get("/")  # type: ignore[untyped-decorator]
    def read_root() -> dict[str, str]:
        """
        Обработчик GET-запроса для отображения статуса приложения.

        Возвращает сообщение о том, что frontend еще не скомпилирован.
        """
        return {"status": "frontend not built yet, serve only API"}


@app.get("/api/health")  # type: ignore[untyped-decorator]
def health() -> dict[str, str]:
    """
    Обработчик GET-запроса для проверки работоспособности приложения.

    Возвращает сообщение о том, что приложение работает.
    """
    return {"status": "healthy"}


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор сессий базы данных для использования в зависимостях FastAPI.

    Создает асинхронную сессию SQLAlchemy и предоставляет ее как зависимость.
    Автоматически закрывает сессию после использования.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy для работы с базой данных
    """
    async with new_session() as session:
        yield session


@app.get("/short_url")  # type: ignore[untyped-decorator]
async def serve_frontend() -> RedirectResponse:
    """
    Обработчик GET-запроса для отображения frontend.

    Перенаправляет пользователя на главную страницу frontend.

    Returns:
        RedirectResponse: Ответ с перенаправлением на frontend
    """
    return RedirectResponse(url="/short_url")


@app.post("/short_url")  # type: ignore[untyped-decorator]
async def generate_slug(
    long_url: Annotated[str, Body(embed=True)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, str]:
    """
    Генерирует короткий URL для переданного длинного URL.

    Args:
        long_url: Длинный URL для сокращения
        session: Асинхронная сессия базы данных (внедряется автоматически)

    Returns:
        Словарь с ключом "short_url" и значением - сгенерированным коротким URL

    Raises:
        HTTPException: При невалидном URL или ошибках ��енерации
    """
    res = await is_valid_url_regex(long_url)
    if res is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL невалиден",
        )
    try:
        new_slug = await generate_short_url(long_url, session)
    except SlugAlreadyExistsError:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось сгенерировать slug",
        )
    return {"short_url": new_slug}


@app.get("/{slug}")  # type: ignore[untyped-decorator]
async def redirect_to_url(
    slug: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RedirectResponse:
    """
    Обработчик GET-запроса для редиректа по короткому URL.

    Находит оригинальный URL по короткому инидикатору и перенаправляет на него.

    Args:
        slug: Короткий идентификатор URL
        session: Асинхронная сессия базы данных (внедряется автоматически)

    Returns:
        RedirectResponse: Ответ с перенаправлением на оригинальный URL

    Raises:
        HTTPException: Если URL с таким идентификатором не найден
    """
    try:
        long_url = await get_url_by_slug(slug, session)
    except NoLongUrlFoundError:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ссылка не существует",
        )
    return RedirectResponse(
        url=long_url, status_code=status.HTTP_302_FOUND
    )
