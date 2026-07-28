FROM python:3.13-slim

# Copy the uv binary from its official distroless image — fast, no extra install step
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first so this layer is cached unless deps change
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "lustrum_oblomow.main:app", "--host", "0.0.0.0", "--port", "8000"]
