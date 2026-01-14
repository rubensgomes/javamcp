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
Integration tests for MCP tools.
"""

from unittest.mock import MagicMock, patch

import pytest

from javamcp.context.context_builder import ContextBuilder
from javamcp.indexer.indexer import APIIndexer
from javamcp.indexer.query_engine import QueryEngine
from javamcp.models.java_entities import JavaClass, JavaDoc, JavaMethod, JavaParameter
from javamcp.models.mcp_protocol import (
    AnalyzeClassRequest,
    ExtractApisRequest,
    GenerateGuideRequest,
    SearchMethodsRequest,
)
from javamcp.tools.analyze_class import analyze_class_tool
from javamcp.tools.generate_guide import _extract_keywords, generate_guide_tool
from javamcp.tools.search_methods import search_methods_tool


@pytest.fixture
def sample_java_class():
    """Create a sample Java class for testing."""
    javadoc = JavaDoc(
        summary="Test class for examples",
        description="Detailed description",
    )
    method = JavaMethod(
        name="testMethod",
        return_type="void",
        parameters=[
            JavaParameter(name="param1", type="String"),
        ],
        javadoc=JavaDoc(
            summary="Test method",
            params={"param1": "First parameter"},
        ),
    )
    return JavaClass(
        name="TestClass",
        fully_qualified_name="com.example.TestClass",
        package="com.example",
        javadoc=javadoc,
        methods=[method],
    )


@pytest.fixture
def indexer_with_data(sample_java_class):
    """Create indexer with sample data."""
    indexer = APIIndexer()
    indexer.add_class(sample_java_class, "test-repo")
    return indexer


@pytest.fixture
def query_engine_with_data(indexer_with_data):
    """Create query engine with sample data."""
    return QueryEngine(indexer_with_data)


class TestSearchMethodsTool:
    """Tests for search_methods_tool function."""

    def test_search_methods_basic(self, query_engine_with_data):
        """Test basic method search."""
        request = SearchMethodsRequest(
            method_name="testMethod",
        )

        response = search_methods_tool(request, query_engine_with_data)

        assert response.total_found == 1
        assert len(response.methods) == 1
        assert response.query == request

    def test_search_methods_no_results(self, query_engine_with_data):
        """Test method search with no results."""
        request = SearchMethodsRequest(
            method_name="nonexistent",
        )

        response = search_methods_tool(request, query_engine_with_data)

        assert response.total_found == 0
        assert len(response.methods) == 0

    def test_search_methods_case_sensitive(self, query_engine_with_data):
        """Test case-sensitive method search."""
        request = SearchMethodsRequest(
            method_name="testmethod",
            case_sensitive=True,
        )

        response = search_methods_tool(request, query_engine_with_data)

        assert response.total_found == 0

    def test_search_methods_case_insensitive(self, query_engine_with_data):
        """Test case-insensitive method search."""
        request = SearchMethodsRequest(
            method_name="testmethod",
            case_sensitive=False,
        )

        response = search_methods_tool(request, query_engine_with_data)

        assert response.total_found == 1

    def test_search_methods_with_class_filter(self, query_engine_with_data):
        """Test method search with class filter."""
        request = SearchMethodsRequest(
            method_name="testMethod",
            class_name="TestClass",
        )

        response = search_methods_tool(request, query_engine_with_data)

        assert response.total_found == 1

    def test_search_methods_with_wrong_class_filter(self, query_engine_with_data):
        """Test method search with wrong class filter."""
        request = SearchMethodsRequest(
            method_name="testMethod",
            class_name="WrongClass",
        )

        response = search_methods_tool(request, query_engine_with_data)

        assert response.total_found == 0


class TestAnalyzeClassTool:
    """Tests for analyze_class_tool function."""

    def test_analyze_class_found(self, query_engine_with_data):
        """Test analyzing existing class."""
        request = AnalyzeClassRequest(
            fully_qualified_name="com.example.TestClass",
        )

        response = analyze_class_tool(request, query_engine_with_data)

        assert response.found is True
        assert response.matches == 1
        assert response.java_class is not None
        assert response.java_class.name == "TestClass"

    def test_analyze_class_not_found(self, query_engine_with_data):
        """Test analyzing non-existent class."""
        request = AnalyzeClassRequest(
            fully_qualified_name="com.example.NonExistent",
        )

        response = analyze_class_tool(request, query_engine_with_data)

        assert response.found is False
        assert response.matches == 0
        assert response.java_class is None

    def test_analyze_class_with_repository_filter_match(
        self, query_engine_with_data, sample_java_class
    ):
        """Test analyzing class with matching repository filter."""
        request = AnalyzeClassRequest(
            fully_qualified_name="com.example.TestClass",
            repository_name="test-repo",
        )

        response = analyze_class_tool(request, query_engine_with_data)

        assert response.found is True
        assert response.matches == 1

    def test_analyze_class_with_repository_filter_no_match(
        self, query_engine_with_data
    ):
        """Test analyzing class with non-matching repository filter."""
        from javamcp.indexer.exceptions import RepositoryNotIndexedError

        request = AnalyzeClassRequest(
            fully_qualified_name="com.example.TestClass",
            repository_name="wrong-repo",
        )

        # Should raise exception for non-existent repository
        with pytest.raises(RepositoryNotIndexedError):
            analyze_class_tool(request, query_engine_with_data)


class TestGenerateGuideTool:
    """Tests for generate_guide_tool function."""

    def test_generate_guide_basic(self, query_engine_with_data):
        """Test basic guide generation."""
        request = GenerateGuideRequest(
            use_case="How to use TestClass",
            max_results=10,
        )

        response = generate_guide_tool(request, query_engine_with_data)

        assert response.use_case == request.use_case
        assert response.guide is not None
        assert "API Usage Guide" in response.guide
        assert isinstance(response.relevant_classes, list)
        assert isinstance(response.relevant_methods, list)

    def test_generate_guide_finds_relevant_classes(self, query_engine_with_data):
        """Test that guide finds relevant classes."""
        request = GenerateGuideRequest(
            use_case="TestClass usage",
            max_results=10,
        )

        response = generate_guide_tool(request, query_engine_with_data)

        assert len(response.relevant_classes) > 0

    def test_generate_guide_with_max_results(self, query_engine_with_data):
        """Test guide generation with max results limit."""
        request = GenerateGuideRequest(
            use_case="How to use testMethod in TestClass",
            max_results=1,
        )

        response = generate_guide_tool(request, query_engine_with_data)

        assert len(response.relevant_classes) <= 1
        assert len(response.relevant_methods) <= 1

    def test_extract_keywords_basic(self):
        """Test keyword extraction."""
        use_case = "How to use String manipulation"

        keywords = _extract_keywords(use_case)

        assert "use" in keywords
        assert "string" in keywords
        assert "manipulation" in keywords
        assert "how" not in keywords
        assert "to" not in keywords

    def test_extract_keywords_filters_common_words(self):
        """Test that common words are filtered."""
        use_case = "the quick brown fox"

        keywords = _extract_keywords(use_case)

        assert "quick" in keywords
        assert "brown" in keywords
        assert "the" not in keywords

    def test_extract_keywords_filters_short_words(self):
        """Test that short words are filtered."""
        use_case = "a bb ccc"

        keywords = _extract_keywords(use_case)

        assert "a" not in keywords
        assert "bb" not in keywords
        assert "ccc" in keywords

    def test_generate_guide_empty_use_case(self, query_engine_with_data):
        """Test guide generation with empty use case."""
        request = GenerateGuideRequest(
            use_case="",
            max_results=10,
        )

        response = generate_guide_tool(request, query_engine_with_data)

        assert response.use_case == ""
        assert response.guide is not None


class TestExtractApisTool:
    """Tests for extract_apis_tool function."""

    @patch("javamcp.tools.extract_apis.RepositoryManager")
    @patch("javamcp.tools.extract_apis.JavaSourceParser")
    def test_extract_apis_basic(self, mock_parser_class, mock_repo_manager_class):
        """Test basic API extraction."""
        # Setup mocks
        mock_repo_manager = MagicMock()
        mock_repo_manager_class.return_value = mock_repo_manager
        mock_repo_manager.get_java_files.return_value = []

        indexer = APIIndexer()
        request = ExtractApisRequest(
            repository_url="https://github.com/example/repo.git",
            branch="main",
        )

        from javamcp.tools.extract_apis import extract_apis_tool

        response = extract_apis_tool(request, indexer)

        mock_repo_manager.initialize_repositories.assert_called_once()
        assert response.total_classes == 0
        assert response.total_methods == 0
        assert response.repository_url == request.repository_url

    @patch("javamcp.tools.extract_apis.RepositoryManager")
    @patch("javamcp.tools.extract_apis.JavaSourceParser")
    def test_extract_apis_parses_files(
        self, mock_parser_class, mock_repo_manager_class, sample_java_class, tmp_path
    ):
        """Test that API extraction parses files."""
        # Setup mocks
        mock_repo_manager = MagicMock()
        mock_repo_manager_class.return_value = mock_repo_manager

        java_file = tmp_path / "Test.java"
        java_file.write_text("public class Test {}")
        mock_repo_manager.get_java_files.return_value = [java_file]

        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        mock_parser.parse_file.return_value = sample_java_class

        indexer = APIIndexer()
        request = ExtractApisRequest(
            repository_url="https://github.com/example/repo.git",
            branch="main",
        )

        from javamcp.tools.extract_apis import extract_apis_tool

        response = extract_apis_tool(request, indexer)

        mock_parser.parse_file.assert_called_once()
        assert response.total_classes == 1
        assert len(indexer.class_index) == 1

    @patch("javamcp.tools.extract_apis.RepositoryManager")
    @patch("javamcp.tools.extract_apis.JavaSourceParser")
    def test_extract_apis_with_package_filter(
        self, mock_parser_class, mock_repo_manager_class
    ):
        """Test API extraction with package filter."""
        # Setup mocks
        mock_repo_manager = MagicMock()
        mock_repo_manager_class.return_value = mock_repo_manager
        mock_repo_manager.filter_java_files_by_package.return_value = []

        indexer = APIIndexer()
        request = ExtractApisRequest(
            repository_url="https://github.com/example/repo.git",
            branch="main",
            package_filter="com.example",
        )

        from javamcp.tools.extract_apis import extract_apis_tool

        response = extract_apis_tool(request, indexer)

        mock_repo_manager.filter_java_files_by_package.assert_called_once_with(
            request.repository_url, request.package_filter
        )

    @patch("javamcp.tools.extract_apis.RepositoryManager")
    @patch("javamcp.tools.extract_apis.JavaSourceParser")
    def test_extract_apis_with_class_filter(
        self, mock_parser_class, mock_repo_manager_class, sample_java_class, tmp_path
    ):
        """Test API extraction with class filter."""
        # Setup mocks
        mock_repo_manager = MagicMock()
        mock_repo_manager_class.return_value = mock_repo_manager

        java_file = tmp_path / "Test.java"
        java_file.write_text("public class Test {}")
        mock_repo_manager.get_java_files.return_value = [java_file]

        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser

        # Create class that doesn't match filter
        non_matching_class = JavaClass(
            name="OtherClass",
            fully_qualified_name="com.example.OtherClass",
            package="com.example",
        )
        mock_parser.parse_file.return_value = non_matching_class

        indexer = APIIndexer()
        request = ExtractApisRequest(
            repository_url="https://github.com/example/repo.git",
            branch="main",
            class_filter="Test",
        )

        from javamcp.tools.extract_apis import extract_apis_tool

        response = extract_apis_tool(request, indexer)

        # Class should be filtered out
        assert response.total_classes == 0

    @patch("javamcp.tools.extract_apis.RepositoryManager")
    @patch("javamcp.tools.extract_apis.JavaSourceParser")
    def test_extract_apis_handles_parse_errors(
        self, mock_parser_class, mock_repo_manager_class, tmp_path
    ):
        """Test that API extraction handles parse errors gracefully."""
        # Setup mocks
        mock_repo_manager = MagicMock()
        mock_repo_manager_class.return_value = mock_repo_manager

        java_file = tmp_path / "Test.java"
        java_file.write_text("invalid java")
        mock_repo_manager.get_java_files.return_value = [java_file]

        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        mock_parser.parse_file.side_effect = Exception("Parse error")

        indexer = APIIndexer()
        request = ExtractApisRequest(
            repository_url="https://github.com/example/repo.git",
            branch="main",
        )

        from javamcp.tools.extract_apis import extract_apis_tool

        response = extract_apis_tool(request, indexer)

        # Should handle error and continue
        assert response.total_classes == 0
