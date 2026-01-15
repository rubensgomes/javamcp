# General Disclaimer
#
# **AI Generated Content**
#
# This project's source code and documentation were generated predominantly
# by an Artificial Intelligence Large Language Model (AI LLM). The project
# lead, [Rubens Gomes](https://rubensgomes.com), provided initial prompts,
# reviewed, and made refinements to the generated output. While human review and
# refinement have occurred, users should be aware that the output may contain
# inaccuracies, errors, or security vulnerabilities
#
# **Third-Party Content Notice**
#
# This software may include components or snippets derived from third-party
# sources. The software's users and distributors are responsible for ensuring
# compliance with any underlying licenses applicable to such components.
#
# **Copyright Status Statement**
#
# Copyright protection, if any, is limited to the original human contributions and
# modifications made to this project. The AI-generated portions of the code and
# documentation are not subject to copyright and are considered to be in the
# public domain.
#
# **Limitation of liability**
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR
# OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
#
# **No-Warranty Disclaimer**
#
# THIS SOFTWARE IS PROVIDED 'AS IS,' WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT.

"""
FastMCP server for exposing Java APIs to AI assistants.

This module uses lazy initialization via server_factory to ensure logging
is configured before FastMCP instantiation.
"""

from typing import Optional

from javamcp.config.loader import load_config
from javamcp.config.schema import ApplicationConfig, RepositoryConfig
from javamcp.context.context_builder import ContextBuilder
from javamcp.indexer.indexer import APIIndexer
from javamcp.indexer.query_engine import QueryEngine
from javamcp.logging import get_logger, log_tool_invocation
from javamcp.models.mcp_protocol import (
    AnalyzeClassRequest,
    AnalyzeClassResponse,
    ExtractApisRequest,
    ExtractApisResponse,
    GenerateGuideRequest,
    GenerateGuideResponse,
    ProjectContextResponse,
    SearchMethodsRequest,
    SearchMethodsResponse,
)
from javamcp.parser.java_parser import JavaSourceParser
from javamcp.repository.manager import RepositoryManager
from javamcp.resources.project_context_builder import ProjectContextBuilder
from javamcp.server_factory import get_mcp_server

# Module-level logger for server operations
logger = get_logger("server")


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
    logger.info("Initializing server with configuration from: %s", config_path)
    _state.config = load_config(config_path)

    logger.info(
        "Creating repository manager for %d repositories",
        len(_state.config.repositories.urls),
    )
    _state.repository_manager = RepositoryManager(_state.config.repositories)

    _state.indexer = APIIndexer()
    _state.query_engine = QueryEngine(_state.indexer)

    # Initialize repositories
    logger.info("Initializing repositories: %s", _state.config.repositories.urls)
    _state.repository_manager.initialize_repositories()

    logger.info("Server initialization complete")
    _state.initialized = True


def get_state() -> ServerState:
    """Get the current server state."""
    return _state


def register_tools_and_resources() -> None:
    """
    Register all MCP tools and resources with the FastMCP server.

    This function must be called after logging is configured to ensure
    the FastMCP instance is created with proper logging settings.
    """
    mcp = get_mcp_server()

    # Register tools
    mcp.tool()(search_methods)
    mcp.tool()(analyze_class)
    mcp.tool()(extract_apis)
    mcp.tool()(generate_guide)

    # Register resources
    mcp.resource("javamcp://project/{repository_name}/context")(get_project_context)


# Tool: Search Methods
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
    log_tool_invocation(
        logger,
        "search_methods",
        method_name=method_name,
        class_name=class_name,
        case_sensitive=case_sensitive,
    )

    if not _state.initialized:
        logger.warning("search_methods called but server not initialized")
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

    logger.info(
        "search_methods completed: found %d methods matching '%s'",
        len(methods_with_context),
        method_name,
    )
    return response.model_dump()


