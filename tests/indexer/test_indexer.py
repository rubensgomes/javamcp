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
Unit tests for APIIndexer.
"""

import pytest

from javamcp.indexer.indexer import APIIndexer
from javamcp.models.java_entities import JavaClass, JavaMethod


class TestAPIIndexer:
    """Tests for APIIndexer class."""

    def test_init(self):
        """Test indexer initialization."""
        indexer = APIIndexer()
        assert not indexer.is_built()
        assert len(indexer.class_index) == 0

    def test_add_class(self):
        """Test adding a single class to index."""
        indexer = APIIndexer()

        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        indexer.add_class(java_class, "https://github.com/example/repo.git")

        assert indexer.is_built()
        assert indexer.get_total_classes() == 1
        assert indexer.get_class_by_fqn("com.example.TestClass") == java_class

    def test_add_classes(self):
        """Test adding multiple classes to index."""
        indexer = APIIndexer()

        class1 = JavaClass(
            name="Class1",
            fully_qualified_name="com.example.Class1",
            package="com.example",
        )
        class2 = JavaClass(
            name="Class2",
            fully_qualified_name="com.example.Class2",
            package="com.example",
        )

        indexer.add_classes([class1, class2], "https://github.com/example/repo.git")

        assert indexer.get_total_classes() == 2

    def test_index_methods(self):
        """Test indexing methods."""
        indexer = APIIndexer()

        method1 = JavaMethod(name="doSomething", return_type="void")
        method2 = JavaMethod(name="calculate", return_type="int")

        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            methods=[method1, method2],
        )

        indexer.add_class(java_class, "https://github.com/example/repo.git")

        assert indexer.get_total_methods() == 2
        methods = indexer.get_methods_by_name("doSomething")
        assert len(methods) == 1
        assert methods[0][1].name == "doSomething"

    def test_get_classes_by_name(self):
        """Test getting classes by simple name."""
        indexer = APIIndexer()

        class1 = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )
        class2 = JavaClass(
            name="TestClass",
            fully_qualified_name="org.other.TestClass",
            package="org.other",
        )

        indexer.add_class(class1, "https://github.com/example/repo.git")
        indexer.add_class(class2, "https://github.com/other/repo.git")

        classes = indexer.get_classes_by_name("TestClass")
        assert len(classes) == 2

    def test_get_classes_by_package(self):
        """Test getting classes by package."""
        indexer = APIIndexer()

        class1 = JavaClass(
            name="Class1",
            fully_qualified_name="com.example.Class1",
            package="com.example",
        )
        class2 = JavaClass(
            name="Class2",
            fully_qualified_name="com.example.Class2",
            package="com.example",
        )
        class3 = JavaClass(
            name="Class3",
            fully_qualified_name="org.other.Class3",
            package="org.other",
        )

        indexer.add_classes(
            [class1, class2, class3], "https://github.com/example/repo.git"
        )

        classes = indexer.get_classes_by_package("com.example")
        assert len(classes) == 2

    def test_get_classes_by_repository(self):
        """Test getting classes by repository."""
        indexer = APIIndexer()

        class1 = JavaClass(
            name="Class1",
            fully_qualified_name="com.example.Class1",
            package="com.example",
        )
        class2 = JavaClass(
            name="Class2",
            fully_qualified_name="org.other.Class2",
            package="org.other",
        )

        indexer.add_class(class1, "https://github.com/repo1.git")
        indexer.add_class(class2, "https://github.com/repo2.git")

        repo1_classes = indexer.get_classes_by_repository(
            "https://github.com/repo1.git"
        )
        assert len(repo1_classes) == 1
        assert repo1_classes[0].name == "Class1"

    def test_get_methods_by_class(self):
        """Test getting methods by class name."""
        indexer = APIIndexer()

        method1 = JavaMethod(name="method1", return_type="void")
        method2 = JavaMethod(name="method2", return_type="int")

        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            methods=[method1, method2],
        )

        indexer.add_class(java_class, "https://github.com/example/repo.git")

        methods = indexer.get_methods_by_class("com.example.TestClass")
        assert len(methods) == 2

    def test_reindex_repository(self):
        """Test re-indexing a repository."""
        indexer = APIIndexer()

        # Initial index
        class1 = JavaClass(
            name="Class1",
            fully_qualified_name="com.example.Class1",
            package="com.example",
        )
        indexer.add_class(class1, "https://github.com/repo.git")

        # Re-index with new classes
        class2 = JavaClass(
            name="Class2",
            fully_qualified_name="com.example.Class2",
            package="com.example",
        )
        indexer.reindex_repository("https://github.com/repo.git", [class2])

        # Old class should be gone
        assert indexer.get_class_by_fqn("com.example.Class1") is None
        # New class should be present
        assert indexer.get_class_by_fqn("com.example.Class2") is not None

    def test_clear(self):
        """Test clearing the index."""
        indexer = APIIndexer()

        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )
        indexer.add_class(java_class, "https://github.com/example/repo.git")

        assert indexer.is_built()
        indexer.clear()
        assert not indexer.is_built()
        assert indexer.get_total_classes() == 0

    def test_get_all_classes(self):
        """Test getting all classes."""
        indexer = APIIndexer()

        class1 = JavaClass(
            name="Class1",
            fully_qualified_name="com.example.Class1",
            package="com.example",
        )
        class2 = JavaClass(
            name="Class2",
            fully_qualified_name="com.example.Class2",
            package="com.example",
        )

        indexer.add_classes([class1, class2], "https://github.com/example/repo.git")

        all_classes = indexer.get_all_classes()
        assert len(all_classes) == 2
