# Release Plan for JavaMCP v0.1.0

## Pre-Release Checklist
- [ ] Fix all pylint errors in `src/javamcp`
- [ ] Run full test suite and ensure all tests pass
- [ ] Verify code coverage is above 80%
- [ ] Run code quality tools (black, isort, mypy)
- [ ] Update version from 0.0.1 to 0.1.0 in `pyproject.toml`

## Documentation
- [ ] Create `CHANGELOG.md` with release notes for v0.1.0
- [ ] Review and update README.md if needed
- [ ] Verify all configuration examples are current

## Build & Test
- [ ] Build the package with `poetry build`
- [ ] Test the built package locally
- [ ] Verify package metadata and dependencies

## Git & GitHub
- [ ] Commit all changes with descriptive message
- [ ] Create git tag `v0.1.0`
- [ ] Push commits and tags to GitHub
- [ ] Create GitHub release with release notes

## Post-Release
- [ ] Test installation from built package
- [ ] Update README with installation instructions
- [ ] Announce release (if applicable)
