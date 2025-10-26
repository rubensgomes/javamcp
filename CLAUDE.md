# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

JavaMCP is a Python-based MCP (Model Context Protocol) server that provides AI
coding assistants with rich contextual information about Java APIs. It clones
Java repositories, parses source code using ANTLR4, extracts Javadocs and API
information, and exposes this data through 4 MCP tools and 1 MCP resource.

## Essential Development Commands

### Environment Setup

```bash
# Install dependencies
poetry install

# Generate ANTLR4 parser (one-time setup, only if grammars change)
pushd grammars
antlr4 -Dlanguage=Python3 JavaLexer.g4 JavaParser.g4 -o ../src/javamcp/antlr4
popd

# Configure repositories
# Edit config.yml to add Java repository URLs
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src/javamcp --cov-report=term-missing

# Run specific test module
poetry run pytest tests/models/

# Run with coverage report
poetry run python -m coverage run -m pytest tests/
poetry run python -m coverage report -m
```

### Code Quality

```bash
# Format code (must run before committing)
poetry run black src/ tests/

# Lint
poetry run pylint --ignore-paths='^.*/antlr4/.*' "src/javamcp"

# Sort imports
poetry run isort src/ tests/

# Type checking
poetry run mypy src/
```

### Running the Server

```bash
# Run with explicit config file
poetry run python -m javamcp --config config.yml

# Run with default config location (~/.config/javamcp/config.yml)
poetry run python -m javamcp

# Run single test
poetry run pytest tests/path/to/test_file.py::test_function_name
```

## Project Structure

```
.
├── src/javamcp/                   # Main source code
│   ├── config/                   # Configuration loading and schemas
│   │   ├── loader.py             # YAML/JSON config loader
│   │   └── schema.py             # Pydantic config models
│   ├── context/                  # Context building and formatting
│   │   ├── context_builder.py    # Rich context construction
│   │   └── formatter.py          # Output formatting
│   ├── indexer/                  # API indexing and query engine
│   │   ├── indexer.py            # In-memory API indexer
│   │   ├── query_engine.py       # Search and query logic
│   │   └── exceptions.py         # Indexer exceptions
│   ├── logging/                  # Logging configuration
│   │   └── logger.py             # Centralized logging setup
│   ├── models/                   # Pydantic data models
│   │   ├── java_entities.py      # JavaClass, JavaMethod models
│   │   ├── mcp_protocol.py       # MCP request/response models
│   │   └── repository.py         # Repository metadata models
│   ├── parser/                   # ANTLR4 Java parser and AST visitor
│   │   ├── java_parser.py        # Main parser orchestration
│   │   ├── javadoc_parser.py     # Javadoc extraction
│   │   ├── ast_visitor.py        # ANTLR4 AST visitor
│   │   └── exceptions.py         # Parser exceptions
│   ├── repository/               # Git repository management
│   │   ├── manager.py            # Repository lifecycle management
│   │   ├── git_operations.py     # Git clone/update operations
│   │   └── exceptions.py         # Repository exceptions
│   ├── resources/                # MCP resource implementations
│   │   └── project_context_builder.py  # Project context resource
│   ├── tools/                    # Legacy tool implementations
│   │   ├── search_methods.py     # Search methods tool
│   │   ├── analyze_class.py      # Analyze class tool
│   │   ├── extract_apis.py       # Extract APIs tool
│   │   └── generate_guide.py     # Generate guide tool
│   ├── utils/                    # Helper utilities
│   │   └── helpers.py            # Shared utility functions
│   ├── antlr4/                   # Generated ANTLR4 parser code
│   ├── __init__.py               # Package initialization
│   ├── __main__.py               # Entry point
│   ├── server.py                 # MCP server with tools/resources
│   └── server_factory.py         # Lazy FastMCP initialization
├── tests/                        # Test suite (mirrors src/ structure)
│   ├── config/
│   │   ├── test_loader.py
│   │   └── test_schema.py
│   ├── context/
│   │   ├── test_context_builder.py
│   │   └── test_formatter.py
│   ├── indexer/
│   │   ├── test_indexer.py
│   │   └── test_query_engine.py
│   ├── logging/
│   │   └── test_logger.py
│   ├── models/
│   │   ├── test_java_entities.py
│   │   ├── test_mcp_protocol.py
│   │   └── test_repository.py
│   ├── parser/
│   │   ├── test_java_parser.py
│   │   └── test_javadoc_parser.py
│   ├── repository/
│   │   ├── test_git_operations.py
│   │   └── test_manager.py
│   ├── resources/
│   │   └── test_project_context_builder.py
│   ├── server/
│   │   └── test_server.py
│   ├── tools/
│   │   └── test_tools.py
│   ├── utils/
│   └── test_main.py
├── misc/                         # Project metadata and plans
│   ├── memory/                   # LLM understanding documents
│   │   ├── PROJ_REQUIREMENTS.md
│   │   ├── RULES_UNDERSTANDING.md
│   │   └── USER_CLAUDE.md
│   └── tasks/                    # Implementation plans and tasks
│       ├── javamcp_implementation_plan.md
│       ├── fastmcp_refactor_plan.md
│       ├── logging_initialization_fix_implementation.md
│       └── release_plan_*.md     # Various release plans
├── design/                       # Design documents
│   └── REQUIREMENTS.md           # Original project requirements
├── grammars/                     # ANTLR4 Java grammar files
│   ├── JavaLexer.g4              # Java lexer grammar
│   ├── JavaParser.g4             # Java parser grammar
│   └── README.md                 # Grammar documentation
├── repositories/                 # Cloned Java repos (gitignored)
├── CHANGELOG.md                  # Version history
├── CLAUDE.md                     # This file - Claude Code guidance
├── DEVSETUP.md                   # Development environment setup
├── LICENSE                       # Apache 2.0 license
├── MANIFEST.in                   # Python package manifest
├── README.md                     # Project README
├── config.yml                    # Server configuration
├── poetry.lock                   # Locked dependencies
└── pyproject.toml                # Poetry project definition
```

