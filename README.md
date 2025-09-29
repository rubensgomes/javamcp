# javamcp

The purpose of this project is to build an MCP (Model Context Protocol) server in Python to expose Java 21 APIs. This MCP server is meant to expose Java API information, such as packages, classes, methods, and Javadoc to AI coding assistants. The Java APIs are extracted from Java source code stored in Git repositories.

## Pre-requisites

1. ANTLR Java Grammars

The Java 21+ grammars should be previously downloaded from [ANTLR Grammars] (https://github.com/antlr/grammars-v4/tree/master/java/java)  to the project `grammars` folder.  Then, the ANTLR4 tool should be used to generate the Python JavaLexter/JavaParser source code files from the Java grammar files. The generated lexer and parser code files are  expected to be previously placed in the project src `antlr4` folder.

For example:

```bash
pushd grammars
# generates Python3 lexer and parser files into ../src/javamcp/antlr4
antlr4 -Dlanguage=Python3 JavaLexer.g4 JavaParser.g4 -o ../src/javamcp/antlr4
popd
```

## Technology Stack

The technology stack can be found in the [design/TECH_STACK.md](design/TECH_STACK.md) file.

## High Level Components

The hih level components can be found in the [design/COMPONENTS.md](design/COMPONENTS.md) file.

---
Author:  [Rubens Gomes](https://rubensgomes.com/)
