"""FastAPI application entrypoint."""

from fastapi import FastAPI

from core.config import get_settings
from core.logging import configure_logging

configure_logging(get_settings())

app = FastAPI(title="ai-project")


@app.get("/")
def root() -> dict[str, str]:
    """Confirm the API is up."""
    return {"status": "ok", "health": "/health", "docs": "/docs"}


@app.get("/health")
def health() -> dict[str, str]:
    """Report that the process is running."""
    return {"status": "ok"}
