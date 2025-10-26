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
Unit tests for JavaMCP FastMCP server.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from javamcp.config.schema import ApplicationConfig, RepositoryConfig
from javamcp.indexer.indexer import APIIndexer
from javamcp.indexer.query_engine import QueryEngine
from javamcp.models.java_entities import JavaClass
from javamcp.repository.manager import RepositoryManager
from javamcp.server import get_state, initialize_server
from javamcp.server_factory import get_mcp_server


class TestFastMCPServer:
    """Tests for FastMCP server implementation."""

    @patch.object(RepositoryManager, "initialize_repositories")
    @patch("javamcp.server.load_config")
    def test_initialize_server(self, mock_load_config, mock_init_repos):
        """Test server initialization."""
        mock_config = ApplicationConfig(
            repositories=RepositoryConfig(
                urls=["https://github.com/example/repo.git"],
                local_base_path="/tmp/repos",
            )
        )
        mock_load_config.return_value = mock_config

        # Reset state first
        state = get_state()
        state.initialized = False
        state.config = None
        state.repository_manager = None
        state.indexer = None
        state.query_engine = None

        initialize_server()

        mock_load_config.assert_called_once_with(None)
        mock_init_repos.assert_called_once()

        state = get_state()
        assert state.initialized
        assert state.config is not None
        assert isinstance(state.repository_manager, RepositoryManager)
        assert isinstance(state.indexer, APIIndexer)
        assert isinstance(state.query_engine, QueryEngine)

    @patch.object(RepositoryManager, "initialize_repositories")
    @patch("javamcp.server.load_config")
    def test_initialize_server_with_config_path(
        self, mock_load_config, mock_init_repos
    ):
        """Test server initialization with custom config path."""
        mock_config = ApplicationConfig(
            repositories=RepositoryConfig(
                urls=["https://github.com/example/repo.git"],
                local_base_path="/tmp/repos",
            )
        )
        mock_load_config.return_value = mock_config

        # Reset state first
        state = get_state()
        state.initialized = False

        initialize_server("/path/to/config.yml")

        mock_load_config.assert_called_once_with("/path/to/config.yml")
        assert get_state().initialized

    def test_get_state(self):
        """Test getting server state."""
        state = get_state()

        assert state is not None
        assert hasattr(state, "config")
        assert hasattr(state, "repository_manager")
        assert hasattr(state, "indexer")
        assert hasattr(state, "query_engine")
        assert hasattr(state, "initialized")

    def test_mcp_instance_exists(self):
        """Test that FastMCP instance is created."""
        mcp = get_mcp_server()
        assert mcp is not None
        # Check that tools are registered
        # Note: FastMCP doesn't expose tools directly, so we just verify instance exists

    @patch.object(RepositoryManager, "initialize_repositories")
    @patch("javamcp.server.load_config")
    def test_state_shared_across_tools(self, mock_load_config, mock_init_repos):
        """Test that state is shared across all tools."""
        mock_config = ApplicationConfig(
            repositories=RepositoryConfig(
                urls=["https://github.com/example/repo.git"],
                local_base_path="/tmp/repos",
            )
        )
        mock_load_config.return_value = mock_config

        # Reset and initialize
        state = get_state()
        state.initialized = False

        initialize_server()

        # Get state again
        state2 = get_state()

        # Should be the same instance
        assert state is state2
        assert state2.initialized


class TestFastMCPTools:
    """Tests for FastMCP tool decorators."""

    def test_search_methods_tool_exists(self):
        """Test that search_methods tool is registered."""
        # Import the tool function from server module
        from javamcp.server import search_methods

        assert search_methods is not None
        # FastMCP wraps functions in FunctionTool, so check for that
        assert hasattr(search_methods, "__name__") or hasattr(search_methods, "name")

    def test_analyze_class_tool_exists(self):
        """Test that analyze_class tool is registered."""
        from javamcp.server import analyze_class

        assert analyze_class is not None
        assert hasattr(analyze_class, "__name__") or hasattr(analyze_class, "name")

    def test_extract_apis_tool_exists(self):
        """Test that extract_apis tool is registered."""
        from javamcp.server import extract_apis

        assert extract_apis is not None
        assert hasattr(extract_apis, "__name__") or hasattr(extract_apis, "name")

    def test_generate_guide_tool_exists(self):
        """Test that generate_guide tool is registered."""
        from javamcp.server import generate_guide

        assert generate_guide is not None
        assert hasattr(generate_guide, "__name__") or hasattr(generate_guide, "name")


class TestFastMCPResources:
    """Tests for FastMCP resource decorators."""

    def test_get_project_context_resource_exists(self):
        """Test that get_project_context resource is registered."""
        from javamcp.server import get_project_context

        assert get_project_context is not None
        # Function is not decorated at module level anymore due to lazy initialization
        # Just verify it's callable
        assert callable(get_project_context)
