#### Requirement
Inspect the repository and explain the current architecture and behavior.

Please identify:

1. The code flow from the FastAPI application entrypoint through the `/descriptions` endpoint to the DescriptionService and PrimaryAIProvider & FallbackAIProvider.
2. The major classes/functions and their responsibilities.
3. The code layers and how they interact.
4. The provider calls, timeout and non-timeout execeptions around provider calls and retries.
5. The existing tests and what behavior each test currently covers.

For each point, reference the relevant file and class/function.

#### Constraints
- Do not modify any files.
- Do not propose implementation changes yet.
- Focus only on the current state of the repository.