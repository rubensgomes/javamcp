"""
Custom exceptions for repository operations.

This module defines specific exception classes for different types of
repository operation failures.
"""

from typing import Optional


class RepositoryError(Exception):
    """
    Base exception for all repository-related errors.

    This is the parent class for all repository operation exceptions,
    providing a common interface for error handling.

    Attributes:
        message: Human-readable error message
        repository_url: URL of the repository that caused the error
        details: Additional error details or context
    """

    def __init__(
        self,
        message: str,
        repository_url: Optional[str] = None,
        details: Optional[str] = None
    ) -> None:
        """
        Initialize the repository error.

        Args:
            message: Human-readable error message
            repository_url: URL of the repository that caused the error
            details: Additional error details or context
        """
        super().__init__(message)
        self.message = message
        self.repository_url = repository_url
        self.details = details

    def __str__(self) -> str:
        """Return a string representation of the error."""
        parts = [self.message]
        if self.repository_url:
            parts.append(f"Repository: {self.repository_url}")
        if self.details:
            parts.append(f"Details: {self.details}")
        return " | ".join(parts)


class RepositoryCloneError(RepositoryError):
    """
    Exception raised when repository cloning fails.

    This exception is raised when a fresh clone operation cannot be
    completed successfully.
    """

    def __init__(
        self,
        message: str,
        repository_url: Optional[str] = None,
        details: Optional[str] = None
    ) -> None:
        """
        Initialize the clone error.

        Args:
            message: Human-readable error message
            repository_url: URL of the repository that failed to clone
            details: Additional error details from Git operation
        """
        super().__init__(
            f"Clone failed: {message}",
            repository_url,
            details
        )


class RepositorySyncError(RepositoryError):
    """
    Exception raised when repository synchronization fails.

    This exception is raised when an existing repository cannot be
    synchronized with its remote origin.
    """

    def __init__(
        self,
        message: str,
        repository_url: Optional[str] = None,
        details: Optional[str] = None
    ) -> None:
        """
        Initialize the sync error.

        Args:
            message: Human-readable error message
            repository_url: URL of the repository that failed to sync
            details: Additional error details from Git operation
        """
        super().__init__(
            f"Sync failed: {message}",
            repository_url,
            details
        )


class RepositoryNotFoundError(RepositoryError):
    """
    Exception raised when a repository cannot be found or accessed.

    This exception is raised when the repository URL is invalid,
    the repository doesn't exist, or access is denied.
    """

    def __init__(
        self,
        message: str,
        repository_url: Optional[str] = None,
        details: Optional[str] = None
    ) -> None:
        """
        Initialize the not found error.

        Args:
            message: Human-readable error message
            repository_url: URL of the repository that was not found
            details: Additional error details from network or Git operation
        """
        super().__init__(
            f"Repository not found: {message}",
            repository_url,
            details
        )