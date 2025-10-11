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
Unit tests for Javadoc parser.
"""

import pytest

from javamcp.parser.javadoc_parser import parse_javadoc


class TestParseJavadoc:
    """Tests for parse_javadoc function."""

    def test_parse_empty_javadoc(self):
        """Test parsing empty Javadoc returns None."""
        result = parse_javadoc("")
        assert result is None

        result = parse_javadoc(None)
        assert result is None

    def test_parse_simple_javadoc(self):
        """Test parsing simple Javadoc with summary only."""
        javadoc_text = """
        /**
         * This is a summary.
         */
        """
        result = parse_javadoc(javadoc_text)

        assert result is not None
        assert "summary" in result.summary.lower()

    def test_parse_javadoc_with_params(self):
        """Test parsing Javadoc with @param tags."""
        javadoc_text = """
        /**
         * Calculates the sum.
         * @param a First number
         * @param b Second number
         */
        """
        result = parse_javadoc(javadoc_text)

        assert result is not None
        assert len(result.params) == 2
        assert "a" in result.params
        assert "b" in result.params
        assert "First number" in result.params["a"]

    def test_parse_javadoc_with_return(self):
        """Test parsing Javadoc with @return tag."""
        javadoc_text = """
        /**
         * Gets the value.
         * @return The current value
         */
        """
        result = parse_javadoc(javadoc_text)

        assert result is not None
        assert "current value" in result.returns.lower()

    def test_parse_javadoc_with_throws(self):
        """Test parsing Javadoc with @throws tags."""
        javadoc_text = """
        /**
         * Processes data.
         * @throws IOException If file cannot be read
         * @throws IllegalArgumentException If input is invalid
         */
        """
        result = parse_javadoc(javadoc_text)

        assert result is not None
        assert len(result.throws) == 2
        assert "IOException" in result.throws
        assert "IllegalArgumentException" in result.throws

    def test_parse_javadoc_with_see(self):
        """Test parsing Javadoc with @see tags."""
        javadoc_text = """
        /**
         * Related method.
         * @see OtherClass#method()
         */
        """
        result = parse_javadoc(javadoc_text)

        assert result is not None
        assert len(result.see) == 1
        assert "OtherClass" in result.see[0]

    def test_parse_javadoc_with_since(self):
        """Test parsing Javadoc with @since tag."""
        javadoc_text = """
        /**
         * New feature.
         * @since 1.5
         */
        """
        result = parse_javadoc(javadoc_text)

        assert result is not None
        assert result.since == "1.5"

    def test_parse_javadoc_with_deprecated(self):
        """Test parsing Javadoc with @deprecated tag."""
        javadoc_text = """
        /**
         * Old method.
         * @deprecated Use newMethod() instead
         */
        """
        result = parse_javadoc(javadoc_text)

        assert result is not None
        assert "newMethod" in result.deprecated

    def test_parse_javadoc_with_author(self):
        """Test parsing Javadoc with @author tags."""
        javadoc_text = """
        /**
         * My class.
         * @author John Doe
         * @author Jane Smith
         */
        """
        result = parse_javadoc(javadoc_text)

        assert result is not None
        assert len(result.author) == 2
        assert "John Doe" in result.author

    def test_parse_complete_javadoc(self):
        """Test parsing complete Javadoc with all tags."""
        javadoc_text = """
        /**
         * Processes the user input and returns a result.
         *
         * This method validates the input, performs processing,
         * and returns the computed result.
         *
         * @param input The user input string
         * @param options Processing options
         * @return The processed result
         * @throws IOException If processing fails
         * @throws IllegalArgumentException If input is invalid
         * @see ProcessorUtils
         * @since 2.0
         * @author John Doe
         */
        """
        result = parse_javadoc(javadoc_text)

        assert result is not None
        assert "processes" in result.summary.lower()
        assert "validates" in result.description.lower()
        assert len(result.params) == 2
        assert "input" in result.params
        assert result.returns != ""
        assert len(result.throws) == 2
        assert len(result.see) == 1
        assert result.since == "2.0"
        assert len(result.author) == 1
