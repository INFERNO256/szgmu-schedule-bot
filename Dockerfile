# Stage 1: Builder
FROM python:3.14-slim-bookworm AS builder

# Install uv (copy from official image for speed)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set env vars for build
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Install dependencies first (caching layer)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Install project
COPY src/ src/
COPY alembic.ini .
COPY migrations/ migrations/
COPY README.md .
RUN uv sync --frozen --no-dev

# Stage 2: Runtime (distroless/minimal)
FROM python:3.14-slim-bookworm

# Runtime env vars
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy virtualenv and code from builder
COPY --from=builder /app /app

# Add entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN sed -i 's/\r$//' /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "src/main.py"]
