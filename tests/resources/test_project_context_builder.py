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
Tests for ProjectContextBuilder.
"""

from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest

from javamcp.indexer.indexer import APIIndexer
from javamcp.indexer.query_engine import QueryEngine
from javamcp.models.java_entities import JavaClass, JavaDoc, JavaMethod
from javamcp.models.repository import RepositoryMetadata
from javamcp.repository.manager import RepositoryManager
from javamcp.resources.project_context_builder import ProjectContextBuilder


@pytest.fixture
def mock_repository_manager():
    """Create mock repository manager."""
    manager = Mock(spec=RepositoryManager)
    metadata = RepositoryMetadata(
        url="https://github.com/test/repo.git",
        branch="main",
        local_path="/tmp/test-repo",
    )
    manager.get_repository_metadata.return_value = metadata
    return manager


@pytest.fixture
def mock_indexer():
    """Create mock API indexer."""
    return Mock(spec=APIIndexer)


@pytest.fixture
def mock_query_engine():
    """Create mock query engine."""
    return Mock(spec=QueryEngine)


@pytest.fixture
def sample_java_class():
    """Create sample Java class with Javadoc."""
    javadoc = JavaDoc(
        summary="Test class for demonstration",
        description="This is a test class",
    )
    method = JavaMethod(
        name="testMethod",
        return_type="void",
        javadoc=JavaDoc(summary="Test method"),
    )
    return JavaClass(
        name="TestClass",
        fully_qualified_name="com.example.TestClass",
        package="com.example",
        methods=[method],
        javadoc=javadoc,
    )


def test_build_project_context_success(
    mock_repository_manager,
    mock_indexer,
    mock_query_engine,
    sample_java_class,
    tmp_path,
):
    """Test successful project context building."""
    readme_path = tmp_path / "README.md"
    readme_path.write_text("# Test Repository\n\nThis is a test.")

    metadata = RepositoryMetadata(
        url="https://github.com/test/repo.git",
        branch="main",
        local_path=str(tmp_path),
    )
    mock_repository_manager.get_repository_metadata.return_value = metadata
    mock_query_engine.get_all_apis_from_repository.return_value = [sample_java_class]

    builder = ProjectContextBuilder(
        mock_repository_manager, mock_indexer, mock_query_engine
    )

    context = builder.build_project_context("https://github.com/test/repo.git")

    assert context["repository_name"] == "repo"
    assert context["repository_url"] == "https://github.com/test/repo.git"
    assert "Test Repository" in context["readme_content"]
    assert context["statistics"]["total_classes"] == 1
    assert context["statistics"]["total_methods"] == 1


def test_build_project_context_repository_not_found(
    mock_repository_manager, mock_indexer, mock_query_engine
):
    """Test project context when repository not found."""
    mock_repository_manager.get_repository_metadata.return_value = None

    builder = ProjectContextBuilder(
        mock_repository_manager, mock_indexer, mock_query_engine
    )

    context = builder.build_project_context("https://github.com/test/nonexistent.git")

    assert "error" in context
    assert "not found" in context["error"].lower()


def test_extract_readme_content(
    mock_repository_manager, mock_indexer, mock_query_engine, tmp_path
):
    """Test README extraction."""
    readme_path = tmp_path / "README.md"
    readme_content = "# My Project\n\nProject description here."
    readme_path.write_text(readme_content)

    builder = ProjectContextBuilder(
        mock_repository_manager, mock_indexer, mock_query_engine
    )

    content = builder._extract_readme_content(tmp_path)

    assert content == readme_content


def test_extract_readme_content_not_found(
    mock_repository_manager, mock_indexer, mock_query_engine, tmp_path
):
    """Test README extraction when file doesn't exist."""
    builder = ProjectContextBuilder(
        mock_repository_manager, mock_indexer, mock_query_engine
    )

    content = builder._extract_readme_content(tmp_path)

    assert content is None


def test_extract_llms_txt(
    mock_repository_manager, mock_indexer, mock_query_engine, tmp_path
):
    """Test llms.txt extraction."""
    llms_path = tmp_path / "llms.txt"
    llms_content = "Project context for LLMs"
    llms_path.write_text(llms_content)

    builder = ProjectContextBuilder(
        mock_repository_manager, mock_indexer, mock_query_engine
    )

    content = builder._extract_llms_txt(tmp_path)

    assert content == llms_content


def test_extract_llms_txt_not_found(
    mock_repository_manager, mock_indexer, mock_query_engine, tmp_path
):
    """Test llms.txt extraction when file doesn't exist."""
    builder = ProjectContextBuilder(
        mock_repository_manager, mock_indexer, mock_query_engine
    )

    content = builder._extract_llms_txt(tmp_path)

    assert content is None


