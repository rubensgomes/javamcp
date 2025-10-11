# Release Plan v0.3.0

## Overview

Release version 0.3.0 with new MCP resource for comprehensive project context access.

**Version Type**: MINOR (backward-compatible new feature)

**Key Changes**:
- New MCP resource: `javamcp://project/{repository_name}/context`
- New `ProjectContextBuilder` component (346 lines)
- Comprehensive test coverage (324 test lines)
- Enhanced README documentation
- New protocol model `ProjectContextResponse`

## Pre-Release Checklist

### Code Quality & Testing
- [ ] Run full test suite and verify all tests pass
- [ ] Run code coverage and ensure >= 95% coverage
- [ ] Run pylint and verify score >= 9.5/10
- [ ] Run black formatter on all Python files
- [ ] Run isort on all Python files
- [ ] Verify no type errors with mypy

### Documentation
- [ ] Update CHANGELOG.md with v0.3.0 changes
- [ ] Verify README.md is up to date
- [ ] Update version number in pyproject.toml to 0.3.0
- [ ] Review all docstrings in new modules

### Repository State
- [ ] Commit all changes with descriptive message
- [ ] Verify git status is clean (no uncommitted changes)
- [ ] Verify all changes are on main branch
- [ ] Verify no merge conflicts

## Release Steps

### 1. Version Update
- [ ] Update version in pyproject.toml from 0.2.3 to 0.3.0
- [ ] Update CHANGELOG.md with release date and details
- [ ] Commit version updates

### 2. Final Quality Checks
- [ ] Run: `poetry run pytest` (all tests must pass)
- [ ] Run: `poetry run python -m coverage run -m pytest` (verify coverage)
- [ ] Run: `poetry run pylint src/javamcp` (verify score >= 9.5/10)
- [ ] Run: `poetry run black .` (apply formatting)
- [ ] Run: `poetry run isort .` (apply import sorting)

### 3. Build & Package
- [ ] Clean dist directory: `rm -rf dist/`
- [ ] Run: `poetry build` (create distribution packages)
- [ ] Verify dist/ contains both .tar.gz and .whl files
- [ ] Check package metadata in dist files

### 4. Git Operations
- [ ] Create git tag: `git tag v0.3.0`
- [ ] Push commits: `git push origin main`
- [ ] Push tag: `git push origin v0.3.0`

### 5. GitHub Release
- [ ] Create GitHub release using gh CLI or web interface
- [ ] Upload distribution files
- [ ] Set release title: "v0.3.0 - Project Context Resource"
- [ ] Add release notes from CHANGELOG.md

### 6. PyPI Publication (Optional)
- [ ] Configure PyPI credentials (if publishing)
- [ ] Run: `poetry publish` (if publishing to PyPI)
- [ ] Verify package appears on PyPI

## Post-Release

### Verification
- [ ] Verify GitHub release is visible and complete
- [ ] Verify git tag v0.3.0 exists
- [ ] Test installation from git: `pip install git+https://github.com/rubensgomes/javamcp.git@v0.3.0`
- [ ] Verify MCP server works with new resource
- [ ] Test new project context resource functionality

### Communication
- [ ] Update project documentation if needed
- [ ] Close related issues (if any)
- [ ] Announce release (if applicable)

## Rollback Plan

If issues are discovered after release:
1. Do NOT delete the git tag
2. Create a new patch version (v0.3.1) with fixes
3. Document issues in CHANGELOG.md
4. Release new version following this plan

## Changelog Entry

### [0.3.0] - 2025-10-11

#### Added
- **New MCP Resource**: `javamcp://project/{repository_name}/context`
  - Access comprehensive project context for Java API repositories
  - Provides repository information, README content, llms.txt content
  - Includes API statistics (classes, methods, packages)
  - Package-level summaries with class and method counts
  - Top classes with Javadoc documentation
  - Documentation coverage metrics for classes and methods
- **ProjectContextBuilder Component**: New module for building rich project context
  - Aggregates information from README, llms.txt, Javadocs
  - Generates API statistics and package summaries
  - Calculates documentation coverage metrics
  - 346 lines of production code
- **ProjectContextResponse Model**: New protocol model for resource responses
- **Enhanced Repository Manager**: Added `get_repository_by_name()` method
- **Comprehensive Test Suite**: 324 lines of tests for new functionality

#### Changed
- Updated README.md with MCP Resources section and examples
- Enhanced server.py with resource registration
- Updated MCP protocol models

#### Technical
- All tests passing (expected ~260+ tests with new additions)
- Code coverage maintained at 95%+
- Pylint score maintained >= 9.5/10
- No breaking changes - fully backward compatible
- Follows semantic versioning (MINOR increment for new feature)

## Release Artifacts

Expected artifacts after release:
- Git tag: `v0.3.0`
- GitHub release: `https://github.com/rubensgomes/javamcp/releases/tag/v0.3.0`
- Distribution files:
  - `javamcp-0.3.0.tar.gz`
  - `javamcp-0.3.0-py3-none-any.whl`

