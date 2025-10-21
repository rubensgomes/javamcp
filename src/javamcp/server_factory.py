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
Factory module for creating FastMCP server with proper logging initialization.

This module provides lazy initialization of the FastMCP server to ensure
logging is configured before FastMCP library code executes.
"""

from fastmcp import FastMCP

# Global server instance (initialized lazily)
_mcp_instance = None


def get_mcp_server() -> FastMCP:
    """
    Get or create the FastMCP server instance.

    This function provides lazy initialization to ensure logging is
    configured before FastMCP creates its loggers.

    Returns:
        FastMCP server instance
    """
    global _mcp_instance

    if _mcp_instance is None:
        _mcp_instance = FastMCP(
            name="JavaMCP",
            instructions="""
              This MCP server exposes Java APIs for AI assistants. The Java APIs
              are indexed from Java source code Git repositories.
              """,
        )

    return _mcp_instance
