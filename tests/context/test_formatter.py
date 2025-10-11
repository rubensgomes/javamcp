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
Unit tests for context formatters.
"""

from javamcp.context.formatter import (format_class_context,
                                       format_class_hierarchy,
                                       format_method_context,
                                       format_method_signature)
from javamcp.models.java_entities import (JavaAnnotation, JavaClass, JavaDoc,
                                          JavaField, JavaMethod, JavaParameter)


class TestFormatClassContext:
    """Tests for format_class_context function."""

    def test_format_basic_class(self):
        """Test formatting basic class without methods."""
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        result = format_class_context(java_class)

        assert "# com.example.TestClass" in result
        assert "**Type:** Class" in result
        assert "**Package:** com.example" in result

    def test_format_class_with_javadoc(self):
        """Test formatting class with javadoc."""
        javadoc = JavaDoc(
            summary="Test class summary",
            description="Detailed description of test class",
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            javadoc=javadoc,
        )

        result = format_class_context(java_class)

        assert "**Summary:** Test class summary" in result
        assert "**Description:**" in result
        assert "Detailed description of test class" in result

    def test_format_class_with_modifiers(self):
        """Test formatting class with modifiers."""
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            modifiers=["public", "final"],
        )

        result = format_class_context(java_class)

        assert "**Modifiers:** public, final" in result

    def test_format_class_with_annotations(self):
        """Test formatting class with annotations."""
        annotation = JavaAnnotation(name="Service", attributes={"value": "testService"})
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            annotations=[annotation],
        )

        result = format_class_context(java_class)

        assert "**Annotations:** Service" in result

    def test_format_class_with_inheritance(self):
        """Test formatting class with inheritance."""
        java_class = JavaClass(
            name="ChildClass",
            fully_qualified_name="com.example.ChildClass",
            package="com.example",
            extends="ParentClass",
            implements=["Serializable", "Comparable"],
        )

        result = format_class_context(java_class)

        assert "**Extends:** ParentClass" in result
        assert "**Implements:** Serializable, Comparable" in result

    def test_format_class_with_methods(self):
        """Test formatting class with methods."""
        javadoc = JavaDoc(summary="Test method")
        method = JavaMethod(
            name="testMethod",
            return_type="void",
            parameters=[],
            signature="void testMethod()",
            javadoc=javadoc,
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            methods=[method],
        )

        result = format_class_context(java_class)

        assert "## Methods" in result
        assert "### testMethod" in result
        assert "**Signature:** `void testMethod()`" in result
        assert "**Summary:** Test method" in result

    def test_format_class_with_fields(self):
        """Test formatting class with fields."""
        javadoc = JavaDoc(summary="Test field")
        field = JavaField(
            name="testField",
            type="String",
            modifiers=["private"],
            javadoc=javadoc,
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            fields=[field],
        )

        result = format_class_context(java_class)

        assert "## Fields" in result
        assert "- `String testField`" in result
        assert "- Test field" in result

    def test_format_interface(self):
        """Test formatting interface."""
        java_class = JavaClass(
            name="TestInterface",
            fully_qualified_name="com.example.TestInterface",
            package="com.example",
            is_interface=True,
        )

        result = format_class_context(java_class)

        assert "**Type:** Interface" in result

    def test_format_enum(self):
        """Test formatting enum."""
        java_class = JavaClass(
            name="TestEnum",
            fully_qualified_name="com.example.TestEnum",
            package="com.example",
            is_enum=True,
        )

        result = format_class_context(java_class)

        assert "**Type:** Enum" in result

    def test_format_abstract_class(self):
        """Test formatting abstract class."""
        java_class = JavaClass(
            name="AbstractClass",
            fully_qualified_name="com.example.AbstractClass",
            package="com.example",
            is_abstract=True,
        )

        result = format_class_context(java_class)

        assert "**Type:** Abstract Class" in result


class TestFormatMethodContext:
    """Tests for format_method_context function."""

    def test_format_basic_method(self):
        """Test formatting basic method."""
        method = JavaMethod(
            name="testMethod",
            return_type="void",
            parameters=[],
            signature="void testMethod()",
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        result = format_method_context(method, java_class)

        assert "# com.example.TestClass.testMethod" in result
        assert "**Signature:** `void testMethod()`" in result

    def test_format_method_with_javadoc(self):
        """Test formatting method with javadoc."""
        javadoc = JavaDoc(
            summary="Test method summary",
            description="Detailed method description",
        )
        method = JavaMethod(
            name="testMethod",
            return_type="void",
            parameters=[],
            signature="public void testMethod()",
            javadoc=javadoc,
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        result = format_method_context(method, java_class)

        assert "**Summary:** Test method summary" in result
        assert "**Description:**" in result
        assert "Detailed method description" in result

    def test_format_method_with_parameters(self):
        """Test formatting method with parameters."""
        javadoc = JavaDoc(
            summary="Test method",
            params={"param1": "First parameter", "param2": "Second parameter"},
        )
        param1 = JavaParameter(name="param1", type="String")
        param2 = JavaParameter(name="param2", type="int")
        method = JavaMethod(
            name="testMethod",
            return_type="void",
            parameters=[param1, param2],
            signature="public void testMethod(String param1, int param2)",
            javadoc=javadoc,
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        result = format_method_context(method, java_class)

        assert "**Parameters:**" in result
        assert "- `param1`: First parameter" in result
        assert "- `param2`: Second parameter" in result

    def test_format_method_with_return(self):
        """Test formatting method with return value."""
        javadoc = JavaDoc(
            summary="Test method",
            returns="The result value",
        )
        method = JavaMethod(
            name="testMethod",
            return_type="int",
            parameters=[],
            signature="public int testMethod()",
            javadoc=javadoc,
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        result = format_method_context(method, java_class)

        assert "**Returns:** The result value" in result

    def test_format_method_with_throws(self):
        """Test formatting method with throws clause."""
        javadoc = JavaDoc(
            summary="Test method",
            throws={"IOException": "When IO fails", "SQLException": "When SQL fails"},
        )
        method = JavaMethod(
            name="testMethod",
            return_type="void",
            parameters=[],
            signature="public void testMethod()",
            javadoc=javadoc,
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        result = format_method_context(method, java_class)

        assert "**Throws:**" in result
        assert "- `IOException`: When IO fails" in result
        assert "- `SQLException`: When SQL fails" in result

    def test_format_method_with_examples(self):
        """Test formatting method with examples."""
        javadoc = JavaDoc(
            summary="Test method",
            examples=["testMethod();", "int result = testMethod();"],
        )
        method = JavaMethod(
            name="testMethod",
            return_type="void",
            parameters=[],
            signature="public void testMethod()",
            javadoc=javadoc,
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        result = format_method_context(method, java_class)

        assert "**Examples:**" in result
        assert "```java" in result
        assert "testMethod();" in result

    def test_format_method_with_modifiers(self):
        """Test formatting method with modifiers."""
        method = JavaMethod(
            name="testMethod",
            return_type="void",
            parameters=[],
            signature="public static void testMethod()",
            modifiers=["public", "static"],
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        result = format_method_context(method, java_class)

        assert "**Modifiers:** public, static" in result

    def test_format_method_with_annotations(self):
        """Test formatting method with annotations."""
        annotation = JavaAnnotation(name="Override")
        method = JavaMethod(
            name="toString",
            return_type="String",
            parameters=[],
            signature="public String toString()",
            annotations=[annotation],
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        result = format_method_context(method, java_class)

        assert "**Annotations:** Override" in result


class TestFormatMethodSignature:
    """Tests for format_method_signature function."""

    def test_format_void_method(self):
        """Test formatting void method signature."""
        method = JavaMethod(
            name="testMethod",
            return_type="void",
            parameters=[],
        )

        result = format_method_signature(method)

        assert result == "void testMethod()"

    def test_format_method_with_return_type(self):
        """Test formatting method with return type."""
        method = JavaMethod(
            name="getValue",
            return_type="int",
            parameters=[],
        )

        result = format_method_signature(method)

        assert result == "int getValue()"

    def test_format_method_with_parameters(self):
        """Test formatting method with parameters."""
        param1 = JavaParameter(name="x", type="int")
        param2 = JavaParameter(name="y", type="int")
        method = JavaMethod(
            name="add",
            return_type="int",
            parameters=[param1, param2],
        )

        result = format_method_signature(method)

        assert result == "int add(int x, int y)"

    def test_format_method_with_complex_types(self):
        """Test formatting method with complex parameter types."""
        param1 = JavaParameter(name="list", type="List<String>")
        param2 = JavaParameter(name="map", type="Map<String, Integer>")
        method = JavaMethod(
            name="process",
            return_type="void",
            parameters=[param1, param2],
        )

        result = format_method_signature(method)

        assert result == "void process(List<String> list, Map<String, Integer> map)"


class TestFormatClassHierarchy:
    """Tests for format_class_hierarchy function."""

    def test_format_basic_class(self):
        """Test formatting basic class hierarchy."""
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        result = format_class_hierarchy(java_class)

        assert result == "TestClass"

    def test_format_class_with_extends(self):
        """Test formatting class with extends clause."""
        java_class = JavaClass(
            name="ChildClass",
            fully_qualified_name="com.example.ChildClass",
            package="com.example",
            extends="ParentClass",
        )

        result = format_class_hierarchy(java_class)

        assert result == "ChildClass extends ParentClass"

    def test_format_class_with_implements(self):
        """Test formatting class with implements clause."""
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            implements=["Serializable", "Comparable"],
        )

        result = format_class_hierarchy(java_class)

        assert result == "TestClass implements Serializable, Comparable"

    def test_format_class_with_extends_and_implements(self):
        """Test formatting class with both extends and implements."""
        java_class = JavaClass(
            name="ChildClass",
            fully_qualified_name="com.example.ChildClass",
            package="com.example",
            extends="ParentClass",
            implements=["Serializable", "Comparable"],
        )

        result = format_class_hierarchy(java_class)

        assert (
            result
            == "ChildClass extends ParentClass implements Serializable, Comparable"
        )
