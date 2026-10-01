# Problem 8 — Cache Invalidation

## Scenario

This service generates an AI recommendation for a user based on the user's stored interests.

To avoid repeated AI calls, recommendations are cached by `user_id`.

The application also allows a user's interests to be updated.

The current implementation has a stale-cache bug: after a profile update, the previously cached recommendation can still be returned.

## New Requirement

Update the system so that:

1. `GET /users/{user_id}/recommendation` keeps the existing cache behavior:
   - cache miss -> load profile, call AI provider, cache result, return result
   - cache hit -> return cached result without calling the repository or AI provider again

2. `PUT /users/{user_id}` updates the user's interests.

3. After a successful profile update:
   - invalidate only that user's cached recommendation
   - do not clear cached recommendations for other users

4. The next recommendation request for the updated user must:
   - load the updated profile
   - call the AI provider again
   - cache the new recommendation

5. If the profile update fails:
   - do not invalidate the existing cache entry

6. Preserve the existing API request and response shapes.

7. Do not add TTLs, distributed caching, versioning, or background refresh.

8. Add focused tests for the new behavior.

## Constraints

- Make the smallest maintainable change.
- Keep cache behavior explicit and easy to reason about.
- Do not move persistence logic into the cache.
- Do not add new frameworks or abstractions unless justified.
- Existing tests should continue to pass.

## Your Workflow

Start with:

### Step 1
Read the requirement yourself.

### Step 2
Inspect the repo manually:
- project structure
- route -> service -> repository / AI / cache flow
- where dependencies are composed
- how cache hits and misses work
- how profile updates work
- existing tests

Then tell ChatGPT:
- your understanding of the current architecture
- where you think invalidation should happen
- what object should own the invalidation operation
- which files you expect may need changes
- which test cases the requirement implies
- any edge cases/tradeoffs you notice

Do not implement anything yet.
