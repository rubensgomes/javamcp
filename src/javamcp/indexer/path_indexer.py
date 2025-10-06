"""
Java source file path indexing functionality.

This module provides the JavaPathIndexer class for discovering and
indexing Java source files in cloned Git repositories.
"""

import logging
from pathlib import Path
from typing import List, Union

from .models import IndexerConfig, IndexResult, JavaFilePath
from .exceptions import (
    IndexerError,
    DirectoryAccessError,
    NoJavaFilesFoundError
)

logger = logging.getLogger(__name__)


class JavaPathIndexer:
    """
    Indexes Java source files in Git repository directories.

    This class traverses repository directories to identify and index
    all Java source files located under src/main/java directories. It
    provides structured results with file paths and error reporting.

    Attributes:
        config: Configuration for indexing operations
        indexed_files: List of discovered Java file paths
    """

    def __init__(
        self,
        repository_dirs: List[Union[str, Path]],
        java_source_pattern: str = "src/main/java"
    ) -> None:
        """
        Initialize the JavaPathIndexer.

        Args:
            repository_dirs: List of repository directory paths to index
            java_source_pattern: Pattern to identify Java source dirs

        Raises:
            IndexerError: If repository directories are invalid
        """
        path_list = [
            Path(d).resolve() for d in repository_dirs
        ]

        self.config = IndexerConfig(
            repository_dirs=path_list,
            java_source_pattern=java_source_pattern
        )
        self.indexed_files: List[JavaFilePath] = []

        logger.info(
            f"Initialized JavaPathIndexer with "
            f"{len(self.config.repository_dirs)} repositories"
        )

    def _find_java_source_dirs(
        self,
        repository_dir: Path
    ) -> List[Path]:
        """
        Find all src/main/java directories in a repository.

        Args:
            repository_dir: Repository directory to search

        Returns:
            List of paths to src/main/java directories

        Raises:
            DirectoryAccessError: If directory cannot be accessed
        """
        java_source_dirs = []

        try:
            for path in repository_dir.rglob(
                self.config.java_source_pattern
            ):
                if path.is_dir():
                    java_source_dirs.append(path)
                    logger.debug(
                        f"Found Java source directory: {path}"
                    )

        except (OSError, PermissionError) as e:
            raise DirectoryAccessError(
                f"Cannot access directory tree",
                repository_dir=repository_dir,
                details=str(e)
            ) from e

        return java_source_dirs

    def _collect_java_files(
        self,
        java_source_dir: Path,
        repository_dir: Path
    ) -> List[JavaFilePath]:
        """
        Collect all Java files from a Java source directory.

        Args:
            java_source_dir: Java source directory to search
            repository_dir: Repository root directory

        Returns:
            List of JavaFilePath objects for discovered files

        Raises:
            DirectoryAccessError: If directory cannot be accessed
        """
        java_files = []

        try:
            for java_file in java_source_dir.rglob("*.java"):
                if java_file.is_file():
                    relative_path = java_file.relative_to(
                        repository_dir
                    )

                    java_file_path = JavaFilePath(
                        absolute_path=java_file,
                        relative_path=relative_path,
                        repository_dir=repository_dir
                    )
                    java_files.append(java_file_path)

                    logger.debug(
                        f"Found Java file: {relative_path}"
                    )

        except (OSError, PermissionError) as e:
            raise DirectoryAccessError(
                f"Cannot access Java source files",
                repository_dir=repository_dir,
                details=str(e)
            ) from e

        return java_files

    def _index_repository(
        self,
        repository_dir: Path
    ) -> IndexResult:
        """
        Index all Java files in a single repository.

        Args:
            repository_dir: Repository directory to index

        Returns:
            IndexResult with discovered files and status
        """
        try:
            logger.info(
                f"Indexing repository: {repository_dir}"
            )

            java_source_dirs = self._find_java_source_dirs(
                repository_dir
            )

            if not java_source_dirs:
                raise NoJavaFilesFoundError(
                    f"No src/main/java directories found",
                    repository_dir=repository_dir,
                    details=(
                        f"Expected pattern: "
                        f"{self.config.java_source_pattern}"
                    )
                )

            all_java_files = []
            for java_source_dir in java_source_dirs:
                java_files = self._collect_java_files(
                    java_source_dir,
                    repository_dir
                )
                all_java_files.extend(java_files)

            if not all_java_files:
                raise NoJavaFilesFoundError(
                    f"No .java files found in src/main/java",
                    repository_dir=repository_dir
                )

            self.indexed_files.extend(all_java_files)

            logger.info(
                f"Successfully indexed {len(all_java_files)} "
                f"Java files from {repository_dir}"
            )

            return IndexResult(
                repository_dir=repository_dir,
                java_files=all_java_files,
                success=True,
                message=(
                    f"Indexed {len(all_java_files)} Java files "
                    f"successfully"
                )
            )

        except (DirectoryAccessError, NoJavaFilesFoundError) as e:
            logger.error(
                f"Indexing failed for {repository_dir}: {e}"
            )

            return IndexResult(
                repository_dir=repository_dir,
                java_files=[],
                success=False,
                message=str(e),
                error_details=getattr(e, 'details', None)
            )

        except Exception as e:
            logger.error(
                f"Unexpected error indexing {repository_dir}: {e}"
            )

            return IndexResult(
                repository_dir=repository_dir,
                java_files=[],
                success=False,
                message=f"Unexpected error: {e}",
                error_details=str(e)
            )

    def index_repositories(self) -> List[IndexResult]:
        """
        Index all configured repositories.

        This method processes all repository directories and discovers
        Java source files in src/main/java directories. It continues
        processing even if individual repositories fail.

        Returns:
            List of IndexResult objects with operation outcomes

        Note:
            This method does not raise exceptions for individual
            repository failures. All errors are in returned results.
        """
        results = []

        logger.info(
            f"Indexing {len(self.config.repository_dirs)} "
            f"repositories"
        )

        for repository_dir in self.config.repository_dirs:
            result = self._index_repository(repository_dir)
            results.append(result)

        successful_count = sum(1 for r in results if r.success)
        failed_count = len(results) - successful_count
        total_files = sum(len(r.java_files) for r in results)

        logger.info(
            f"Indexing completed. Repositories - "
            f"Successful: {successful_count}, "
            f"Failed: {failed_count}. "
            f"Total Java files: {total_files}"
        )

        return results

    def get_all_java_files(self) -> List[JavaFilePath]:
        """
        Get all indexed Java files.

        Returns:
            List of all JavaFilePath objects discovered during indexing
        """
        return self.indexed_files.copy()
