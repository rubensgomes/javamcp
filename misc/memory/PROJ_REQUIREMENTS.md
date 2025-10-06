# Understanding of REQUIREMENTS.md

**Source:** `design/REQUIREMENTS.md`

## Project Goal
Build an MCP (Model Context Protocol) server in Python to expose Java 21 APIs and javadocs to AI coding assistants.

## Core Functionality
- Fetch Java source files from public Git repositories
- Parse Java files using ANTLR4 (JavaLexer.py and JavaParser.py in `src/javamcp/antlr4`)
- Expose Java APIs and documentation as structured, queryable data

## MCP Server Tools
1. **Search methods** - by name, optionally filter by class name
2. **Analyze class** - by fully-qualified name, optionally filter by repository
3. **Extract APIs** - from specific Git repository/branch, optionally filter by package/class
4. **Generate usage guides** - based on use case/functionality, optionally focus on specific repository

## Exposed Information
- Packages, classes, methods, parameters, annotations, javadocs
- Contextual information about Java APIs via MCP protocol

## Technical Requirements
- JSON payloads conforming to well-defined schemas
- Configuration file (YAML or JSON) specifying:
  - Mode of operation (stdio or HTTP)
  - Server port (for HTTP mode)
  - List of public Git repository URLs to clone
  - Local path for cloned repositories
- Logging for operations, errors, and important events
- Modular and extensible design

## Quality Requirements
- Unit tests and integration tests
- Clear documentation for setup, configuration, and usage
- Examples of requests/responses for each tool
- Simplicity and ease of use prioritized

## Tech Stack
- **FastMCP** - MCP server framework
- **GitPython** - Git repository operations
- **ANTLR4** - Java source code parsing
- **Pydantic** - Data validation and models
- **Poetry** - Dependency management