def test_build_api_statistics(
    mock_repository_manager, mock_indexer, mock_query_engine, sample_java_class
):
    """Test API statistics building."""
    mock_query_engine.get_all_apis_from_repository.return_value = [
        sample_java_class,
        sample_java_class,
    ]

    builder = ProjectContextBuilder(
        mock_repository_manager, mock_indexer, mock_query_engine
    )

    stats = builder._build_api_statistics("https://github.com/test/repo.git")

    assert stats["total_classes"] == 2
    assert stats["total_methods"] == 2
    assert stats["total_packages"] == 1
    assert stats["average_methods_per_class"] == 1.0


def test_build_package_summary(
    mock_repository_manager, mock_indexer, mock_query_engine, sample_java_class
):
    """Test package summary building."""
    class1 = JavaClass(
        name="Class1",
        fully_qualified_name="com.example.Class1",
        package="com.example",
        methods=[JavaMethod(name="method1", return_type="void")],
    )
    class2 = JavaClass(
        name="Class2",
        fully_qualified_name="com.example.Class2",
        package="com.example",
        methods=[JavaMethod(name="method2", return_type="void")],
    )

    mock_query_engine.get_all_apis_from_repository.return_value = [class1, class2]

    builder = ProjectContextBuilder(
        mock_repository_manager, mock_indexer, mock_query_engine
    )

    packages = builder._build_package_summary("https://github.com/test/repo.git")

    assert len(packages) == 1
    assert packages[0]["name"] == "com.example"
    assert packages[0]["class_count"] == 2
    assert packages[0]["method_count"] == 2


def test_build_top_classes_summary(
    mock_repository_manager, mock_indexer, mock_query_engine, sample_java_class
):
    """Test top classes summary building."""
    mock_query_engine.get_all_apis_from_repository.return_value = [sample_java_class]

    builder = ProjectContextBuilder(
        mock_repository_manager, mock_indexer, mock_query_engine
    )

    top_classes = builder._build_top_classes_summary(
        "https://github.com/test/repo.git", limit=5
    )

    assert len(top_classes) == 1
    assert top_classes[0]["name"] == "TestClass"
    assert top_classes[0]["fully_qualified_name"] == "com.example.TestClass"
    assert "Test class" in top_classes[0]["summary"]


def test_calculate_javadoc_coverage(
    mock_repository_manager, mock_indexer, mock_query_engine, sample_java_class
):
    """Test Javadoc coverage calculation."""
    class_with_doc = sample_java_class
    class_without_doc = JavaClass(
        name="NoDocClass",
        fully_qualified_name="com.example.NoDocClass",
        package="com.example",
        methods=[JavaMethod(name="method", return_type="void")],
    )

    mock_query_engine.get_all_apis_from_repository.return_value = [
        class_with_doc,
        class_without_doc,
    ]

    builder = ProjectContextBuilder(
        mock_repository_manager, mock_indexer, mock_query_engine
    )

    coverage = builder._calculate_javadoc_coverage("https://github.com/test/repo.git")

    assert coverage["total_classes"] == 2
    assert coverage["documented_classes"] == 1
    assert coverage["class_documentation_rate"] == 50.0
    assert coverage["total_methods"] == 2
    assert coverage["documented_methods"] == 1
    assert coverage["method_documentation_rate"] == 50.0


def test_extract_repository_name(
    mock_repository_manager, mock_indexer, mock_query_engine
):
    """Test repository name extraction from URL."""
    builder = ProjectContextBuilder(
        mock_repository_manager, mock_indexer, mock_query_engine
    )

    name1 = builder._extract_repository_name("https://github.com/user/repo.git")
    assert name1 == "repo"

    name2 = builder._extract_repository_name("https://github.com/user/my-project")
    assert name2 == "my-project"


def test_format_project_description(
    mock_repository_manager, mock_indexer, mock_query_engine, tmp_path
):
    """Test project description formatting."""
    readme_path = tmp_path / "README.md"
    readme_path.write_text("# Test Project\n\nThis is a description.")

    mock_query_engine.get_all_apis_from_repository.return_value = []

    builder = ProjectContextBuilder(
        mock_repository_manager, mock_indexer, mock_query_engine
    )

    description = builder._format_project_description(
        "https://github.com/test/repo.git", tmp_path
    )

    assert "repo" in description
    assert "Total Classes: 0" in description
    assert "Test Project" in description
