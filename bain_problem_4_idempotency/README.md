# Bain Problem 4 — Idempotency + Persistence Boundary

## Scenario

The `POST /jobs` endpoint creates a new job every time it is called.

Clients may retry the same request after a network failure. If the same
`idempotency_key` is submitted twice, the system currently creates two jobs.

## Requirement

Change the system so that:

- the first request for an `idempotency_key` creates a new job
- a repeated request with the same `idempotency_key` returns the existing job
- duplicate requests must not create a second job
- existing response shape stays unchanged
- the idempotency rule should live at the appropriate application layer
- keep the change minimal and maintainable
- tests should prove both first-request and duplicate-request behavior
- do not introduce a database or external cache for this exercise
- preserve the existing repository abstraction and dependency injection
