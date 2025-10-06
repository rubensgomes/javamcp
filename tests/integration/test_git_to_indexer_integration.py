"""
Integration tests for GitRepositoryManager and JavaPathIndexer.

This module tests the complete workflow of cloning a real Git repository
and indexing its Java source files.
"""

from pathlib import Path

import pytest

from javamcp.repositories import GitRepositoryManager
from javamcp.indexer import JavaPathIndexer


class TestGitToIndexerIntegration:
    """Integration tests for Git clone and Java indexing workflow."""

    def test_complete_workflow_git_clone_and_java_indexing(
        self,
        test_repository_url: str,
        integration_tmp_dir: Path
    ) -> None:
        """
        Test complete workflow: clone repository and index Java files.

        This integration test demonstrates the end-to-end process:
        1. Clone a real public Git repository (ms-base-lib)
        2. Index all Java source files in the cloned repository
        3. Validate the complete integration pipeline

        The test uses the real repository:
        https://github.com/rubensgomes/ms-base-lib

        Args:
            test_repository_url: URL of the test repository
            integration_tmp_dir: Temporary directory for cloning

        Assertions:
            - Repository clones successfully
            - Java files are discovered and indexed
            - All indexed files exist and have correct extensions
            - Relative paths are computed correctly
        """
        # =====================================================
        # STEP 1: Initialize GitRepositoryManager
        # =====================================================
        print(
            f"\n[STEP 1] Initializing GitRepositoryManager with "
            f"repository: {test_repository_url}"
        )
        print(f"[STEP 1] Clone target directory: {integration_tmp_dir}")

        manager = GitRepositoryManager(
            [test_repository_url],
            integration_tmp_dir
        )

        assert len(manager.repositories) == 1
        print("[STEP 1] GitRepositoryManager initialized successfully")

        # =====================================================
        # STEP 2: Clone the repository
        # =====================================================
        print(
            "\n[STEP 2] Cloning repository (this may take a moment)..."
        )

        clone_results = manager.process_repositories()

        assert len(clone_results) == 1
        clone_result = clone_results[0]

        print(f"[STEP 2] Clone result: {clone_result.message}")

        # =====================================================
        # STEP 3: Verify clone was successful
        # =====================================================
        print("\n[STEP 3] Verifying clone success...")

        assert clone_result.success, (
            f"Clone failed: {clone_result.message}"
        )

        cloned_repo_path = clone_result.repository.local_path

        assert cloned_repo_path.exists(), (
            f"Cloned directory does not exist: {cloned_repo_path}"
        )
        assert cloned_repo_path.is_dir(), (
            f"Cloned path is not a directory: {cloned_repo_path}"
        )

        git_dir = cloned_repo_path / ".git"
        assert git_dir.exists(), (
            f"No .git directory found: {git_dir}"
        )

        print(f"[STEP 3] Repository cloned successfully to:")
        print(f"[STEP 3]   {cloned_repo_path}")
        print(f"[STEP 3] .git directory confirmed")

        # =====================================================
        # STEP 4: Initialize JavaPathIndexer
        # =====================================================
        print("\n[STEP 4] Initializing JavaPathIndexer...")

        indexer = JavaPathIndexer([cloned_repo_path])

        assert len(indexer.config.repository_dirs) == 1
        print("[STEP 4] JavaPathIndexer initialized successfully")

        # =====================================================
        # STEP 5: Index Java files
        # =====================================================
        print("\n[STEP 5] Indexing Java source files...")

        index_results = indexer.index_repositories()

        assert len(index_results) == 1
        index_result = index_results[0]

        print(f"[STEP 5] Indexing result: {index_result.message}")

        # =====================================================
        # STEP 6: Verify indexing was successful
        # =====================================================
        print("\n[STEP 6] Verifying indexing success...")

        assert index_result.success, (
            f"Indexing failed: {index_result.message}"
        )

        java_files = index_result.java_files

        assert len(java_files) > 0, (
            "No Java files found in repository"
        )

        print(f"[STEP 6] Found {len(java_files)} Java source files")

        # =====================================================
        # STEP 7: Validate indexed file paths
        # =====================================================
        print("\n[STEP 7] Validating indexed file paths...")

        for java_file in java_files:
            # Check absolute path exists
            assert java_file.absolute_path.exists(), (
                f"Indexed file does not exist: "
                f"{java_file.absolute_path}"
            )

            # Check file extension
            assert java_file.absolute_path.suffix == ".java", (
                f"Indexed file is not a .java file: "
                f"{java_file.absolute_path}"
            )

            # Check repository directory matches
            assert java_file.repository_dir == cloned_repo_path, (
                f"Repository directory mismatch: "
                f"expected {cloned_repo_path}, "
                f"got {java_file.repository_dir}"
            )

            # Check relative path computation
            full_path = cloned_repo_path / java_file.relative_path
            assert full_path == java_file.absolute_path, (
                f"Relative path computation incorrect: "
                f"{java_file.relative_path}"
            )

        print("[STEP 7] All file paths validated successfully")

        # =====================================================
        # STEP 8: Display discovered Java files
        # =====================================================
        print(
            "\n[STEP 8] =========================================="
        )
        print("[STEP 8] DISCOVERED JAVA FILES:")
        print(
            "[STEP 8] =========================================="
        )

        for idx, java_file in enumerate(java_files, 1):
            print(f"[STEP 8] {idx}. {java_file.relative_path}")
            print(
                f"[STEP 8]    Absolute: {java_file.absolute_path}"
            )

        print(
            "[STEP 8] =========================================="
        )

        # =====================================================
        # STEP 9: Summary
        # =====================================================
        print("\n[STEP 9] ========================================")
        print("[STEP 9] INTEGRATION TEST SUMMARY")
        print("[STEP 9] ========================================")
        print(f"[STEP 9] Repository URL: {test_repository_url}")
        print(f"[STEP 9] Clone location: {cloned_repo_path}")
        print(f"[STEP 9] Java files found: {len(java_files)}")
        print("[STEP 9] Clone status: SUCCESS ✅")
        print("[STEP 9] Indexing status: SUCCESS ✅")
        print("[STEP 9] Integration test: PASSED ✅")
        print("[STEP 9] ========================================")

    def test_get_all_java_files_from_indexer(
        self,
        test_repository_url: str,
        integration_tmp_dir: Path
    ) -> None:
        """
        Test retrieving all indexed files using get_all_java_files().

        This test verifies that the indexer's get_all_java_files()
        method returns all discovered Java files correctly.

        Args:
            test_repository_url: URL of the test repository
            integration_tmp_dir: Temporary directory for cloning
        """
        # Clone repository
        manager = GitRepositoryManager(
            [test_repository_url],
            integration_tmp_dir
        )
        clone_results = manager.process_repositories()
        assert clone_results[0].success

        cloned_repo_path = clone_results[0].repository.local_path

        # Index Java files
        indexer = JavaPathIndexer([cloned_repo_path])
        index_results = indexer.index_repositories()
        assert index_results[0].success

        # Get all indexed files
        all_files = indexer.get_all_java_files()

        # Verify count matches
        expected_count = len(index_results[0].java_files)
        assert len(all_files) == expected_count

        # Verify all files are accessible
        for java_file in all_files:
            assert java_file.absolute_path.exists()
            assert java_file.absolute_path.suffix == ".java"

        print(
            f"\n✅ get_all_java_files() returned "
            f"{len(all_files)} Java files"
        )
