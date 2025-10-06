# JavaMCP

A Python-based MCP (Model Context Protocol) server that provides AI coding assistants with rich contextual information about Java APIs, including Javadocs, method signatures, class hierarchies, and usage examples.

## Features

- **4 MCP Tools** for comprehensive Java API exploration
- **Rich Context** with Javadoc summaries and API documentation
- **Git Repository Integration** for automatic code discovery
- **ANTLR4-based Parser** for accurate Java 21+ source code analysis
- **Comprehensive Indexing** for fast API lookups
- **Query Engine** with flexible search and filtering

## Installation

### Prerequisites

- Python 3.13+
- Poetry (for dependency management)
- ANTLR4 Java Grammars

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd javamcp
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Generate ANTLR4 Parser (one-time setup):**

   Download Java 21+ grammars from [ANTLR Grammars](https://github.com/antlr/grammars-v4/tree/master/java/java) to the project `grammars` folder:

   ```bash
   pushd grammars
   # Generate Python3 lexer and parser files into ../src/javamcp/antlr4
   antlr4 -Dlanguage=Python3 JavaLexer.g4 JavaParser.g4 -o ../src/javamcp/antlr4
   popd
   ```

## Configuration

Create a configuration file based on the examples:

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml` to add your Java repositories:

```yaml
server:
  mode: stdio

repositories:
  urls:
    - https://github.com/apache/commons-lang.git
    - https://github.com/google/guava.git
  local_base_path: ./repositories
  branch: main

logging:
  level: INFO
  output: console
```

## Usage

### Running the Server

```bash
poetry run python -m javamcp --config config.yaml
```

### MCP Tools

JavaMCP provides 4 MCP tools for AI assistants:

#### 1. Search Methods (`search_methods`)
Search for Java methods by name with full context.

**Request:**
```json
{
  "method_name": "substring",
  "class_name": "String",
  "case_sensitive": false
}
```

**Response:**
- Method signature
- Javadoc summary and description
- Parameter descriptions
- Return type documentation
- Containing class information

#### 2. Analyze Class (`analyze_class`)
Get complete information about a Java class.

**Request:**
```json
{
  "fully_qualified_name": "java.lang.String",
  "repository_name": "jdk"
}
```

**Response:**
- Class-level Javadoc
- All methods with Javadocs
- All fields with Javadocs
- Inheritance hierarchy
- Annotations

#### 3. Extract APIs (`extract_apis`)
Extract and index APIs from a Git repository.

**Request:**
```json
{
  "repository_url": "https://github.com/apache/commons-lang.git",
  "branch": "main",
  "package_filter": "org.apache.commons.lang3",
  "class_filter": "String"
}
```

**Response:**
- List of extracted classes with Javadocs
- Total classes and methods indexed
- API summaries

#### 4. Generate Usage Guide (`generate_guide`)
Generate usage guides for specific use cases.

**Request:**
```json
{
  "use_case": "How to manipulate strings",
  "max_results": 10
}
```

**Response:**
- Relevant classes and methods
- Javadoc-based usage examples
- Formatted guide with context

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src/javamcp --cov-report=term-missing

# Run specific test module
poetry run pytest tests/models/
```

### Code Quality

```bash
# Format code
poetry run black src/ tests/

# Lint
poetry run pylint src/javamcp

# Type checking
poetry run mypy src/

# Sort imports
poetry run isort src/ tests/
```

## Architecture

```
javamcp/
├── models/          # Pydantic data models
├── config/          # Configuration management
├── repository/      # Git repository operations
├── parser/          # ANTLR4 Java parser
├── indexer/         # API indexing and query engine
├── context/         # Context building and formatting
├── tools/           # MCP tool implementations
├── server/          # MCP server
├── logging/         # Logging utilities
└── utils/           # Helper utilities
```

## Test Coverage

- **247 tests** across all modules
- **95%+ average coverage** for production code
- Comprehensive unit and integration tests

## Contributing

Contributions are welcome! Please ensure:
- All tests pass
- Code coverage remains above 80%
- Code follows Black formatting
- Type hints are included

## License

[Apache Version 2.0 License](LICENSE)

## Author

[Rubens Gomes](https://rubensgomes.com/)
