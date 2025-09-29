"""
Git repository management functionality.

This module provides the GitRepositoryManager class for cloning and
synchronizing Git repositories containing Java source code.
"""

import logging
from pathlib import Path
from typing import List, Union
from urllib.parse import urlparse

import git
from pydantic import HttpUrl, ValidationError

from .models import Repository, RepositoryStatus, RepositoryResult
from .exceptions import (
    RepositoryError,
    RepositoryCloneError,
    RepositorySyncError,
    RepositoryNotFoundError
)

logger = logging.getLogger(__name__)


class GitRepositoryManager:
    """
    Manages Git repository cloning and synchronization operations.

    This class handles the cloning of new repositories and synchronization
    of existing repositories with their remote origins. It focuses on the
    main branch only and supports public repositories without authentication.

    Attributes:
        repositories: List of repository configurations to manage
        base_local_path: Base directory where repositories will be stored
    """

    def __init__(
        self,
        repository_urls: List[Union[str, HttpUrl]],
        base_local_path: Union[str, Path]
    ) -> None:
        """
        Initialize the GitRepositoryManager.

        Args:
            repository_urls: List of Git repository URLs to manage
            base_local_path: Base directory path for repository storage

        Raises:
            RepositoryError: If base_local_path is invalid or inaccessible
            ValidationError: If any repository URL is invalid
        """
        self.base_local_path = self._validate_base_path(base_local_path)
        self.repositories = self._create_repository_configs(repository_urls)

        logger.info(
            f"Initialized GitRepositoryManager with {len(self.repositories)} "
            f"repositories, base path: {self.base_local_path}"
        )

    def _validate_base_path(self, path: Union[str, Path]) -> Path:
        """
        Validate and create the base local path.

        Args:
            path: Base directory path for repository storage

        Returns:
            Validated Path object

        Raises:
            RepositoryError: If path is invalid or cannot be created
        """
        base_path = Path(path).resolve()

        try:
            base_path.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            raise RepositoryError(
                f"Cannot create base directory: {base_path}",
                details=str(e)
            ) from e

        if not base_path.is_dir():
            raise RepositoryError(
                f"Base path is not a directory: {base_path}"
            )

        return base_path

    def _create_repository_configs(
        self,
        urls: List[Union[str, HttpUrl]]
    ) -> List[Repository]:
        """
        Create repository configuration objects from URLs.

        Args:
            urls: List of repository URLs

        Returns:
            List of Repository configuration objects

        Raises:
            ValidationError: If any URL is invalid
        """
        repositories = []

        for url in urls:
            try:
                if isinstance(url, str):
                    validated_url = HttpUrl(url)
                else:
                    validated_url = url

                local_path = self._generate_local_path(validated_url)
                repository = Repository(
                    url=validated_url,
                    local_path=local_path
                )
                repositories.append(repository)

            except ValidationError as e:
                logger.error(f"Invalid repository URL: {url}")
                raise ValidationError(
                    f"Invalid repository URL: {url}"
                ) from e

        return repositories

    def _generate_local_path(self, url: HttpUrl) -> Path:
        """
        Generate local filesystem path for a repository URL.

        Args:
            url: Repository URL

        Returns:
            Local path where the repository should be stored
        """
        parsed = urlparse(str(url))
        path_parts = parsed.path.strip('/').split('/')

        if len(path_parts) >= 2:
            owner = path_parts[-2]
            repo_name = path_parts[-1]
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]
            folder_name = f"{owner}_{repo_name}"
        else:
            folder_name = parsed.netloc.replace('.', '_')

        return self.base_local_path / folder_name

    def _repository_exists(self, repository: Repository) -> bool:
        """
        Check if a repository already exists locally.

        Args:
            repository: Repository configuration to check

        Returns:
            True if repository exists and is valid, False otherwise
        """
        try:
            if not repository.local_path.exists():
                return False

            if not repository.local_path.is_dir():
                logger.warning(
                    f"Local path exists but is not a directory: "
                    f"{repository.local_path}"
                )
                return False

            git_dir = repository.local_path / '.git'
            if not git_dir.exists():
                logger.warning(
                    f"Directory exists but is not a Git repository: "
                    f"{repository.local_path}"
                )
                return False

            return True

        except (OSError, PermissionError) as e:
            logger.warning(
                f"Cannot access repository path {repository.local_path}: {e}"
            )
            return False

    def _validate_repository_remote(self, repository: Repository) -> bool:
        """
        Validate that local repository remote matches expected URL.

        Args:
            repository: Repository configuration to validate

        Returns:
            True if remote URL matches, False otherwise
        """
        try:
            repo = git.Repo(repository.local_path)
            origin = repo.remote('origin')
            remote_url = origin.url

            if remote_url == str(repository.url):
                return True

            if remote_url.endswith('.git') and not str(repository.url).endswith('.git'):
                if remote_url[:-4] == str(repository.url):
                    return True

            if not remote_url.endswith('.git') and str(repository.url).endswith('.git'):
                if remote_url == str(repository.url)[:-4]:
                    return True

            logger.warning(
                f"Repository remote URL mismatch. "
                f"Expected: {repository.url}, Found: {remote_url}"
            )
            return False

        except (git.exc.GitError, git.exc.InvalidGitRepositoryError) as e:
            logger.warning(
                f"Cannot validate repository remote for "
                f"{repository.local_path}: {e}"
            )
            return False

    def _clone_repository(self, repository: Repository) -> RepositoryResult:
        """
        Clone a fresh repository from remote URL.

        Args:
            repository: Repository configuration to clone

        Returns:
            RepositoryResult with operation outcome
        """
        try:
            logger.info(f"Cloning repository {repository.url} to {repository.local_path}")
            repository.status = RepositoryStatus.CLONING

            if repository.local_path.exists():
                logger.warning(
                    f"Target directory already exists, removing: "
                    f"{repository.local_path}"
                )
                import shutil
                shutil.rmtree(repository.local_path)

            repository.local_path.parent.mkdir(parents=True, exist_ok=True)

            git.Repo.clone_from(
                str(repository.url),
                repository.local_path,
                branch='main',
                single_branch=True,
                depth=1
            )

            repository.status = RepositoryStatus.SUCCESS
            logger.info(f"Successfully cloned repository to {repository.local_path}")

            return RepositoryResult(
                repository=repository,
                success=True,
                message=f"Repository cloned successfully to {repository.local_path}"
            )

        except git.exc.GitCommandError as e:
            repository.status = RepositoryStatus.FAILED
            error_msg = f"Git command failed: {e}"
            logger.error(f"Clone failed for {repository.url}: {error_msg}")

            if "Repository not found" in str(e) or "does not exist" in str(e):
                raise RepositoryNotFoundError(
                    f"Repository not found or inaccessible",
                    repository_url=str(repository.url),
                    details=str(e)
                ) from e
            else:
                raise RepositoryCloneError(
                    error_msg,
                    repository_url=str(repository.url),
                    details=str(e)
                ) from e

        except Exception as e:
            repository.status = RepositoryStatus.FAILED
            error_msg = f"Unexpected error during clone: {e}"
            logger.error(f"Clone failed for {repository.url}: {error_msg}")

            raise RepositoryCloneError(
                error_msg,
                repository_url=str(repository.url),
                details=str(e)
            ) from e

    def _sync_repository(self, repository: Repository) -> RepositoryResult:
        """
        Synchronize an existing repository with its remote origin.

        Args:
            repository: Repository configuration to synchronize

        Returns:
            RepositoryResult with operation outcome
        """
        try:
            logger.info(f"Syncing repository {repository.url} at {repository.local_path}")
            repository.status = RepositoryStatus.SYNCING

            repo = git.Repo(repository.local_path)

            if not self._validate_repository_remote(repository):
                raise RepositorySyncError(
                    "Repository remote URL does not match expected URL",
                    repository_url=str(repository.url),
                    details=f"Local path: {repository.local_path}"
                )

            origin = repo.remote('origin')

            try:
                origin.fetch()
            except git.exc.GitCommandError as e:
                raise RepositorySyncError(
                    f"Failed to fetch from remote: {e}",
                    repository_url=str(repository.url),
                    details=str(e)
                ) from e

            if repo.active_branch.name != 'main':
                try:
                    repo.git.checkout('main')
                except git.exc.GitCommandError:
                    try:
                        repo.git.checkout('-b', 'main', 'origin/main')
                    except git.exc.GitCommandError as e:
                        raise RepositorySyncError(
                            f"Cannot checkout main branch: {e}",
                            repository_url=str(repository.url),
                            details=str(e)
                        ) from e

            try:
                repo.git.reset('--hard', 'origin/main')
            except git.exc.GitCommandError as e:
                raise RepositorySyncError(
                    f"Failed to reset to origin/main: {e}",
                    repository_url=str(repository.url),
                    details=str(e)
                ) from e

            repository.status = RepositoryStatus.SUCCESS
            logger.info(f"Successfully synced repository at {repository.local_path}")

            return RepositoryResult(
                repository=repository,
                success=True,
                message=f"Repository synchronized successfully at {repository.local_path}"
            )

        except git.exc.InvalidGitRepositoryError as e:
            repository.status = RepositoryStatus.FAILED
            error_msg = f"Invalid Git repository: {e}"
            logger.error(f"Sync failed for {repository.url}: {error_msg}")

            raise RepositorySyncError(
                error_msg,
                repository_url=str(repository.url),
                details=str(e)
            ) from e

        except git.exc.GitCommandError as e:
            repository.status = RepositoryStatus.FAILED
            error_msg = f"Git command failed: {e}"
            logger.error(f"Sync failed for {repository.url}: {error_msg}")

            raise RepositorySyncError(
                error_msg,
                repository_url=str(repository.url),
                details=str(e)
            ) from e

        except Exception as e:
            repository.status = RepositoryStatus.FAILED
            error_msg = f"Unexpected error during sync: {e}"
            logger.error(f"Sync failed for {repository.url}: {error_msg}")

            raise RepositorySyncError(
                error_msg,
                repository_url=str(repository.url),
                details=str(e)
            ) from e

    def process_repositories(self) -> List[RepositoryResult]:
        """
        Process all configured repositories by cloning or syncing as needed.

        This method iterates through all repository configurations and either
        clones new repositories or synchronizes existing ones. It continues
        processing even if individual repositories fail, collecting all results.

        Returns:
            List of RepositoryResult objects with operation outcomes

        Note:
            This method does not raise exceptions for individual repository
            failures. All errors are captured in the returned results.
        """
        results = []

        logger.info(
            f"Processing {len(self.repositories)} repositories in "
            f"{self.base_local_path}"
        )

        for repository in self.repositories:
            try:
                if self._repository_exists(repository):
                    logger.info(
                        f"Repository exists locally, syncing: {repository.url}"
                    )
                    result = self._sync_repository(repository)
                else:
                    logger.info(
                        f"Repository does not exist locally, cloning: "
                        f"{repository.url}"
                    )
                    result = self._clone_repository(repository)

                results.append(result)

            except (RepositoryError, RepositoryCloneError,
                    RepositorySyncError, RepositoryNotFoundError) as e:
                logger.error(f"Repository operation failed: {e}")

                repository.status = RepositoryStatus.FAILED
                result = RepositoryResult(
                    repository=repository,
                    success=False,
                    message=str(e),
                    error_details=getattr(e, 'details', None)
                )
                results.append(result)

            except Exception as e:
                logger.error(
                    f"Unexpected error processing repository "
                    f"{repository.url}: {e}"
                )

                repository.status = RepositoryStatus.FAILED
                result = RepositoryResult(
                    repository=repository,
                    success=False,
                    message=f"Unexpected error: {e}",
                    error_details=str(e)
                )
                results.append(result)

        successful_count = sum(1 for r in results if r.success)
        failed_count = len(results) - successful_count

        logger.info(
            f"Repository processing completed. "
            f"Successful: {successful_count}, Failed: {failed_count}"
        )

        return results