"""
Custom exceptions for Java path indexing operations.

This module defines specific exception classes for different types of
indexing operation failures.
"""

from pathlib import Path
from typing import Optional


class IndexerError(Exception):
    """
    Base exception for all indexer-related errors.

    This is the parent class for all indexing operation exceptions,
    providing a common interface for error handling.

    Attributes:
        message: Human-readable error message
        repository_dir: Repository directory that caused the error
        details: Additional error details or context
    """

    def __init__(
        self,
        message: str,
        repository_dir: Optional[Path] = None,
        details: Optional[str] = None
    ) -> None:
        """
        Initialize the indexer error.

        Args:
            message: Human-readable error message
            repository_dir: Repository directory that caused the error
            details: Additional error details or context
        """
        super().__init__(message)
        self.message = message
        self.repository_dir = repository_dir
        self.details = details

    def __str__(self) -> str:
        """Return a string representation of the error."""
        parts = [self.message]
        if self.repository_dir:
            parts.append(f"Directory: {self.repository_dir}")
        if self.details:
            parts.append(f"Details: {self.details}")
        return " | ".join(parts)


class DirectoryAccessError(IndexerError):
    """
    Exception raised when a directory cannot be accessed.

    This exception is raised when a repository directory or its
    subdirectories cannot be read due to permission issues or
    other access problems.
    """

    def __init__(
        self,
        message: str,
        repository_dir: Optional[Path] = None,
        details: Optional[str] = None
    ) -> None:
        """
        Initialize the directory access error.

        Args:
            message: Human-readable error message
            repository_dir: Repository directory that cannot be accessed
            details: Additional error details from OS operation
        """
        super().__init__(
            f"Directory access failed: {message}",
            repository_dir,
            details
        )


class NoJavaFilesFoundError(IndexerError):
    """
    Exception raised when no Java files are found in a repository.

    This exception is raised when a repository directory does not
    contain any Java source files in the expected src/main/java
    directory structure.
    """

    def __init__(
        self,
        message: str,
        repository_dir: Optional[Path] = None,
        details: Optional[str] = None
    ) -> None:
        """
        Initialize the no Java files found error.

        Args:
            message: Human-readable error message
            repository_dir: Repository directory with no Java files
            details: Additional error details or context
        """
        super().__init__(
            f"No Java files found: {message}",
            repository_dir,
            details
        )
