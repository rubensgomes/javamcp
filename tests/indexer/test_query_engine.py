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
Unit tests for QueryEngine.
"""

import pytest

from javamcp.indexer.exceptions import IndexNotBuiltError, RepositoryNotIndexedError
from javamcp.indexer.indexer import APIIndexer
from javamcp.indexer.query_engine import QueryEngine
from javamcp.models.java_entities import JavaClass, JavaMethod


class TestQueryEngine:
    """Tests for QueryEngine class."""

    def test_init(self):
        """Test query engine initialization."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)
        assert engine.indexer == indexer

    def test_search_methods_not_built(self):
        """Test searching methods on unbuilt index raises error."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

        with pytest.raises(IndexNotBuiltError):
            engine.search_methods("test")

    def test_search_methods_exact(self):
        """Test exact method name search."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

        method = JavaMethod(name="doSomething", return_type="void")
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            methods=[method],
        )

        indexer.add_class(java_class, "https://github.com/example/repo.git")

        results = engine.search_methods("doSomething")
        assert len(results) == 1
        assert results[0][1].name == "doSomething"

    def test_search_methods_case_insensitive(self):
        """Test case-insensitive method search."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

        method = JavaMethod(name="doSomething", return_type="void")
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            methods=[method],
        )

        indexer.add_class(java_class, "https://github.com/example/repo.git")

        results = engine.search_methods("dosomething", case_sensitive=False)
        assert len(results) == 1

    def test_search_methods_with_class_filter(self):
        """Test method search with class filter."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

        method1 = JavaMethod(name="test", return_type="void")
        method2 = JavaMethod(name="test", return_type="int")

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

        indexer.add_classes([class1, class2], "https://github.com/example/repo.git")

        results = engine.search_methods("test", class_name="Class1")
        assert len(results) == 1
        assert results[0][0].name == "Class1"

    def test_search_methods_partial(self):
        """Test partial method name search."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

        method1 = JavaMethod(name="getUserName", return_type="String")
        method2 = JavaMethod(name="getUserAge", return_type="int")
        method3 = JavaMethod(name="setName", return_type="void")

        java_class = JavaClass(
            name="User",
            fully_qualified_name="com.example.User",
            package="com.example",
            methods=[method1, method2, method3],
        )

        indexer.add_class(java_class, "https://github.com/example/repo.git")

        results = engine.search_methods_partial("getUser")
        assert len(results) == 2

    def test_search_class(self):
        """Test searching for a class."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        indexer.add_class(java_class, "https://github.com/example/repo.git")

        result = engine.search_class("com.example.TestClass")
        assert result is not None
        assert result.name == "TestClass"

    def test_search_class_case_insensitive(self):
        """Test case-insensitive class search."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        indexer.add_class(java_class, "https://github.com/example/repo.git")

        result = engine.search_class("com.example.testclass", case_sensitive=False)
        assert result is not None

    def test_filter_classes_by_repository(self):
        """Test filtering classes by repository."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

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

        results = engine.filter_classes_by_repository("https://github.com/repo1.git")
        assert len(results) == 1
        assert results[0].name == "Class1"

    def test_filter_classes_by_repository_not_indexed(self):
        """Test filtering by non-indexed repository raises error."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

        java_class = JavaClass(
            name="Class1",
            fully_qualified_name="com.example.Class1",
            package="com.example",
        )
        indexer.add_class(java_class, "https://github.com/repo1.git")

        with pytest.raises(RepositoryNotIndexedError):
            engine.filter_classes_by_repository("https://github.com/other.git")

    def test_filter_classes_by_package(self):
        """Test filtering classes by package."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

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

        results = engine.filter_classes_by_package("com.example")
        assert len(results) == 2

    def test_filter_classes_by_package_with_repository(self):
        """Test filtering by package with repository filter."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

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

        indexer.add_class(class1, "https://github.com/repo1.git")
        indexer.add_class(class2, "https://github.com/repo2.git")

        results = engine.filter_classes_by_package(
            "com.example", repository_url="https://github.com/repo1.git"
        )
        assert len(results) == 1
        assert results[0].name == "Class1"

    def test_get_all_apis_from_repository(self):
        """Test getting all APIs from repository."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

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

        results = engine.get_all_apis_from_repository(
            "https://github.com/example/repo.git"
        )
        assert len(results) == 2

    def test_get_all_apis_from_package(self):
        """Test getting all APIs from package in repository."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

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

        results = engine.get_all_apis_from_package(
            "com.example", "https://github.com/example/repo.git"
        )
        assert len(results) == 2

    def test_get_classes_by_name(self):
        """Test getting classes by simple name."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

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

        indexer.add_class(class1, "https://github.com/repo1.git")
        indexer.add_class(class2, "https://github.com/repo2.git")

        results = engine.get_classes_by_name("TestClass")
        assert len(results) == 2

    def test_get_statistics(self):
        """Test getting index statistics."""
        indexer = APIIndexer()
        engine = QueryEngine(indexer)

        method1 = JavaMethod(name="method1", return_type="void")
        method2 = JavaMethod(name="method2", return_type="int")

        class1 = JavaClass(
            name="Class1",
            fully_qualified_name="com.example.Class1",
            package="com.example",
            methods=[method1, method2],
        )

        indexer.add_class(class1, "https://github.com/example/repo.git")

        stats = engine.get_statistics()
        assert stats["total_classes"] == 1
        assert stats["total_methods"] == 2
        assert stats["total_repositories"] == 1
        assert stats["total_packages"] == 1
