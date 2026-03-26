# ── Stage 1: Build dependencies ───────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        "fastapi[standard]>=0.128.0" \
        "sqlmodel>=0.0.21" \
        "psycopg2-binary>=2.9.9"

# ── Stage 2: Runtime image ────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Non-root user (matches runAsUser: 1000 in K8s)
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --no-create-home appuser

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

COPY app/ ./app/

# Writable tmp for any runtime writes
RUN mkdir -p /tmp/app && chown appuser:appgroup /tmp/app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# DATABASE_URL injected from K8s Secret volume or env
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
