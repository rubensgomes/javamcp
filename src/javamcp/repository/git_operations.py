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
Git operations using GitPython.
"""

from typing import Optional

from git import GitCommandError, InvalidGitRepositoryError, Repo

from .exceptions import (CloneFailedError, GitOperationError,
                         InvalidRepositoryError)


def clone_repository(
    url: str, local_path: str, branch: str = "main", depth: int = 1
) -> Repo:
    """
    Clone a Git repository from URL to local path.

    Args:
        url: Git repository URL
        local_path: Local filesystem path for cloning
        branch: Branch to checkout (default: "main")
        depth: Depth of clone history (default: 1 for shallow clone)

    Returns:
        Repo instance

    Raises:
        CloneFailedError: If cloning fails
    """
    try:
        repo = Repo.clone_from(url, local_path, branch=branch, depth=depth)
        return repo
    except GitCommandError as e:
        raise CloneFailedError(f"Failed to clone repository {url}: {e}") from e
    except Exception as e:
        raise CloneFailedError(f"Unexpected error cloning repository {url}: {e}") from e


def pull_repository(local_path: str) -> None:
    """
    Pull latest changes from remote repository.

    Args:
        local_path: Local repository path

    Raises:
        InvalidRepositoryError: If path is not a valid Git repository
        GitOperationError: If pull operation fails
    """
    if not is_git_repository(local_path):
        raise InvalidRepositoryError(f"Not a valid Git repository: {local_path}")

    try:
        repo = Repo(local_path)
        origin = repo.remotes.origin
        origin.pull()
    except GitCommandError as e:
        raise GitOperationError(
            f"Failed to pull repository at {local_path}: {e}"
        ) from e
    except Exception as e:
        raise GitOperationError(
            f"Unexpected error pulling repository at {local_path}: {e}"
        ) from e


def checkout_branch(local_path: str, branch: str) -> None:
    """
    Checkout a specific branch in the repository.

    Args:
        local_path: Local repository path
        branch: Branch name to checkout

    Raises:
        InvalidRepositoryError: If path is not a valid Git repository
        GitOperationError: If checkout fails
    """
    if not is_git_repository(local_path):
        raise InvalidRepositoryError(f"Not a valid Git repository: {local_path}")

    try:
        repo = Repo(local_path)
        repo.git.checkout(branch)
    except GitCommandError as e:
        raise GitOperationError(
            f"Failed to checkout branch {branch} at {local_path}: {e}"
        ) from e
    except Exception as e:
        raise GitOperationError(
            f"Unexpected error checking out branch {branch} at {local_path}: {e}"
        ) from e


def is_git_repository(local_path: str) -> bool:
    """
    Check if a path contains a valid Git repository.

    Args:
        local_path: Path to check

    Returns:
        True if valid Git repository, False otherwise
    """
    try:
        Repo(local_path)
        return True
    except InvalidGitRepositoryError:
        return False
    except Exception:  # pylint: disable=broad-exception-caught
        return False


def get_current_commit_hash(local_path: str) -> Optional[str]:
    """
    Get the current commit hash of the repository.

    Args:
        local_path: Local repository path

    Returns:
        Commit hash string, or None if unable to retrieve

    Raises:
        InvalidRepositoryError: If path is not a valid Git repository
    """
    if not is_git_repository(local_path):
        raise InvalidRepositoryError(f"Not a valid Git repository: {local_path}")

    try:
        repo = Repo(local_path)
        return repo.head.commit.hexsha
    except Exception:  # pylint: disable=broad-exception-caught
        return None
