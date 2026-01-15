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

from javamcp.logging import get_logger

from .exceptions import CloneFailedError, GitOperationError, InvalidRepositoryError

# Module-level logger
logger = get_logger("repository.git")


def clone_repository(
    url: str, local_path: str, branch: Optional[str] = None, depth: int = 1
) -> Repo:
    """
    Clone a Git repository from URL to local path.

    Args:
        url: Git repository URL
        local_path: Local filesystem path for cloning
        branch: Branch to checkout (default: None, which clones the remote's default branch)
        depth: Depth of clone history (default: 1 for shallow clone)

    Returns:
        Repo instance

    Raises:
        CloneFailedError: If cloning fails
    """
    logger.info(
        "Cloning repository: %s -> %s (branch=%s, depth=%d)",
        url,
        local_path,
        branch or "default",
        depth,
    )
    try:
        # Only pass branch parameter if explicitly specified
        if branch is not None:
            repo = Repo.clone_from(url, local_path, branch=branch, depth=depth)
        else:
            repo = Repo.clone_from(url, local_path, depth=depth)
        logger.debug("Clone successful: %s", url)
        return repo
    except GitCommandError as e:
        logger.error("Git clone failed for %s: %s", url, e)
        raise CloneFailedError(f"Failed to clone repository {url}: {e}") from e
    except Exception as e:
        logger.error("Unexpected error cloning %s: %s", url, e, exc_info=True)
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
    logger.debug("Pulling latest changes: %s", local_path)
    if not is_git_repository(local_path):
        logger.error("Not a valid Git repository: %s", local_path)
        raise InvalidRepositoryError(f"Not a valid Git repository: {local_path}")

    try:
        repo = Repo(local_path)
        origin = repo.remotes.origin
        origin.pull()
        logger.debug("Pull successful: %s", local_path)
    except GitCommandError as e:
        logger.error("Git pull failed for %s: %s", local_path, e)
        raise GitOperationError(
            f"Failed to pull repository at {local_path}: {e}"
        ) from e
    except Exception as e:
        logger.error("Unexpected error pulling %s: %s", local_path, e, exc_info=True)
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
    logger.info("Checking out branch '%s' in %s", branch, local_path)
    if not is_git_repository(local_path):
        logger.error("Not a valid Git repository: %s", local_path)
        raise InvalidRepositoryError(f"Not a valid Git repository: {local_path}")

    try:
        repo = Repo(local_path)
        repo.git.checkout(branch)
        logger.debug("Checkout successful: %s -> %s", local_path, branch)
    except GitCommandError as e:
        logger.error("Git checkout failed for %s branch %s: %s", local_path, branch, e)
        raise GitOperationError(
            f"Failed to checkout branch {branch} at {local_path}: {e}"
        ) from e
    except Exception as e:
        logger.error(
            "Unexpected error checking out %s branch %s: %s",
            local_path,
            branch,
            e,
            exc_info=True,
        )
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
        logger.debug("Path is not a git repository: %s", local_path)
        return False
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.debug("Path %s is not a valid git repository: %s", local_path, e)
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
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.warning("Could not get commit hash for %s: %s", local_path, e)
        return None


def get_current_branch_name(local_path: str) -> Optional[str]:
    """
    Get the current branch name of the repository.

    Args:
        local_path: Local repository path

    Returns:
        Branch name string, or None if unable to retrieve (e.g., detached HEAD)

    Raises:
        InvalidRepositoryError: If path is not a valid Git repository
    """
    if not is_git_repository(local_path):
        raise InvalidRepositoryError(f"Not a valid Git repository: {local_path}")

    try:
        repo = Repo(local_path)
        if repo.head.is_detached:
            logger.debug("Repository %s has detached HEAD", local_path)
            return None
        return repo.active_branch.name
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.warning("Could not get branch name for %s: %s", local_path, e)
        return None
