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
MCP tool for analyzing a specific Java class.

NOTE: This tool is now implemented as a FastMCP decorated function in server.py.
This module is kept for backwards compatibility and testing purposes.
"""

from javamcp.context.context_builder import ContextBuilder
from javamcp.indexer.query_engine import QueryEngine
from javamcp.models.mcp_protocol import (AnalyzeClassRequest,
                                         AnalyzeClassResponse)


def analyze_class_tool(
    request: AnalyzeClassRequest, query_engine: QueryEngine
) -> AnalyzeClassResponse:
    """
    Analyze a specific Java class by fully-qualified name.

    Provides complete class information including methods, fields, javadocs,
    inheritance hierarchy, and annotations.

    NOTE: For production use, the FastMCP tool in server.py should be used.
    This function is maintained for testing and backwards compatibility.

    Args:
        request: AnalyzeClassRequest with class name and optional repository filter
        query_engine: QueryEngine instance for searching

    Returns:
        AnalyzeClassResponse with complete class analysis and context
    """
    context_builder = ContextBuilder()

    # Search for the class
    java_class = query_engine.search_class(request.fully_qualified_name)

    if not java_class:
        return AnalyzeClassResponse(found=False, matches=0)

    # If repository filter specified, verify class is from that repository
    if request.repository_name:
        repo_classes = query_engine.filter_classes_by_repository(
            request.repository_name
        )
        if java_class not in repo_classes:
            return AnalyzeClassResponse(found=False, matches=0)

    # Build rich context
    context_builder.build_class_context(java_class, include_methods=True)

    return AnalyzeClassResponse(
        java_class=java_class,
        found=True,
        matches=1,
    )
