# javamcp

The purpose of this project is to build an MCP (Model Context Protocol) server
in Python to expose Java 21 APIs (e.g., packages, classes, methods, and
javadocs) to AI coding assistants (e.g., Claude Code, GitHub Copilot). The
Java source files are extracted from public Git repositories and parsed
using ANTLR4 Java grammars Lexer and Parser.

## Pre-requisites

1. ANTLR Java Grammars

The Java 21+ grammars should be previously downloaded
from [ANTLR Grammars] (https://github.com/antlr/grammars-v4/tree/master/java/java)
to the project `grammars` folder. Then, the ANTLR4 tool should be used to
generate the Python JavaLexer/JavaParser source code files from the Java
grammar files.

For example:

```bash
pushd grammars
# generates Python3 lexer and parser files into ../src/javamcp/antlr4
antlr4 -Dlanguage=Python3 JavaLexer.g4 JavaParser.g4 -o ../src/javamcp/antlr4
popd
```

## Technology Stack

The technology stack can be found in
the [design/TECH_STACK.md](design/TECH_STACK.md) file.

## High Level Components

The high level description of components can be found in
the [design/COMPONENTS.md](design/COMPONENTS.md) file.

---
Author:  [Rubens Gomes](https://rubensgomes.com/)
