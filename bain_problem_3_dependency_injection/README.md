# Bain Problem 3 — Dependency Injection + Testability Refactor

## Scenario

`RecommendationService` currently constructs its concrete dependencies internally.

This makes the service difficult to test in isolation and tightly couples it to the current repository and AI client implementations.

## Requirement

Refactor the system so that:

- `RecommendationService` can receive its dependencies from outside
- existing runtime behavior remains unchanged
- tests can exercise the service without using the real repository or real AI client
- keep the change minimal and maintainable
- do not introduce unnecessary abstractions
- preserve the existing FastAPI endpoint behavior

## Interview workflow

1. Read the requirement yourself
2. Manually inspect the repo
3. Ask Codex for analysis only
4. Decide the architecture/change boundary
5. Create/refine a plan
6. Implement
7. Run focused tests
8. Run full tests
9. Review the diff
10. Explain the change and tradeoffs
