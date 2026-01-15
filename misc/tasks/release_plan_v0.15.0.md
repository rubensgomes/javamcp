# Release Plan: JavaMCP v0.15.0

## Release Summary
**Version:** 0.15.0
**Type:** Minor release (new features, backward compatible)
**Theme:** Granular Per-Logger Configuration
**Date:** 2026-01-15

## Changes Included

### Added
- **Hierarchical Logging Configuration**
  - New `root` section for configuring root logger level
  - New `loggers` dictionary for per-logger level configuration
  - Individual log level control for specific loggers (e.g., `uvicorn: WARNING`, `fastmcp: DEBUG`)
  - `RootLoggerConfig` Pydantic model for root logger settings
  - `get_effective_root_level()` method for resolving the effective root level

- **Named Logger Support**
  - `_configure_named_loggers()` function for setting up individual logger handlers
  - Each named logger gets its own handlers with `propagate=False` to prevent duplicates
  - Per-logger file output support when file logging is enabled

### Changed
- **Logging Configuration Schema**
  - `level` field now optional and deprecated (use `root.level` instead)
  - `root` field added for new hierarchical configuration
  - `loggers` field added as dict mapping logger names to levels
  - Automatic migration: legacy `level` field still works for backward compatibility

- **Logger Setup Logic**
  - Removed hardcoded third-party logger list (uvicorn, fastmcp, mcp, etc.)
  - Named loggers now configured dynamically from `config.loggers` dict
  - Root logger always configured with effective root level

- **CLI Help Documentation**
  - Updated examples to use `poetry run python -m javamcp` syntax
  - Added installation prerequisite (`poetry install`)
  - Reordered examples: version, help, then run commands
  - Removed redundant "Initializing JavaMCP server..." log message

### Technical
- All 307 tests passing (20 new tests from v0.14.0)
- Pylint score: 9.77/10
- Black and isort: passing
- Backward compatible - existing configs work without changes

## New Configuration Format

```yaml
logging:
  # New hierarchical format (recommended)
  root:
    level: INFO  # Default level for all loggers
  loggers:
    uvicorn: WARNING      # Suppress uvicorn info logs
    uvicorn.access: ERROR # Suppress access logs
    fastmcp: INFO         # FastMCP at INFO level
    javamcp: DEBUG        # Application at DEBUG for troubleshooting

  # Legacy format (still supported)
  # level: INFO  # Applies to all loggers

  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  date_format: "%Y-%m-%d %H:%M:%S"
  use_colors: true
  output: stderr
```

## Release Checklist

### Pre-Release Verification
- [x] All 307 tests pass (`poetry run pytest`)
- [x] Code quality checks pass (`poetry run black --check src/ tests/`)
- [x] Import sorting verified (`poetry run isort --check-only src/ tests/`)
- [x] Pylint score >= 9.70 (`poetry run pylint --ignore-paths='^.*/antlr4/.*' "src/javamcp"`) - Score: 9.77/10
- [x] Type checking reviewed (`poetry run mypy "src/javamcp"`)

### Version Update
- [x] Update version in `pyproject.toml` from `0.14.0` to `0.15.0`
- [x] Update `CHANGELOG.md` with v0.15.0 release notes
- [x] Add v0.15.0 link to CHANGELOG.md footer

### Documentation
- [x] Verify config.yml example includes new logging format
- [x] Update CLAUDE.md Configuration section with new logging format

### Final Release
- [x] Stage all changes (`git add -A`)
- [x] Commit with release message (`git commit -m "feat: release v0.15.0 with per-logger configuration"`)
- [x] Create git tag (`git tag v0.15.0`)
- [ ] Push changes to remote (`git push origin main`) - **PENDING: Manual push required (auth issue)**
- [ ] Push tag to remote (`git push origin v0.15.0`) - **PENDING: Manual push required (auth issue)**

### Post-Release
- [ ] Verify tag appears on GitHub releases page
- [ ] Update this release plan with completed checkboxes

## Files Modified (8 files, +449/-84 lines)

1. `src/javamcp/config/schema.py` - New `RootLoggerConfig` model, `loggers` dict, validators
2. `src/javamcp/logging/logger.py` - `_configure_named_loggers()`, dynamic logger setup
3. `src/javamcp/__main__.py` - Updated help examples with poetry commands
4. `src/javamcp/server.py` - Removed duplicate log message
5. `config.yml` - Example configuration with new logging format
6. `tests/config/test_schema.py` - Tests for new logging configuration
7. `tests/logging/test_logger.py` - Tests for named logger configuration
8. `.gitignore` - Minor update

## Migration Guide

### For Existing Users
No action required. Existing configurations with top-level `level` field continue to work:

```yaml
# Old format - still works
logging:
  level: INFO
```

### To Use New Features
Update your config.yml to use the new hierarchical format:

```yaml
# New format - more control
logging:
  root:
    level: INFO
  loggers:
    uvicorn: WARNING  # Quiet uvicorn logs
```

### Benefits of New Format
1. **Reduce noise**: Suppress verbose third-party library logs
2. **Debug specific components**: Enable DEBUG for javamcp while keeping others at INFO
3. **Production tuning**: Set access logs to ERROR for quieter production output
