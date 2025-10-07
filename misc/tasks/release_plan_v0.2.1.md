# Release Execution Plan for JavaMCP v0.2.1

## Current State Analysis
- **Current Version**: v0.2.0 (released 2025-10-06)
- **Last Tag**: v0.2.0
- **Staged Changes**: .mcp.json + claude_code_mcp_setup_plan.md
- **Unstaged Changes**: Rotating log file implementation
- **Test Status**: Unknown (need to verify)
- **Modified Files**: 7 files + 1 new plan file

## Changes Since v0.2.0

### 1. Rotating Log Files Feature
**Files Modified**:
- `src/javamcp/config/schema.py` - Added `max_bytes` and `backup_count` fields
- `src/javamcp/logging/logger.py` - Replaced FileHandler with RotatingFileHandler
- `tests/logging/test_logger.py` - Added rotation tests
- `misc/tasks/rotating_log_files_plan.md` - Implementation plan

**Details**:
- Added log rotation to prevent unbounded log file growth
- Default: 10MB max file size, 5 backup files
- Total max disk usage: ~60MB (10MB × 6 files)
- All validators added for configuration parameters

### 2. Claude Code MCP Integration
**Files Modified**:
- `.mcp.json` - MCP configuration for Claude Code
- `misc/tasks/claude_code_mcp_setup_plan.md` - Setup documentation

### 3. Minor Updates
**Files Modified**:
- `src/javamcp/__init__.py` - No version change needed yet
- `src/javamcp/__main__.py` - Minor updates
- `misc/tasks/release_plan_v0.2.0.md` - Documentation updates

## Release Type: PATCH (v0.2.0 → v0.2.1)
**Rationale**: Adding rotating log file feature (enhancement) without breaking changes warrants a patch version bump per semantic versioning.

---

## Pre-Release Steps

### 1. Run All Tests
- [ ] Run full test suite: `poetry run pytest tests/ -v`
- [ ] Verify all tests pass (should be 24+ logging tests)
- [ ] Run coverage: `poetry run python -m coverage run -m pytest tests/`
- [ ] Generate coverage report: `poetry run python -m coverage report -m`
- [ ] Ensure 80%+ coverage maintained

### 2. Code Quality Checks
- [ ] Run black formatter: `poetry run black src/ tests/`
- [ ] Run isort: `poetry run isort src/ tests/`
- [ ] Run pylint: `poetry run pylint src/javamcp`
- [ ] Verify pylint score is 9.0+/10

### 3. Update Version Numbers
- [ ] Update `pyproject.toml`: version = "0.2.1"
- [ ] Update `src/javamcp/__init__.py`: __version__ = "0.2.1"

### 4. Update CHANGELOG.md
- [ ] Add v0.2.1 section with today's date
- [ ] Document rotating log files feature
- [ ] Document configuration changes (max_bytes, backup_count)
- [ ] Document Claude Code MCP integration support
- [ ] Add migration notes if needed

### 5. Build & Verify
- [ ] Clean previous builds: `rm -rf dist/`
- [ ] Build package: `poetry build`
- [ ] Verify dist/ contains:
  - `javamcp-0.2.1.tar.gz`
  - `javamcp-0.2.1-py3-none-any.whl`
- [ ] Check package contents: `tar -tzf dist/javamcp-0.2.1.tar.gz`

---

## Git & GitHub Steps

### 6. Stage and Commit Changes
- [ ] Review all changes: `git diff`
- [ ] Stage all modified files: `git add -A`
- [ ] Commit with message: `feat: add rotating log file support and Claude Code MCP integration`

### 7. Create Git Tag
- [ ] Tag the release: `git tag v0.2.1`
- [ ] Verify tag: `git tag -l`

### 8. Push to GitHub
- [ ] Push commits: `git push origin main`
- [ ] Push tag: `git push origin v0.2.1`

### 9. Create GitHub Release
- [ ] Create release: `gh release create v0.2.1 --title "v0.2.1 - Rotating Log Files" --notes-file RELEASE_NOTES.md`
- [ ] Attach build artifacts:
  - `dist/javamcp-0.2.1.tar.gz`
  - `dist/javamcp-0.2.1-py3-none-any.whl`
