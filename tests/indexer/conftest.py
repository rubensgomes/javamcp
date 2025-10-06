"""
Pytest fixtures for indexer tests.
"""

from pathlib import Path
from typing import List

import pytest

from javamcp.indexer import JavaPathIndexer


@pytest.fixture
def sample_java_repo(tmp_path: Path) -> Path:
    """
    Create a sample Java repository structure with source files.

    Args:
        tmp_path: Pytest temporary directory

    Returns:
        Path to the sample repository root
    """
    repo_dir = tmp_path / "sample_repo"
    java_src_dir = repo_dir / "src" / "main" / "java" / "com" / "example"
    java_src_dir.mkdir(parents=True)

    (java_src_dir / "Main.java").write_text(
        "package com.example;\n\npublic class Main {}\n"
    )
    (java_src_dir / "Utils.java").write_text(
        "package com.example;\n\npublic class Utils {}\n"
    )

    subpackage_dir = java_src_dir / "model"
    subpackage_dir.mkdir()
    (subpackage_dir / "User.java").write_text(
        "package com.example.model;\n\npublic class User {}\n"
    )

    return repo_dir


@pytest.fixture
def empty_repo(tmp_path: Path) -> Path:
    """
    Create an empty repository without Java files.

    Args:
        tmp_path: Pytest temporary directory

    Returns:
        Path to the empty repository root
    """
    repo_dir = tmp_path / "empty_repo"
    repo_dir.mkdir()
    (repo_dir / "README.md").write_text("# Empty Repository\n")

    return repo_dir


@pytest.fixture
def multi_module_repo(tmp_path: Path) -> Path:
    """
    Create a multi-module repository with multiple src/main/java dirs.

    Args:
        tmp_path: Pytest temporary directory

    Returns:
        Path to the multi-module repository root
    """
    repo_dir = tmp_path / "multi_module_repo"

    module1_dir = repo_dir / "module1" / "src" / "main" / "java"
    module1_dir.mkdir(parents=True)
    (module1_dir / "Module1.java").write_text(
        "public class Module1 {}\n"
    )

    module2_dir = repo_dir / "module2" / "src" / "main" / "java"
    module2_dir.mkdir(parents=True)
    (module2_dir / "Module2.java").write_text(
        "public class Module2 {}\n"
    )

    return repo_dir


@pytest.fixture
def test_repository_dirs(
    sample_java_repo: Path,
    multi_module_repo: Path
) -> List[Path]:
    """
    Provide a list of test repository directories.

    Args:
        sample_java_repo: Sample repository fixture
        multi_module_repo: Multi-module repository fixture

    Returns:
        List of repository directory paths
    """
    return [sample_java_repo, multi_module_repo]


@pytest.fixture
def java_path_indexer(test_repository_dirs: List[Path]) -> JavaPathIndexer:
    """
    Create a JavaPathIndexer instance with test repositories.

    Args:
        test_repository_dirs: List of test repository directories

    Returns:
        Configured JavaPathIndexer instance
    """
    return JavaPathIndexer(test_repository_dirs)


@pytest.fixture
def single_repo_indexer(sample_java_repo: Path) -> JavaPathIndexer:
    """
    Create a JavaPathIndexer for a single repository.

    Args:
        sample_java_repo: Sample repository fixture

    Returns:
        Configured JavaPathIndexer instance
    """
    return JavaPathIndexer([sample_java_repo])
