# AGENTS.md

Instrukcje dla agentów pracujących w tym repozytorium.

## Stack

- Python 3.12, menedżer pakietów: uv (`pyproject.toml`, `uv.lock`)
- LangGraph (grafy agentów), FastAPI + uvicorn (API)
- pydantic-settings (konfiguracja), Google Gemini przez `langchain-google-genai`
- Lint i format: ruff. Typy: mypy. Testy: pytest. Hooki: pre-commit

## Struktura

Moduły leżą bezpośrednio w `src/` i importuje się je jako pakiety najwyższego poziomu:

- `src/agents/` — grafy LangGraph (`from agents...`)
- `src/tools/` — narzędzia agentów (`from tools...`)
- `src/api/` — FastAPI, wejście: `api.main:app`, endpoint `GET /health`
- `src/core/` — `config.py` (Settings), `logging.py`, `llm.py` (`get_llm()`)
- `tests/` — pytest
- `docs/`, `scripts/` — miejsce na dokumentację i skrypty

Build (hatchling) ma `packages = ["src/core", "src/agents", "src/tools", "src/api"]`, więc katalog `src/` nie jest częścią nazwy importu.

## Konwencje

- Kod, komentarze i nazwy po angielsku. Type hints przy funkcjach publicznych.
- Nową logikę pokrywaj testem w `tests/`. Testy nie mogą wymagać klucza API ani sieci.
- Nazwa modelu Gemini pochodzi wyłącznie ze zmiennej `GEMINI_MODEL`. Nie wpisuj jej na sztywno w kodzie.
- `get_llm()` obsługuje teraz tylko `llm_provider=gemini`. Kolejnych dostawców (na przykład Groq) dodawaj jako następne gałęzie, bez zmiany reszty aplikacji.
- Zależności dodawaj przez `uv add` / `uv add --dev`. Nie twórz `requirements.txt` i nie wymyślaj wersji ręcznie.
- Przed oddaniem zmian uruchom `uv run ruff check .` i `uv run pytest`.
- Nigdy nie commituj sekretów (`.env`, klucze API). W repozytorium zostaje tylko `.env.example`.
- Nie wysyłaj danych prywatnych do darmowego API Gemini.
