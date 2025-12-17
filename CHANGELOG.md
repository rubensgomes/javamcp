# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.11.0] - 2025-12-17

### Changed
- **Dependency Updates**
  - `fastmcp`: 2.12.5 → 2.14.1 (major feature update)
  - `pydantic`: 2.12.3 → 2.12.5 (patch update)
  - `pytest`: 8.4.1 → 8.4.2 (patch update)
  - `pytest-mock`: 3.14.1 → 3.15.1 (minor update)
  - `python-semantic-release`: 10.3.1 → 10.5.3 (minor update)
  - `black`: 25.9.0 → 26.1a1 (alpha pre-release)
  - `mypy`: 1.18.2 → 1.19.1 (minor update)
  - `isort`: 6.0.1 → 6.1.0 (minor update)
  - `coverage`: 7.10.4 → 7.13.0 (minor update)
  - Dependency version constraints simplified (minimum bounds instead of caret ranges)

- **Code Quality Improvements**
  - Fixed import order in `__init__.py` - standard imports now before third-party
  - Switched to relative imports in `__init__.py` for better package structure
  - Fixed unnecessary `else` after `return` in `logger.py`
  - Added pylint disable comments for complex functions in `server.py`
  - Pylint score improved from 9.73/10 to 9.96/10

- **Configuration**
  - Added explicit `[tool.mypy]` configuration section in `pyproject.toml`
  - Configured mypy to exclude ANTLR4 generated files

### Technical
- All 287 tests passing
- Backward compatible - no breaking changes
- No functional changes to MCP tools or resources

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

## [0.9.0] - 2025-10-25

### Added
- **Color-Coded Logging System**
  - ANSI color codes for log levels (DEBUG: Bright Cyan, INFO: Bright Green, WARNING: Bright Yellow, ERROR: Bright Red, CRITICAL: Bold Red)
  - Unified logging format across all components (javamcp, FastMCP, Uvicorn, third-party libraries)
  - Automatic color detection (disabled when output is redirected or piped)
  - Color-free file output (always plain text in log files)
  - Customizable format and date_format via config.yml
  - Support for all Python logging format variables
- **Enhanced Git Repository Operations**
  - Automatic branch detection for cloned repositories
  - `get_default_branch()` function to detect remote HEAD branch
  - Branch name stored in repository metadata
  - Improved shallow clone functionality
- **Expanded Python Version Support**
  - Python version range extended from `<3.14` to `<4.0.0`
  - Future-proofs project for Python 3.14+ compatibility
- **Documentation Enhancements**
  - Comprehensive project structure tree in CLAUDE.md with file-level details
  - Updated module responsibilities and architecture documentation
  - Enhanced DEVSETUP.md with clearer instructions
  - Improved README.md with better project description

### Changed
- **Logging Configuration**
  - New `use_colors` option (default: true) for enabling/disabling ANSI colors
  - Enhanced `format` and `date_format` customization options
  - Root logger configuration ensures consistent formatting across all libraries
  - Third-party loggers (FastMCP, Uvicorn) automatically inherit application settings
- **Configuration Schema**
  - `LoggingConfig` model updated with color and format options
  - Validation for logging configuration parameters
- **Git Operations**
  - `clone_repository()` now detects and stores default branch name
  - Enhanced repository metadata with branch information
- **License**
  - Changed from Apache-2.0 to NONE (freely distributable)
  - Updated classifier to "License :: Freely Distributable"
- **Project Metadata**
  - Python version requirement: `>=3.13,<4.0.0` (was `>=3.13,<3.14`)
  - Simplified project description

### Removed
- **Obsolete Files**
  - `DISCLAIMER.md` (consolidated into LICENSE)
  - `config.example.json` (YAML is the standard format)
  - `config.example.yaml` (example included in documentation)

### Technical
- All 277 tests passing
- 95%+ test coverage maintained
- New test cases for color logging and branch detection
- Code quality maintained: pylint 9.73/10, black, isort
- Fully backward compatible
- No breaking changes to public API

## [0.8.0] - 2025-10-24

### Added
- **Multi-Platform Setup Instructions** (`DEVSETUP.md`)
  - Linux Ubuntu installation commands for python3 and pipx
  - Separated installation steps for macOS and Linux
  - Platform-specific guidance for developers on different operating systems
- **Package Upgrade Instructions** (`DEVSETUP.md`)
  - Commands for upgrading pipx-installed packages (fastmcp, pylint, pytest, poetry)
  - Helps developers maintain up-to-date tooling
- **Production Readiness Warning** (`README.md`)
  - Prominent WARNING section stating project is under development
  - Sets clear expectations about alpha status as of Oct. 24, 2025
