# JavaMCP

A Python-based AI MCP (Model Context Protocol) server that provides AI coding
assistant agents with rich contextual information about Java APIs found in Java
source code files stored in configured Git repositories.

The information gathered from the Java source code files includes Javadocs,
public method signatures, class hierarchies, and usage examples.

The intent is that, during the development of a Java application or library, we
can incorporate other Java APIs from libraries defined in the “javamcp”
MCP-configured Git repositories.

## Features

- **4 MCP Tools** for comprehensive Java API exploration
- **1 MCP Resource** for accessing comprehensive project context
- **Rich Context** with Javadoc summaries and API documentation
- **Git Repository Integration** for automatic code discovery
- **ANTLR4-based Parser** for accurate Java 21+ source code analysis
- **Comprehensive Indexing** for fast API lookups
- **Query Engine** with flexible search and filtering

## Installation

NOTE:  instructions provided for Unix-based systems (Linux, macOS) only.

### Prerequisites

- UNIX-based system (e.g., Linux, macOS)
- Python 3.14+

## Configuration

- Create and edit `~/.config/javamcp/config.yml` to add your Git 
  repositories. For example:

```yaml
# Configuration for JavaMCP Server

# Server configuration
server:
    mode: http # Server mode: "stdio" or "http"
    host: localhost  # Host for HTTP mode
    port: 8000  # Port for HTTP mode

# Repository configuration
repositories:
    # The default branch in the remote Git repository is cloned.  That is, 
    # the branch that remote's HEAD reference points to. Historically, this 
    # branch has most commonly been named master, but main has become an 
    # increasingly prevalent default in recent years, particularly on 
    # platforms like GitHub. Other names like trunk or development are also
    # used.

    urls:
        # TODO: Add your git repo URLs below.  For example:
        - https://github.com/apache/commons-lang.git
        - https://github.com/google/guava.git
    local_base_path: ./repositories  # Local directory for cloned repos

# Logging configuration
logging:
    level: DEBUG # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    output: both # Output: "stderr", "file", or "both"
    file_path: /tmp/javamcp.log # Log file path (required if output is "file" or "both")
```

## Usage

### Displaying the version

```bash
poetry run python -m javamcp --version
poetry run python -m javamcp -v
```

### Displaying the help

```bash
poetry run python -m javamcp --help
poetry run python -m javamcp -h
```

### Running the Server

```bash
poetry run python -m javamcp --config config.yml
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

### MCP Resources

JavaMCP provides 1 MCP resource for accessing project-level information:

#### Project Context Resource (`javamcp://project/{repository_name}/context`)

Access comprehensive contextual information about a Java API project.

**URI Pattern:**

```
javamcp://project/{repository_name}/context
```

**Parameters:**

- `repository_name`: Repository name (extracted from Git URL, e.g., "
  commons-lang" for "https://github.com/apache/commons-lang.git")

**Response includes:**

- **Repository Information**: Name and URL
- **Project Description**: Generated overview with statistics
- **README Content**: Full README.md file content (if available)
- **LLMs.txt Content**: Context file for LLMs (if available)
- **API Statistics**: Total classes, methods, packages, and averages
- **Package Summaries**: Package-level information with class and method counts
- **Top Classes**: Most significant classes with Javadocs
- **Documentation Coverage**: Javadoc coverage metrics for classes and methods

**Example Usage:**

If you have indexed `https://github.com/apache/commons-lang.git`, access its
context via:

```
javamcp://project/commons-lang/context
```

**Response Structure:**

```json
{
    "repository_name": "commons-lang",
    "repository_url": "https://github.com/apache/commons-lang.git",
    "description": "# commons-lang\n\nRepository: https://github.com/apache/commons-lang.git...",
    "readme_content": "# Apache Commons Lang...",
    "llms_txt_content": null,
    "statistics": {
        "total_classes": 150,
        "total_methods": 2500,
        "total_packages": 15,
        "average_methods_per_class": 16.67
    },
    "packages": [
        {
            "name": "org.apache.commons.lang3",
            "class_count": 50,
            "method_count": 800,
            "classes": [
                "StringUtils",
                "ArrayUtils",
                "ObjectUtils"
            ]
        }
    ],
    "top_classes": [
        {
            "name": "StringUtils",
            "fully_qualified_name": "org.apache.commons.lang3.StringUtils",
            "package": "org.apache.commons.lang3",
            "summary": "Operations on String that are null safe",
            "method_count": 120,
            "type": "class"
        }
    ],
    "javadoc_coverage": {
        "class_documentation_rate": 95.5,
        "method_documentation_rate": 87.3,
        "documented_classes": 143,
        "total_classes": 150,
        "documented_methods": 2183,
        "total_methods": 2500
    }
}
```

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

## Claude Code Commands

- Update `Claude Code` to the latest version:

    ```bash
    claude update
    ```

- List configure MCP servers:

    ```bash
    claude mcp list
    ```

- See `Claude Code` version:

    ```bash
    claude --version
    ```

- Start `Claude Code` in IDE mode:

    ```bash
    claude --verbose --debug ide
    ```

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rubensgomes/javamcp
   cd javamcp
   ```

2. Follow the instructions in the cloned repository `DEVSETUP.md` file.


---
Author:  [Rubens Gomes](https://rubensgomes.com/)
