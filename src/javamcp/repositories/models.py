"""
Pydantic models for repository operations.

This module defines the data models used for repository configuration,
status tracking, and operation results.
"""

from enum import Enum
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field, ConfigDict


class RepositoryStatus(str, Enum):
    """Enumeration of repository operation statuses."""

    PENDING = "pending"
    CLONING = "cloning"
    SYNCING = "syncing"
    SUCCESS = "success"
    FAILED = "failed"


class Repository(BaseModel):
    """
    Model representing a Git repository configuration.

    Attributes:
        url: The HTTP/HTTPS URL of the Git repository
        local_path: Local filesystem path where repository will be stored
        status: Current status of the repository operation
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    url: HttpUrl = Field(
        ...,
        description="HTTP/HTTPS URL of the Git repository"
    )
    local_path: Path = Field(
        ...,
        description="Local filesystem path for the repository"
    )
    status: RepositoryStatus = Field(
        default=RepositoryStatus.PENDING,
        description="Current status of repository operation"
    )


class RepositoryResult(BaseModel):
    """
    Model representing the result of a repository operation.

    Attributes:
        repository: The repository that was processed
        success: Whether the operation was successful
        message: Human-readable message describing the result
        error_details: Additional error information if operation failed
    """

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    repository: Repository = Field(
        ...,
        description="Repository that was processed"
    )
    success: bool = Field(
        ...,
        description="Whether the operation was successful"
    )
    message: str = Field(
        ...,
        description="Human-readable result message"
    )
    error_details: Optional[str] = Field(
        default=None,
        description="Additional error information if operation failed"
    )