# Makefile для управления задачами в Python-проекте

.PHONY: install dev install-hooks lint fix typecheck test check pre-commit all clean coverage docker docker-build docker-run

PYTHON := python
UV := uv
PRE_COMMIT := pre-commit
RUFF := $(UV) run ruff
BLACK := $(UV) run black
MYPY := $(UV) run mypy

# Установка зависимостей
install:
	$(UV) pip install -e .

dev: install
	$(UV) pip install ".[dev]"

# Установка pre-commit хуков
install-hooks:
	$(PRE_COMMIT) install

# Линтинг и форматирование
lint:
	$(RUFF) check src/

fix:
	$(BLACK) src/
	$(RUFF) check src/ --fix
	$(MYPY) src/

# Проверка типов
typecheck:
	$(MYPY) src/

# Тесты
test:
	PYTHONPATH=src $(PYTHON) -m pytest

# Покрытие кода тестами
coverage:
	PYTHONPATH=src $(PYTHON) -m pytest --cov=src --cov-report=html --cov-report=term

# Полная проверка (как в CI)
check:
	$(BLACK) --check src/
	$(RUFF) check src/
	$(MYPY) src/
	PYTHONPATH=src $(PYTHON) -m pytest

# Запуск pre-commit вручную (для проверки)
pre-commit:
	$(PRE_COMMIT) run --all-files

# Единая команда для локальной разработки
all: fix check

# Очистка
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage

# Docker
docker-build:
	docker build -t myapp .

docker-run: docker-build
	docker run -p 8000:8000 myapp

docker: docker-run
