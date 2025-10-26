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
Unit tests for Git operations.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from git import GitCommandError, Repo

from javamcp.repository.exceptions import (CloneFailedError, GitOperationError,
                                           InvalidRepositoryError)
from javamcp.repository.git_operations import (checkout_branch,
                                               clone_repository,
                                               get_current_branch_name,
                                               get_current_commit_hash,
                                               is_git_repository,
                                               pull_repository)


class TestCloneRepository:
    """Tests for clone_repository function."""

    @patch("javamcp.repository.git_operations.Repo")
    def test_clone_repository_success(self, mock_repo_class):
        """Test successful repository cloning with default branch (None)."""
        mock_repo = MagicMock()
        mock_repo_class.clone_from.return_value = mock_repo

        repo = clone_repository("https://github.com/example/repo.git", "/tmp/repo")

        assert repo == mock_repo
        mock_repo_class.clone_from.assert_called_once_with(
            "https://github.com/example/repo.git", "/tmp/repo", depth=1
        )

    @patch("javamcp.repository.git_operations.Repo")
    def test_clone_repository_custom_branch(self, mock_repo_class):
        """Test cloning with custom branch."""
        mock_repo = MagicMock()
        mock_repo_class.clone_from.return_value = mock_repo

        clone_repository(
            "https://github.com/example/repo.git", "/tmp/repo", branch="develop"
        )

        mock_repo_class.clone_from.assert_called_once_with(
            "https://github.com/example/repo.git",
            "/tmp/repo",
            branch="develop",
            depth=1,
        )

    @patch("javamcp.repository.git_operations.Repo")
    def test_clone_repository_custom_depth(self, mock_repo_class):
        """Test cloning with custom depth."""
        mock_repo = MagicMock()
        mock_repo_class.clone_from.return_value = mock_repo

        clone_repository("https://github.com/example/repo.git", "/tmp/repo", depth=5)

        mock_repo_class.clone_from.assert_called_once_with(
            "https://github.com/example/repo.git", "/tmp/repo", depth=5
        )

    @patch("javamcp.repository.git_operations.Repo")
    def test_clone_repository_fails(self, mock_repo_class):
        """Test cloning failure raises CloneFailedError."""
        mock_repo_class.clone_from.side_effect = GitCommandError("clone", "error")

        with pytest.raises(CloneFailedError, match="Failed to clone"):
            clone_repository("https://github.com/example/repo.git", "/tmp/repo")


class TestPullRepository:
    """Tests for pull_repository function."""

    @patch("javamcp.repository.git_operations.is_git_repository")
    @patch("javamcp.repository.git_operations.Repo")
    def test_pull_repository_success(self, mock_repo_class, mock_is_git):
        """Test successful repository pull."""
        mock_is_git.return_value = True
        mock_repo = MagicMock()
        mock_origin = MagicMock()
        mock_repo.remotes.origin = mock_origin
        mock_repo_class.return_value = mock_repo

        pull_repository("/tmp/repo")

        mock_origin.pull.assert_called_once()

    @patch("javamcp.repository.git_operations.is_git_repository")
    def test_pull_repository_invalid_repo(self, mock_is_git):
        """Test pull on invalid repository raises error."""
        mock_is_git.return_value = False

        with pytest.raises(InvalidRepositoryError, match="Not a valid Git repository"):
            pull_repository("/tmp/not-a-repo")

    @patch("javamcp.repository.git_operations.is_git_repository")
    @patch("javamcp.repository.git_operations.Repo")
    def test_pull_repository_fails(self, mock_repo_class, mock_is_git):
        """Test pull failure raises GitOperationError."""
        mock_is_git.return_value = True
        mock_repo = MagicMock()
        mock_origin = MagicMock()
        mock_origin.pull.side_effect = GitCommandError("pull", "error")
        mock_repo.remotes.origin = mock_origin
        mock_repo_class.return_value = mock_repo

        with pytest.raises(GitOperationError, match="Failed to pull"):
            pull_repository("/tmp/repo")


class TestCheckoutBranch:
    """Tests for checkout_branch function."""

    @patch("javamcp.repository.git_operations.is_git_repository")
    @patch("javamcp.repository.git_operations.Repo")
    def test_checkout_branch_success(self, mock_repo_class, mock_is_git):
        """Test successful branch checkout."""
        mock_is_git.return_value = True
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo

        checkout_branch("/tmp/repo", "develop")

        mock_repo.git.checkout.assert_called_once_with("develop")

    @patch("javamcp.repository.git_operations.is_git_repository")
    def test_checkout_branch_invalid_repo(self, mock_is_git):
        """Test checkout on invalid repository raises error."""
        mock_is_git.return_value = False

        with pytest.raises(InvalidRepositoryError, match="Not a valid Git repository"):
            checkout_branch("/tmp/not-a-repo", "develop")

    @patch("javamcp.repository.git_operations.is_git_repository")
    @patch("javamcp.repository.git_operations.Repo")
    def test_checkout_branch_fails(self, mock_repo_class, mock_is_git):
        """Test checkout failure raises GitOperationError."""
        mock_is_git.return_value = True
        mock_repo = MagicMock()
        mock_repo.git.checkout.side_effect = GitCommandError("checkout", "error")
        mock_repo_class.return_value = mock_repo

        with pytest.raises(GitOperationError, match="Failed to checkout branch"):
            checkout_branch("/tmp/repo", "develop")


