# Release Plan: v0.10.0 - Default Configuration Path

**Repository**: rubensgomes/javamcp
**Current Version**: 0.9.0
**Target Version**: 0.10.0
**Release Type**: Minor (New Feature)
**Date**: 2025-10-25

## Release Summary

This release adds default configuration file path support, allowing JavaMCP to automatically look for configuration at `~/.config/javamcp/config.yml` when no explicit config path is provided. This improves user experience by eliminating the need to specify the config path on every invocation.

## Key Changes

### Added
- **Default Configuration Path Support**
  - Automatic config file lookup at `~/.config/javamcp/config.yml`
  - Helpful error message with sample config when default config not found
  - Config template embedded as package resource (`src/javamcp/config_template.yml`)
  - New helper functions in `__main__.py`:
    - `get_default_config_path()`: Returns default config path
    - `get_config_template()`: Reads embedded config template
    - `display_config_error_and_exit()`: Shows helpful error with sample
    - `resolve_config_path()`: Handles config path resolution logic
  - Comprehensive test coverage for new config path behavior (8 new tests)
  - Documentation updates in CLAUDE.md

### Changed
- `__main__.py`: Enhanced config resolution logic
- Updated documentation with default path information

## Release Checklist

### Pre-Release Tasks

- [x] Review and verify all changes since v0.9.0
- [x] Update version number in pyproject.toml (0.9.0 → 0.10.0)
- [x] Update CHANGELOG.md with v0.10.0 entry
- [x] Run full test suite and verify all tests pass (287/287 tests passing)
- [x] Run code quality checks (black, isort, pylint - 9.72/10 rating)
- [x] Verify test coverage remains above 80% (84% coverage)
- [x] Review documentation updates (CLAUDE.md, README.md if needed)
- [ ] Commit all changes with appropriate commit message
- [ ] Push changes to main branch

### Release Tasks

- [ ] Create git tag: `git tag v0.10.0`
- [ ] Push tag to GitHub: `git push origin v0.10.0`
- [ ] Build package: `poetry build`
- [ ] Create GitHub release using gh CLI
- [ ] Upload distribution files to GitHub release
- [ ] Verify release appears correctly on GitHub

### Post-Release Tasks

- [ ] Verify package installation from built distribution
- [ ] Test default config path functionality end-to-end
- [ ] Update project board/issues if applicable
- [ ] Announce release (if applicable)

## Testing Verification

### Unit Tests
- [ ] All existing tests pass (287 tests)
- [ ] New config path resolution tests pass (8 tests)
- [ ] Test coverage > 80% maintained

### Integration Tests
- [ ] Test with explicit --config flag
- [ ] Test with default config at ~/.config/javamcp/config.yml
- [ ] Test error message when default config missing
- [ ] Verify config template is readable from package resources

### Manual Testing
- [ ] Install package from built distribution
- [ ] Run without --config flag (should look for default)
- [ ] Run with --config flag (should use specified path)
- [ ] Verify error message formatting when config not found

## CHANGELOG Entry

```markdown
## [0.10.0] - 2025-10-25

### Added
- **Default Configuration Path Support**
  - JavaMCP now automatically looks for configuration at `~/.config/javamcp/config.yml` when no `--config` flag is provided
  - Helpful error message with sample configuration template when default config file is not found
  - Configuration template embedded as package resource for easy reference
  - New helper functions for config path resolution and error handling
  - Comprehensive test coverage for config path resolution logic
  - Documentation updates in CLAUDE.md with default path information

### Changed
- `__main__.py`: Enhanced configuration resolution logic to support default path
- Improved user experience by eliminating need to specify config path on every invocation
```

## Commit Message

```
feat: add default configuration path support

Add automatic config file lookup at ~/.config/javamcp/config.yml when no
explicit --config flag is provided. This improves user experience by
eliminating the need to specify the config path on every invocation.

Changes:
- Add config_template.yml as embedded package resource
- Implement config path resolution logic in __main__.py
- Add helper functions for default path and error handling
- Add comprehensive test coverage (8 new tests)
- Update CLAUDE.md documentation

When no config is specified and default config doesn't exist, users now
see a helpful error message with the full sample configuration template.

All 287 tests passing. Backward compatible - explicit --config flag
still works as before.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## GitHub Release Notes

```markdown
# v0.10.0 - Default Configuration Path

## 🎯 What's New

JavaMCP now supports a **default configuration path**, making it easier to use without specifying the config file location every time!

## ✨ Key Features

### Default Config Path
- Run `javamcp` without `--config` flag
- Automatically looks for config at `~/.config/javamcp/config.yml`
- Helpful error message with sample config if file not found

### Usage Examples

**Before (still works):**
```bash
javamcp --config /path/to/config.yml
```

**Now (new default path):**
```bash
# Just create ~/.config/javamcp/config.yml and run:
javamcp
```

### Error Handling
If the default config file doesn't exist, you'll see:
```
Error: No configuration file found.

Please create a configuration file at: ~/.config/javamcp/config.yml

You can use the following sample configuration as a template:

[full sample config displayed]
```

## 📝 Full Changelog

### Added
- Default configuration path support at `~/.config/javamcp/config.yml`
- Embedded configuration template as package resource
- Helper functions for config path resolution
- Comprehensive test coverage for new functionality
- Updated documentation in CLAUDE.md

### Technical Details
- All 287 tests passing
- Backward compatible with explicit `--config` flag
- Test coverage maintained above 80%

## 🔄 Upgrade Notes

No breaking changes. Existing usage with `--config` flag continues to work exactly as before.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Notes

- This is a minor version bump (0.9.0 → 0.10.0) as it adds new functionality
- No breaking changes - fully backward compatible
- The feature improves user experience significantly
- All tests passing with comprehensive coverage of new functionality
- Documentation has been updated to reflect the new behavior

## Dependencies

No new dependencies required. Uses built-in `importlib.resources` for reading the embedded config template.

## Risks

**Low Risk**:
- Backward compatible - existing usage patterns continue to work
- Well-tested with 8 new unit tests
- Simple, isolated change to config resolution logic
- Fallback error handling in place