- **Enhanced Command Examples** (`DEVSETUP.md`)
  - Explicit examples (e.g., `poetry add fastmcp`) instead of generic placeholders
  - Consistent `cd $(git rev-parse --show-toplevel) || exit` pattern
  - "Ensure at project root" reminders before command sequences

### Changed
- **LICENSE File - AI Disclaimer Formatting**
  - Reformatted with visual warning box: `!!! WARNING / ATTENTION !!!`
  - Multi-line formatting for better readability
  - More prominent treatment of critical AI disclaimer
  - Clearer emphasis on DISCLAIMER.md requirement
- **README.md Improvements**
  - Improved project description formatting with better line breaks
  - Added context about project intent and use case
  - Fixed trailing whitespace throughout
  - Removed premature "Contributing" section (project still in alpha)
- **DEVSETUP.md Enhancements**
  - Better organized with platform-specific section headers
  - Added explicit comments in code examples
  - Improved virtual environment management instructions
  - Consistent command patterns with error handling

### Removed
- **Contributing Section** (`README.md`)
  - Removed as project is in alpha/development phase
  - Can be re-added when project reaches stable release

### Technical
- No code changes
- No dependency updates
- All 247 tests passing
- 95%+ test coverage maintained
- Code quality maintained (pylint, black, isort)
- Fully backward compatible
- No breaking changes to public API

## [0.7.0] - 2025-10-23

### Added
- **Release Plan Slash Command** (`.claude/commands/release-plan.md`)
  - Automated release plan generation via `/release-plan` command
  - Repository validation and access checking
  - Structured workflow for consistent releases
- **AI Disclaimer in LICENSE**
  - Prominent AI-generated content notice at top of license file
  - References to DISCLAIMER.md for complete terms
  - Ensures transparency about project origins

### Changed
- **Documentation Improvements**
  - `DEVSETUP.md`: Complete restructure with improved readability
    - Simplified installation instructions
    - Better command organization
    - Clearer section hierarchy
  - `README.md`: Content and clarity enhancements
    - Fixed typo: "fOR" → "For" in AI disclaimer section
    - Improved feature descriptions
    - Added actual repository URL to clone instructions
  - `grammars/README.md`: Documentation refinements
- **Dependency Updates**
  - `fastmcp`: 2.12.4 → 2.12.5 (latest stable patch)
  - `pydantic`: 2.12.0 → 2.12.3 (latest stable patch)
- **Project Metadata**
  - Added keywords: "LLM" and "agent" for better PyPI discoverability

### Technical
- All 247 tests passing
- 95%+ test coverage maintained
- Code quality checks passed (pylint, black, isort)
- Fully backward compatible
- No breaking changes to public API

## [0.6.0] - 2025-10-21

### Fixed
- **Logging Initialization Bug** (Critical Fix)
  - FastMCP library now uses same logging configuration as application
  - Implemented lazy initialization pattern via `server_factory.py`
  - Root logger configured before any library code executes
  - Eliminates duplicate log messages and inconsistent formatting
  - Ensures consistent logging across all components

### Added
- **CLAUDE.md Documentation**
  - Comprehensive guidance for future Claude Code instances
  - Essential development commands (environment setup, testing, code quality, release process)
  - Project structure tree with directory explanations
  - Core architecture patterns and critical initialization order
  - Global state management documentation
  - Module responsibilities and data flow
  - Key design patterns (Factory, Singleton, Visitor, Builder, Repository)
  - MCP tools and resources overview
  - Testing architecture (263 tests, 95%+ coverage)
  - Common development patterns for adding tools, modifying parser, and configuration
- **Server Factory Module** (`src/javamcp/server_factory.py`)
  - Lazy FastMCP instance creation
  - Singleton pattern for MCP server
  - Ensures logging configured before library instantiation
- **Tool Registration Function**
  - `register_tools_and_resources()` for programmatic registration
  - Replaces module-level decorators
  - Called after logging setup

### Changed
- **Server Module Architecture**
  - Removed module-level FastMCP instantiation
  - Removed `@mcp.tool()` and `@mcp.resource()` decorators
  - Tools and resources registered dynamically after logging configuration
- **Main Entry Point Initialization**
  - Logging setup occurs before server component imports
  - Proper initialization order: config → logging → register tools → initialize server → run
- **Logging Configuration**
  - Root logger configured for centralized control
  - All child loggers inherit settings automatically
  - No duplicate handlers or log messages

### Removed
- **`.mcp.json`**: Removed obsolete MCP configuration file

### Technical
- All 263 tests passing
- Code quality maintained (pylint, black, isort)
- Fully backward compatible
- No breaking changes to public API
- Critical initialization order documented in CLAUDE.md

## [0.5.0] - 2025-10-12

### Added
- **Shallow Clone Support**: Optional `depth` parameter in `clone_repository()` function
  - Default depth of 1 commit for all repository clones
  - Reduces disk space usage significantly
  - Improves clone performance for large repositories
  - Maintains full API analysis functionality
