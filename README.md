# ai-project

Szkielet aplikacji z agentami LLM: LangGraph, FastAPI i Google Gemini (klucz z Google AI Studio).

Importy są płaskie (`from core.config import Settings`), bo hatchling instaluje każdy katalog z `src/` jako osobny pakiet najwyższego poziomu (`packages = ["src/core", ...]`). Po `uv sync` działa to w `uv run`, w testach i w obrazie Dockera.

## Wymagania

- Python 3.12 (pobierze go `uv`, nie musi być w systemie)
- [uv](https://docs.astral.sh/uv/)
- Docker, jeśli uruchamiasz stos przez Compose

## Klucz Google AI Studio

1. Wejdź na [Google AI Studio](https://aistudio.google.com/).
2. Zaloguj się na konto Google.
3. Utwórz klucz API (Get API key).
4. Skopiuj `.env.example` do `.env`.
5. Wklej klucz do `GOOGLE_API_KEY`.
6. W AI Studio sprawdź aktualną nazwę darmowego modelu Flash i wpisz ją w `GEMINI_MODEL`. Nazwa modelu nie jest wpisana w kodzie.

Nie commituj pliku `.env` i nie wysyłaj danych prywatnych do darmowego API.

## Uruchomienie lokalne

```powershell
uv sync
copy .env.example .env
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Albo `make run` po `make install`. Sprawdzenie: [http://localhost:8000/health](http://localhost:8000/health).

## Docker Compose

```powershell
copy .env.example .env
docker compose up --build
```

Albo `make docker-up`. Usługa `app` montuje `./src` i startuje uvicorn z `--reload`. Obraz produkcyjny (sam `Dockerfile`) startuje bez przeładowania, jako użytkownik nie-root. Usługa Postgres jest w pliku zakomentowana.

Jeśli build pada na `invalid peer certificate`, antywirus albo proxy skanuje HTTPS. Wyeksportuj ten urząd certyfikacji do `certs/*.crt` (pliki certyfikatów są w `.gitignore`) i zbuduj obraz jeszcze raz.

## Testy i lint

```powershell
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Przykładowy graf w `src/agents/example.py` nie woła modelu, więc test przechodzi bez klucza API.
