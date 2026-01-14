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
MCP tool for searching Java methods by name.

NOTE: This tool is now implemented as a FastMCP decorated function in server.py.
This module is kept for backwards compatibility and testing purposes.
"""

from javamcp.context.context_builder import ContextBuilder
from javamcp.indexer.query_engine import QueryEngine
from javamcp.models.mcp_protocol import SearchMethodsRequest, SearchMethodsResponse


def search_methods_tool(
    request: SearchMethodsRequest, query_engine: QueryEngine
) -> SearchMethodsResponse:
    """
    Search for Java methods by name with optional class filter.

    Provides rich context including method signatures, javadocs, parameters,
    and containing class information.

    NOTE: For production use, the FastMCP tool in server.py should be used.
    This function is maintained for testing and backwards compatibility.

    Args:
        request: SearchMethodsRequest with method name and optional filters
        query_engine: QueryEngine instance for searching

    Returns:
        SearchMethodsResponse with matching methods and full context
    """
    context_builder = ContextBuilder()

    # Search for methods
    results = query_engine.search_methods(
        request.method_name,
        class_name=request.class_name,
        case_sensitive=request.case_sensitive,
    )

    # Build rich context for each method
    methods_with_context = []
    for java_class, method in results:
        # Add context to method
        context_builder.build_method_context(method, java_class)
        methods_with_context.append(method)

    return SearchMethodsResponse(
        methods=methods_with_context,
        total_found=len(methods_with_context),
        query=request,
    )
