# Bain Problem 1 — Retry + Timeout + Exception Translation

## Requirement

The `/classify` endpoint calls an upstream AI provider.

Change the system so that:
- each provider attempt has a 2-second timeout
- timeout failures are retried exactly once
- if both attempts time out, raise `ClassificationUnavailableError`
- the API returns HTTP 503 for that domain exception
- non-timeout exceptions preserve existing behavior
- keep the change minimal and maintainable
- add appropriate tests

The new retry/timeout behavior is intentionally NOT implemented.

## Run

```bash
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```
