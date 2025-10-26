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
Unit tests for MCP protocol models.
"""

import pytest
from pydantic import ValidationError

from javamcp.models.java_entities import JavaClass, JavaMethod
from javamcp.models.mcp_protocol import (AnalyzeClassRequest,
                                         AnalyzeClassResponse, ErrorResponse,
                                         ExtractApisRequest,
                                         ExtractApisResponse,
                                         GenerateGuideRequest,
                                         GenerateGuideResponse,
                                         SearchMethodsRequest,
                                         SearchMethodsResponse)


class TestSearchMethodsRequest:
    """Tests for SearchMethodsRequest model."""

    def test_create_search_methods_request(self):
        """Test creating a search methods request."""
        request = SearchMethodsRequest(method_name="findById")
        assert request.method_name == "findById"
        assert request.class_name is None
        assert not request.case_sensitive

    def test_search_methods_request_with_class_filter(self):
        """Test search request with class filter."""
        request = SearchMethodsRequest(method_name="save", class_name="UserRepository")
        assert request.class_name == "UserRepository"


class TestSearchMethodsResponse:
    """Tests for SearchMethodsResponse model."""

    def test_create_search_methods_response(self):
        """Test creating a search methods response."""
        request = SearchMethodsRequest(method_name="test")
        method = JavaMethod(name="test", return_type="void")
        response = SearchMethodsResponse(methods=[method], total_found=1, query=request)
        assert len(response.methods) == 1
        assert response.total_found == 1


class TestAnalyzeClassRequest:
    """Tests for AnalyzeClassRequest model."""

    def test_create_analyze_class_request(self):
        """Test creating an analyze class request."""
        request = AnalyzeClassRequest(fully_qualified_name="java.util.ArrayList")
        assert request.fully_qualified_name == "java.util.ArrayList"
        assert request.repository_name is None


class TestAnalyzeClassResponse:
    """Tests for AnalyzeClassResponse model."""

    def test_create_analyze_class_response_found(self):
        """Test creating an analyze class response when class is found."""
        java_class = JavaClass(
            name="ArrayList",
            fully_qualified_name="java.util.ArrayList",
            package="java.util",
        )
        response = AnalyzeClassResponse(java_class=java_class, found=True, matches=1)
        assert response.found
        assert response.matches == 1
        assert response.java_class is not None

    def test_create_analyze_class_response_not_found(self):
        """Test creating an analyze class response when class is not found."""
        response = AnalyzeClassResponse(found=False, matches=0)
        assert not response.found
        assert response.java_class is None


class TestExtractApisRequest:
    """Tests for ExtractApisRequest model."""

    def test_create_extract_apis_request(self):
        """Test creating an extract APIs request."""
        request = ExtractApisRequest(
            repository_url="https://github.com/example/repo.git"
        )
        assert request.repository_url == "https://github.com/example/repo.git"
        assert request.branch is None

    def test_extract_apis_request_with_filters(self):
        """Test extract APIs request with filters."""
        request = ExtractApisRequest(
            repository_url="https://github.com/example/repo.git",
            branch="develop",
            package_filter="com.example.service",
            class_filter="UserService",
        )
        assert request.branch == "develop"
        assert request.package_filter == "com.example.service"
        assert request.class_filter == "UserService"


class TestExtractApisResponse:
    """Tests for ExtractApisResponse model."""

    def test_create_extract_apis_response(self):
        """Test creating an extract APIs response."""
        java_class = JavaClass(
            name="MyClass",
            fully_qualified_name="com.example.MyClass",
            package="com.example",
        )
        response = ExtractApisResponse(
            classes=[java_class],
            total_classes=1,
            total_methods=0,
            repository_url="https://github.com/example/repo.git",
            branch="main",
        )
        assert len(response.classes) == 1
        assert response.total_classes == 1


class TestGenerateGuideRequest:
    """Tests for GenerateGuideRequest model."""

    def test_create_generate_guide_request(self):
        """Test creating a generate guide request."""
        request = GenerateGuideRequest(use_case="How to implement authentication")
        assert request.use_case == "How to implement authentication"
        assert request.max_results == 10

    def test_generate_guide_request_with_filter(self):
        """Test generate guide request with repository filter."""
        request = GenerateGuideRequest(
            use_case="Database operations",
            repository_filter="https://github.com/spring/spring-boot",
            max_results=5,
        )
        assert request.repository_filter == "https://github.com/spring/spring-boot"
        assert request.max_results == 5


class TestGenerateGuideResponse:
    """Tests for GenerateGuideResponse model."""

    def test_create_generate_guide_response(self):
        """Test creating a generate guide response."""
        response = GenerateGuideResponse(
            guide="Step 1: ...\nStep 2: ...",
            use_case="How to implement authentication",
        )
        assert "Step 1" in response.guide
        assert response.use_case == "How to implement authentication"


class TestErrorResponse:
    """Tests for ErrorResponse model."""

    def test_create_error_response(self):
        """Test creating an error response."""
        error = ErrorResponse(
            error="Class not found",
            error_code="NOT_FOUND",
            details="Class com.example.NonExistent does not exist",
        )
        assert error.error == "Class not found"
        assert error.error_code == "NOT_FOUND"
        assert error.details is not None
