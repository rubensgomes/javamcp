# Release Plan v0.2.3

## Overview

Release version 0.2.3 with Apache 2.0 license headers added to all Python source files.

## Pre-Release Checklist

### Code Quality & Testing
- [ ] Run full test suite and verify all tests pass
- [ ] Run code coverage and ensure >= 95% coverage
- [ ] Run pylint and verify score >= 9.5/10
- [ ] Run black formatter on all Python files
- [ ] Run isort on all Python files
- [ ] Verify no type errors with mypy

### License Compliance
- [ ] Verify all 68 Python files have Apache 2.0 license headers
- [ ] Verify SPDX-License-Identifier is present in all source files
- [ ] Confirm LICENSE file exists in repository root

### Documentation
- [ ] Update CHANGELOG.md with v0.2.3 changes
- [ ] Verify README.md is up to date
- [ ] Update version number in pyproject.toml to 0.2.3

### Repository State
- [ ] Commit all license header changes
- [ ] Verify git status is clean (no uncommitted changes)
- [ ] Verify all changes are on main branch

## Release Steps

### 1. Version Update
- [ ] Update version in pyproject.toml from 0.2.2 to 0.2.3
- [ ] Update CHANGELOG.md with release date and details

### 2. Final Quality Checks
- [ ] Run: `poetry run pytest` (all tests must pass)
- [ ] Run: `poetry run python -m coverage run -m pytest` (verify coverage)
- [ ] Run: `poetry run pylint src/javamcp` (verify score)
- [ ] Run: `poetry run black --check .` (verify formatting)
- [ ] Run: `poetry run isort --check .` (verify imports)

### 3. Build & Package
- [ ] Run: `poetry build` (create distribution packages)
- [ ] Verify dist/ contains both .tar.gz and .whl files
- [ ] Check package metadata in dist files

### 4. Git Operations
- [ ] Commit version bump and CHANGELOG updates
- [ ] Create git tag: `git tag v0.2.3`
- [ ] Push commits: `git push origin main`
- [ ] Push tag: `git push origin v0.2.3`

### 5. GitHub Release
- [ ] Create GitHub release using gh CLI or web interface
- [ ] Upload distribution files (optional)
- [ ] Set release title: "v0.2.3 - License Headers"
- [ ] Add release notes from CHANGELOG.md

### 6. PyPI Publication (Optional)
- [ ] Configure PyPI credentials (if publishing)
- [ ] Run: `poetry publish` (if publishing to PyPI)
- [ ] Verify package appears on PyPI

## Post-Release

### Verification
- [ ] Verify GitHub release is visible and complete
- [ ] Verify git tag v0.2.3 exists
- [ ] Test installation from git: `pip install git+https://github.com/rubensgomes/javamcp.git@v0.2.3`
- [ ] Verify MCP server works with new version

### Communication
- [ ] Update project documentation if needed
- [ ] Close related issues (if any)
- [ ] Announce release (if applicable)

## Rollback Plan

If issues are discovered after release:
1. Do NOT delete the git tag
2. Create a new patch version (v0.2.4) with fixes
3. Document issues in CHANGELOG.md
4. Release new version following this plan

## Changelog Entry

### [0.2.3] - 2025-10-11

#### Changed
- **License Compliance**: Added Apache 2.0 license headers to all Python source files
  - Added SPDX-License-Identifier to 68 Python files
  - Ensures clear licensing and copyright information
  - Full Apache 2.0 license header in all source and test files

#### Technical
- All 249+ tests passing
- Code coverage maintained at 95%+
- Pylint score >= 9.5/10
- No breaking changes

## Release Artifacts

Expected artifacts after release:
- Git tag: `v0.2.3`
- GitHub release: `https://github.com/rubensgomes/javamcp/releases/tag/v0.2.3`
- Distribution files:
  - `javamcp-0.2.3.tar.gz`
  - `javamcp-0.2.3-py3-none-any.whl`

## Notes

- This is a maintenance release focused on license compliance
- No functional changes or new features
- No breaking changes - fully backward compatible
- Version follows semantic versioning (PATCH increment)
- Apache 2.0 license already declared in pyproject.toml
