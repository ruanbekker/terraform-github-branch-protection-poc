FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Test stage: unit tests run here, never part of the shipped image.
FROM base AS test

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY pytest.ini .
COPY main.py .
COPY tests/ tests/

RUN pytest -q

# Runtime stage: only the application and its runtime dependencies.
FROM base AS runtime

COPY main.py .

RUN useradd --system --no-create-home --uid 10001 appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
