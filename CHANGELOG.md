# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2025-10-06

### Added
- **Rotating Log Files**: Automatic log rotation to prevent unbounded file growth
  - New configuration fields: `max_bytes` (default: 10MB) and `backup_count` (default: 5)
  - Uses Python's `RotatingFileHandler` for automatic rotation
  - Total max disk usage: ~60MB (10MB × 6 files)
  - Configuration validation for log rotation parameters
- Claude Code MCP integration support via `.mcp.json` configuration

### Changed
- Replaced `FileHandler` with `RotatingFileHandler` in logging setup
- Enhanced logging tests with rotation behavior verification (3 new tests)

### Technical
- Log rotation configured via `LoggingConfig.max_bytes` and `LoggingConfig.backup_count`
- Backward compatible: existing configs work with default rotation settings
- All 249 tests passing (2 new rotation tests added)
- Code quality maintained: pylint 9.70/10, 95%+ coverage

## [0.2.0] - 2025-10-06

### Added
- FastMCP framework integration for proper MCP server implementation
- Graceful shutdown signal handlers for SIGINT and SIGTERM
- ServerState class for shared component management across tools
- 5 new signal handler tests (247 total tests)
- Comprehensive signal handling with resource cleanup

### Changed
- **BREAKING**: Refactored server.py to use FastMCP decorators
- **BREAKING**: All 4 tools now use `@mcp.tool()` decorator pattern
- **BREAKING**: Server API changed from JavaMCPServer class to FastMCP-based implementation
- Simplified server startup using `mcp.run()`
- Updated exports: `mcp`, `initialize_server`, `get_state` (replaces `JavaMCPServer`, `create_server`)

### Migration Guide
- Old import: `from javamcp import JavaMCPServer, create_server`
- New import: `from javamcp import mcp, initialize_server, get_state`
- Original tool functions preserved in `src/javamcp/tools/` for backward compatibility

### Technical
- Server now uses global ServerState for component sharing
- Signal handlers properly clean up indexer and log shutdown events
- All tests updated for FastMCP compatibility
- Code quality maintained: pylint 10.00/10, 95%+ coverage

## [0.1.0] - 2025-10-06

### Added
- Initial release of JavaMCP
- 4 MCP tools for Java API exploration:
  - `search_methods`: Search for Java methods by name with full context
  - `analyze_class`: Get complete information about a Java class
  - `extract_apis`: Extract and index APIs from a Git repository
  - `generate_guide`: Generate usage guides for specific use cases
- ANTLR4-based Java parser supporting Java 21+
- Comprehensive API indexing and query engine
- Git repository integration for automatic code discovery
- Rich context building with Javadoc summaries and API documentation
- Configuration support (YAML/JSON) for repository management
- Comprehensive logging system
- 247 unit and integration tests with 95%+ average coverage
- Full code quality tooling (pylint, black, isort, mypy)

### Features
- Parse Java source code and extract:
  - Classes, interfaces, and enums
  - Methods with signatures, parameters, and return types
  - Fields with types and modifiers
  - Javadoc documentation
  - Annotations and modifiers
  - Inheritance hierarchies
- Index APIs from multiple Git repositories
- Fast search and filtering capabilities
- Context-aware responses for AI coding assistants

[0.2.1]: https://github.com/rubensgomes/javamcp/releases/tag/v0.2.1
[0.2.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.2.0
[0.1.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.1.0