class TestIsGitRepository:
    """Tests for is_git_repository function."""

    @patch("javamcp.repository.git_operations.Repo")
    def test_is_git_repository_valid(self, mock_repo_class):
        """Test valid Git repository returns True."""
        mock_repo_class.return_value = MagicMock()

        result = is_git_repository("/tmp/repo")

        assert result is True

    @patch("javamcp.repository.git_operations.Repo")
    def test_is_git_repository_invalid(self, mock_repo_class):
        """Test invalid repository returns False."""
        from git import InvalidGitRepositoryError

        mock_repo_class.side_effect = InvalidGitRepositoryError

        result = is_git_repository("/tmp/not-a-repo")

        assert result is False


class TestGetCurrentCommitHash:
    """Tests for get_current_commit_hash function."""

    @patch("javamcp.repository.git_operations.is_git_repository")
    @patch("javamcp.repository.git_operations.Repo")
    def test_get_commit_hash_success(self, mock_repo_class, mock_is_git):
        """Test getting commit hash successfully."""
        mock_is_git.return_value = True
        mock_repo = MagicMock()
        mock_repo.head.commit.hexsha = "abc123def456"
        mock_repo_class.return_value = mock_repo

        commit_hash = get_current_commit_hash("/tmp/repo")

        assert commit_hash == "abc123def456"

    @patch("javamcp.repository.git_operations.is_git_repository")
    def test_get_commit_hash_invalid_repo(self, mock_is_git):
        """Test getting commit hash from invalid repository raises error."""
        mock_is_git.return_value = False

        with pytest.raises(InvalidRepositoryError, match="Not a valid Git repository"):
            get_current_commit_hash("/tmp/not-a-repo")

    @patch("javamcp.repository.git_operations.is_git_repository")
    @patch("javamcp.repository.git_operations.Repo")
    def test_get_commit_hash_fails(self, mock_repo_class, mock_is_git):
        """Test getting commit hash failure returns None."""
        mock_is_git.return_value = True
        mock_repo = MagicMock()
        # Configure the mock to raise an exception when accessing hexsha
        type(mock_repo.head.commit).hexsha = property(
            lambda self: (_ for _ in ()).throw(Exception("error"))
        )
        mock_repo_class.return_value = mock_repo

        commit_hash = get_current_commit_hash("/tmp/repo")

        assert commit_hash is None


class TestGetCurrentBranchName:
    """Tests for get_current_branch_name function."""

    @patch("javamcp.repository.git_operations.is_git_repository")
    @patch("javamcp.repository.git_operations.Repo")
    def test_get_branch_name_success(self, mock_repo_class, mock_is_git):
        """Test getting branch name successfully."""
        mock_is_git.return_value = True
        mock_repo = MagicMock()
        mock_repo.head.is_detached = False
        mock_repo.active_branch.name = "main"
        mock_repo_class.return_value = mock_repo

        branch_name = get_current_branch_name("/tmp/repo")

        assert branch_name == "main"

    @patch("javamcp.repository.git_operations.is_git_repository")
    @patch("javamcp.repository.git_operations.Repo")
    def test_get_branch_name_master(self, mock_repo_class, mock_is_git):
        """Test getting branch name for master branch."""
        mock_is_git.return_value = True
        mock_repo = MagicMock()
        mock_repo.head.is_detached = False
        mock_repo.active_branch.name = "master"
        mock_repo_class.return_value = mock_repo

        branch_name = get_current_branch_name("/tmp/repo")

        assert branch_name == "master"

    @patch("javamcp.repository.git_operations.is_git_repository")
    @patch("javamcp.repository.git_operations.Repo")
    def test_get_branch_name_detached_head(self, mock_repo_class, mock_is_git):
        """Test getting branch name with detached HEAD returns None."""
        mock_is_git.return_value = True
        mock_repo = MagicMock()
        mock_repo.head.is_detached = True
        mock_repo_class.return_value = mock_repo

        branch_name = get_current_branch_name("/tmp/repo")

        assert branch_name is None

    @patch("javamcp.repository.git_operations.is_git_repository")
    def test_get_branch_name_invalid_repo(self, mock_is_git):
        """Test getting branch name from invalid repository raises error."""
        mock_is_git.return_value = False

        with pytest.raises(InvalidRepositoryError, match="Not a valid Git repository"):
            get_current_branch_name("/tmp/not-a-repo")

    @patch("javamcp.repository.git_operations.is_git_repository")
    @patch("javamcp.repository.git_operations.Repo")
    def test_get_branch_name_fails(self, mock_repo_class, mock_is_git):
        """Test getting branch name failure returns None."""
        mock_is_git.return_value = True
        mock_repo = MagicMock()
        mock_repo.head.is_detached = False
        # Configure the mock to raise an exception when accessing active_branch.name
        type(mock_repo).active_branch = property(
            lambda self: (_ for _ in ()).throw(Exception("error"))
        )
        mock_repo_class.return_value = mock_repo

        branch_name = get_current_branch_name("/tmp/repo")

        assert branch_name is None
