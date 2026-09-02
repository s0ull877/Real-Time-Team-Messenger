# Этап 1: сборка
FROM python:3.13-slim AS builder

WORKDIR /app

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Сначала зависимости
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

# Копируем код
COPY . .

# Устанавливаем проект
RUN uv sync --frozen --no-dev


# Этап 2: production
FROM python:3.13-slim

WORKDIR /app

# Виртуальное окружение
COPY --from=builder /app/.venv /app/.venv

# Код приложения
COPY --from=builder /app/src /app/src

# Alembic
COPY --from=builder /app/alembic.ini /app/alembic.ini
COPY --from=builder /app/alembic /app/alembic

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# CMD ["app"]