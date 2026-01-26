# JavaMCP Codebase Workflow Analysis

## Executive Summary

JavaMCP uses a **lazy, on-demand** architecture:
- **Server startup**: Clones repositories but does NOT parse Java files
- **ANTLR4 parsing**: Only triggered by `extract_apis` tool
- **Indexing**: Happens during `extract_apis`, builds in-memory indices
- **Context building**: Happens in every MCP tool response to enrich output

---

## Complete Workflow: Start to End

### Phase 1: Server Startup (`__main__.py`)

```
Command: poetry run python -m javamcp --config config.yml

__main__.py:main()
  │
  ├─ 1. resolve_config_path() → Find config file
  │
  ├─ 2. load_config() → Parse YAML, create ApplicationConfig
  │
  ├─ 3. setup_logging() → Configure loggers BEFORE FastMCP
  │
  ├─ 4. register_tools_and_resources()
  │      └─ Creates FastMCP instance (lazy factory)
  │      └─ Registers 4 tools: search_methods, analyze_class, extract_apis, generate_guide
  │      └─ Registers 1 resource: javamcp://project/{name}/context
  │
  ├─ 5. setup_signal_handlers() → Graceful shutdown
  │
  ├─ 6. initialize_server()
  │      ├─ Create RepositoryManager
  │      ├─ Create APIIndexer (EMPTY)
  │      ├─ Create QueryEngine (wraps indexer)
  │      └─ initialize_repositories()
  │           └─ Clone/pull repos (Git only, NO parsing)
  │
  └─ 7. mcp.run() → Start FastMCP server (stdio or http)
```

**Key Point**: At startup, repositories are cloned but **no Java parsing or indexing occurs**. The indexer remains empty until tools are invoked.

---

### Phase 2: ANTLR4 Parser Execution

**When**: Only during `extract_apis` tool invocation

**Files Involved**:
- `src/javamcp/parser/java_parser.py` - Main orchestration
- `src/javamcp/parser/ast_visitor.py` - AST traversal
- `src/javamcp/antlr4/JavaLexer.py` - Generated lexer
- `src/javamcp/antlr4/JavaParser.py` - Generated parser

**Workflow**:
```
extract_apis(repository_url, package_filter, class_filter)
  │
  ├─ Clone/update repository
  ├─ get_java_files() → Find all .java files
  │
  └─ FOR EACH .java file:
       │
       └─ JavaSourceParser.parse_file(file_path)
            │
            ├─ FileStream(file_path) → Read file bytes
            │
            ├─ JavaLexer(input_stream)
            │    └─ Tokenizes Java source code
            │
            ├─ CommonTokenStream(lexer)
            │    └─ Creates token stream
            │
            ├─ JavaParser(token_stream)
            │    └─ parser.compilationUnit() ← PARSING HAPPENS HERE
            │
            ├─ Check for parse errors
            │
            ├─ _extract_package(tree) → Get package name
            ├─ _extract_imports(tree) → Get imports
            │
            └─ JavaASTVisitor.visit(tree)
                 │
                 ├─ Extract class/interface/enum declarations
                 ├─ Extract methods, fields, constructors
                 ├─ Extract modifiers, annotations
                 ├─ Extract parameters, return types
                 │
                 └─ Return JavaClass model
```

**Note**: Javadoc extraction from ANTLR4 is **not functional** - comments are hidden tokens that ANTLR4 doesn't expose to the AST.

---

### Phase 3: Indexer Execution

**When**: Immediately after parsing each Java file in `extract_apis`

**Files Involved**:
- `src/javamcp/indexer/indexer.py` - APIIndexer class
- `src/javamcp/indexer/query_engine.py` - QueryEngine class

**Workflow**:
```
After JavaSourceParser.parse_file() returns JavaClass:
  │
  └─ indexer.add_class(java_class, repository_url)
       │
       ├─ class_index[fqn] = java_class
       │    └─ Lookup by fully-qualified name
       │
       ├─ class_name_index[name].append(java_class)
       │    └─ Lookup by simple class name
       │
       ├─ package_index[package].append(java_class)
       │    └─ Lookup by package
       │
       ├─ repository_index[url].append(java_class)
       │    └─ Lookup by repository
       │
       └─ FOR EACH method in java_class.methods:
            ├─ method_index[method.name].append((java_class, method))
            └─ class_method_index[fqn].append(method)
```

**Indexer State**:
| Tool | Creates Index | Queries Index |
|------|---------------|---------------|
| `extract_apis` | YES | NO |
| `search_methods` | NO | YES |
| `analyze_class` | NO | YES |
| `generate_guide` | NO | YES |
| Project Resource | NO | YES |

---

### Phase 4: Context Execution

**When**: In EVERY MCP tool response to format output

**Files Involved**:
- `src/javamcp/context/context_builder.py` - ContextBuilder class
- `src/javamcp/context/formatter.py` - Output formatting
- `src/javamcp/resources/project_context_builder.py` - Project resource

