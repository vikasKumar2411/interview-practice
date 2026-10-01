# Problem 7 — Structured AI Output Validation

## Scenario

This service asks an AI provider to classify a support ticket.

The AI provider returns a Python dictionary that is expected to follow a strict schema.

The current service trusts the provider output and returns it directly.

## New Requirement

Update the system so that:

1. The service validates the AI provider output before returning it.
2. A valid AI response must contain:
   - `category`: one of `"billing"`, `"technical"`, `"account"`
   - `priority`: one of `"low"`, `"medium"`, `"high"`
   - `summary`: a non-empty string
3. Extra fields from the AI provider are allowed and should be ignored.
4. If the AI response is invalid, raise a domain exception named `InvalidAIResponseError`.
5. Preserve the original invalid provider payload on the exception as `payload`.
6. The API layer must translate `InvalidAIResponseError` into HTTP `502`.
7. The HTTP response body must be:

   ```json
   {
     "detail": "AI provider returned an invalid response"
   }
   ```

8. Non-validation exceptions from the AI provider must continue to propagate unchanged.
9. Do not retry the provider.
10. Preserve the existing successful API response shape.
11. Add focused tests for the new behavior.

## Constraints

- Make the smallest maintainable change.
- Keep provider logic provider-specific; do not move validation into the provider.
- Do not add retries or fallback behavior.
- Do not introduce a new framework.
- Existing tests should continue to pass.

## Your Workflow

Start with:

### Step 1
Read the requirement yourself.

### Step 2
Inspect the repo manually:
- project structure
- route → service → provider flow
- current response models
- exception handling
- existing tests

Then tell ChatGPT:
- your understanding of the current architecture
- where you think validation should live
- where HTTP exception translation should live
- which files you expect may need changes
- which test cases the requirement implies
- any edge cases or tradeoffs you notice

Do not implement anything yet.
