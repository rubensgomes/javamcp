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
Utility helper functions for JavaMCP server.
"""

import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


def normalize_path(path: str) -> Path:
    """
    Normalize file path to absolute path.

    Args:
        path: File path (relative or absolute)

    Returns:
        Absolute Path object
    """
    return Path(path).expanduser().resolve()


def is_java_file(path: Path) -> bool:
    """
    Check if file is a Java source file.

    Args:
        path: File path

    Returns:
        True if file ends with .java
    """
    return path.suffix.lower() == ".java"


def validate_java_file(path: Path) -> bool:
    """
    Validate that path points to an existing Java file.

    Args:
        path: File path

    Returns:
        True if path exists and is a Java file
    """
    return path.exists() and path.is_file() and is_java_file(path)


def format_method_signature(
    method_name: str, parameters: list[tuple[str, str]], return_type: str
) -> str:
    """
    Format method signature string.

    Args:
        method_name: Method name
        parameters: List of (type, name) tuples
        return_type: Return type

    Returns:
        Formatted signature string
    """
    params = ", ".join(f"{ptype} {pname}" for ptype, pname in parameters)
    return f"{return_type} {method_name}({params})"


def format_class_name(fully_qualified_name: str) -> str:
    """
    Extract simple class name from fully-qualified name.

    Args:
        fully_qualified_name: Fully-qualified class name

    Returns:
        Simple class name
    """
    return fully_qualified_name.split(".")[-1]


def get_package_name(fully_qualified_name: str) -> str:
    """
    Extract package name from fully-qualified class name.

    Args:
        fully_qualified_name: Fully-qualified class name

    Returns:
        Package name (empty string if no package)
    """
    parts = fully_qualified_name.split(".")
    if len(parts) > 1:
        return ".".join(parts[:-1])
    return ""


def validate_repository_url(url: str) -> bool:
    """
    Validate repository URL format.

    Args:
        url: Repository URL

    Returns:
        True if URL appears to be a valid Git repository URL
    """
    # Basic validation - check if it's a valid URL or git URL
    if url.startswith("git@"):
        # SSH format: git@github.com:user/repo.git
        return bool(re.match(r"^git@[\w\.-]+:[\w\-]+/[\w\-]+\.git$", url))

    try:
        result = urlparse(url)
        # Check if scheme is http/https and has netloc
        if result.scheme in ["http", "https"] and result.netloc:
            # Should end with .git
            return result.path.endswith(".git") or "/" in result.path
        return False
    except Exception:  # pylint: disable=broad-exception-caught
        return False


def validate_branch_name(branch: str) -> bool:
    """
    Validate Git branch name.

    Args:
        branch: Branch name

    Returns:
        True if branch name is valid
    """
    if not branch or not isinstance(branch, str):
        return False

    # Branch name cannot contain: .., ~, ^, :, ?, *, [, \, space at beginning/end
    invalid_patterns = [r"\.\.", "~", r"\^", ":", r"\?", r"\*", r"\[", "\\\\"]

    for pattern in invalid_patterns:
        if re.search(pattern, branch):
            return False

    # Cannot start/end with slash, dot, or space
    if branch.startswith(("/", ".", " ")) or branch.endswith(("/", ".", " ")):
        return False

    return True


def extract_repository_name(url: str) -> Optional[str]:
    """
    Extract repository name from URL.

    Args:
        url: Repository URL

    Returns:
        Repository name or None if cannot extract
    """
    if url.startswith("git@"):
        # SSH format: git@github.com:user/repo.git
        match = re.search(r":(.+)/(.+)\.git$", url)
        if match:
            return match.group(2)
        return None

    try:
        result = urlparse(url)
        path = result.path.rstrip("/")
        if path.endswith(".git"):
            path = path[:-4]
        return path.split("/")[-1]
    except Exception:  # pylint: disable=broad-exception-caught
        return None


def format_list(items: list[str], max_items: int = 5) -> str:
    """
    Format list of items for display, truncating if too long.

    Args:
        items: List of items
        max_items: Maximum items to show

    Returns:
        Formatted string
    """
    if not items:
        return "none"

    if len(items) <= max_items:
        return ", ".join(items)

    shown = items[:max_items]
    remaining = len(items) - max_items
    return f"{', '.join(shown)} (and {remaining} more)"
