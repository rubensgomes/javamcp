# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

JavaMCP is a Python-based MCP (Model Context Protocol) server that provides AI coding assistants with rich contextual information about Java APIs. It clones Java repositories, parses source code using ANTLR4, extracts Javadocs and API information, and exposes this data through 4 MCP tools and 1 MCP resource.

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
cp config.example.yaml config.yaml
# Edit config.yaml to add Java repository URLs
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
poetry run pylint src/javamcp

# Sort imports
poetry run isort src/ tests/

# Type checking
poetry run mypy src/
```

### Running the Server
```bash
# Run with config file
poetry run python -m javamcp --config config.yaml

# Run single test
poetry run pytest tests/path/to/test_file.py::test_function_name
```

### Release Process
```bash
# Build distribution
poetry build

# Create git tag and release (requires GH_TOKEN)
git tag v0.x.x
git push origin v0.x.x
gh release create v0.x.x --title "v0.x.x" --notes "Release notes"

# Semantic release (automated versioning)
poetry run python -m semantic_release -vvv version
poetry run python -m semantic_release -vvv publish
```

**Git Commit Message Convention:**
- `feat:` → minor version bump (0.1.0 → 0.2.0)
- `fix:` → patch version bump (0.1.0 → 0.1.1)
- `BREAKING CHANGE:` → major version bump (0.1.0 → 1.0.0)
- `chore:`, `docs:` → no version bump

## Project Structure

```
.
├── src/javamcp/              # Main source code
│   ├── config/              # Configuration loading and schemas
│   ├── context/             # Context building and formatting
│   ├── indexer/             # API indexing and query engine
│   ├── logging/             # Logging configuration
│   ├── models/              # Pydantic data models
│   ├── parser/              # ANTLR4 Java parser and AST visitor
│   ├── repository/          # Git repository management
│   ├── resources/           # MCP resource implementations
│   ├── tools/               # Legacy tool implementations
│   ├── utils/               # Helper utilities
│   ├── __main__.py          # Entry point
│   ├── server.py            # MCP server with tools/resources
│   └── server_factory.py    # Lazy FastMCP initialization
├── tests/                   # Test suite (mirrors src/ structure)
│   ├── config/
│   ├── context/
│   ├── indexer/
│   ├── logging/
│   ├── models/
│   ├── parser/
│   ├── repository/
│   ├── resources/
│   ├── server/
│   ├── tools/
│   └── utils/
├── misc/                    # Project metadata and plans
│   ├── memory/             # LLM understanding documents
│   └── tasks/              # Implementation plans and tasks
├── design/                  # Design documents
├── grammars/               # ANTLR4 Java grammar files (not in repo)
├── repositories/           # Cloned Java repos (gitignored)
├── config.yaml             # Server configuration
├── config.example.yaml     # Example configuration
└── pyproject.toml          # Poetry project definition
```

## Architecture

### Core Architecture Pattern

JavaMCP follows a **layered architecture** with clear separation of concerns:

1. **Entry Point** (`__main__.py`): Initializes logging → registers tools → initializes server state → starts FastMCP
2. **Server Layer** (`server.py`): Maintains global state (ServerState) and implements MCP tool/resource functions
3. **Factory Pattern** (`server_factory.py`): Lazy initialization of FastMCP to ensure logging is configured first
4. **Tool Layer** (`tools/`): Legacy tool implementations (NOTE: tools are now implemented directly in server.py)
5. **Domain Layers**: Repository management, parsing, indexing, context building

### Critical Initialization Order

**IMPORTANT:** Logging MUST be configured BEFORE FastMCP instance creation. The initialization sequence in `__main__.py` is:

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

This order ensures FastMCP library code uses the configured logging settings. **DO NOT** create the FastMCP instance before logging setup.

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

All MCP tools access this shared state via `get_state()`. The state is initialized once during server startup and remains global throughout the server lifecycle.

### Module Responsibilities

- **config/**: YAML/JSON configuration loading and Pydantic schemas
- **repository/**: Git repository cloning, updating, and Java file discovery
- **parser/**: ANTLR4-based Java source parsing, AST visiting, Javadoc extraction
- **indexer/**: In-memory API indexing and query engine for searching classes/methods
- **context/**: Building rich context (Javadocs, summaries) for MCP responses
- **resources/**: Project context resource implementation
- **models/**: Pydantic data models for Java entities and MCP protocol
- **logging/**: Centralized logging configuration and utilities

### Data Flow

1. **Initialization**: Config → RepositoryManager → clone repos → discover .java files
2. **Parsing**: Java files → ANTLR4 parser → AST → JavaSourceParser → JavaClass/JavaMethod models
3. **Indexing**: JavaClass objects → APIIndexer → in-memory indexes (by name, package, repository)
4. **Query**: MCP tool request → QueryEngine → search indexes → return results
5. **Context Building**: Results → ContextBuilder → enrich with Javadocs → format response

### Key Design Patterns

- **Factory Pattern**: `server_factory.py` for lazy FastMCP initialization
- **Singleton Pattern**: Global `_mcp_instance` and `ServerState`
- **Visitor Pattern**: `ast_visitor.py` for traversing ANTLR4 AST
- **Builder Pattern**: `ContextBuilder`, `ProjectContextBuilder` for constructing responses
- **Repository Pattern**: `RepositoryManager` for Git operations

## Configuration

The server uses YAML/JSON configuration (`config.yaml`):

```yaml
server:
  mode: stdio  # or "http"
  host: localhost
  port: 8000

repositories:
  urls:
    - https://github.com/apache/commons-lang.git
  local_base_path: ./repositories
  branch: main

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  output: console  # "console", "file", or "both"
  file_path: null
```

## MCP Tools and Resources

**4 MCP Tools** (all implemented in `server.py`):
1. `search_methods`: Search for methods by name with optional class filter
2. `analyze_class`: Get complete class information by fully-qualified name
3. `extract_apis`: Clone/parse repository and extract APIs
4. `generate_guide`: Generate usage guide based on use case description

**1 MCP Resource**:
- `javamcp://project/{repository_name}/context`: Get comprehensive project context including README, statistics, top classes, package summaries, and Javadoc coverage

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
3. Register tool in `register_tools_and_resources()` via `mcp.tool()(function_name)`
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
