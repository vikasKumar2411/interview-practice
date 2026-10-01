## Task
Implement the approved idempotency key check and create job behavior.

## Approved design
- Change create_job in `app/services/job_service.py` to check if a job with the idempotency key already exists. If found return the job else call the current repository.create_job(idempotency_key, payload) logic

## Requirements
- first request for an idempotency_key creates a job
- repeated request with the same key returns the existing job
- no duplicate job is created
- response shape stays unchanged
- idempotency logic lives at the right layer
- repository abstraction and DI are preserved
- no database/cache is added for this exercise
- tests prove both first-request and duplicate-request behavior

## Files expected to change
Prefer changes only in:
- `app/services/job_service.py`
- `tests/test_routes.py`
- `tests/test_job_service.py`

Do not modify `JobRepository` or unrelated files unless there is a concrete reason.

## Tests
Add focused service tests for:

1. api test for both first-request and duplicate-request behavior
   - returns the result

2. service test for both first-request and duplicate-request behavior
   - returns the result

Retain existing relevant tests.

## After implementation
- run the focused service tests
- run the full test suite
- show me the diff
- briefly explain:
    - what changed
    - why the change is minimal
    - whether any behavior outside the requirement changed
