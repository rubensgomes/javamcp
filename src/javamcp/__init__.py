"""
javamcp - Java MCP Server for AI Coding Assistants.

This package provides an MCP (Model Context Protocol) server that exposes
Java API information to AI coding assistants by parsing Java source code
from Git repositories.
"""

from .repositories import (
    GitRepositoryManager,
    Repository,
    RepositoryStatus,
    RepositoryResult,
    RepositoryError,
    RepositoryCloneError,
    RepositorySyncError,
    RepositoryNotFoundError
)

__version__ = "0.0.1"

__all__ = [
    "GitRepositoryManager",
    "Repository",
    "RepositoryStatus",
    "RepositoryResult",
    "RepositoryError",
    "RepositoryCloneError",
    "RepositorySyncError",
    "RepositoryNotFoundError",
]