## Architecture

### Core Architecture Pattern

JavaMCP follows a **layered architecture** with clear separation of concerns:

1. **Entry Point** (`__main__.py`): Initializes logging → registers tools →
   initializes server state → starts FastMCP
2. **Server Layer** (`server.py`): Maintains global state (ServerState) and
   implements MCP tool/resource functions
3. **Factory Pattern** (`server_factory.py`): Lazy initialization of FastMCP to
   ensure logging is configured first
4. **Tool Layer** (`tools/`): Legacy tool implementations (NOTE: tools are now
   implemented directly in server.py)
5. **Domain Layers**: Repository management, parsing, indexing, context building

### Critical Initialization Order

**IMPORTANT:** Logging MUST be configured BEFORE FastMCP instance creation. The
initialization sequence in `__main__.py` is:

```python
# 1. Load config
config = load_config(args.config)

# 2. Setup logging FIRST
logger = setup_logging(config.logging)

# 3. THEN register tools (creates FastMCP instance via factory)
register_tools_and_resources()

# 4. Initialize server state
initialize_server(args.config)

# 5. Start FastMCP
mcp.run()
```

This order ensures FastMCP library code uses the configured logging settings. *
*DO NOT** create the FastMCP instance before logging setup.

### Global State Management

Server state is managed through a `ServerState` class in `server.py`:

```python
class ServerState:
    config: ApplicationConfig
    repository_manager: RepositoryManager
    indexer: APIIndexer
    query_engine: QueryEngine
    initialized: bool
```

All MCP tools access this shared state via `get_state()`. The state is
initialized once during server startup and remains global throughout the server
lifecycle.

### Module Responsibilities

