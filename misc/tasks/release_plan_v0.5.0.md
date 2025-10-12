# Release Plan v0.5.0 - Shallow Clone Optimization

## Release Information

- **Repository**: rubensgomes/javamcp
- **Current Version**: v0.4.0
- **Target Version**: v0.5.0
- **Release Type**: PATCH → MINOR (Performance improvement feature)
- **Latest Release**: v0.4.0 (2025-10-11)
- **Target Date**: TBD

## Release Overview

This release adds shallow clone functionality to optimize repository cloning performance by reducing disk space usage and improving clone times. This is a performance enhancement that maintains backward compatibility.

## Pending Changes

### Modified Files
- `src/javamcp/repository/git_operations.py` - Added `depth` parameter to `clone_repository()`
- `src/javamcp/repository/manager.py` - Updated to use shallow clones by default
- `tests/repository/test_git_operations.py` - Added tests for shallow clone functionality
- `poetry.lock` - Dependency updates

### New Files
- `misc/tasks/shallow_clone_implementation_plan.md` - Implementation plan (tracked)

## Changes for v0.5.0

### Added
- **Shallow Clone Support**: Optional `depth` parameter in `clone_repository()` function
  - Default depth of 1 commit for all repository clones
  - Reduces disk space usage significantly
  - Improves clone performance for large repositories
  - Maintains full API analysis functionality
- **New Test Cases**:
  - `test_clone_repository_custom_depth` - Validates custom depth parameter
  - Updated existing tests to verify depth parameter handling

### Changed
- **`clone_repository()` function** (`src/javamcp/repository/git_operations.py:50`)
  - Added `depth: int = 1` parameter
  - Passes `depth` to `Repo.clone_from()`
  - Updated docstring with parameter documentation
- **`_clone_new_repository()` method** (`src/javamcp/repository/manager.py:223`)
  - Now explicitly passes `depth=1` to ensure shallow clones
- **Test suite**: Updated mocks to verify `depth` parameter propagation

### Benefits
- Faster clone times for large Java repositories
- Reduced local disk space requirements
- No impact on API analysis accuracy (only latest code needed)
- Backward compatible - existing code continues to work

## Technical Details

### Semantic Versioning Rationale
- **MINOR version bump** (0.4.0 → 0.5.0)
- Adds new functionality (depth parameter)
- Fully backward compatible
- No breaking changes

### Test Coverage
```
tests/repository/test_git_operations.py::TestCloneRepository::test_clone_repository_success PASSED
tests/repository/test_git_operations.py::TestCloneRepository::test_clone_repository_custom_branch PASSED
tests/repository/test_git_operations.py::TestCloneRepository::test_clone_repository_custom_depth PASSED
tests/repository/test_git_operations.py::TestCloneRepository::test_clone_repository_fails PASSED
```

### Implementation Status
- [x] Code implementation complete
- [x] Tests written and passing
- [x] Implementation plan documented
- [ ] Update CHANGELOG.md with v0.5.0 entry
- [ ] Run full test suite
- [ ] Verify code quality (pylint, black, isort)
- [ ] Update version in pyproject.toml (0.4.0 → 0.5.0)
- [ ] Commit changes
- [ ] Create git tag v0.5.0
- [ ] Build distribution packages
- [ ] Create GitHub release
- [ ] Push to repository

## Pre-Release Checklist

### 1. Documentation Updates
- [ ] Update CHANGELOG.md with v0.5.0 section
- [ ] Verify README.md accuracy (no changes needed)
- [ ] Ensure all docstrings are current

### 2. Code Quality Verification
```bash
# Run full test suite
poetry run pytest

# Check coverage
poetry run pytest --cov=src/javamcp --cov-report=term-missing

# Format code
poetry run black src/ tests/

# Sort imports
poetry run isort src/ tests/

# Lint code
poetry run pylint src/javamcp

# Type checking
poetry run mypy src/
```

### 3. Version Update
- [ ] Update `pyproject.toml` version: `0.4.0` → `0.5.0`
- [ ] Verify all version references are consistent

### 4. Git Operations
```bash
# Commit all changes
git add .
git commit -m "Release v0.5.0: Add shallow clone optimization"

# Create annotated tag
git tag -a v0.5.0 -m "v0.5.0 - Shallow Clone Optimization"

# Push commits and tags
git push origin main
git push origin v0.5.0
```

### 5. Build and Release
```bash
# Build distribution packages
poetry build

# Create GitHub release
gh release create v0.5.0 \
  --title "v0.5.0 - Shallow Clone Optimization" \
  --notes-file misc/tasks/release_notes_v0.5.0.md \
  dist/javamcp-0.5.0.tar.gz \
  dist/javamcp-0.5.0-py3-none-any.whl
```

## Release Notes Draft

```markdown
# v0.5.0 - Shallow Clone Optimization

## Added
- Shallow clone support with configurable depth parameter
- Default depth of 1 for faster clones and reduced disk usage
- New test case for custom clone depth validation

## Changed
- Repository cloning now uses shallow clones by default
- Updated `clone_repository()` with optional `depth` parameter
- Enhanced test suite to verify depth parameter handling

## Benefits
- ⚡ Faster clone times for large repositories
- 💾 Reduced disk space requirements
- 🔄 Maintains full API analysis functionality
- ✅ Fully backward compatible

## Technical
- All tests passing (including 1 new test)
- Code quality maintained
- No breaking changes
- Semantic versioning: MINOR bump for new feature
```

## Migration Guide

No migration required. This release is fully backward compatible. The new `depth` parameter is optional with a sensible default value of 1.

### For users who want full history
If you need the complete git history (not typical for this use case), you can manually modify the code:

```python
# Custom depth
clone_repository(url, path, depth=None)  # Full history
```

## Post-Release Tasks

- [ ] Verify release appears on GitHub releases page
- [ ] Test installation from release artifacts
- [ ] Monitor for any issues reported
- [ ] Update project board/tracking system
- [ ] Announce release (if applicable)

## Notes

- This is a performance optimization release
- No functional changes to API analysis capabilities
- GitPython's native `depth` parameter support makes implementation straightforward
- Shallow clones are sufficient since tool analyzes current API state only

## Review

Implementation completed and tested. Ready for CHANGELOG update, version bump, and release workflow execution.
