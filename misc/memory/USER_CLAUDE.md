# Understanding of CLAUDE.md and CLAUDE_PYTHON.md

**Source Files:**
- `/home/rubens/.claude/CLAUDE.md`
- `/home/rubens/.claude/CLAUDE_PYTHON.md`

## Core Workflow Requirements

1. **Planning First**: Always create implementation plans before coding
2. **User Approval**: Get approval on plans before implementing
3. **Task Tracking**: Store plans in `misc/tasks/` using checkbox format (- [ ] syntax)
4. **Incremental Work**: Check off tasks as completed, work step-by-step
5. **Communication**: High-level summaries only, add Review section when wrapping up
6. **File Creation**: NEVER create files unless absolutely necessary, ALWAYS prefer editing existing files

## Coding Standards

**General Principles:**
- Clarity over cleverness
- SOLID & Clean Code principles
- Functions: <20 lines ideal, max 60 lines
- Descriptive names (no abbreviations)
- Document all public code
- No globals or static state
- Never swallow exceptions
- Early returns over deep nesting
- Named constants instead of magic numbers
- Immutability and pure functions preferred
- DRY principle
- Meaningful logging with context

## Python-Specific Requirements

**Formatting & Style:**
- Use Black for auto-formatting
- Follow PEP8 standards
- Run `poetry run flake8 src/ tests/` for linting

**Code Organization:**
- Poetry standard layout (src/, tests/)
- Feature-based organization
- Avoid large monolithic modules

**Best Practices:**
- Type hints everywhere
- Pydantic models for DTOs
- async/await for I/O operations
- Raise meaningful exceptions (not None)
- f-strings for formatting
- `is`/`is not` for None checks
- `with` for file operations
- `pathlib` instead of `os.path`
- No wildcard imports
- `enumerate()` over `range(len())`

**Testing Requirements:**
- pytest framework
- Mirror src/ structure in tests/
- pytest fixtures for setup/teardown
- pytest-cov for coverage (80%+ target)
- Mock only external dependencies (DB, APIs)
- pytest-mock for mocking
- Test behavior, not implementation
- @pytest.mark.parametrize for multiple inputs
- Small, focused, fast tests
- Test success and failure scenarios
- Clear test names
- Test edge cases and error handling

## Critical Constraints

- NEVER create files unless absolutely necessary
- ALWAYS prefer editing existing files
- NEVER proactively create documentation files
- Do only what's asked, nothing more
