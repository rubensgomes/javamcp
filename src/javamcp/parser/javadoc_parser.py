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
Javadoc comment parser.
"""

import re
from typing import Optional

from javamcp.logging import get_logger
from javamcp.models.java_entities import JavaDoc

from .exceptions import JavaDocParseError

# Module-level logger
logger = get_logger("parser.javadoc")


def parse_javadoc(javadoc_text: Optional[str]) -> Optional[JavaDoc]:
    """
    Parse Javadoc comment text into JavaDoc model.

    Args:
        javadoc_text: Raw javadoc comment text (including /** */ delimiters)

    Returns:
        JavaDoc model or None if text is empty

    Raises:
        JavaDocParseError: If parsing fails
    """
    if not javadoc_text or not javadoc_text.strip():
        logger.debug("Empty javadoc text, returning None")
        return None

    logger.debug("Parsing javadoc (%d chars)", len(javadoc_text))
    try:
        # Remove /** and */ delimiters and leading asterisks
        cleaned = _clean_javadoc(javadoc_text)

        # Extract summary (first sentence or paragraph)
        summary = _extract_summary(cleaned)

        # Extract description (everything before tags)
        description = _extract_description(cleaned)

        # Extract tags
        params = _extract_param_tags(cleaned)
        returns = _extract_return_tag(cleaned)
        throws = _extract_throws_tags(cleaned)
        see = _extract_see_tags(cleaned)
        since = _extract_since_tag(cleaned)
        deprecated = _extract_deprecated_tag(cleaned)
        author = _extract_author_tags(cleaned)
        examples = _extract_example_tags(cleaned)

        result = JavaDoc(
            summary=summary,
            description=description,
            params=params,
            returns=returns,
            throws=throws,
            see=see,
            since=since,
            deprecated=deprecated,
            author=author,
            examples=examples,
        )
        logger.debug(
            "Javadoc parsed: params=%d, throws=%d, examples=%d",
            len(params),
            len(throws),
            len(examples),
        )
        return result
    except Exception as e:
        logger.error("Failed to parse javadoc: %s", e)
        raise JavaDocParseError(f"Failed to parse Javadoc: {e}") from e


def _clean_javadoc(text: str) -> str:
    """Remove Javadoc delimiters and leading asterisks."""
    # Remove /** and */
    text = re.sub(r"/\*\*", "", text)
    text = re.sub(r"\*/", "", text)

    # Remove leading asterisks from each line
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        # Remove leading whitespace and asterisk
        line = re.sub(r"^\s*\*\s?", "", line)
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def _extract_summary(text: str) -> str:
    """Extract summary (first sentence)."""
    # Get text before first tag
    before_tags = _get_text_before_tags(text)

    # Extract first sentence (up to period followed by space or newline)
    match = re.search(r"^(.*?\.)\s", before_tags, re.DOTALL)
    if match:
        return match.group(1).strip()

    # If no period found, take first line or paragraph
    lines = before_tags.strip().split("\n")
    if lines:
        return lines[0].strip()

    return ""


def _extract_description(text: str) -> str:
    """Extract full description (everything before tags)."""
    before_tags = _get_text_before_tags(text)
    return before_tags.strip()


def _get_text_before_tags(text: str) -> str:
    """Get text content before any @ tags."""
    match = re.search(r"(.*?)(?=@\w+)", text, re.DOTALL)
    if match:
        return match.group(1)
    return text


def _extract_param_tags(text: str) -> dict[str, str]:
    """Extract @param tags."""
    params = {}
    pattern = r"@param\s+(\w+)\s+([^\n@]+)"
    for match in re.finditer(pattern, text):
        param_name = match.group(1).strip()
        param_desc = match.group(2).strip()
        params[param_name] = param_desc
    return params


def _extract_return_tag(text: str) -> str:
    """Extract @return tag."""
    match = re.search(r"@return\s+([^\n@]+)", text)
    if match:
        return match.group(1).strip()
    return ""


def _extract_throws_tags(text: str) -> dict[str, str]:
    """Extract @throws tags."""
    throws = {}
    pattern = r"@throws\s+(\w+)\s+([^\n@]+)"
    for match in re.finditer(pattern, text):
        exception_name = match.group(1).strip()
        exception_desc = match.group(2).strip()
        throws[exception_name] = exception_desc
    return throws


def _extract_see_tags(text: str) -> list[str]:
    """Extract @see tags."""
    see_list = []
    pattern = r"@see\s+([^\n@]+)"
    for match in re.finditer(pattern, text):
        see_list.append(match.group(1).strip())
    return see_list


def _extract_since_tag(text: str) -> str:
    """Extract @since tag."""
    match = re.search(r"@since\s+([^\n@]+)", text)
    if match:
        return match.group(1).strip()
    return ""


def _extract_deprecated_tag(text: str) -> str:
    """Extract @deprecated tag."""
    match = re.search(r"@deprecated\s+([^\n@]+)", text)
    if match:
        return match.group(1).strip()
    return ""


def _extract_author_tags(text: str) -> list[str]:
    """Extract @author tags."""
    authors = []
    pattern = r"@author\s+([^\n@]+)"
    for match in re.finditer(pattern, text):
        authors.append(match.group(1).strip())
    return authors


def _extract_example_tags(text: str) -> list[str]:
    """Extract @example tags or code blocks."""
    examples = []

    # Extract @example tags
    pattern = r"@example\s+([^\n@]+(?:\n(?!@)\s*.*)*)"
    for match in re.finditer(pattern, text, re.MULTILINE):
        examples.append(match.group(1).strip())

    # Extract <pre> blocks
    pre_pattern = r"<pre>(.*?)</pre>"
    for match in re.finditer(pre_pattern, text, re.DOTALL):
        examples.append(match.group(1).strip())

    return examples
