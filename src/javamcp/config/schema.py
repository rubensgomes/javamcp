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
Configuration schema using Pydantic models.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ServerMode(str, Enum):
    """Server operation mode."""

    STDIO = "stdio"
    HTTP = "http"


class ServerConfig(BaseModel):
    """
    MCP server configuration.

    Attributes:
        mode: Server operation mode (stdio or http)
        port: Server port for HTTP mode (ignored in stdio mode)
        host: Server host for HTTP mode (default: "localhost")
    """

    mode: ServerMode = Field(
        default=ServerMode.STDIO, description="Server operation mode"
    )
    port: int = Field(default=8000, description="Server port for HTTP mode")
    host: str = Field(default="localhost", description="Server host for HTTP mode")

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Validate port is in valid range."""
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v


class RepositoryConfig(BaseModel):
    """
    Git repository configuration.

    Attributes:
        urls: List of Git repository URLs to clone and parse
        local_base_path: Base directory path where repositories will be cloned
        auto_update: Whether to automatically pull latest changes on startup
    """

    urls: list[str] = Field(
        default_factory=list, description="List of Git repository URLs"
    )
    local_base_path: str = Field(
        default="./repositories", description="Base path for cloned repositories"
    )
    auto_update: bool = Field(
        default=True, description="Auto-update repositories on startup"
    )

    @field_validator("urls")
    @classmethod
    def validate_urls(cls, v: list[str]) -> list[str]:
        """Validate repository URLs are not empty."""
        if not v:
            raise ValueError("At least one repository URL must be specified")
        for url in v:
            if not url.strip():
                raise ValueError("Repository URLs cannot be empty")
        return v

    @field_validator("local_base_path")
    @classmethod
    def validate_local_base_path(cls, v: str) -> str:
        """Ensure local base path is valid."""
        if not v or not v.strip():
            raise ValueError("Local base path cannot be empty")
        return v


class LoggingConfig(BaseModel):
    """
    Logging configuration.

    Attributes:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format: Log message format (supports Python logging format variables)
        date_format: Date/time format for log messages (strftime format)
        use_colors: Enable ANSI color codes for log levels in console output
        output: Log output destination ("stderr", "file", or "both")
        file_path: Log file path (required if output is "file" or "both")
        max_bytes: Maximum size in bytes before rotating log file (default: 10MB)
        backup_count: Number of backup log files to keep (default: 5)
    """

    level: str = Field(default="INFO", description="Log level")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format (Python logging format)",
    )
    date_format: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="Date/time format (strftime format)",
    )
    use_colors: bool = Field(
        default=True,
        description="Enable colored log levels in console output",
    )
    output: str = Field(default="stderr", description="Log output destination")
    file_path: Optional[str] = Field(None, description="Log file path")
    max_bytes: int = Field(
        default=10485760, description="Maximum log file size before rotation (bytes)"
    )
    backup_count: int = Field(
        default=5, description="Number of backup log files to keep"
    )

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v_upper

    @field_validator("output")
    @classmethod
    def validate_output(cls, v: str) -> str:
        """Validate log output destination."""
        valid_outputs = {"stderr", "file", "both"}
        v_lower = v.lower()
        if v_lower not in valid_outputs:
            raise ValueError(f"Log output must be one of {valid_outputs}")
        return v_lower

    @field_validator("max_bytes")
    @classmethod
    def validate_max_bytes(cls, v: int) -> int:
        """Validate max_bytes is positive."""
        if v <= 0:
            raise ValueError("max_bytes must be positive")
        return v

    @field_validator("backup_count")
    @classmethod
    def validate_backup_count(cls, v: int) -> int:
        """Validate backup_count is non-negative."""
        if v < 0:
            raise ValueError("backup_count must be non-negative")
        return v


class ApplicationConfig(BaseModel):
    """
    Root application configuration aggregating all sub-configurations.

    Attributes:
        server: Server configuration
        repositories: Repository configuration
        logging: Logging configuration
    """

    server: ServerConfig = Field(
        default_factory=ServerConfig, description="Server configuration"
    )
    repositories: RepositoryConfig = Field(
        default_factory=RepositoryConfig, description="Repository configuration"
    )
    logging: LoggingConfig = Field(
        default_factory=LoggingConfig, description="Logging configuration"
    )

    def validate_logging_file_path(self) -> None:
        """Validate that file_path is set when output is 'file' or 'both'."""
        if self.logging.output in ("file", "both") and not self.logging.file_path:
            raise ValueError(
                "Logging file_path must be specified when output is 'file' or 'both'"
            )