**Workflow per Tool**:

```
search_methods:
  └─ query_engine.search_methods() → Returns [(JavaClass, JavaMethod), ...]
       └─ ContextBuilder.build_method_context(method, class)
            └─ Format signature, params, javadoc

analyze_class:
  └─ query_engine.search_class() → Returns JavaClass
       └─ ContextBuilder.build_class_context(class, include_methods=True)
            └─ Format class info, methods, fields, javadoc

extract_apis:
  └─ For each parsed JavaClass:
       └─ ContextBuilder.build_class_context(class)
            └─ Format for response

generate_guide:
  └─ query_engine.search_methods_partial() + get_classes_by_name()
       └─ ContextBuilder.build_api_summary(class)
            └─ Format usage guide

Project Resource:
  └─ ProjectContextBuilder.build_project_context(url)
       ├─ Read README.md content
       ├─ Read llms.txt content
       ├─ _build_api_statistics() → Query indexer
       ├─ _build_package_summary() → Query indexer
       ├─ _build_top_classes_summary() → Query + context
       └─ _calculate_javadoc_coverage() → Query indexer
```

---

## Complete Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SERVER STARTUP                                  │
│  ┌──────────┐    ┌─────────┐    ┌──────────┐    ┌───────────────┐           │
│  │  Config  │───▶│ Logging │───▶│ FastMCP  │───▶│ Repositories  │           │
│  │  Loader  │    │  Setup  │    │ Factory  │    │ (Git Clone)   │           │
│  └──────────┘    └─────────┘    └──────────┘    └───────────────┘           │
│                                                         │                    │
│                                              (NO PARSING YET)                │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MCP TOOL: extract_apis                             │
│                                                                              │
│  ┌──────────┐    ┌─────────┐    ┌──────────┐    ┌───────────┐               │
│  │ .java    │───▶│ ANTLR4  │───▶│   AST    │───▶│ JavaClass │               │
│  │ files    │    │ Lexer/  │    │ Visitor  │    │  Model    │               │
│  │          │    │ Parser  │    │          │    │           │               │
│  └──────────┘    └─────────┘    └──────────┘    └─────┬─────┘               │
│                                                       │                      │
│                                                       ▼                      │
│                                              ┌───────────────┐               │
│                                              │   APIIndexer  │               │
│                                              │  (populate)   │               │
│                                              └───────────────┘               │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MCP TOOLS: search_methods, analyze_class, generate_guide  │
│                                                                              │
│  ┌───────────────┐    ┌─────────────┐    ┌────────────────┐                 │
│  │  QueryEngine  │───▶│ JavaClass/  │───▶│ ContextBuilder │                 │
│  │   (search)    │    │ JavaMethod  │    │   (format)     │                 │
│  └───────────────┘    └─────────────┘    └────────────────┘                 │
│          │                                        │                          │
│          ▼                                        ▼                          │
│  ┌───────────────┐                      ┌────────────────┐                  │
│  │  APIIndexer   │                      │  MCP Response  │                  │
│  │   (lookup)    │                      │    (JSON)      │                  │
│  └───────────────┘                      └────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Key File Locations

| Component | Primary File | Line Reference |
|-----------|--------------|----------------|
| Entry Point | `src/javamcp/__main__.py` | `main()` at line 254 |
| Server Init | `src/javamcp/server.py` | `initialize_server()` at line 87 |
| FastMCP Factory | `src/javamcp/server_factory.py` | `get_mcp_server()` at line 51 |
| Java Parser | `src/javamcp/parser/java_parser.py` | `parse_file()` at line 67 |
| AST Visitor | `src/javamcp/parser/ast_visitor.py` | `JavaASTVisitor` class |
| Indexer | `src/javamcp/indexer/indexer.py` | `APIIndexer` at line 52 |
| Query Engine | `src/javamcp/indexer/query_engine.py` | `QueryEngine` at line 54 |
| Context Builder | `src/javamcp/context/context_builder.py` | `ContextBuilder` class |
| Project Context | `src/javamcp/resources/project_context_builder.py` | `ProjectContextBuilder` |
| Tool Implementations | `src/javamcp/server.py` | Lines 138-500 |

---

## Summary Table: When Each Component Executes

| Component | Startup | extract_apis | search_methods | analyze_class | generate_guide | Resource |
|-----------|---------|--------------|----------------|---------------|----------------|----------|
| Config Loader | YES | - | - | - | - | - |
| Logging Setup | YES | - | - | - | - | - |
| Repository Clone | YES | YES (temp) | - | - | - | - |
| **ANTLR4 Parser** | NO | **YES** | NO | NO | NO | NO |
| **Indexer Build** | NO | **YES** | NO | NO | NO | NO |
| Indexer Query | - | NO | YES | YES | YES | YES |
| **Context Build** | NO | **YES** | **YES** | **YES** | **YES** | **YES** |
