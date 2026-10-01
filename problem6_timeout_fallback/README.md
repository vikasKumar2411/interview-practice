# Problem 6 — Timeout + Fallback

## Scenario

This service generates a short product description using a primary AI provider.

The current implementation works when the primary provider succeeds, but the product team now wants a resilience policy for slow provider responses.

## New Requirement

Update the system so that:

1. The primary AI provider gets **one attempt only**.
2. The primary provider call must have a timeout of **0.2 seconds**.
3. If the primary provider **times out**, call the fallback provider.
4. The fallback provider should also get **one attempt only**.
5. Do **not** apply an additional timeout to the fallback provider.
6. If the fallback succeeds, return its result normally.
7. If the fallback fails with any exception, let that fallback exception propagate unchanged.
8. If the primary provider fails with a **non-timeout exception**, do **not** call the fallback; propagate the original exception unchanged.
9. Preserve the existing API contract and response shape.
10. Add focused tests for the new behavior.

## Constraints

- Make the smallest maintainable change.
- Do not add retries.
- Do not change the provider classes unless necessary.
- Do not add new frameworks or abstractions unless the requirement justifies them.
- Existing tests should continue to pass.

## Your Workflow

Start with:

### Step 1
Read the requirement yourself.

### Step 2
Inspect the repo manually:
- project structure
- route → service → provider call flow
- dependency construction
- existing tests

Then tell ChatGPT:
- your understanding of the current architecture
- where you think the new behavior belongs
- what files you expect may need changes
- any edge cases/tradeoffs you notice

Do not implement anything yet.
