# Release Plan: JavaMCP v0.14.0

## Release Summary
**Version:** 0.14.0
**Type:** Minor release (new features, backward compatible)
**Theme:** Enhanced Logging and Observability
**Date:** 2026-01-14

## Changes Included

### Added
- **Comprehensive Logging Throughout Codebase**
  - Added logging to 11 modules for improved troubleshooting and observability
  - MCP tool invocation logging with `log_tool_invocation()` for all 4 tools and 1 resource
  - Repository lifecycle logging (initialization, clone, update operations)
  - Git operation logging (clone, pull, checkout with success/failure status)
  - Parse operation logging with detailed file and result tracking
  - Index operation logging (add_classes, reindex, clear)
  - Query engine logging with search parameters and result counts
  - Configuration loading and validation logging
  - AST visitor logging for class/interface/enum extraction
  - Javadoc parser logging with extraction statistics
  - Context builder logging for class context generation

### Fixed
- **Silent Exception Handlers**
  - Fixed 6 silent exception handlers in `project_context_builder.py` that were hiding failures
  - All exceptions now properly logged with appropriate severity levels

### Technical
- All 287 tests passing
- Pylint score: 9.77/10 (improved from 9.75/10)
- Backward compatible - no breaking changes

## Release Checklist

- [x] Update version in `pyproject.toml` from `0.13.0` to `0.14.0`
- [x] Update `CHANGELOG.md` with v0.14.0 release notes
- [x] Run full test suite to verify all tests pass
- [x] Run code quality checks (black, isort, pylint, mypy)
- [x] Commit all changes with release message
- [x] Create and push git tag `v0.14.0`
- [x] Push changes to remote repository

## Files Modified (12 files, +414/-50 lines)
1. `src/javamcp/server.py` - MCP tool invocation logging
2. `src/javamcp/repository/manager.py` - Repository lifecycle logging
3. `src/javamcp/repository/git_operations.py` - Git operation logging
4. `src/javamcp/resources/project_context_builder.py` - Fixed silent exceptions + logging
5. `src/javamcp/parser/java_parser.py` - Parse operation logging
6. `src/javamcp/indexer/indexer.py` - Index operation logging
7. `src/javamcp/indexer/query_engine.py` - Query logging
8. `src/javamcp/config/loader.py` - Config loading logging
9. `src/javamcp/parser/ast_visitor.py` - AST traversal logging
10. `src/javamcp/parser/javadoc_parser.py` - Javadoc parsing logging
11. `src/javamcp/context/context_builder.py` - Context building logging
12. `README.md` - Documentation updates
