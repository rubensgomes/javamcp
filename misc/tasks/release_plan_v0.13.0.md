# Release Plan: JavaMCP v0.13.0

**Repository:** javamcp
**Current Version:** 0.12.0
**Target Version:** 0.13.0
**Release Type:** Minor (new features, backward compatible)
**Date Created:** 2026-01-14

---

## Summary of Changes

This release includes enhanced CLI help documentation, dependency updates, and code quality improvements.

### New Features
- **Enhanced CLI Help System** - Comprehensive `--help` output with:
  - Detailed configuration file documentation in epilog
  - Full list of configuration properties and their descriptions
  - Usage examples for common operations
  - MCP tools and resources overview in main description

### Changes
- **Documentation Updates**
  - README.md: Updated Python version requirement to 3.14+
  - README.md: Added sections for displaying version and help commands
  - README.md: Fixed logging output option from "console" to "stderr"
  - DEVSETUP.md: Minor formatting improvements

- **Dependency Updates** (via poetry.lock)
  - anyio: 4.12.0 → 4.12.1
  - certifi: 2025.11.12 → 2026.1.4
  - cyclopts: 4.4.3 → 4.4.5
  - Various other transitive dependency updates

- **Code Quality Improvements**
  - Import formatting cleanup across multiple modules
  - Consistent import grouping with parentheses
  - Minor parser and AST visitor cleanups

### Technical
- All 287 tests passing
- Pylint score: 9.75/10
- Black formatting: ✓ (all files compliant)
- Import sorting needs minor fixes before release

---

## Pre-Release Checklist

### 1. Code Quality
- [ ] Fix isort import ordering issues in test files
- [ ] Run full test suite and verify all tests pass
- [ ] Run pylint and verify score ≥ 9.70/10
- [ ] Run black formatter check
- [ ] Run mypy type checking

### 2. Version Bump
- [ ] Update version in `pyproject.toml` from 0.12.0 to 0.13.0

### 3. Documentation
- [ ] Update CHANGELOG.md with v0.13.0 release notes
- [ ] Verify README.md is accurate and up-to-date
- [ ] Review CLAUDE.md for any needed updates

### 4. Git Operations
- [ ] Stage all changes
- [ ] Create release commit with message: `feat: release v0.13.0 with enhanced CLI help`
- [ ] Create git tag: `v0.13.0`
- [ ] Push commit and tag to origin

### 5. Post-Release
- [ ] Verify GitHub release page
- [ ] Update release plan checkboxes to mark completed

---

## Detailed Steps

### Step 1: Fix Import Sorting
```bash
poetry run isort src/ tests/
```

Files that need fixing:
- tests/logging/test_logger.py
- tests/models/test_mcp_protocol.py
- tests/models/test_java_entities.py
- tests/config/test_schema.py
- tests/indexer/test_query_engine.py

### Step 2: Run Code Quality Checks
```bash
poetry run pytest
poetry run black --check src/ tests/
poetry run isort --check-only src/ tests/
poetry run pylint --ignore-paths='^.*/antlr4/.*' "src/javamcp"
poetry run mypy "src/javamcp"
```

### Step 3: Update Version
Edit `pyproject.toml`:
```toml
version = "0.13.0"
```

### Step 4: Update CHANGELOG.md
Add new section at top of changelog for v0.13.0.

### Step 5: Commit and Tag
```bash
git add .
git commit -m "feat: release v0.13.0 with enhanced CLI help"
git tag v0.13.0
git push origin main --tags
```

---

## CHANGELOG Entry (Draft)

```markdown
## [0.13.0] - 2026-01-14

### Added
- **Enhanced CLI Help Documentation**
  - Comprehensive `--help` output with detailed epilog
  - Full configuration file property documentation
  - Usage examples for common operations
  - MCP tools and resources overview in description
  - `get_help_epilog()` function for generating help text

### Changed
- **README.md Updates**
  - Python version requirement updated to 3.14+
  - Added "Displaying the version" section with example commands
  - Added "Displaying the help" section with example commands
  - Fixed logging output option from "console" to "stderr"

- **Dependency Updates**
  - anyio: 4.12.0 → 4.12.1
  - certifi: 2025.11.12 → 2026.1.4
  - cyclopts: 4.4.3 → 4.4.5
  - Various transitive dependency updates

- **Code Formatting**
  - Import statement formatting cleanup across modules
  - Consistent multi-line import grouping

### Technical
- All 287 tests passing
- Pylint score: 9.75/10
- Backward compatible - no breaking changes
```

---

## Rollback Plan

If issues are discovered after release:

1. Delete the git tag locally and remotely:
   ```bash
   git tag -d v0.13.0
   git push origin :refs/tags/v0.13.0
   ```

2. Revert the release commit:
   ```bash
   git revert HEAD
   git push origin main
   ```

3. Investigate and fix issues before re-releasing.

---

## Approval

**Status:** Pending Approval

Please review this release plan and confirm to proceed with the release.
