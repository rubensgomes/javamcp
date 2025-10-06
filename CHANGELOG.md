# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.1.0]: https://github.com/rubensgomes/javamcp/releases/tag/v0.1.0