- **config/**: YAML/JSON configuration loading and Pydantic schemas
- **repository/**: Git repository cloning, updating, and Java file discovery
- **parser/**: ANTLR4-based Java source parsing, AST visiting, Javadoc
  extraction
- **indexer/**: In-memory API indexing and query engine for searching
  classes/methods
- **context/**: Building rich context (Javadocs, summaries) for MCP responses
- **resources/**: Project context resource implementation
- **models/**: Pydantic data models for Java entities and MCP protocol
- **logging/**: Centralized logging configuration and utilities

### Data Flow

1. **Initialization**: Config → RepositoryManager → clone repos → discover .java
   files
2. **Parsing**: Java files → ANTLR4 parser → AST → JavaSourceParser →
   JavaClass/JavaMethod models
3. **Indexing**: JavaClass objects → APIIndexer → in-memory indexes (by name,
   package, repository)
4. **Query**: MCP tool request → QueryEngine → search indexes → return results
5. **Context Building**: Results → ContextBuilder → enrich with Javadocs →
   format response

### Key Design Patterns

- **Factory Pattern**: `server_factory.py` for lazy FastMCP initialization
- **Singleton Pattern**: Global `_mcp_instance` and `ServerState`
- **Visitor Pattern**: `ast_visitor.py` for traversing ANTLR4 AST
- **Builder Pattern**: `ContextBuilder`, `ProjectContextBuilder` for
  constructing responses
- **Repository Pattern**: `RepositoryManager` for Git operations

## Configuration

The server uses YAML configuration. If no config file is specified via the `--config`
or `-c` flag, the server looks for a configuration file at the default location:

**Default Config Path:** `~/.config/javamcp/config.yml`

If the default config file is not found, the server will exit with an error message
showing the sample configuration template.

Configuration format (`config.yaml`):

```yaml
server:
    mode: stdio  # or "http"
    host: localhost
    port: 8000

repositories:
    urls:
        - https://github.com/apache/commons-lang.git
    local_base_path: ./repositories
    # Note: Repositories are cloned using their default branch (main, master, etc.)

logging:
    level: INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Python logging format
    date_format: "%Y-%m-%d %H:%M:%S"  # strftime format
    use_colors: true  # Enable ANSI color codes for log levels
    output: console  # "console", "file", or "both"
    file_path: null  # Required if output is "file" or "both"
```

**Repository Cloning Behavior:**

- JavaMCP automatically clones the default branch from each repository
- The default branch is detected from the remote repository (e.g., `main`,
  `master`, `develop`)
- No manual branch configuration is required
- The detected branch name is stored in repository metadata

**Logging Configuration:**

- **Default Format**: `2025-10-25 18:25:55 - javamcp - INFO - Message`
- **Unified Format**: All logs (javamcp, FastMCP, Uvicorn, third-party
  libraries) use the same format
- **Color-Coded Levels**: Log levels are displayed in different colors in
  terminal output:
    - `DEBUG` - Bright Cyan
    - `INFO` - Bright Green
    - `WARNING` - Bright Yellow
    - `ERROR` - Bright Red
    - `CRITICAL` - Bold Red
- **Colors Auto-Detection**: Colors are automatically disabled when output is
  redirected or piped
- **File Output**: Log files never contain color codes (always plain text)
- **Customizable**: Both format and date_format can be customized via config.yml
- **Third-Party Integration**: Uvicorn, FastMCP, and other library loggers are
  automatically configured
- **Available Format Variables**: All Python logging format variables are
  supported:
    - `%(asctime)s` - Timestamp
    - `%(name)s` - Logger name (e.g., "javamcp", "fastmcp", "uvicorn")
    - `%(levelname)s` - Log level (DEBUG, INFO, etc.)
    - `%(message)s` - Log message
    - `%(pathname)s`, `%(filename)s`, `%(lineno)d`, etc.

## MCP Tools and Resources

**4 MCP Tools** (all implemented in `server.py`):

1. `search_methods`: Search for methods by name with optional class filter
2. `analyze_class`: Get complete class information by fully-qualified name
3. `extract_apis`: Clone/parse repository and extract APIs
4. `generate_guide`: Generate usage guide based on use case description

**1 MCP Resource**:

- `javamcp://project/{repository_name}/context`: Get comprehensive project
  context including README, statistics, top classes, package summaries, and
  Javadoc coverage

## Important Constraints

- **Python Version**: Requires Python 3.13 (not 3.14+)
- **ANTLR4 Grammars**: Must be generated from Java 21+ grammars before first run
- **Logging Order**: Logging MUST be configured before FastMCP instantiation
- **Test Coverage**: Maintain 80%+ coverage (currently 95%+)
- **Type Hints**: All public functions and methods require type hints
- **Pydantic Models**: Use Pydantic for all DTOs and data validation

## Testing Architecture

- **247 tests** with 95%+ average coverage
- Tests mirror `src/` structure in `tests/`
- Use `pytest-mock` for mocking (mock only external dependencies)
- Use `pytest.mark.parametrize` for testing multiple inputs
- Test both success and failure scenarios
- Fast unit tests (no real Git cloning in tests)

## Common Development Patterns

### Adding a New MCP Tool

1. Define request/response models in `models/mcp_protocol.py`
2. Implement tool function in `server.py`
3. Register tool in `register_tools_and_resources()` via
   `mcp.tool()(function_name)`
4. Add comprehensive tests mirroring the structure

### Modifying Parser Logic

1. Update `parser/ast_visitor.py` for AST traversal changes
2. Update `parser/javadoc_parser.py` for Javadoc extraction changes
3. Ensure `parser/java_parser.py` orchestrates correctly
4. Run parser tests: `poetry run pytest tests/parser/`

### Adding Configuration Options

1. Add field to appropriate config class in `config/schema.py` (Pydantic model)
2. Update `config.example.yaml` with new option and documentation
3. Update config loader in `config/loader.py` if needed
4. Add tests in `tests/config/`
