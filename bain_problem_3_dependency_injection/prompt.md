
## Prompt
## Task
Refactor the system so that RecommendationService can receive its dependencies from outside

## Approved design
- Add dependency injecttions &#32;repository and AI client to RecommendationService __init__ constructor in `app/services/recommendation.py`. Keep `RecommendationService.recommend` and the `/recommend` handler’s behavior as they are.
- At the `app/api/routes.py`  pass concrete `UserRepository()` and `AIClient()` instances to RecommendationService class

## Requirements
Refactor the system so that:
- RecommendationService can receive its dependencies from outside
- existing runtime behavior remains unchanged
- tests can exercise the service without using the real UserRepository. It can utilize Mock class for repository. 
- tests can exercise the service without using the real AIClient. It can utilize ASyncMock class for AIClient. 
- dependency injection is preserved cleanly
- the FastAPI endpoint behavior remains unchanged
- keep the change minimal and maintainable
- do not introduce unnecessary abstractions

## Files expected to change
Prefer changes only in:
- `app/services/recommendation.py`
- `app/api/routes.py`
- `tests/test_recommendation_service.py`

Do not modify `AIClient` or `user_repository.py` unrelated files unless there is a concrete reason.

## Tests
Add focused service tests for:

1. service test with Asyncmock
   - returns the result
   - await called once

Retain existing relevant tests.

## After implementation
- run the focused service tests
- run the full test suite
- show me the diff
- briefly explain: