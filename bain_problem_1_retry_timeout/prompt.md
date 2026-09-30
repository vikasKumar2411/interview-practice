## Task
Implement the approved retry/timeout behavior for classification.

## Approved design
Keep `AIClient` responsible for a single provider call.

Put the retry and timeout orchestration in `ClassificationService`.

## Requirements
- each provider attempt must have a 2-second timeout
- retry exactly once on timeout
- if both attempts time out, raise `ClassificationUnavailableError`
- preserve all non-timeout exception behavior unchanged
- do not change the existing HTTP 503 handler
- do not change the route unless required by the implementation
- keep the change minimal

## Files expected to change
Prefer changes only in:
- `app/services/classification.py`
- `tests/test_classification_service.py`

Do not modify `AIClient`, route handling, or unrelated files unless there is a concrete reason.

## Implementation guidance
- use a per-attempt timeout around `client.classify(text)`
- make at most two total attempts
- retry only timeout-related failures
- after the second timeout, raise `ClassificationUnavailableError`
- preserve the original timeout as the exception cause where appropriate
- do not add a retry library or unnecessary abstraction

## Tests
Add focused service tests for:

1. success on the first attempt
   - returns the result
   - client called once

2. first attempt times out, second succeeds
   - returns the second result
   - client awaited exactly twice

3. both attempts time out
   - raises `ClassificationUnavailableError`
   - client awaited exactly twice

4. non-timeout exception
   - propagates unchanged
   - no retry occurs

Retain existing relevant tests.

## After implementation
- run the focused service tests
- run the full test suite
- show me the diff
- briefly explain:
  - what changed
  - why the change is minimal
  - whether any behavior outside the requirement changed