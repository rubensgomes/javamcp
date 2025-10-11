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
Unit tests for repository models.
"""

from datetime import datetime

import pytest

from javamcp.models.java_entities import JavaClass, JavaMethod
from javamcp.models.repository import RepositoryIndex, RepositoryMetadata


class TestRepositoryMetadata:
    """Tests for RepositoryMetadata model."""

    def test_create_repository_metadata(self):
        """Test creating repository metadata."""
        metadata = RepositoryMetadata(
            url="https://github.com/example/repo.git",
            branch="main",
            local_path="/tmp/repo",
        )
        assert metadata.url == "https://github.com/example/repo.git"
        assert metadata.branch == "main"
        assert metadata.local_path == "/tmp/repo"

    def test_repository_metadata_with_timestamps(self):
        """Test repository metadata with timestamps."""
        now = datetime.now()
        metadata = RepositoryMetadata(
            url="https://github.com/example/repo.git",
            branch="main",
            local_path="/tmp/repo",
            last_cloned=now,
            last_updated=now,
            commit_hash="abc123",
        )
        assert metadata.last_cloned == now
        assert metadata.last_updated == now
        assert metadata.commit_hash == "abc123"


class TestRepositoryIndex:
    """Tests for RepositoryIndex model."""

    def test_create_empty_repository_index(self):
        """Test creating an empty repository index."""
        metadata = RepositoryMetadata(
            url="https://github.com/example/repo.git",
            branch="main",
            local_path="/tmp/repo",
        )
        index = RepositoryIndex(repository=metadata)
        assert index.classes == []
        assert index.total_files == 0
        assert index.total_classes == 0
        assert index.total_methods == 0

    def test_repository_index_with_classes(self):
        """Test repository index with classes."""
        metadata = RepositoryMetadata(
            url="https://github.com/example/repo.git",
            branch="main",
            local_path="/tmp/repo",
        )

        method1 = JavaMethod(name="method1", return_type="void")
        method2 = JavaMethod(name="method2", return_type="int")

        class1 = JavaClass(
            name="Class1",
            fully_qualified_name="com.example.Class1",
            package="com.example",
            methods=[method1],
        )
        class2 = JavaClass(
            name="Class2",
            fully_qualified_name="com.example.Class2",
            package="com.example",
            methods=[method2],
        )

        index = RepositoryIndex(
            repository=metadata,
            classes=[class1, class2],
            total_files=2,
        )
        assert len(index.classes) == 2
        assert index.total_files == 2

    def test_update_counts(self):
        """Test updating counts in repository index."""
        metadata = RepositoryMetadata(
            url="https://github.com/example/repo.git",
            branch="main",
            local_path="/tmp/repo",
        )

        method1 = JavaMethod(name="method1", return_type="void")
        method2 = JavaMethod(name="method2", return_type="int")
        method3 = JavaMethod(name="method3", return_type="String")

        class1 = JavaClass(
            name="Class1",
            fully_qualified_name="com.example.Class1",
            package="com.example",
            methods=[method1, method2],
        )
        class2 = JavaClass(
            name="Class2",
            fully_qualified_name="com.example.Class2",
            package="com.example",
            methods=[method3],
        )

        index = RepositoryIndex(repository=metadata, classes=[class1, class2])
        index.update_counts()

        assert index.total_classes == 2
        assert index.total_methods == 3
