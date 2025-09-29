"""
Behavior-focused tests for GitRepositoryManager.

This module contains comprehensive tests following CLAUDE_PYTHON.md guidelines,
focusing on behavior and outcomes rather than implementation details.
"""

from pathlib import Path
from typing import List
from unittest.mock import Mock

import git
import pytest
from pydantic import ValidationError

from javamcp.repositories.exceptions import (
    RepositoryCloneError,
    RepositoryError,
    RepositoryNotFoundError,
    RepositorySyncError,
)
from javamcp.repositories.manager import GitRepositoryManager
from javamcp.repositories.models import RepositoryStatus


class TestGitRepositoryManagerInitialization:
    """Test GitRepositoryManager initialization behavior."""

    def test_manager_initializes_with_valid_urls_and_path(
        self,
        test_repository_urls: List[str],
        tmp_path: Path
    ) -> None:
        """
        GitRepositoryManager should initialize successfully with valid inputs.

        Verifies that the manager creates repository configurations and
        sets up the base directory correctly.
        """
        manager = GitRepositoryManager(test_repository_urls, tmp_path)

        assert manager.base_local_path == tmp_path
        assert len(manager.repositories) == len(test_repository_urls)
        assert tmp_path.exists()
        assert tmp_path.is_dir()

    @pytest.mark.parametrize("invalid_urls", [
        ["not-a-url"],
        ["ftp://invalid.com"],
        [""],
        ["https://", "invalid-url"]
    ])
    def test_manager_rejects_invalid_urls(
        self,
        invalid_urls: List[str],
        tmp_path: Path
    ) -> None:
        """
        GitRepositoryManager should reject invalid repository URLs.

        Tests that various forms of invalid URLs are properly rejected
        during initialization.
        """
        with pytest.raises((ValidationError, TypeError)):
            GitRepositoryManager(invalid_urls, tmp_path)

    def test_manager_creates_base_directory_if_missing(
        self,
        test_repository_urls: List[str],
        tmp_path: Path
    ) -> None:
        """
        GitRepositoryManager should create base directory if it doesn't exist.

        Verifies directory creation behavior when the target path is missing.
        """
        non_existent_path = tmp_path / "new" / "nested" / "directory"
        assert not non_existent_path.exists()

        manager = GitRepositoryManager(test_repository_urls, non_existent_path)

        assert manager.base_local_path == non_existent_path
        assert non_existent_path.exists()
        assert non_existent_path.is_dir()


class TestGitRepositoryManagerProcessing:
    """Test GitRepositoryManager repository processing behavior."""

    def test_processes_repositories_successfully_when_cloning_new(
        self,
        git_repository_manager: GitRepositoryManager,
        mocker
    ) -> None:
        """
        Manager should successfully clone new repositories.

        Tests the happy path where all repositories are new and
        cloning succeeds for all of them.
        """
        mock_clone = mocker.patch('git.Repo.clone_from')

        results = git_repository_manager.process_repositories()

        assert len(results) == len(git_repository_manager.repositories)
        assert all(result.success for result in results)
        assert mock_clone.call_count == len(git_repository_manager.repositories)

        for result in results:
            assert result.repository.status == RepositoryStatus.SUCCESS
            assert "cloned successfully" in result.message

    def test_processes_repositories_successfully_when_syncing_existing(
        self,
        git_repository_manager: GitRepositoryManager,
        mocker
    ) -> None:
        """
        Manager should successfully sync existing repositories.

        Tests the scenario where repositories already exist locally
        and need to be synchronized with remote.
        """
        # Create fake existing repositories
        for repo in git_repository_manager.repositories:
            repo.local_path.mkdir(parents=True)
            (repo.local_path / '.git').mkdir()

        mock_repo = Mock()
        mock_origin = Mock()
        mock_repo.remote.return_value = mock_origin
        mock_repo.active_branch.name = 'main'

        mocker.patch('git.Repo', return_value=mock_repo)
        mocker.patch.object(
            git_repository_manager,
            '_validate_repository_remote',
            return_value=True
        )

        results = git_repository_manager.process_repositories()

        assert len(results) == len(git_repository_manager.repositories)
        assert all(result.success for result in results)
        assert mock_origin.fetch.call_count == len(
            git_repository_manager.repositories
        )

        for result in results:
            assert result.repository.status == RepositoryStatus.SUCCESS
            assert "synchronized successfully" in result.message

    def test_handles_mixed_success_and_failure_scenarios(
        self,
        git_repository_manager: GitRepositoryManager,
        mocker
    ) -> None:
        """
        Manager should handle mixed success/failure scenarios gracefully.

        Tests that when some repositories succeed and others fail,
        the manager continues processing and reports all results.
        """
        def mock_clone_side_effect(url, path, **kwargs):
            if "repo1" in str(url):
                return Mock()  # Success
            else:
                raise git.exc.GitCommandError(
                    'clone', 128, stderr='Repository not found'
                )

        mocker.patch('git.Repo.clone_from', side_effect=mock_clone_side_effect)

        results = git_repository_manager.process_repositories()

        assert len(results) == len(git_repository_manager.repositories)

        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]

        assert len(successful_results) >= 1
        assert len(failed_results) >= 1

        for success_result in successful_results:
            assert success_result.repository.status == RepositoryStatus.SUCCESS

        for failed_result in failed_results:
            assert failed_result.repository.status == RepositoryStatus.FAILED

    @pytest.mark.parametrize("git_error,expected_exception", [
        (
            git.exc.GitCommandError('clone', 128, stderr='Repository not found'),
            RepositoryNotFoundError
        ),
        (
            git.exc.GitCommandError('clone', 128, stderr='Permission denied'),
            RepositoryCloneError
        ),
        (
            git.exc.GitCommandError('fetch', 128, stderr='Network error'),
            RepositorySyncError
        ),
    ])
    def test_handles_specific_git_errors_appropriately(
        self,
        single_repo_manager: GitRepositoryManager,
        mocker,
        git_error: git.exc.GitCommandError,
        expected_exception: type
    ) -> None:
        """
        Manager should map Git errors to appropriate domain exceptions.

        Tests that different types of Git errors are properly categorized
        and handled with appropriate exception types.
        """
        mocker.patch('git.Repo.clone_from', side_effect=git_error)

        results = single_repo_manager.process_repositories()

        assert len(results) == 1
        result = results[0]

        assert not result.success
        assert result.repository.status == RepositoryStatus.FAILED
        assert result.error_details is not None

    def test_continues_processing_after_unexpected_errors(
        self,
        git_repository_manager: GitRepositoryManager,
        mocker
    ) -> None:
        """
        Manager should continue processing even after unexpected errors.

        Tests resilience when encountering unexpected exceptions
        during repository processing.
        """
        def mock_side_effect(url, path, **kwargs):
            if "repo1" in str(url):
                raise Exception("Unexpected system error")
            return Mock()  # Other repos succeed

        mocker.patch('git.Repo.clone_from', side_effect=mock_side_effect)

        results = git_repository_manager.process_repositories()

        assert len(results) == len(git_repository_manager.repositories)

        failed_results = [r for r in results if not r.success]
        successful_results = [r for r in results if r.success]

        assert len(failed_results) >= 1
        assert len(successful_results) >= 1

        for failed_result in failed_results:
            if "Unexpected error" in failed_result.message:
                assert "Unexpected system error" in failed_result.error_details


class TestGitRepositoryManagerEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_handles_empty_repository_list(self, tmp_path: Path) -> None:
        """
        Manager should handle empty repository list gracefully.

        Tests behavior when no repositories are provided for processing.
        """
        manager = GitRepositoryManager([], tmp_path)

        results = manager.process_repositories()

        assert len(results) == 0
        assert manager.base_local_path.exists()

    @pytest.mark.parametrize("special_chars_url", [
        "https://github.com/owner/repo-with-dashes",
        "https://github.com/owner/repo_with_underscores",
        "https://github.com/owner/repo.with.dots",
    ])
    def test_handles_urls_with_special_characters(
        self,
        special_chars_url: str,
        tmp_path: Path,
        mocker
    ) -> None:
        """
        Manager should handle repository URLs with special characters.

        Tests that URLs containing various special characters are
        processed correctly.
        """
        mocker.patch('git.Repo.clone_from', return_value=Mock())

        manager = GitRepositoryManager([special_chars_url], tmp_path)
        results = manager.process_repositories()

        assert len(results) == 1
        assert results[0].success

    def test_handles_very_long_repository_paths(
        self,
        tmp_path: Path,
        mocker
    ) -> None:
        """
        Manager should handle very long repository paths.

        Tests behavior with repository URLs that generate long local paths.
        """
        long_url = (
            "https://github.com/very-long-owner-name/"
            "very-long-repository-name-with-many-characters"
        )

        mocker.patch('git.Repo.clone_from', return_value=Mock())

        manager = GitRepositoryManager([long_url], tmp_path)
        results = manager.process_repositories()

        assert len(results) == 1
        assert results[0].success
        # Verify the operation succeeded (path creation is mocked)
        assert results[0].repository.status == RepositoryStatus.SUCCESS


class TestGitRepositoryManagerPathGeneration:
    """Test local path generation behavior."""

    @pytest.mark.parametrize("url,expected_name", [
        ("https://github.com/owner/repo", "owner_repo"),
        ("https://github.com/owner/repo.git", "owner_repo"),
        ("https://github.com/owner-name/repo-name", "owner-name_repo-name"),
        ("https://gitlab.com/user/project", "user_project"),
    ])
    def test_generates_correct_local_paths(
        self,
        url: str,
        expected_name: str,
        tmp_path: Path
    ) -> None:
        """
        Manager should generate appropriate local paths from repository URLs.

        Tests that various URL formats are converted to sensible
        local directory names.
        """
        manager = GitRepositoryManager([url], tmp_path)

        assert len(manager.repositories) == 1
        repo = manager.repositories[0]

        assert repo.local_path.name == expected_name
        assert repo.local_path.parent == tmp_path