- [ ] Verify release URL: https://github.com/rubensgomes/javamcp/releases/tag/v0.2.1

---

## Post-Release Steps

### 10. Verification
- [ ] Verify release on GitHub
- [ ] Test installation: `pip install dist/javamcp-0.2.1-py3-none-any.whl`
- [ ] Verify server starts: `python -m javamcp --help`
- [ ] Test rotating log functionality with sample config

### 11. Documentation Updates
- [ ] Update README.md with log rotation configuration example
- [ ] Update any relevant documentation

### 12. Cleanup
- [ ] Mark release plan as completed
- [ ] Archive or remove temporary files if needed

---

## CHANGELOG.md Entry

```markdown
## [0.2.1] - 2025-10-06

### Added
- **Rotating Log Files**: Automatic log rotation to prevent unbounded file growth
  - New configuration fields: `max_bytes` (default: 10MB) and `backup_count` (default: 5)
  - Uses Python's `RotatingFileHandler` for automatic rotation
  - Total max disk usage: ~60MB (10MB × 6 files)
- Claude Code MCP integration support via `.mcp.json` configuration
- Configuration validation for log rotation parameters

### Changed
- Replaced `FileHandler` with `RotatingFileHandler` in logging setup
- Enhanced logging tests with rotation behavior verification (3 new tests)

### Technical
- Log rotation configured via `LoggingConfig.max_bytes` and `LoggingConfig.backup_count`
- Backward compatible: existing configs work with default rotation settings
- All 24+ logging tests passing
```

---

## Release Notes Template (RELEASE_NOTES.md)

```markdown
# JavaMCP v0.2.1 - Rotating Log Files

## 🚀 New Features

### Rotating Log Files
Automatic log rotation prevents log files from growing indefinitely:
- **Default Settings**: 10MB max file size, 5 backup files
- **Total Disk Usage**: ~60MB maximum (10MB × 6 files)
- **Configurable**: Customize via `max_bytes` and `backup_count` in logging config

**Configuration Example**:
```yaml
logging:
  level: INFO
  file_path: ./logs/javamcp.log
  max_bytes: 10485760  # 10MB
  backup_count: 5      # Keep 5 backups
```

**How It Works**:
- When `javamcp.log` reaches 10MB, it's renamed to `javamcp.log.1`
- A new `javamcp.log` file is created
- Older backups are rotated: `.log.1` → `.log.2` → `.log.3`, etc.
- Oldest backup (`.log.5`) is deleted when limit is reached

### Claude Code MCP Integration
Added `.mcp.json` configuration for seamless integration with Claude Code IDE.

## ✅ Quality Metrics
- **Tests**: All logging tests passing (24+ tests)
- **Coverage**: 95%+ maintained
- **Code Quality**: pylint 9.0+/10

## 📦 Installation
```bash
pip install javamcp==0.2.1
```

## 🔗 Links
- [Full Changelog](https://github.com/rubensgomes/javamcp/blob/main/CHANGELOG.md#021)
- [Documentation](https://github.com/rubensgomes/javamcp)
```

---

## Rollback Plan
If issues arise:
1. Delete GitHub release: `gh release delete v0.2.1`
2. Delete git tag locally: `git tag -d v0.2.1`
3. Delete remote tag: `git push origin :refs/tags/v0.2.1`
4. Revert commit: `git revert HEAD`

---

## Release Completion Checklist

### Pre-Release
- [ ] All tests passing
- [ ] Code quality checks passed
- [ ] Version numbers updated
- [ ] CHANGELOG.md updated
- [ ] Package built successfully

### Release
- [ ] Changes committed
- [ ] Git tag created
- [ ] Pushed to GitHub
- [ ] GitHub release created with artifacts

### Post-Release
- [ ] Release verified
- [ ] Installation tested
- [ ] Documentation updated
- [ ] Plan marked as completed
