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
Pydantic models representing Java API entities (packages, classes, methods, fields, etc.).
"""

from typing import Optional

from pydantic import BaseModel, Field


class JavaAnnotation(BaseModel):
    """
    Represents a Java annotation.

    Attributes:
        name: The annotation name (e.g., "@Override", "@Deprecated")
        parameters: Optional annotation parameters as key-value pairs
    """

    name: str = Field(..., description="Annotation name including @ symbol")
    parameters: dict[str, str] = Field(
        default_factory=dict, description="Annotation parameters"
    )


class JavaDoc(BaseModel):
    """
    Represents parsed Javadoc documentation.

    Attributes:
        summary: Brief summary/description
        description: Full detailed description
        params: Parameter descriptions (param name -> description)
        returns: Return value description
        throws: Exception descriptions (exception type -> description)
        see: Cross-references
        since: Version information
        deprecated: Deprecation notice
        author: Author information
        examples: Code examples
    """

    summary: str = Field(default="", description="Brief summary")
    description: str = Field(default="", description="Detailed description")
    params: dict[str, str] = Field(
        default_factory=dict, description="Parameter descriptions"
    )
    returns: str = Field(default="", description="Return value description")
    throws: dict[str, str] = Field(
        default_factory=dict, description="Exception descriptions"
    )
    see: list[str] = Field(default_factory=list, description="Cross-references")
    since: str = Field(default="", description="Version information")
    deprecated: str = Field(default="", description="Deprecation notice")
    author: list[str] = Field(default_factory=list, description="Authors")
    examples: list[str] = Field(default_factory=list, description="Code examples")


class JavaParameter(BaseModel):
    """
    Represents a method parameter.

    Attributes:
        name: Parameter name
        type: Parameter type (e.g., "String", "int", "List<String>")
        annotations: List of annotations on this parameter
    """

    name: str = Field(..., description="Parameter name")
    type: str = Field(..., description="Parameter type")
    annotations: list[JavaAnnotation] = Field(
        default_factory=list, description="Parameter annotations"
    )


class JavaField(BaseModel):
    """
    Represents a class field.

    Attributes:
        name: Field name
        type: Field type
        modifiers: Access modifiers (public, private, static, final, etc.)
        annotations: Field annotations
        javadoc: Field documentation
        initial_value: Initial value if present
    """

    name: str = Field(..., description="Field name")
    type: str = Field(..., description="Field type")
    modifiers: list[str] = Field(
        default_factory=list, description="Modifiers (public, private, static, etc.)"
    )
    annotations: list[JavaAnnotation] = Field(
        default_factory=list, description="Field annotations"
    )
    javadoc: Optional[JavaDoc] = Field(None, description="Field documentation")
    initial_value: Optional[str] = Field(None, description="Initial value if present")


class JavaMethod(BaseModel):
    """
    Represents a Java method.

    Attributes:
        name: Method name
        return_type: Return type (use "void" for void methods)
        parameters: List of method parameters
        modifiers: Access modifiers (public, private, static, abstract, etc.)
        annotations: Method annotations
        javadoc: Method documentation
        throws: List of exception types this method throws
        is_constructor: True if this is a constructor
    """

    name: str = Field(..., description="Method name")
    return_type: str = Field(..., description="Return type")
    parameters: list[JavaParameter] = Field(
        default_factory=list, description="Method parameters"
    )
    modifiers: list[str] = Field(
        default_factory=list, description="Modifiers (public, private, static, etc.)"
    )
    annotations: list[JavaAnnotation] = Field(
        default_factory=list, description="Method annotations"
    )
    javadoc: Optional[JavaDoc] = Field(None, description="Method documentation")
    throws: list[str] = Field(
        default_factory=list, description="Exception types thrown"
    )
    is_constructor: bool = Field(False, description="True if this is a constructor")

    @property
    def signature(self) -> str:
        """Generate method signature string."""
        params = ", ".join(f"{p.type} {p.name}" for p in self.parameters)
        return f"{self.return_type} {self.name}({params})"


class JavaClass(BaseModel):
    """
    Represents a Java class or interface.

    Attributes:
        name: Simple class name
        fully_qualified_name: Fully-qualified name (e.g., "java.util.ArrayList")
        package: Package name
        modifiers: Class modifiers (public, abstract, final, etc.)
        annotations: Class annotations
        extends: Superclass name (if any)
        implements: List of implemented interface names
        methods: List of methods in this class
        fields: List of fields in this class
        javadoc: Class documentation
        is_interface: True if this is an interface
        is_abstract: True if this is an abstract class
        is_enum: True if this is an enum
        inner_classes: List of inner class names
    """

    name: str = Field(..., description="Simple class name")
    fully_qualified_name: str = Field(..., description="Fully-qualified class name")
    package: str = Field(..., description="Package name")
    modifiers: list[str] = Field(default_factory=list, description="Class modifiers")
    annotations: list[JavaAnnotation] = Field(
        default_factory=list, description="Class annotations"
    )
    extends: Optional[str] = Field(None, description="Superclass name")
    implements: list[str] = Field(
        default_factory=list, description="Implemented interfaces"
    )
    methods: list[JavaMethod] = Field(default_factory=list, description="Class methods")
    fields: list[JavaField] = Field(default_factory=list, description="Class fields")
    javadoc: Optional[JavaDoc] = Field(None, description="Class documentation")
    is_interface: bool = Field(False, description="True if interface")
    is_abstract: bool = Field(False, description="True if abstract")
    is_enum: bool = Field(False, description="True if enum")
    inner_classes: list[str] = Field(
        default_factory=list, description="Inner class names"
    )


class JavaPackage(BaseModel):
    """
    Represents a Java package.

    Attributes:
        name: Package name (e.g., "java.util")
        classes: List of classes in this package
    """

    name: str = Field(..., description="Package name")
    classes: list[JavaClass] = Field(
        default_factory=list, description="Classes in this package"
    )