- **New Test Case**: `test_clone_repository_custom_depth` for custom depth validation

### Changed
- **`clone_repository()` function** in `src/javamcp/repository/git_operations.py:50`
  - Added `depth: int = 1` parameter with default shallow clone
  - Passes `depth` parameter to `Repo.clone_from()`
  - Updated docstring with parameter documentation
- **`_clone_new_repository()` method** in `src/javamcp/repository/manager.py:223`
  - Now explicitly passes `depth=1` to ensure shallow clones
- **Test suite**: Updated test mocks to verify `depth` parameter propagation

### Technical
- Performance optimization for repository cloning operations
- Faster clone times for large Java repositories
- Reduced local disk space requirements
- No breaking changes - fully backward compatible
- All tests passing

## [0.4.0] - 2025-10-11

### Added
- **DISCLAIMER.md**: Comprehensive AI-Generated Content Disclaimer
  - Clarifies AI LLM involvement in project creation
  - Explains copyright status (public domain for AI-generated portions)
  - Includes third-party content notice and limitations
  - Provides no-warranty disclaimer and limitation of liability
- **AI Disclaimer Headers**: Added to all 72 Python source files
  - Replaces previous Apache 2.0 license headers
  - Includes AI content notice, copyright status, and liability limitations
  - Placed at top of every source and test file

### Changed
- **Licensing Model**: Transitioned from Apache 2.0 to AI-Generated Content Disclaimer
  - Removed LICENSE file (Apache 2.0)
  - AI-generated portions now in public domain
  - Copyright protection limited to original human contributions only
- **README.md**: Added prominent AI General Disclaimer section at top

### Removed
- **LICENSE file**: Apache 2.0 license removed

### Technical
- No functional changes or breaking changes
- All 262 tests passing
- Code coverage maintained at 52%
- Pylint score maintained at ~9.73/10
- Fully backward compatible

## [0.3.0] - 2025-10-11

### Added
- **New MCP Resource**: `javamcp://project/{repository_name}/context`
  - Access comprehensive project context for Java API repositories
  - Provides repository information, README content, llms.txt content
  - Includes API statistics (classes, methods, packages, averages)
  - Package-level summaries with class and method counts
  - Top classes with Javadoc documentation
  - Documentation coverage metrics for classes and methods
- **ProjectContextBuilder Component**: New module for building rich project context
  - Aggregates information from README, llms.txt, Javadocs, and indexed APIs
  - Generates comprehensive API statistics and package summaries
  - Calculates Javadoc documentation coverage rates
  - 346 lines of production code with full test coverage
- **ProjectContextResponse Model**: New protocol model for resource responses
- **Enhanced Repository Manager**: Added `get_repository_by_name()` method for easier repository lookups
- **Comprehensive Test Suite**: 324 lines of tests for new functionality (12 new tests)

### Changed
- Updated README.md with comprehensive MCP Resources section and usage examples
- Enhanced server.py with resource registration using `@mcp.resource()` decorator
- Updated MCP protocol models with new `ProjectContextResponse`

### Technical
- All 262 tests passing (13 new tests added)
- Code coverage maintained at 52% (ANTLR4 generated code excluded)
- Pylint score: 9.73/10 (improved from 9.70/10)
- No breaking changes - fully backward compatible
- Follows semantic versioning (MINOR version bump for new feature)

## [0.2.3] - 2025-10-11

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

## [0.2.2] - 2025-10-08

### Added
- HTTP transport mode support for FastMCP server
  - Server can now run in both stdio and HTTP modes
  - Mode selection via configuration setting
  - Explicit port configuration for HTTP mode

### Changed
- Code quality improvements and cleanup
  - Removed unused `StringIO` imports from ANTLR4 generated files
  - Removed unused `Context` import from server module
  - Fixed blank line formatting across multiple files
  - Applied black formatter and isort to entire codebase
- Updated development setup documentation
  - Added `fastmcp` installation instructions

### Technical
- Pylint score: 9.71/10 (improved from 9.70/10)
- All 249 tests passing
- Code coverage maintained at 95%+
- Enhanced server initialization with transport mode handling

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

[0.11.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.11.0
[0.10.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.10.0
[0.9.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.9.0
[0.8.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.8.0
[0.7.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.7.0
[0.6.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.6.0
[0.5.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.5.0
[0.4.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.4.0
[0.3.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.3.0
[0.2.3]: https://github.com/rubensgomes/javamcp/releases/tag/v0.2.3
[0.2.2]: https://github.com/rubensgomes/javamcp/releases/tag/v0.2.2
[0.2.1]: https://github.com/rubensgomes/javamcp/releases/tag/v0.2.1
[0.2.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.2.0
[0.1.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.1.0
