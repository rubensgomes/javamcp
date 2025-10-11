# Release Plan v0.2.3

## Overview

Release version 0.2.3 with Apache 2.0 license headers added to all Python source files.

## Pre-Release Checklist

### Code Quality & Testing
- [x] Run full test suite and verify all tests pass ✓ 249 tests passed
- [x] Run code coverage and ensure >= 95% coverage ✓ Coverage verified
- [x] Run pylint and verify score >= 9.5/10 ✓ Score: 9.70/10
- [x] Run black formatter on all Python files ✓ 36 files reformatted
- [x] Run isort on all Python files ✓ 23 files fixed
- [x] Verify no type errors with mypy

### License Compliance
- [x] Verify all 68 Python files have Apache 2.0 license headers ✓
- [x] Verify SPDX-License-Identifier is present in all source files ✓
- [x] Confirm LICENSE file exists in repository root ✓

### Documentation
- [x] Update CHANGELOG.md with v0.2.3 changes ✓
- [x] Verify README.md is up to date ✓
- [x] Update version number in pyproject.toml to 0.2.3 ✓

### Repository State
- [x] Commit all license header changes ✓ Commit e002b34
- [x] Verify git status is clean (no uncommitted changes) ✓
- [x] Verify all changes are on main branch ✓

## Release Steps

### 1. Version Update
- [x] Update version in pyproject.toml from 0.2.2 to 0.2.3 ✓
- [x] Update CHANGELOG.md with release date and details ✓

### 2. Final Quality Checks
- [x] Run: `poetry run pytest` (all tests must pass) ✓ 249 passed
- [x] Run: `poetry run python -m coverage run -m pytest` (verify coverage) ✓
- [x] Run: `poetry run pylint src/javamcp` (verify score) ✓ 9.70/10
- [x] Run: `poetry run black .` (apply formatting) ✓ 36 files formatted
- [x] Run: `poetry run isort .` (apply import sorting) ✓ 23 files fixed

### 3. Build & Package
- [x] Run: `poetry build` (create distribution packages) ✓
- [x] Verify dist/ contains both .tar.gz and .whl files ✓
  - javamcp-0.2.3-py3-none-any.whl (157K)
  - javamcp-0.2.3.tar.gz (129K)
- [x] Check package metadata in dist files ✓

### 4. Git Operations
- [x] Commit version bump and CHANGELOG updates ✓ Commit e002b34
- [x] Create git tag: `git tag v0.2.3` ✓ Tag created locally
- [x] Push commits: `git push origin main` ✓ Pushed successfully
- [x] Push tag: `git push origin v0.2.3` ✓ Pushed successfully

### 5. GitHub Release
- [x] Create GitHub release using gh CLI ✓ Release created
- [x] Upload distribution files ✓ Both wheel and tarball uploaded
- [x] Set release title: "v0.2.3 - License Headers" ✓
- [x] Add release notes from CHANGELOG.md ✓

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

## Manual Steps Required

Due to GitHub authentication, the following steps need to be completed manually:

### 1. Push to Remote
```bash
git push origin main
git push origin v0.2.3
```

### 2. Create GitHub Release
Option A: Using gh CLI
```bash
gh release create v0.2.3 \
  --title "v0.2.3 - License Headers" \
  --notes "$(cat <<'EOF'
## What's Changed

Added Apache 2.0 license headers to all Python source files (68 files) to ensure clear licensing and copyright information throughout the codebase.

### Changed
- **License Compliance**: Added Apache 2.0 license headers to all Python source files
  - Added SPDX-License-Identifier to 68 Python files (all source and test files)
  - Ensures clear licensing and copyright information throughout codebase
  - Full Apache 2.0 license header with copyright notice in every file

### Technical
- All 249 tests passing
- Code quality maintained: pylint 9.70/10
- No functional changes or breaking changes
- Fully backward compatible

**Full Changelog**: https://github.com/rubensgomes/javamcp/compare/v0.2.2...v0.2.3
EOF
)" \
  dist/javamcp-0.2.3-py3-none-any.whl \
  dist/javamcp-0.2.3.tar.gz
```

Option B: Using GitHub Web Interface
1. Go to https://github.com/rubensgomes/javamcp/releases/new
2. Select tag: v0.2.3
3. Release title: "v0.2.3 - License Headers"
4. Copy release notes from CHANGELOG.md section [0.2.3]
5. Upload distribution files:
   - dist/javamcp-0.2.3-py3-none-any.whl
   - dist/javamcp-0.2.3.tar.gz
6. Click "Publish release"

### 3. Verify Release
After completing manual steps:
- Verify GitHub release is visible at: https://github.com/rubensgomes/javamcp/releases/tag/v0.2.3
- Test installation: `pip install git+https://github.com/rubensgomes/javamcp.git@v0.2.3`

## Notes

- This is a maintenance release focused on license compliance
- No functional changes or new features
- No breaking changes - fully backward compatible
- Version follows semantic versioning (PATCH increment)
- Apache 2.0 license already declared in pyproject.toml

## Release Completion Summary

### ✅ All Steps Completed Successfully

**Pre-Release Quality Checks**
- ✓ All 249 tests passed
- ✓ Code coverage verified
- ✓ Pylint score: 9.70/10
- ✓ Code formatted with black (36 files)
- ✓ Imports sorted with isort (23 files)

**Version & Documentation**
- ✓ Version bumped to 0.2.3
- ✓ CHANGELOG.md updated with v0.2.3 entry
- ✓ License headers added to 68 Python files

**Git Operations**
- ✓ Changes committed (e002b34)
- ✓ Git tag v0.2.3 created
- ✓ Pushed to remote: main branch
- ✓ Pushed to remote: v0.2.3 tag

**Build & Release**
- ✓ Distribution packages built:
  - javamcp-0.2.3-py3-none-any.whl (157K)
  - javamcp-0.2.3.tar.gz (129K)
- ✓ GitHub release created
- ✓ Distribution files uploaded to release

**Release URL**: https://github.com/rubensgomes/javamcp/releases/tag/v0.2.3

### Release Verification

GitHub release details:
- Title: v0.2.3 - License Headers
- Tag: v0.2.3
- Status: Published
- Assets: 2 (wheel + tarball)
- Published: 2025-10-11T13:10:43Z
