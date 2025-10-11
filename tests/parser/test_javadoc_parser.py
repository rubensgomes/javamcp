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
