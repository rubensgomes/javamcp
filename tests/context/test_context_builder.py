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
Unit tests for ContextBuilder.
"""

from javamcp.context.context_builder import ContextBuilder
from javamcp.models.java_entities import (
    JavaAnnotation,
    JavaClass,
    JavaDoc,
    JavaField,
    JavaMethod,
    JavaParameter,
)


class TestContextBuilder:
    """Tests for ContextBuilder class."""

    def test_build_class_context(self):
        """Test building class context."""
        builder = ContextBuilder()

        javadoc = JavaDoc(
            summary="Test class for examples", description="Detailed description"
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            javadoc=javadoc,
        )

        context = builder.build_class_context(java_class)

        assert context["name"] == "TestClass"
        assert context["fully_qualified_name"] == "com.example.TestClass"
        assert context["package"] == "com.example"
        assert context["summary"] == "Test class for examples"

    def test_build_class_context_with_annotations(self):
        """Test building class context with annotations."""
        builder = ContextBuilder()

        annotation = JavaAnnotation(name="Service", attributes={"value": "testService"})
        java_class = JavaClass(
            name="ServiceClass",
            fully_qualified_name="com.example.ServiceClass",
            package="com.example",
            annotations=[annotation],
        )

        context = builder.build_class_context(java_class)

        assert context["annotations"] == ["Service"]

    def test_build_class_context_with_inheritance(self):
        """Test building class context with inheritance info."""
        builder = ContextBuilder()

        java_class = JavaClass(
            name="ChildClass",
            fully_qualified_name="com.example.ChildClass",
            package="com.example",
            extends="com.example.ParentClass",
            implements=["Serializable", "Comparable"],
        )

        context = builder.build_class_context(java_class)

        assert context["inheritance"]["extends"] == "com.example.ParentClass"
        assert context["inheritance"]["implements"] == ["Serializable", "Comparable"]

    def test_build_class_context_with_methods(self):
        """Test building class context with methods."""
        builder = ContextBuilder()

        method = JavaMethod(
            name="testMethod",
            return_type="void",
            parameters=[],
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            methods=[method],
        )

        context = builder.build_class_context(java_class, include_methods=True)

        assert len(context["methods"]) == 1
        assert context["methods"][0]["name"] == "testMethod"

    def test_build_class_context_with_fields(self):
        """Test building class context with fields."""
        builder = ContextBuilder()

        field = JavaField(
            name="testField",
            type="String",
            modifiers=["private"],
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            fields=[field],
        )

        context = builder.build_class_context(java_class, include_methods=True)

        assert len(context["fields"]) == 1
        assert context["fields"][0]["name"] == "testField"
        assert context["fields"][0]["type"] == "String"

    def test_build_class_context_without_methods(self):
        """Test building class context without methods."""
        builder = ContextBuilder()

        method = JavaMethod(name="testMethod", return_type="void", parameters=[])
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            methods=[method],
        )

        context = builder.build_class_context(java_class, include_methods=False)

        assert "methods" not in context
        assert "fields" not in context

    def test_build_method_context(self):
        """Test building method context."""
        builder = ContextBuilder()

        javadoc = JavaDoc(
            summary="Calculates sum",
            params={"a": "First number", "b": "Second number"},
            returns="Sum of a and b",
        )
        param1 = JavaParameter(name="a", type="int")
        param2 = JavaParameter(name="b", type="int")
        method = JavaMethod(
            name="add",
            return_type="int",
            parameters=[param1, param2],
            javadoc=javadoc,
        )

        context = builder.build_method_context(method)

        assert context["name"] == "add"
        assert context["return_type"] == "int"
        assert len(context["parameters"]) == 2
        assert context["summary"] == "Calculates sum"
        assert context["return_description"] == "Sum of a and b"

    def test_build_method_context_with_containing_class(self):
        """Test building method context with containing class."""
        builder = ContextBuilder()

        method = JavaMethod(name="testMethod", return_type="void", parameters=[])
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        context = builder.build_method_context(method, containing_class=java_class)

        assert context["class_name"] == "TestClass"
        assert context["class_fqn"] == "com.example.TestClass"

    def test_build_method_context_with_throws(self):
        """Test building method context with throws clause."""
        builder = ContextBuilder()

        method = JavaMethod(
            name="riskyMethod",
            return_type="void",
            parameters=[],
            throws=["IOException", "SQLException"],
        )

        context = builder.build_method_context(method)

        assert context["throws"] == ["IOException", "SQLException"]

    def test_build_method_context_with_annotations(self):
        """Test building method context with annotations."""
        builder = ContextBuilder()

        annotation = JavaAnnotation(name="Override")
        method = JavaMethod(
            name="toString",
            return_type="String",
            parameters=[],
            annotations=[annotation],
        )

        context = builder.build_method_context(method)

        assert context["annotations"] == ["Override"]

    def test_build_method_context_constructor(self):
        """Test building method context for constructor."""
        builder = ContextBuilder()

        method = JavaMethod(
            name="TestClass",
            return_type="",
            parameters=[],
            is_constructor=True,
        )

        context = builder.build_method_context(method)

        assert context["is_constructor"] is True

    def test_build_api_summary(self):
        """Test building API summary."""
        builder = ContextBuilder()

        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        summary = builder.build_api_summary(java_class)

        assert isinstance(summary, str)
        assert "TestClass" in summary

    def test_build_method_summary(self):
        """Test building method summary."""
        builder = ContextBuilder()

        method = JavaMethod(name="testMethod", return_type="void", parameters=[])
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
        )

        summary = builder.build_method_summary(method, java_class)

        assert isinstance(summary, str)
        assert "testMethod" in summary

    def test_aggregate_class_contexts(self):
        """Test aggregating contexts for multiple classes."""
        builder = ContextBuilder()

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

        contexts = builder.aggregate_class_contexts([class1, class2])

        assert len(contexts) == 2
        assert contexts[0]["name"] == "Class1"
        assert contexts[1]["name"] == "Class2"

    def test_get_class_type_interface(self):
        """Test class type determination for interface."""
        builder = ContextBuilder()

        java_class = JavaClass(
            name="TestInterface",
            fully_qualified_name="com.example.TestInterface",
            package="com.example",
            is_interface=True,
        )

        context = builder.build_class_context(java_class)

        assert context["type"] == "interface"

    def test_get_class_type_enum(self):
        """Test class type determination for enum."""
        builder = ContextBuilder()

        java_class = JavaClass(
            name="TestEnum",
            fully_qualified_name="com.example.TestEnum",
            package="com.example",
            is_enum=True,
        )

        context = builder.build_class_context(java_class)

        assert context["type"] == "enum"

    def test_get_class_type_abstract(self):
        """Test class type determination for abstract class."""
        builder = ContextBuilder()

        java_class = JavaClass(
            name="AbstractClass",
            fully_qualified_name="com.example.AbstractClass",
            package="com.example",
            is_abstract=True,
        )

        context = builder.build_class_context(java_class)

        assert context["type"] == "abstract class"

    def test_get_class_type_regular(self):
        """Test class type determination for regular class."""
        builder = ContextBuilder()

        java_class = JavaClass(
            name="RegularClass",
            fully_qualified_name="com.example.RegularClass",
            package="com.example",
        )

        context = builder.build_class_context(java_class)

        assert context["type"] == "class"

    def test_format_javadoc_with_all_fields(self):
        """Test Javadoc formatting with all fields."""
        builder = ContextBuilder()

        javadoc = JavaDoc(
            summary="Test summary",
            description="Test description",
            params={"param1": "Parameter 1"},
            returns="Return value",
            throws={"IOException": "When IO fails"},
            see=["java.util.List"],
            since="1.0",
            deprecated="Use newMethod instead",
            author=["John Doe"],
            examples=["Example usage"],
        )

        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            javadoc=javadoc,
        )

        context = builder.build_class_context(java_class)

        assert context["javadoc"]["summary"] == "Test summary"
        assert context["javadoc"]["description"] == "Test description"
        assert context["javadoc"]["params"] == {"param1": "Parameter 1"}
        assert context["javadoc"]["returns"] == "Return value"
        assert context["javadoc"]["deprecated"] == "Use newMethod instead"

    def test_format_javadoc_none(self):
        """Test Javadoc formatting with None."""
        builder = ContextBuilder()

        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            javadoc=None,
        )

        context = builder.build_class_context(java_class)

        assert context["javadoc"] is None

    def test_get_param_description_exists(self):
        """Test getting parameter description when it exists."""
        builder = ContextBuilder()

        javadoc = JavaDoc(
            summary="Test method",
            params={"param1": "First parameter"},
        )
        param = JavaParameter(name="param1", type="String")
        method = JavaMethod(
            name="testMethod",
            return_type="void",
            parameters=[param],
            javadoc=javadoc,
        )

        context = builder.build_method_context(method)

        assert context["parameters"][0]["description"] == "First parameter"

    def test_get_param_description_not_exists(self):
        """Test getting parameter description when it doesn't exist."""
        builder = ContextBuilder()

        param = JavaParameter(name="param1", type="String")
        method = JavaMethod(
            name="testMethod",
            return_type="void",
            parameters=[param],
        )

        context = builder.build_method_context(method)

        assert context["parameters"][0]["description"] == ""

    def test_build_field_context_with_javadoc(self):
        """Test building field context with javadoc."""
        builder = ContextBuilder()

        javadoc = JavaDoc(summary="Test field")
        field = JavaField(
            name="testField",
            type="String",
            modifiers=["private", "final"],
            javadoc=javadoc,
        )
        java_class = JavaClass(
            name="TestClass",
            fully_qualified_name="com.example.TestClass",
            package="com.example",
            fields=[field],
        )

        context = builder.build_class_context(java_class, include_methods=True)

        assert context["fields"][0]["javadoc"]["summary"] == "Test field"
