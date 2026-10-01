## Task
Implement the approved max provider calls are in flight and provider excdeption functionlity

## Approved design
- Update `app/services/batch_service.py` to have semaphore limit of 3. 
In `process_items`, an item helper acquires it, awaits `self.client.process(item)`, and returns either the existing success dictionary or `{"item": item, "result": None, "error": str(exc)}` for an ordinary provider exception. 
Run those helpers with `asyncio.gather`. Its returned list retains input order even when calls finish in a different order.

## Requirements
Change it so that:
- at most 3 provider calls are in flight at once
- processing remains concurrent
- output order matches input order
- if one item fails, the rest continue
- failed item returns:
  - result = None
  - error = str(exception)
- successful items keep the same shape
- DI is preserved
- AIClient is unchanged
- tests cover concurrency limiting, ordering, and partial failure

## Files expected to change
Prefer changes only in:
- `app/services/batch_service.py`
- `tests/test_routes.py`
- `/tests/test_batch_service.py`

Do not modify `AIClient` or unrelated files unless there is a concrete reason.

## Tests
Add focused service tests for:

service test
    1. check max provider concurrent calls is 3
    2. if one item fails:
            1. check item has result = None and error = str(exception)
            2. success items has the right shape
            3. input -> output order of the items is the same
            4. len of inps is the same as len of ops
            

route test
    1.if one item fails:
        1. check item has result = None and error = str(exception)
        2. success items has the right shape
        3. input -> output order of the items is the same

Retain existing relevant tests.

## After implementation
- run the focused service tests
- run the full test suite
- show me the diff
- briefly explain:
    - what changed
    - why the change is minimal
    - whether any behavior outside the requirement changed

  