"""
Pytest fixtures for integration tests.
"""

from pathlib import Path

import pytest


@pytest.fixture
def test_repository_url() -> str:
    """
    Provide the test repository URL for integration testing.

    Returns:
        URL of the test repository (ms-base-lib)
    """
    return "https://github.com/rubensgomes/ms-base-lib"


@pytest.fixture
def integration_tmp_dir(tmp_path: Path) -> Path:
    """
    Provide a temporary directory for integration test clones.

    Args:
        tmp_path: Pytest temporary directory

    Returns:
        Path to temporary repos directory
    """
    repos_dir = tmp_path / "repos"
    repos_dir.mkdir(parents=True, exist_ok=True)
    return repos_dir
