"""
Pydantic models for Java path indexing operations.

This module defines the data models used for indexer configuration,
file path tracking, and operation results.
"""

from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class JavaFilePath(BaseModel):
    """
    Model representing a Java source file path.

    Attributes:
        absolute_path: Absolute path to the Java source file
        relative_path: Path relative to repository root
        repository_dir: Repository directory containing this file
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True
    )

    absolute_path: Path = Field(
        ...,
        description="Absolute path to the Java source file"
    )
    relative_path: Path = Field(
        ...,
        description="Path relative to repository root"
    )
    repository_dir: Path = Field(
        ...,
        description="Repository directory containing this file"
    )

    @field_validator('absolute_path', 'repository_dir')
    @classmethod
    def validate_path_exists(cls, v: Path) -> Path:
        """Validate that path exists."""
        if not v.exists():
            raise ValueError(f"Path does not exist: {v}")
        return v

    @field_validator('absolute_path')
    @classmethod
    def validate_java_file(cls, v: Path) -> Path:
        """Validate that file has .java extension."""
        if v.suffix != '.java':
            raise ValueError(
                f"File must have .java extension: {v}"
            )
        return v


class IndexerConfig(BaseModel):
    """
    Model representing indexer configuration.

    Attributes:
        repository_dirs: List of repository directory paths to index
        java_source_pattern: Pattern to identify Java source directories
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True
    )

    repository_dirs: List[Path] = Field(
        ...,
        description="List of repository directory paths to index",
        min_length=1
    )
    java_source_pattern: str = Field(
        default="src/main/java",
        description="Pattern to identify Java source directories"
    )

    @field_validator('repository_dirs')
    @classmethod
    def validate_directories(cls, v: List[Path]) -> List[Path]:
        """Validate that all paths are directories."""
        for path in v:
            if not path.exists():
                raise ValueError(
                    f"Repository directory does not exist: {path}"
                )
            if not path.is_dir():
                raise ValueError(
                    f"Path is not a directory: {path}"
                )
        return v


class IndexResult(BaseModel):
    """
    Model representing the result of an indexing operation.

    Attributes:
        repository_dir: Repository directory that was indexed
        java_files: List of Java file paths found
        success: Whether the indexing operation was successful
        message: Human-readable message describing the result
        error_details: Additional error information if operation failed
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        arbitrary_types_allowed=True
    )

    repository_dir: Path = Field(
        ...,
        description="Repository directory that was indexed"
    )
    java_files: List[JavaFilePath] = Field(
        default_factory=list,
        description="List of Java file paths found"
    )
    success: bool = Field(
        ...,
        description="Whether the indexing operation was successful"
    )
    message: str = Field(
        ...,
        description="Human-readable result message"
    )
    error_details: Optional[str] = Field(
        default=None,
        description="Additional error information if operation failed"
    )
