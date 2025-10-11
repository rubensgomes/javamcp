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
Formatters for creating human-readable API summaries and documentation.
"""

from javamcp.models.java_entities import JavaClass, JavaMethod


def format_class_context(
    java_class: JavaClass,
    include_code_snippets: bool = False,  # pylint: disable=unused-argument
) -> str:
    """
    Format a Java class into a human-readable context string.

    Args:
        java_class: JavaClass to format
        include_code_snippets: Whether to include code examples

    Returns:
        Formatted class context string
    """
    lines = []

    # Header
    class_type = _get_class_type(java_class)
    lines.append(f"# {java_class.fully_qualified_name}")
    lines.append(f"**Type:** {class_type}")
    lines.append(f"**Package:** {java_class.package}")
    lines.append("")

    # Javadoc summary
    if java_class.javadoc:
        if java_class.javadoc.summary:
            lines.append(f"**Summary:** {java_class.javadoc.summary}")
            lines.append("")

        if java_class.javadoc.description:
            lines.append("**Description:**")
            lines.append(java_class.javadoc.description)
            lines.append("")

    # Modifiers and annotations
    if java_class.modifiers:
        lines.append(f"**Modifiers:** {', '.join(java_class.modifiers)}")

    if java_class.annotations:
        annotations = ", ".join(ann.name for ann in java_class.annotations)
        lines.append(f"**Annotations:** {annotations}")

    # Inheritance
    if java_class.extends or java_class.implements:
        lines.append("")
        if java_class.extends:
            lines.append(f"**Extends:** {java_class.extends}")
        if java_class.implements:
            implements = ", ".join(java_class.implements)
            lines.append(f"**Implements:** {implements}")

    # Methods
    if java_class.methods:
        lines.append("")
        lines.append("## Methods")
        lines.append("")
        for method in java_class.methods:
            lines.append(f"### {method.name}")
            lines.append(f"**Signature:** `{method.signature}`")
            if method.javadoc and method.javadoc.summary:
                lines.append(f"**Summary:** {method.javadoc.summary}")
            lines.append("")

    # Fields
    if java_class.fields:
        lines.append("## Fields")
        lines.append("")
        for field in java_class.fields:
            lines.append(f"- `{field.type} {field.name}`")
            if field.javadoc and field.javadoc.summary:
                lines.append(f"  - {field.javadoc.summary}")

    return "\n".join(lines)


def format_method_context(method: JavaMethod, java_class: JavaClass) -> str:
    """
    Format a Java method into a human-readable context string.

    Args:
        method: JavaMethod to format
        java_class: Containing class

    Returns:
        Formatted method context string
    """
    lines = []

    # Header
    lines.append(f"# {java_class.fully_qualified_name}.{method.name}")
    lines.append(f"**Signature:** `{method.signature}`")
    lines.append("")

    # Javadoc summary
    if method.javadoc:
        if method.javadoc.summary:
            lines.append(f"**Summary:** {method.javadoc.summary}")
            lines.append("")

        if method.javadoc.description:
            lines.append("**Description:**")
            lines.append(method.javadoc.description)
            lines.append("")

        # Parameters
        if method.javadoc.params:
            lines.append("**Parameters:**")
            for param_name, param_desc in method.javadoc.params.items():
                lines.append(f"- `{param_name}`: {param_desc}")
            lines.append("")

        # Return
        if method.javadoc.returns:
            lines.append(f"**Returns:** {method.javadoc.returns}")
            lines.append("")

        # Throws
        if method.javadoc.throws:
            lines.append("**Throws:**")
            for exception, desc in method.javadoc.throws.items():
                lines.append(f"- `{exception}`: {desc}")
            lines.append("")

        # Examples
        if method.javadoc.examples:
            lines.append("**Examples:**")
            for example in method.javadoc.examples:
                lines.append("```java")
                lines.append(example)
                lines.append("```")
            lines.append("")

    # Modifiers and annotations
    if method.modifiers:
        lines.append(f"**Modifiers:** {', '.join(method.modifiers)}")

    if method.annotations:
        annotations = ", ".join(ann.name for ann in method.annotations)
        lines.append(f"**Annotations:** {annotations}")

    return "\n".join(lines)


def format_method_signature(method: JavaMethod) -> str:
    """
    Format method signature with parameter types and names.

    Args:
        method: JavaMethod to format

    Returns:
        Formatted signature string
    """
    params = ", ".join(f"{p.type} {p.name}" for p in method.parameters)
    return f"{method.return_type} {method.name}({params})"


def format_class_hierarchy(java_class: JavaClass) -> str:
    """
    Format class hierarchy (extends/implements).

    Args:
        java_class: JavaClass to format

    Returns:
        Formatted hierarchy string
    """
    parts = [java_class.name]

    if java_class.extends:
        parts.append(f"extends {java_class.extends}")

    if java_class.implements:
        implements = ", ".join(java_class.implements)
        parts.append(f"implements {implements}")

    return " ".join(parts)


def _get_class_type(java_class: JavaClass) -> str:
    """Determine class type string."""
    if java_class.is_interface:
        return "Interface"
    if java_class.is_enum:
        return "Enum"
    if java_class.is_abstract:
        return "Abstract Class"
    return "Class"
