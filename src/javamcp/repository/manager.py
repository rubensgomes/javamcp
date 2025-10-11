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
Repository manager for handling multiple Git repositories.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from javamcp.config.schema import RepositoryConfig
from javamcp.models.repository import RepositoryIndex, RepositoryMetadata

from .exceptions import RepositoryNotFoundError
from .git_operations import (clone_repository, get_current_commit_hash,
                             is_git_repository, pull_repository)


class RepositoryManager:
    """
    Manages multiple Git repositories: cloning, updating, and tracking metadata.
    """

    def __init__(self, config: RepositoryConfig):
        """
        Initialize repository manager with configuration.

        Args:
            config: Repository configuration
        """
        self.config = config
        self.repositories: dict[str, RepositoryMetadata] = {}
        self.indices: dict[str, RepositoryIndex] = {}

    def initialize_repositories(self) -> None:
        """
        Initialize all repositories from configuration.
        Clones new repositories and optionally updates existing ones.
        """
        base_path = Path(self.config.local_base_path)
        base_path.mkdir(parents=True, exist_ok=True)

        for url in self.config.urls:
            repo_name = self._get_repo_name_from_url(url)
            local_path = base_path / repo_name

            if local_path.exists() and is_git_repository(str(local_path)):
                # Repository already exists
                if self.config.auto_update:
                    self._update_repository(url, str(local_path))
                else:
                    self._load_existing_repository(url, str(local_path))
            else:
                # Clone new repository
                self._clone_new_repository(url, str(local_path))

    def clone_all_repositories(self) -> None:
        """
        Clone all configured repositories (skip if already exists).
        """
        base_path = Path(self.config.local_base_path)
        base_path.mkdir(parents=True, exist_ok=True)

        for url in self.config.urls:
            repo_name = self._get_repo_name_from_url(url)
            local_path = base_path / repo_name

            if not local_path.exists():
                self._clone_new_repository(url, str(local_path))

    def update_repository(self, url: str) -> None:
        """
        Update (pull) a specific repository by URL.

        Args:
            url: Repository URL

        Raises:
            RepositoryNotFoundError: If repository not found
        """
        if url not in self.repositories:
            raise RepositoryNotFoundError(f"Repository not managed: {url}")

        metadata = self.repositories[url]
        self._update_repository(url, metadata.local_path)

    def get_java_files(self, url: str) -> list[Path]:
        """
        Get list of all Java files in a repository.

        Args:
            url: Repository URL

        Returns:
            List of Path objects for Java files

        Raises:
            RepositoryNotFoundError: If repository not found
        """
        if url not in self.repositories:
            raise RepositoryNotFoundError(f"Repository not managed: {url}")

        metadata = self.repositories[url]
        repo_path = Path(metadata.local_path)

        java_files = list(repo_path.rglob("*.java"))
        return java_files

    def filter_java_files_by_package(self, url: str, package_path: str) -> list[Path]:
        """
        Filter Java files by package path.

        Args:
            url: Repository URL
            package_path: Package path (e.g., "com/example/service")

        Returns:
            List of Path objects matching package path

        Raises:
            RepositoryNotFoundError: If repository not found
        """
        all_files = self.get_java_files(url)
        package_parts = Path(package_path)

        filtered = [
            f
            for f in all_files
            if package_parts in f.relative_to(self.repositories[url].local_path).parents
            or f.parent.name == package_parts.name
        ]

        return filtered

    def get_repository_metadata(self, url: str) -> Optional[RepositoryMetadata]:
        """
        Get metadata for a repository.

        Args:
            url: Repository URL

        Returns:
            RepositoryMetadata or None if not found
        """
        return self.repositories.get(url)

    def get_repository_by_name(self, name: str) -> Optional[RepositoryMetadata]:
        """
        Get repository metadata by repository name.

        Args:
            name: Repository name (extracted from URL)

        Returns:
            RepositoryMetadata or None if not found
        """
        for url, metadata in self.repositories.items():
            repo_name = self._get_repo_name_from_url(url)
            if repo_name == name:
                return metadata
        return None

    def get_repository_path(self, url: str) -> Optional[Path]:
        """
        Get local file system path for a repository.

        Args:
            url: Repository URL

        Returns:
            Path to repository or None if not found
        """
        metadata = self.get_repository_metadata(url)
        if metadata:
            return Path(metadata.local_path)
        return None

    def _get_repo_name_from_url(self, url: str) -> str:
        """Extract repository name from Git URL."""
        # Handle URLs like https://github.com/user/repo.git
        name = url.rstrip("/").split("/")[-1]
        if name.endswith(".git"):
            name = name[:-4]
        return name

    def _clone_new_repository(self, url: str, local_path: str) -> None:
        """Clone a new repository and track metadata."""
        clone_repository(url, local_path)

        commit_hash = get_current_commit_hash(local_path)
        now = datetime.now()

        metadata = RepositoryMetadata(
            url=url,
            branch="main",
            local_path=local_path,
            last_cloned=now,
            last_updated=now,
            commit_hash=commit_hash,
        )

        self.repositories[url] = metadata

    def _update_repository(self, url: str, local_path: str) -> None:
        """Pull latest changes and update metadata."""
        pull_repository(local_path)

        commit_hash = get_current_commit_hash(local_path)
        now = datetime.now()

        if url in self.repositories:
            self.repositories[url].last_updated = now
            self.repositories[url].commit_hash = commit_hash
        else:
            metadata = RepositoryMetadata(
                url=url,
                branch="main",
                local_path=local_path,
                last_updated=now,
                commit_hash=commit_hash,
            )
            self.repositories[url] = metadata

    def _load_existing_repository(self, url: str, local_path: str) -> None:
        """Load metadata for existing repository without updating."""
        commit_hash = get_current_commit_hash(local_path)

        metadata = RepositoryMetadata(
            url=url,
            branch="main",
            local_path=local_path,
            commit_hash=commit_hash,
        )

        self.repositories[url] = metadata