# Tool: Analyze Class
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
    log_tool_invocation(
        logger,
        "analyze_class",
        fully_qualified_name=fully_qualified_name,
        repository_name=repository_name,
    )

    if not _state.initialized:
        logger.warning("analyze_class called but server not initialized")
        return {"error": "Server not initialized", "found": False, "matches": 0}

    request = AnalyzeClassRequest(
        fully_qualified_name=fully_qualified_name,
        repository_name=repository_name,
    )

    context_builder = ContextBuilder()

    # Search for the class
    java_class = _state.query_engine.search_class(request.fully_qualified_name)

    if not java_class:
        logger.info("analyze_class: class '%s' not found", fully_qualified_name)
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

    logger.info(
        "analyze_class completed: found class '%s' with %d methods",
        fully_qualified_name,
        len(java_class.methods),
    )
    return response.model_dump()


# Tool: Extract APIs
def extract_apis(  # pylint: disable=too-many-locals
    repository_url: str,
    branch: Optional[str] = None,
    package_filter: Optional[str] = None,
    class_filter: Optional[str] = None,
) -> dict:
    """
    Extract Java APIs from a Git repository.

    Clones/updates repository, parses Java files, and indexes APIs with
    rich context including javadocs and API summaries.

    Args:
        repository_url: Git repository URL (required)
        branch: Branch name (default: None, which uses the remote's default branch)
        package_filter: Optional package name filter
        class_filter: Optional class name filter

    Returns:
        Dictionary with extracted classes and context
    """
    log_tool_invocation(
        logger,
        "extract_apis",
        repository_url=repository_url,
        branch=branch,
        package_filter=package_filter,
        class_filter=class_filter,
    )

    if not _state.initialized:
        logger.warning("extract_apis called but server not initialized")
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
    logger.info("extract_apis: found %d Java files in repository", len(java_files))

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

        except Exception as e:  # pylint: disable=broad-exception-caught
            # Log and skip files that fail to parse
            logger.warning("Failed to parse file %s: %s", java_file, e)
            continue

    # Build context for response
    for java_class in parsed_classes:
        context_builder.build_class_context(java_class)

    total_methods = sum(len(cls.methods) for cls in parsed_classes)

    # Get the actual branch from repository metadata
    repo_metadata = repo_manager.get_repository_metadata(request.repository_url)
    actual_branch = (
        repo_metadata.branch if repo_metadata else (request.branch or "unknown")
    )

    response = ExtractApisResponse(
        classes=[cls.model_dump() for cls in parsed_classes],
        total_classes=len(parsed_classes),
        total_methods=total_methods,
        repository_url=request.repository_url,
        branch=actual_branch,
    )

    logger.info(
        "extract_apis completed: extracted %d classes with %d methods from %s",
        len(parsed_classes),
        total_methods,
        repository_url,
    )
    return response.model_dump()


# Tool: Generate Guide
def generate_guide(  # pylint: disable=too-many-locals
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
    log_tool_invocation(
        logger,
        "generate_guide",
        use_case=use_case,
        repository_filter=repository_filter,
        max_results=max_results,
    )

    if not _state.initialized:
        logger.warning("generate_guide called but server not initialized")
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

    logger.info(
        "generate_guide: found %d relevant classes and %d relevant methods",
        len(relevant_classes),
        len(relevant_methods),
    )

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


# Resource: Project Context
def get_project_context(repository_name: str) -> str:
    """
    Get comprehensive project context for a Java API repository.

    Provides detailed information including README, llms.txt, API statistics,
    package summaries, top classes with Javadocs, and documentation coverage.

    Args:
        repository_name: Repository name (extracted from URL)

    Returns:
        JSON string with complete project context
    """
    logger.info("get_project_context invoked for repository: %s", repository_name)

    if not _state.initialized:
        logger.warning("get_project_context called but server not initialized")
        return '{"error": "Server not initialized"}'

    # Find repository by name
    metadata = _state.repository_manager.get_repository_by_name(repository_name)

    if not metadata:
        logger.warning(
            "get_project_context: repository '%s' not found", repository_name
        )
        return f'{{"error": "Repository not found: {repository_name}"}}'

    # Build project context
    context_builder = ProjectContextBuilder(
        _state.repository_manager,
        _state.indexer,
        _state.query_engine,
    )

    context = context_builder.build_project_context(metadata.url)

    # Return as formatted response
    response = ProjectContextResponse(**context)
    logger.info("get_project_context completed for repository: %s", repository_name)
    return response.model_dump_json(indent=2)
