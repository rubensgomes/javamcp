# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Rubens Gomes
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
FastMCP server for exposing Java APIs to AI assistants.
"""

from typing import Optional

from fastmcp import FastMCP

from javamcp.config.loader import load_config
from javamcp.config.schema import ApplicationConfig, RepositoryConfig
from javamcp.context.context_builder import ContextBuilder
from javamcp.indexer.indexer import APIIndexer
from javamcp.indexer.query_engine import QueryEngine
from javamcp.models.mcp_protocol import (AnalyzeClassRequest,
                                         AnalyzeClassResponse,
                                         ExtractApisRequest,
                                         ExtractApisResponse,
                                         GenerateGuideRequest,
                                         GenerateGuideResponse,
                                         SearchMethodsRequest,
                                         SearchMethodsResponse)
from javamcp.parser.java_parser import JavaSourceParser
from javamcp.repository.manager import RepositoryManager

# Create FastMCP server instance
mcp = FastMCP(
    name="JavaMCP",
    instructions="""
              This MCP server exposes Java APIs for AI assistants. The Java APIs
              are indexed from Java source code Git repositories.
              """,
)


# Global state for shared components
class ServerState:
    """Shared server state accessible to all tools."""

    config: Optional[ApplicationConfig] = None
    repository_manager: Optional[RepositoryManager] = None
    indexer: Optional[APIIndexer] = None
    query_engine: Optional[QueryEngine] = None
    initialized: bool = False


_state = ServerState()


def initialize_server(config_path: str = None) -> None:
    """
    Initialize the JavaMCP server with configuration.

    Args:
        config_path: Optional path to configuration file
    """
    _state.config = load_config(config_path)
    _state.repository_manager = RepositoryManager(_state.config.repositories)
    _state.indexer = APIIndexer()
    _state.query_engine = QueryEngine(_state.indexer)

    # Initialize repositories
    _state.repository_manager.initialize_repositories()

    _state.initialized = True


def get_state() -> ServerState:
    """Get the current server state."""
    return _state


# Tool: Search Methods
@mcp.tool()
def search_methods(
    method_name: str,
    class_name: Optional[str] = None,
    case_sensitive: bool = False,
) -> dict:
    """
    Search for Java methods by name with optional class filter.

    Provides rich context including method signatures, javadocs, parameters,
    and containing class information.

    Args:
        method_name: Method name to search for (required)
        class_name: Optional filter by class name
        case_sensitive: Whether search is case-sensitive (default: False)

    Returns:
        Dictionary with matching methods and context
    """
    if not _state.initialized:
        return {
            "error": "Server not initialized",
            "methods": [],
            "total_found": 0,
        }

    request = SearchMethodsRequest(
        method_name=method_name,
        class_name=class_name,
        case_sensitive=case_sensitive,
    )

    context_builder = ContextBuilder()

    # Search for methods
    results = _state.query_engine.search_methods(
        request.method_name,
        class_name=request.class_name,
        case_sensitive=request.case_sensitive,
    )

    # Build rich context for each method
    methods_with_context = []
    for java_class, method in results:
        context_builder.build_method_context(method, java_class)
        methods_with_context.append(method.model_dump())

    response = SearchMethodsResponse(
        methods=methods_with_context,
        total_found=len(methods_with_context),
        query=request,
    )

    return response.model_dump()


# Tool: Analyze Class
@mcp.tool()
def analyze_class(
    fully_qualified_name: str,
    repository_name: Optional[str] = None,
) -> dict:
    """
    Analyze a specific Java class by fully-qualified name.

    Provides complete class information including methods, fields, javadocs,
    inheritance hierarchy, and annotations.

    Args:
        fully_qualified_name: Fully-qualified class name (e.g., "java.util.ArrayList")
        repository_name: Optional filter by repository name

    Returns:
        Dictionary with complete class analysis and context
    """
    if not _state.initialized:
        return {"error": "Server not initialized", "found": False, "matches": 0}

    request = AnalyzeClassRequest(
        fully_qualified_name=fully_qualified_name,
        repository_name=repository_name,
    )

    context_builder = ContextBuilder()

    # Search for the class
    java_class = _state.query_engine.search_class(request.fully_qualified_name)

    if not java_class:
        response = AnalyzeClassResponse(found=False, matches=0)
        return response.model_dump()

    # If repository filter specified, verify class is from that repository
    if request.repository_name:
        repo_classes = _state.query_engine.filter_classes_by_repository(
            request.repository_name
        )
        if java_class not in repo_classes:
            response = AnalyzeClassResponse(found=False, matches=0)
            return response.model_dump()

    # Build rich context
    context_builder.build_class_context(java_class, include_methods=True)

    response = AnalyzeClassResponse(
        java_class=java_class,
        found=True,
        matches=1,
    )

    return response.model_dump()


# Tool: Extract APIs
@mcp.tool()
def extract_apis(
    repository_url: str,
    branch: str = "main",
    package_filter: Optional[str] = None,
    class_filter: Optional[str] = None,
) -> dict:
    """
    Extract Java APIs from a Git repository.

    Clones/updates repository, parses Java files, and indexes APIs with
    rich context including javadocs and API summaries.

    Args:
        repository_url: Git repository URL (required)
        branch: Branch name (default: "main")
        package_filter: Optional package name filter
        class_filter: Optional class name filter

    Returns:
        Dictionary with extracted classes and context
    """
    if not _state.initialized:
        return {
            "error": "Server not initialized",
            "classes": [],
            "total_classes": 0,
            "total_methods": 0,
        }

    request = ExtractApisRequest(
        repository_url=repository_url,
        branch=branch,
        package_filter=package_filter,
        class_filter=class_filter,
    )

    context_builder = ContextBuilder()

    # Initialize repository manager for this specific repo
    repo_config = RepositoryConfig(
        urls=[request.repository_url],
        local_base_path="./repositories",
    )
    repo_manager = RepositoryManager(repo_config)

    # Clone/update repository
    repo_manager.initialize_repositories()

    # Get Java files
    java_files = repo_manager.get_java_files(request.repository_url)

    # Filter by package if specified
    if request.package_filter:
        java_files = repo_manager.filter_java_files_by_package(
            request.repository_url, request.package_filter
        )

    # Parse Java files
    parser = JavaSourceParser()
    parsed_classes = []

    for java_file in java_files:
        try:
            java_class = parser.parse_file(str(java_file))

            # Filter by class name if specified
            if request.class_filter:
                if request.class_filter.lower() not in java_class.name.lower():
                    continue

            parsed_classes.append(java_class)

            # Index the class
            _state.indexer.add_class(java_class, request.repository_url)

        except Exception:  # pylint: disable=broad-exception-caught
            # Skip files that fail to parse
            continue

    # Build context for response
    for java_class in parsed_classes:
        context_builder.build_class_context(java_class)

    total_methods = sum(len(cls.methods) for cls in parsed_classes)

    response = ExtractApisResponse(
        classes=[cls.model_dump() for cls in parsed_classes],
        total_classes=len(parsed_classes),
        total_methods=total_methods,
        repository_url=request.repository_url,
        branch=request.branch,
    )

    return response.model_dump()


# Tool: Generate Guide
@mcp.tool()
def generate_guide(
    use_case: str,
    repository_filter: Optional[str] = None,
    max_results: int = 10,
) -> dict:
    """
    Generate an API usage guide based on a use case description.

    Searches for relevant APIs and creates a structured guide with
    javadoc-based examples, method descriptions, and usage patterns.

    Args:
        use_case: Description of use case or functionality (required)
        repository_filter: Optional filter to focus on specific repository
        max_results: Maximum number of relevant APIs to include (default: 10)

    Returns:
        Dictionary with formatted usage guide and relevant APIs
    """
    if not _state.initialized:
        return {
            "error": "Server not initialized",
            "guide": "",
            "relevant_classes": [],
            "relevant_methods": [],
        }

    request = GenerateGuideRequest(
        use_case=use_case,
        repository_filter=repository_filter,
        max_results=max_results,
    )

    context_builder = ContextBuilder()

    # Simple keyword-based search in use case
    keywords = _extract_keywords(request.use_case)

    relevant_classes = []
    relevant_methods = []

    # Search for relevant classes and methods based on keywords
    for keyword in keywords[: request.max_results]:
        # Search methods by partial name
        methods = _state.query_engine.search_methods_partial(
            keyword, case_sensitive=False
        )
        relevant_methods.extend([m for c, m in methods[: request.max_results]])

        # Search classes by name
        classes = _state.query_engine.get_classes_by_name(keyword, case_sensitive=False)
        relevant_classes.extend(classes[: request.max_results])

    # Limit results
    relevant_classes = relevant_classes[: request.max_results]
    relevant_methods = relevant_methods[: request.max_results]

    # Build formatted guide
    guide_lines = []
    guide_lines.append(f"# API Usage Guide: {request.use_case}")
    guide_lines.append("")

    if relevant_classes:
        guide_lines.append("## Relevant Classes")
        guide_lines.append("")
        for java_class in relevant_classes[:5]:
            summary = context_builder.build_api_summary(java_class)
            guide_lines.append(summary)
            guide_lines.append("")

    if relevant_methods:
        guide_lines.append("## Relevant Methods")
        guide_lines.append("")
        guide_lines.append("Found relevant methods for the use case.")
        guide_lines.append("")

    guide = "\n".join(guide_lines)

    response = GenerateGuideResponse(
        guide=guide,
        relevant_classes=[cls.model_dump() for cls in relevant_classes],
        relevant_methods=[m.model_dump() for m in relevant_methods],
        use_case=request.use_case,
    )

    return response.model_dump()


def _extract_keywords(use_case: str) -> list[str]:
    """Extract keywords from use case description."""
    words = use_case.lower().split()
    common_words = {
        "how",
        "to",
        "the",
        "a",
        "an",
        "is",
        "are",
        "for",
        "in",
        "on",
        "with",
    }
    keywords = [w for w in words if w not in common_words and len(w) > 2]
    return keywords
