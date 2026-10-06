# syntax=docker/dockerfile:1

FROM python:3.12-slim-trixie AS builder

COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /uvx /bin/

# Optional PEM files in certs/ (antivirus or proxy HTTPS scanning). Not committed.
COPY certs/ /tmp/extra-certs/
RUN find /tmp/extra-certs -type f -name '*.crt' -exec cp {} /usr/local/share/ca-certificates/ \; \
    && update-ca-certificates \
    && rm -rf /tmp/extra-certs

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    UV_SYSTEM_CERTS=1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

FROM python:3.12-slim-trixie AS runtime

RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid app --home-dir /app --no-create-home --shell /usr/sbin/nologin app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

WORKDIR /app
USER app

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
