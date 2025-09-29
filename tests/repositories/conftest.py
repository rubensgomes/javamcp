"""
Shared pytest fixtures for repositories module tests.

This module provides common fixtures used across repository tests,
following pytest best practices and CLAUDE_PYTHON.md guidelines.
"""

from pathlib import Path
from typing import List

import pytest

from javamcp.repositories.manager import GitRepositoryManager


@pytest.fixture
def test_repository_urls() -> List[str]:
    """
    Provide a list of test repository URLs for testing.

    Returns:
        List of valid test repository URLs with different formats
    """
    return [
        "https://github.com/owner1/repo1",
        "https://github.com/owner2/repo2.git",
        "https://github.com/owner3/test-repo"
    ]


@pytest.fixture
def single_repository_url() -> str:
    """
    Provide a single repository URL for simple test scenarios.

    Returns:
        Single valid repository URL
    """
    return "https://github.com/test-owner/test-repo"


@pytest.fixture
def invalid_repository_urls() -> List[str]:
    """
    Provide invalid repository URLs for error testing.

    Returns:
        List of invalid URLs for testing error scenarios
    """
    return [
        "not-a-url",
        "ftp://invalid.com/repo",
        "file://local/path",
        "",
        "https://",
    ]


@pytest.fixture
def git_repository_manager(
    test_repository_urls: List[str],
    tmp_path: Path
) -> GitRepositoryManager:
    """
    Create a GitRepositoryManager instance for testing.

    Args:
        test_repository_urls: List of test repository URLs
        tmp_path: Temporary directory path from pytest

    Returns:
        Configured GitRepositoryManager instance
    """
    return GitRepositoryManager(test_repository_urls, tmp_path)


@pytest.fixture
def single_repo_manager(
    single_repository_url: str,
    tmp_path: Path
) -> GitRepositoryManager:
    """
    Create a GitRepositoryManager with single repository for simple tests.

    Args:
        single_repository_url: Single test repository URL
        tmp_path: Temporary directory path from pytest

    Returns:
        GitRepositoryManager instance with single repository
    """
    return GitRepositoryManager([single_repository_url], tmp_path)