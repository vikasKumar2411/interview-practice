# Bain Problem 5 — Bounded Concurrency + Partial Failure Handling

## Scenario

The `POST /batch` endpoint processes many items through an external AI provider.

`BatchService.process_items` currently sends all provider calls concurrently with
`asyncio.gather`. For a large batch, that can overwhelm the upstream provider.

Also, if one provider call fails, the current `gather` call fails the whole batch.

## Requirement

Change the system so that:

- no more than 3 provider calls are in flight at once
- items should still be processed concurrently
- results must preserve the original input order
- if one item fails, the rest of the batch should continue
- a failed item should return:
  - `result = None`
  - `error = str(exception)`
- successful items should keep their current response shape
- keep the change minimal and maintainable
- preserve dependency injection
- do not change `AIClient`
- add focused tests for concurrency limiting, order preservation, and partial failure
