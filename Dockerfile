FROM python:3.12-slim

RUN apt-get update && apt-get install -y tzdata curl && apt-get upgrade -y && apt-get clean

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app/

COPY pyproject.toml uv.lock /app/

RUN uv sync --frozen --no-install-project

COPY app /app/app
COPY bot.py /app/bot.py

RUN uv sync

ENV PYTHONPATH=/app/

CMD ["python", "bot.py"]
