# REQUIREMENTS

- I want an MCP (Model Context Protocol) server in Python to expose Java 21 APIs
  and javddocs to AI coding assistants.
- I want this server to fetch Java source files from public Git repositories,
  parse them using the ANTLR4 `JavaLexer.py` and `JavaParser.py` classes
  found in the project `src/javamcp/antlr4` folder.
- I want the Java APIs and documentation exposed as structured, queryable
  data.
- I want the MCP server to provide tools to:
    - Search for Java methods by name, optionally filtering by class name.
    - Analyze a specific Java class by its fully-qualified name, optionally
      filtering by repository name.
    - Extract Java APIs from a specific Git repository and branch, optionally
      filtering by package and class name.
    - Generate API usage guides based on a specific use case or functionality,
      optionally focusing on a specific repository.
- I want the MCP server to expose contextual information about Java APIs
  (e.g., packages, classes, methods, parameters, annotations, and javadocs)
  to AI coding assistants using the MCP protocol.
- I want the MCP server to handle requests and responses using JSON payloads
  that conform to well-defined schemas.
- I want the MCP server to be configurable via a configuration file (e.g.,
  YAML or JSON) that specifies:
    - The mode of operation (stdio or HTTP).
    - The server port (for HTTP mode).
    - The list of public Git repository URLs to clone and parse.
    - The local path to clone those repositories.
- I want the MCP server to log its operations, errors, and important events
  for monitoring and debugging purposes.
- I want the MCP server to be modular and extensible, allowing for easy
  addition of new features and tools in the future.
- I want the MCP server to include unit tests and integration tests to ensure
  its reliability and correctness.
- I want the MCP server to have clear documentation on how to set up, configure,
  and use it, including examples of requests and responses for each tool.
- I want the following Python packages to be used:
    - FastMCP: MCP server framework for AI assistant integration.
    - GitPython: Git repository operations and cloning.
    - ANTLR4: Java source code parsing using generated lexer/parser.
    - Pydantic: Data validation and structured data models.
    - Poetry: Dependency management and virtual environment.
- I want simplicity and ease of use to be prioritized in the design and
  implementation of the MCP server.
