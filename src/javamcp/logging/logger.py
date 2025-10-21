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
Logging configuration and utilities for JavaMCP server.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from javamcp.config.schema import LoggingConfig


def setup_logging(config: LoggingConfig) -> logging.Logger:
    """
    Configure logging based on application configuration.

    This function configures both the application logger and the root logger
    to ensure third-party libraries (like FastMCP) use the same logging settings.

    Args:
        config: LoggingConfig with level and file settings

    Returns:
        Configured logger instance
    """
    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Configure root logger to affect all libraries including FastMCP
    root_logger = logging.getLogger()
    root_logger.setLevel(config.level.upper())
    root_logger.handlers.clear()

    # Console handler for root logger (use stderr to avoid interfering with stdout)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(config.level.upper())
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Rotating file handler for root logger if file path specified
    if config.file_path:
        file_path = Path(config.file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=config.max_bytes,
            backupCount=config.backup_count,
        )
        file_handler.setLevel(config.level.upper())
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Get application-specific logger
    logger = logging.getLogger("javamcp")
    logger.setLevel(config.level.upper())

    # Don't add handlers to application logger since root logger handles it
    # This prevents duplicate log messages

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (defaults to "javamcp")

    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"javamcp.{name}")
    return logging.getLogger("javamcp")


class ContextLogger:
    """
    Logger with contextual information for structured logging.
    """

    def __init__(self, logger: logging.Logger):
        """
        Initialize context logger.

        Args:
            logger: Base logger instance
        """
        self.logger = logger
        self.context = {}

    def set_context(self, **kwargs) -> None:
        """
        Set context information for logging.

        Args:
            **kwargs: Context key-value pairs
        """
        self.context.update(kwargs)

    def clear_context(self) -> None:
        """Clear all context information."""
        self.context.clear()

    def _format_message(self, message: str) -> str:
        """
        Format message with context.

        Args:
            message: Log message

        Returns:
            Formatted message with context
        """
        if not self.context:
            return message

        context_str = " | ".join(f"{k}={v}" for k, v in self.context.items())
        return f"{message} [{context_str}]"

    def debug(self, message: str) -> None:
        """Log debug message with context."""
        self.logger.debug(self._format_message(message))

    def info(self, message: str) -> None:
        """Log info message with context."""
        self.logger.info(self._format_message(message))

    def warning(self, message: str) -> None:
        """Log warning message with context."""
        self.logger.warning(self._format_message(message))

    def error(self, message: str, exc_info: bool = False) -> None:
        """
        Log error message with context.

        Args:
            message: Error message
            exc_info: Include exception info
        """
        self.logger.error(self._format_message(message), exc_info=exc_info)


def log_server_startup(
    logger: logging.Logger, config_path: Optional[str] = None
) -> None:
    """
    Log server startup event.

    Args:
        logger: Logger instance
        config_path: Configuration file path
    """
    logger.info("JavaMCP server starting")
    if config_path:
        logger.info(f"Loading configuration from: {config_path}")


def log_server_shutdown(logger: logging.Logger) -> None:
    """
    Log server shutdown event.

    Args:
        logger: Logger instance
    """
    logger.info("JavaMCP server shutting down")


def log_tool_invocation(logger: logging.Logger, tool_name: str, **params) -> None:
    """
    Log MCP tool invocation.

    Args:
        logger: Logger instance
        tool_name: Name of the tool being invoked
        **params: Tool parameters
    """
    param_str = ", ".join(f"{k}={v}" for k, v in params.items())
    logger.info(f"Tool invocation: {tool_name}({param_str})")


def log_repository_operation(
    logger: logging.Logger, operation: str, repository_url: str, status: str = "success"
) -> None:
    """
    Log repository operation.

    Args:
        logger: Logger instance
        operation: Operation name (clone, update, etc.)
        repository_url: Repository URL
        status: Operation status
    """
    logger.info(f"Repository {operation}: {repository_url} - {status}")


def log_parse_operation(
    logger: logging.Logger,
    file_path: str,
    status: str = "success",
    error: Optional[str] = None,
) -> None:
    """
    Log parsing operation.

    Args:
        logger: Logger instance
        file_path: Path to file being parsed
        status: Parse status
        error: Error message if failed
    """
    if status == "success":
        logger.debug(f"Parsed Java file: {file_path}")
    else:
        logger.warning(f"Failed to parse Java file: {file_path} - {error}")
