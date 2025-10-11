# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Rubens Gomes
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
