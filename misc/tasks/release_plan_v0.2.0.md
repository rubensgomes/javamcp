# Release Execution Plan for JavaMCP v0.2.0

## Current State Analysis
- **Current Version**: v0.1.0 (released 2025-10-06)
- **Last Tag**: v0.1.0
- **Uncommitted Changes**: Major FastMCP refactor + signal handlers
- **Test Status**: All 247 tests passing
- **Modified Files**: 11 files (568 insertions, 312 deletions)

## Major Changes Since v0.1.0
1. **FastMCP Integration** - Refactored server to properly use FastMCP framework
2. **Signal Handlers** - Added graceful shutdown for SIGINT/SIGTERM
3. **New Tests** - Added 5 signal handler tests (247 total tests)

## Release Type: MINOR (v0.1.0 → v0.2.0)
Rationale: Major architectural change (FastMCP refactor) warrants minor version bump per semantic versioning.

---

## Pre-Release Steps

### 1. Update CHANGELOG.md
- [ ] Add v0.2.0 section with release date
- [ ] Document FastMCP integration changes
- [ ] Document signal handler addition
- [ ] Document any breaking changes or migration notes

### 2. Update pyproject.toml Version
- [ ] Change version from "0.1.0" to "0.2.0"

### 3. Update Release Plan Document
- [ ] Create/update `misc/tasks/release_plan_v0.2.0.md`
- [ ] Copy checklist structure from v0.1.0 plan

### 4. Code Quality Checks
- [ ] Run pylint: `poetry run pylint javamcp`
- [ ] Run black formatter: `poetry run black src/`
- [ ] Run isort: `poetry run isort src/`
- [ ] Run mypy (if applicable): `poetry run mypy src/`

### 5. Test & Coverage
- [ ] Run full test suite: `poetry run pytest tests/ -v`
- [ ] Verify coverage: `poetry run python -m coverage run -m pytest tests/`
- [ ] Generate coverage report: `poetry run python -m coverage report -m`
- [ ] Ensure 80%+ coverage maintained

### 6. Build & Verify
- [ ] Clean previous builds: `rm -rf dist/`
- [ ] Build package: `poetry build`
- [ ] Verify dist/ contains .tar.gz and .whl files
- [ ] Check package contents: `tar -tzf dist/javamcp-0.2.0.tar.gz`

---

## Git & GitHub Steps

### 7. Commit Changes
- [ ] Stage all modified files: `git add -A`
- [ ] Commit with conventional commit message:
  ```bash
  git commit -m "feat: integrate FastMCP framework and add graceful shutdown

  - Refactor server.py to use FastMCP decorators
  - Add @mcp.tool() to all 4 tools
  - Implement ServerState for shared components
  - Add SIGINT/SIGTERM signal handlers
  - Update tests for FastMCP integration
  - All 247 tests passing

  BREAKING CHANGE: Server API changed from JavaMCPServer class to FastMCP instance"
  ```

### 8. Create Git Tag
- [ ] Tag the release: `git tag v0.2.0`
- [ ] Verify tag: `git tag -l`

### 9. Push to GitHub
- [ ] Push commits: `git push origin main`
- [ ] Push tag: `git push origin v0.2.0`

### 10. Create GitHub Release
- [ ] Run: `gh release create v0.2.0 --title "JavaMCP v0.2.0 - FastMCP Integration" --notes-file RELEASE_NOTES.md`
- [ ] Attach build artifacts (optional):
  ```bash
  gh release upload v0.2.0 dist/javamcp-0.2.0.tar.gz
  gh release upload v0.2.0 dist/javamcp-0.2.0-py3-none-any.whl
  ```

---

## Semantic Release (Optional)
If using python-semantic-release automation:
- [ ] Run: `poetry run python -m semantic_release -vvv version`
- [ ] Run: `poetry run python -m semantic_release -vvv publish`

---

## Post-Release Steps

### 11. Verification
- [ ] Verify release on GitHub: https://github.com/rubensgomes/javamcp/releases/tag/v0.2.0
- [ ] Test installation: `pip install dist/javamcp-0.2.0-py3-none-any.whl`
- [ ] Verify MCP server starts: `python -m javamcp --help`

### 12. Documentation Updates
- [ ] Update README.md if needed (migration guide)
- [ ] Update DEVSETUP.md if needed
- [ ] Create migration guide from v0.1.0 to v0.2.0

### 13. Cleanup
- [ ] Add `repositories/` to .gitignore (currently untracked)
- [ ] Add `config.yaml` to .gitignore if needed
- [ ] Clean up temporary files

---

## Release Notes Template (RELEASE_NOTES.md)

```markdown
# JavaMCP v0.2.0 - FastMCP Integration

## 🚀 Major Changes

### FastMCP Framework Integration
The server has been completely refactored to properly use the FastMCP framework:
- Created `mcp = FastMCP("JavaMCP")` instance
- All 4 tools now use `@mcp.tool()` decorator
- Simplified server startup with `mcp.run()`
- Implemented shared state management via `ServerState` class

### Graceful Shutdown
Added proper signal handling for clean shutdowns:
- SIGINT (Ctrl+C) and SIGTERM handlers
- Clears API indexer on shutdown
- Logs shutdown events properly

## ⚠️ Breaking Changes

**Server API Changed**: The `JavaMCPServer` class has been replaced with a FastMCP-based implementation.

**Migration Guide**:
- Old: `from javamcp import JavaMCPServer, create_server`
- New: `from javamcp import mcp, initialize_server, get_state`

Original tool functions remain in `src/javamcp/tools/` for backward compatibility and testing.

## ✅ Quality Metrics
- **Tests**: 247 passing (5 new signal handler tests)
- **Coverage**: 95%+ maintained
- **Code Quality**: pylint 10.00/10

## 📦 Installation
```bash
pip install javamcp==0.2.0
```

## 🔗 Links
- [Full Changelog](https://github.com/rubensgomes/javamcp/blob/main/CHANGELOG.md#020)
- [Documentation](https://github.com/rubensgomes/javamcp)
```

---

## Rollback Plan
If issues arise:
1. Delete GitHub release: `gh release delete v0.2.0`
2. Delete git tag locally: `git tag -d v0.2.0`
3. Delete remote tag: `git push origin :refs/tags/v0.2.0`
4. Revert commit: `git revert HEAD`