## Manual Steps for GitHub Release

### Option A: Using gh CLI

```bash
# After all tests pass and build completes:
git tag v0.3.0
git push origin main
git push origin v0.3.0

gh release create v0.3.0 \
  --title "v0.3.0 - Project Context Resource" \
  --notes "$(cat <<'EOF'
## What's New in v0.3.0

This release adds a new MCP resource for accessing comprehensive project context about indexed Java API repositories.

### Added
- **New MCP Resource**: `javamcp://project/{repository_name}/context`
  - Access comprehensive contextual information about Java API projects
  - Provides repository metadata, README content, and llms.txt content
  - Includes detailed API statistics (total classes, methods, packages, averages)
  - Package-level summaries with class and method counts
  - Top classes with their Javadoc documentation
  - Documentation coverage metrics for both classes and methods

- **ProjectContextBuilder Component**: New module for building rich project documentation
  - Aggregates information from multiple sources (README, llms.txt, Javadocs)
  - Generates comprehensive API statistics and package summaries
  - Calculates Javadoc coverage rates
  - 346 lines of well-tested production code

- **Enhanced Repository Manager**: Added `get_repository_by_name()` for easier repository lookups

- **Comprehensive Test Suite**: 324 lines of tests ensuring reliability

### Changed
- Updated README.md with comprehensive MCP Resources documentation and examples
- Enhanced server.py with resource registration
- Updated MCP protocol models with `ProjectContextResponse`

### Technical Details
- All tests passing with expanded test suite
- Code coverage maintained at 95%+
- Pylint score maintained >= 9.5/10
- No breaking changes - fully backward compatible
- Follows semantic versioning (MINOR version bump for new feature)

### Example Usage

After indexing a repository like `https://github.com/apache/commons-lang.git`, access its context:

```
javamcp://project/commons-lang/context
```

The response includes repository info, README content, API statistics, package summaries, top classes with Javadocs, and documentation coverage metrics.

**Full Changelog**: https://github.com/rubensgomes/javamcp/compare/v0.2.3...v0.3.0
EOF
)" \
  dist/javamcp-0.3.0-py3-none-any.whl \
  dist/javamcp-0.3.0.tar.gz
```

### Option B: Using GitHub Web Interface

1. Go to https://github.com/rubensgomes/javamcp/releases/new
2. Select tag: v0.3.0
3. Release title: "v0.3.0 - Project Context Resource"
4. Copy release notes from the CHANGELOG.md section [0.3.0]
5. Upload distribution files:
   - dist/javamcp-0.3.0-py3-none-any.whl
   - dist/javamcp-0.3.0.tar.gz
6. Click "Publish release"

### Verification After Release

```bash
# Verify release exists
gh release view v0.3.0

# Test installation
pip install git+https://github.com/rubensgomes/javamcp.git@v0.3.0

# Test the MCP server with new resource
# (Follow project's test procedures)
```

## Notes

- This is a MINOR version release adding new functionality
- New MCP resource provides comprehensive project context
- Over 670 lines of new code (production + tests)
- No breaking changes - fully backward compatible
- Version follows semantic versioning (MINOR increment)
- All existing tools continue to work as before
- New resource integrates seamlessly with existing architecture

## New Feature Highlights

### ProjectContextBuilder Class

The new `ProjectContextBuilder` provides:
- **Repository Information**: Name and URL extraction
- **README Content**: Automatic detection and extraction
- **LLMs.txt Support**: Context file for LLM integration
- **API Statistics**: Comprehensive metrics calculation
- **Package Summaries**: Detailed per-package information
- **Top Classes**: Most significant classes with documentation
- **Coverage Metrics**: Javadoc documentation coverage rates

### Resource URI Pattern

```
javamcp://project/{repository_name}/context
```

Where `repository_name` is extracted from the Git URL (e.g., "commons-lang" for "https://github.com/apache/commons-lang.git").

### Response Structure

The resource returns a JSON response with:
- `repository_name`: Repository identifier
- `repository_url`: Full Git URL
- `description`: Generated project overview
- `readme_content`: Full README.md content (if available)
- `llms_txt_content`: LLM context file content (if available)
- `statistics`: Total classes, methods, packages, averages
- `packages`: Array of package summaries with counts
- `top_classes`: Most significant classes with Javadocs
- `javadoc_coverage`: Documentation coverage metrics

## Risk Assessment

**Low Risk Release**:
- Additive changes only (no modifications to existing functionality)
- Comprehensive test coverage for new features
- No changes to existing tool interfaces
- No dependency updates
- All existing features remain unchanged

## Success Criteria

Release is successful when:
- [ ] All tests pass (expected ~260+ tests)
- [ ] Code coverage >= 95%
- [ ] Pylint score >= 9.5/10
- [ ] GitHub release created with artifacts
- [ ] Git tag v0.3.0 exists on GitHub
- [ ] Installation from git works correctly
- [ ] New project context resource is functional
- [ ] Existing tools continue to work as before
