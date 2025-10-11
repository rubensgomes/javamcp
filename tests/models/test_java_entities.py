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
Unit tests for Java entity models.
"""

import pytest
from pydantic import ValidationError

from javamcp.models.java_entities import (JavaAnnotation, JavaClass, JavaDoc,
                                          JavaField, JavaMethod, JavaPackage,
                                          JavaParameter)


class TestJavaAnnotation:
    """Tests for JavaAnnotation model."""

    def test_create_simple_annotation(self):
        """Test creating a simple annotation without parameters."""
        annotation = JavaAnnotation(name="@Override")
        assert annotation.name == "@Override"
        assert annotation.parameters == {}

    def test_create_annotation_with_parameters(self):
        """Test creating an annotation with parameters."""
        annotation = JavaAnnotation(
            name="@RequestMapping", parameters={"value": "/api", "method": "GET"}
        )
        assert annotation.name == "@RequestMapping"
        assert annotation.parameters["value"] == "/api"
        assert annotation.parameters["method"] == "GET"


class TestJavaDoc:
    """Tests for JavaDoc model."""

    def test_create_empty_javadoc(self):
        """Test creating an empty JavaDoc."""
        javadoc = JavaDoc()
        assert javadoc.summary == ""
        assert javadoc.description == ""
        assert javadoc.params == {}
        assert javadoc.returns == ""

    def test_create_complete_javadoc(self):
        """Test creating a complete JavaDoc."""
        javadoc = JavaDoc(
            summary="Calculates the sum",
            description="This method calculates the sum of two integers.",
            params={"a": "First number", "b": "Second number"},
            returns="The sum of a and b",
            throws={"IllegalArgumentException": "If inputs are negative"},
            see=["Math.add"],
            since="1.0",
            author=["John Doe"],
        )
        assert javadoc.summary == "Calculates the sum"
        assert javadoc.params["a"] == "First number"
        assert javadoc.returns == "The sum of a and b"


class TestJavaParameter:
    """Tests for JavaParameter model."""

    def test_create_simple_parameter(self):
        """Test creating a simple parameter."""
        param = JavaParameter(name="count", type="int")
        assert param.name == "count"
        assert param.type == "int"
        assert param.annotations == []

    def test_create_parameter_with_annotations(self):
        """Test creating a parameter with annotations."""
        param = JavaParameter(
            name="name",
            type="String",
            annotations=[JavaAnnotation(name="@NonNull")],
        )
        assert param.name == "name"
        assert len(param.annotations) == 1
        assert param.annotations[0].name == "@NonNull"


class TestJavaField:
    """Tests for JavaField model."""

    def test_create_simple_field(self):
        """Test creating a simple field."""
        field = JavaField(name="counter", type="int", modifiers=["private"])
        assert field.name == "counter"
        assert field.type == "int"
        assert field.modifiers == ["private"]

    def test_create_field_with_javadoc(self):
        """Test creating a field with JavaDoc."""
        javadoc = JavaDoc(summary="The total count")
        field = JavaField(
            name="totalCount",
            type="long",
            modifiers=["private", "static"],
            javadoc=javadoc,
        )
        assert field.javadoc is not None
        assert field.javadoc.summary == "The total count"


class TestJavaMethod:
    """Tests for JavaMethod model."""

    def test_create_simple_method(self):
        """Test creating a simple method."""
        method = JavaMethod(name="getName", return_type="String")
        assert method.name == "getName"
        assert method.return_type == "String"
        assert method.parameters == []
        assert not method.is_constructor

    def test_create_method_with_parameters(self):
        """Test creating a method with parameters."""
        params = [
            JavaParameter(name="x", type="int"),
            JavaParameter(name="y", type="int"),
        ]
        method = JavaMethod(
            name="add", return_type="int", parameters=params, modifiers=["public"]
        )
        assert len(method.parameters) == 2
        assert method.parameters[0].name == "x"

    def test_method_signature(self):
        """Test method signature generation."""
        params = [
            JavaParameter(name="name", type="String"),
            JavaParameter(name="age", type="int"),
        ]
        method = JavaMethod(name="createUser", return_type="User", parameters=params)
        assert method.signature == "User createUser(String name, int age)"

    def test_constructor_method(self):
        """Test creating a constructor."""
        method = JavaMethod(name="MyClass", return_type="void", is_constructor=True)
        assert method.is_constructor


class TestJavaClass:
    """Tests for JavaClass model."""

    def test_create_simple_class(self):
        """Test creating a simple class."""
        java_class = JavaClass(
            name="MyClass",
            fully_qualified_name="com.example.MyClass",
            package="com.example",
        )
        assert java_class.name == "MyClass"
        assert java_class.fully_qualified_name == "com.example.MyClass"
        assert java_class.package == "com.example"

    def test_create_class_with_methods(self):
        """Test creating a class with methods."""
        method = JavaMethod(name="doSomething", return_type="void")
        java_class = JavaClass(
            name="MyClass",
            fully_qualified_name="com.example.MyClass",
            package="com.example",
            methods=[method],
        )
        assert len(java_class.methods) == 1
        assert java_class.methods[0].name == "doSomething"

    def test_create_interface(self):
        """Test creating an interface."""
        java_class = JavaClass(
            name="MyInterface",
            fully_qualified_name="com.example.MyInterface",
            package="com.example",
            is_interface=True,
        )
        assert java_class.is_interface

    def test_create_abstract_class(self):
        """Test creating an abstract class."""
        java_class = JavaClass(
            name="AbstractClass",
            fully_qualified_name="com.example.AbstractClass",
            package="com.example",
            is_abstract=True,
            modifiers=["public", "abstract"],
        )
        assert java_class.is_abstract

    def test_class_inheritance(self):
        """Test class with extends and implements."""
        java_class = JavaClass(
            name="ArrayList",
            fully_qualified_name="java.util.ArrayList",
            package="java.util",
            extends="AbstractList",
            implements=["List", "RandomAccess"],
        )
        assert java_class.extends == "AbstractList"
        assert len(java_class.implements) == 2


class TestJavaPackage:
    """Tests for JavaPackage model."""

    def test_create_empty_package(self):
        """Test creating an empty package."""
        package = JavaPackage(name="com.example")
        assert package.name == "com.example"
        assert package.classes == []

    def test_create_package_with_classes(self):
        """Test creating a package with classes."""
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
        package = JavaPackage(name="com.example", classes=[class1, class2])
        assert len(package.classes) == 2
