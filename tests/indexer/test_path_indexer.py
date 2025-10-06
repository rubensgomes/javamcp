"""
Behavior-focused tests for JavaPathIndexer.

This module contains comprehensive tests following CLAUDE_PYTHON.md
guidelines, focusing on behavior and outcomes rather than
implementation details.
"""

from pathlib import Path
from typing import List

import pytest
from pydantic import ValidationError

from javamcp.indexer.path_indexer import JavaPathIndexer
from javamcp.indexer.exceptions import (
    NoJavaFilesFoundError,
    DirectoryAccessError
)


class TestJavaPathIndexerInitialization:
    """Test JavaPathIndexer initialization behavior."""

    def test_indexer_initializes_with_valid_directories(
        self,
        test_repository_dirs: List[Path]
    ) -> None:
        """
        JavaPathIndexer should initialize successfully with valid dirs.

        Verifies that the indexer creates configuration correctly
        with valid repository directories.
        """
        indexer = JavaPathIndexer(test_repository_dirs)

        assert len(indexer.config.repository_dirs) == len(
            test_repository_dirs
        )
        assert indexer.config.java_source_pattern == "src/main/java"
        assert len(indexer.indexed_files) == 0

    def test_indexer_accepts_custom_source_pattern(
        self,
        sample_java_repo: Path
    ) -> None:
        """
        JavaPathIndexer should accept custom Java source patterns.

        Tests that custom patterns for Java source directories
        can be configured.
        """
        custom_pattern = "src/test/java"
        indexer = JavaPathIndexer(
            [sample_java_repo],
            java_source_pattern=custom_pattern
        )

        assert indexer.config.java_source_pattern == custom_pattern

    def test_indexer_rejects_non_existent_directories(
        self,
        tmp_path: Path
    ) -> None:
        """
        JavaPathIndexer should reject non-existent directories.

        Tests that attempting to initialize with non-existent
        paths raises appropriate validation errors.
        """
        non_existent = tmp_path / "does_not_exist"

        with pytest.raises(ValidationError):
            JavaPathIndexer([non_existent])

    def test_indexer_rejects_file_instead_of_directory(
        self,
        tmp_path: Path
    ) -> None:
        """
        JavaPathIndexer should reject file paths instead of dirs.

        Tests that file paths are properly rejected during
        initialization.
        """
        file_path = tmp_path / "file.txt"
        file_path.write_text("test")

        with pytest.raises(ValidationError):
            JavaPathIndexer([file_path])


class TestJavaPathIndexerIndexing:
    """Test JavaPathIndexer indexing behavior."""

    def test_indexes_java_files_successfully(
        self,
        single_repo_indexer: JavaPathIndexer
    ) -> None:
        """
        Indexer should successfully discover Java files.

        Tests the happy path where Java files are found and
        indexed correctly.
        """
        results = single_repo_indexer.index_repositories()

        assert len(results) == 1
        result = results[0]

        assert result.success
        assert len(result.java_files) == 3
        assert all(
            f.absolute_path.suffix == '.java'
            for f in result.java_files
        )

    def test_indexes_multiple_repositories(
        self,
        java_path_indexer: JavaPathIndexer
    ) -> None:
        """
        Indexer should process multiple repositories.

        Tests that the indexer can handle multiple repository
        directories in a single operation.
        """
        results = java_path_indexer.index_repositories()

        assert len(results) == 2
        assert all(result.success for result in results)

        total_files = sum(
            len(result.java_files) for result in results
        )
        assert total_files > 0

    def test_handles_repository_without_java_files(
        self,
        empty_repo: Path
    ) -> None:
        """
        Indexer should handle repositories without Java files.

        Tests behavior when a repository does not contain
        src/main/java directories or Java files.
        """
        indexer = JavaPathIndexer([empty_repo])
        results = indexer.index_repositories()

        assert len(results) == 1
        result = results[0]

        assert not result.success
        assert len(result.java_files) == 0
        assert "No src/main/java directories found" in result.message

    def test_indexes_multi_module_repository(
        self,
        multi_module_repo: Path
    ) -> None:
        """
        Indexer should handle multi-module repositories.

        Tests that repositories with multiple src/main/java
        directories (Maven multi-module) are indexed correctly.
        """
        indexer = JavaPathIndexer([multi_module_repo])
        results = indexer.index_repositories()

        assert len(results) == 1
        result = results[0]

        assert result.success
        assert len(result.java_files) == 2

        file_names = {
            f.absolute_path.name for f in result.java_files
        }
        assert "Module1.java" in file_names
        assert "Module2.java" in file_names

    def test_java_file_paths_have_correct_attributes(
        self,
        single_repo_indexer: JavaPathIndexer,
        sample_java_repo: Path
    ) -> None:
        """
        JavaFilePath objects should have correct attributes.

        Tests that discovered Java files have properly set
        absolute paths, relative paths, and repository dirs.
        """
        results = single_repo_indexer.index_repositories()
        result = results[0]

        for java_file in result.java_files:
            assert java_file.absolute_path.is_absolute()
            assert java_file.absolute_path.exists()
            assert java_file.absolute_path.suffix == '.java'
            assert java_file.repository_dir == sample_java_repo
            assert not java_file.relative_path.is_absolute()

    def test_continues_processing_after_failures(
        self,
        sample_java_repo: Path,
        empty_repo: Path
    ) -> None:
        """
        Indexer should continue processing after failures.

        Tests resilience when some repositories succeed and
        others fail.
        """
        indexer = JavaPathIndexer([sample_java_repo, empty_repo])
        results = indexer.index_repositories()

        assert len(results) == 2

        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]

        assert len(successful) == 1
        assert len(failed) == 1

    def test_get_all_java_files_returns_all_indexed_files(
        self,
        java_path_indexer: JavaPathIndexer
    ) -> None:
        """
        get_all_java_files should return all discovered files.

        Tests that the method returns all Java files discovered
        across all indexed repositories.
        """
        results = java_path_indexer.index_repositories()

        expected_count = sum(
            len(r.java_files) for r in results
        )
        all_files = java_path_indexer.get_all_java_files()

        assert len(all_files) == expected_count


class TestJavaPathIndexerEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_handles_empty_repository_list(self) -> None:
        """
        Indexer should handle empty repository list gracefully.

        Tests behavior when no repositories are provided.
        """
        with pytest.raises(ValidationError):
            JavaPathIndexer([])

    def test_handles_deeply_nested_java_files(
        self,
        tmp_path: Path
    ) -> None:
        """
        Indexer should handle deeply nested Java files.

        Tests that Java files in deep package hierarchies
        are discovered correctly.
        """
        repo_dir = tmp_path / "deep_repo"
        deep_dir = (
            repo_dir / "src" / "main" / "java" /
            "com" / "example" / "very" / "deep" / "package"
        )
        deep_dir.mkdir(parents=True)
        (deep_dir / "DeepClass.java").write_text(
            "package com.example.very.deep.package;\n\n"
            "public class DeepClass {}\n"
        )

        indexer = JavaPathIndexer([repo_dir])
        results = indexer.index_repositories()

        assert len(results) == 1
        assert results[0].success
        assert len(results[0].java_files) == 1

    def test_ignores_non_java_files_in_src_main_java(
        self,
        tmp_path: Path
    ) -> None:
        """
        Indexer should ignore non-Java files in src/main/java.

        Tests that only .java files are indexed, ignoring other
        file types in the Java source directory.
        """
        repo_dir = tmp_path / "mixed_repo"
        java_dir = repo_dir / "src" / "main" / "java"
        java_dir.mkdir(parents=True)

        (java_dir / "Valid.java").write_text(
            "public class Valid {}\n"
        )
        (java_dir / "README.md").write_text("# Readme\n")
        (java_dir / "config.properties").write_text("key=value\n")

        indexer = JavaPathIndexer([repo_dir])
        results = indexer.index_repositories()

        assert len(results) == 1
        assert results[0].success
        assert len(results[0].java_files) == 1
        assert results[0].java_files[0].absolute_path.name == (
            "Valid.java"
        )

    def test_handles_java_files_with_special_names(
        self,
        tmp_path: Path
    ) -> None:
        """
        Indexer should handle Java files with special characters.

        Tests that files with various naming patterns are
        handled correctly.
        """
        repo_dir = tmp_path / "special_names_repo"
        java_dir = repo_dir / "src" / "main" / "java"
        java_dir.mkdir(parents=True)

        special_names = [
            "Class_With_Underscores.java",
            "ClassWith123Numbers.java",
            "Class$Inner.java"
        ]

        for name in special_names:
            (java_dir / name).write_text(
                f"public class {name.replace('.java', '')} {{}}\n"
            )

        indexer = JavaPathIndexer([repo_dir])
        results = indexer.index_repositories()

        assert len(results) == 1
        assert results[0].success
        assert len(results[0].java_files) == len(special_names)


class TestJavaPathIndexerPathGeneration:
    """Test path generation and validation."""

    def test_relative_paths_are_relative_to_repository(
        self,
        single_repo_indexer: JavaPathIndexer,
        sample_java_repo: Path
    ) -> None:
        """
        Relative paths should be correctly calculated.

        Tests that relative paths are properly computed
        relative to the repository root.
        """
        results = single_repo_indexer.index_repositories()
        result = results[0]

        for java_file in result.java_files:
            full_path = (
                sample_java_repo / java_file.relative_path
            )
            assert full_path == java_file.absolute_path

    def test_all_paths_use_pathlib_path_objects(
        self,
        single_repo_indexer: JavaPathIndexer
    ) -> None:
        """
        All paths should use pathlib.Path objects.

        Tests that the indexer uses Path objects consistently
        throughout the results.
        """
        results = single_repo_indexer.index_repositories()
        result = results[0]

        assert isinstance(result.repository_dir, Path)

        for java_file in result.java_files:
            assert isinstance(java_file.absolute_path, Path)
            assert isinstance(java_file.relative_path, Path)
            assert isinstance(java_file.repository_dir, Path)
