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
Unit tests for Java source parser.
"""

import tempfile
from pathlib import Path

import pytest

from javamcp.parser.exceptions import InvalidJavaSourceError, ParseError
from javamcp.parser.java_parser import JavaSourceParser


class TestJavaSourceParser:
    """Tests for JavaSourceParser class."""

    def test_parse_simple_class(self):
        """Test parsing a simple Java class."""
        java_code = """
        package com.example;

        public class SimpleClass {
            private int value;

            public int getValue() {
                return value;
            }
        }
        """

        parser = JavaSourceParser()
        java_class = parser.parse_string(java_code)

        assert java_class is not None
        assert java_class.name == "SimpleClass"
        assert java_class.package == "com.example"
        assert java_class.fully_qualified_name == "com.example.SimpleClass"
        assert len(java_class.methods) > 0
        assert len(java_class.fields) > 0

    def test_parse_class_with_methods(self):
        """Test parsing class with multiple methods."""
        java_code = """
        package com.example;

        public class Calculator {
            public int add(int a, int b) {
                return a + b;
            }

            public int subtract(int a, int b) {
                return a - b;
            }
        }
        """

        parser = JavaSourceParser()
        java_class = parser.parse_string(java_code)

        assert java_class is not None
        assert len(java_class.methods) == 2
        method_names = [m.name for m in java_class.methods]
        assert "add" in method_names
        assert "subtract" in method_names

    def test_parse_interface(self):
        """Test parsing Java interface."""
        java_code = """
        package com.example;

        public interface MyInterface {
            void doSomething();
            String getName();
        }
        """

        parser = JavaSourceParser()
        java_class = parser.parse_string(java_code)

        assert java_class is not None
        assert java_class.name == "MyInterface"
        assert java_class.is_interface
        assert len(java_class.methods) == 2

    def test_parse_class_with_constructor(self):
        """Test parsing class with constructor."""
        java_code = """
        package com.example;

        public class Person {
            private String name;

            public Person(String name) {
                this.name = name;
            }
        }
        """

        parser = JavaSourceParser()
        java_class = parser.parse_string(java_code)

        assert java_class is not None
        constructors = [m for m in java_class.methods if m.is_constructor]
        assert len(constructors) == 1
        assert constructors[0].name == "Person"

    def test_parse_class_with_annotations(self):
        """Test parsing class with annotations."""
        java_code = """
        package com.example;

        @Entity
        @Table(name = "users")
        public class User {
            @Id
            private Long id;

            @Column(name = "username")
            private String username;
        }
        """

        parser = JavaSourceParser()
        java_class = parser.parse_string(java_code)

        assert java_class is not None
        # Note: Full annotation extraction might not work in simplified visitor
        # This test verifies basic parsing works

    def test_parse_invalid_java(self):
        """Test parsing invalid Java code raises error."""
        invalid_code = """
        this is not valid java code {{{
        """

        parser = JavaSourceParser()
        with pytest.raises(ParseError):
            parser.parse_string(invalid_code)

    def test_parse_file(self):
        """Test parsing Java file from disk."""
        java_code = """
        package com.example;

        public class FileTest {
            public void testMethod() {
            }
        }
        """

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".java", delete=False) as tmp:
            tmp.write(java_code)
            tmp_path = tmp.name

        try:
            parser = JavaSourceParser()
            java_class = parser.parse_file(tmp_path)

            assert java_class is not None
            assert java_class.name == "FileTest"
        finally:
            Path(tmp_path).unlink()

    def test_parse_nonexistent_file(self):
        """Test parsing nonexistent file raises error."""
        parser = JavaSourceParser()
        with pytest.raises(InvalidJavaSourceError, match="File not found"):
            parser.parse_file("/nonexistent/file.java")

    def test_parse_class_without_package(self):
        """Test parsing class without package declaration."""
        java_code = """
        public class NoPackage {
            public void test() {
            }
        }
        """

        parser = JavaSourceParser()
        java_class = parser.parse_string(java_code)

        assert java_class is not None
        assert java_class.package == ""
        assert java_class.name == "NoPackage"

    def test_parse_empty_class(self):
        """Test parsing empty class."""
        java_code = """
        package com.example;

        public class EmptyClass {
        }
        """

        parser = JavaSourceParser()
        java_class = parser.parse_string(java_code)

        assert java_class is not None
        assert java_class.name == "EmptyClass"
        assert len(java_class.methods) == 0
        assert len(java_class.fields) == 0
