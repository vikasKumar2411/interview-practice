# Problem 9 — Transactional Consistency

## Scenario

This service creates an order and also records an audit event.

The current implementation performs the two persistence operations separately:

1. create the order
2. create the audit event

If the second write fails, the order remains persisted without its required audit record.

That leaves the system in a partially committed state.

## New Requirement

Update the system so that:

1. Creating an order and creating its audit event are one atomic operation.
2. On success:
   - the order is persisted
   - the audit event is persisted
   - the API returns the created order
3. If order persistence fails:
   - no audit event is created
   - the original exception propagates unchanged
4. If audit persistence fails:
   - the order write must be rolled back
   - no partial state may remain
   - the original audit exception propagates unchanged
5. Preserve the existing request and response shapes.
6. Do not add retries.
7. Do not add background compensation.
8. Do not swallow or translate repository exceptions.
9. Add focused tests for atomic success and rollback behavior.

## Constraints

- Make the smallest maintainable change.
- Keep transaction semantics explicit.
- The service should coordinate the business operation.
- The repository/persistence layer should own transaction mechanics.
- Do not introduce a database framework; use the existing in-memory repository abstraction.
- Existing tests should continue to pass.

## Your Workflow

Start with:

### Step 1
Read the requirement yourself.

### Step 2
Inspect the repo manually:
- project structure
- route -> service -> repository flow
- order creation path
- audit write path
- where shared persistence state lives
- existing tests

Then tell ChatGPT:
- your understanding of the current architecture
- exactly how partial state can occur
- where you think the transaction boundary belongs
- what layer should own rollback mechanics
- which files you expect may need changes
- which test cases the requirement implies
- any tradeoffs or edge cases you notice

Do not implement anything yet.
