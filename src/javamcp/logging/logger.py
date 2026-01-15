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


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds ANSI color codes to log levels.

    Colors are only applied when output is to a terminal (TTY).
    File output always uses plain text without color codes.
    """

    # ANSI color codes for each log level
    COLORS = {
        "DEBUG": "\033[96m",  # Bright Cyan
        "INFO": "\033[92m",  # Bright Green
        "WARNING": "\033[93m",  # Bright Yellow
        "ERROR": "\033[91m",  # Bright Red
        "CRITICAL": "\033[1;91m",  # Bold Bright Red
    }
    RESET = "\033[0m"

    def __init__(
        self, fmt: str, datefmt: Optional[str] = None, use_colors: bool = True
    ):
        """
        Initialize colored formatter.

        Args:
            fmt: Log message format
            datefmt: Date/time format
            use_colors: Enable color output (also checks if output is TTY)
        """
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record with colored level name.

        Args:
            record: Log record to format

        Returns:
            Formatted log message with optional colors
        """
        # Only apply colors if enabled and output is a TTY
        if self.use_colors and hasattr(sys.stderr, "isatty") and sys.stderr.isatty():
            # Save original levelname
            original_levelname = record.levelname

            # Apply color to levelname
            color = self.COLORS.get(record.levelname, "")
            if color:
                record.levelname = f"{color}{record.levelname}{self.RESET}"

            # Format the message
            result = super().format(record)

            # Restore original levelname
            record.levelname = original_levelname

            return result

        # No colors - just format normally
        return super().format(record)


def _configure_named_loggers(
    config: LoggingConfig,
    console_formatter: ColoredFormatter,
    file_formatter: logging.Formatter,
) -> None:
    """
    Configure named loggers based on config.loggers dict.

    Each named logger gets its own handlers and does not propagate to root,
    preventing duplicate log messages while allowing per-logger level control.

    Args:
        config: Logging configuration with loggers dict
        console_formatter: Formatter for console output
        file_formatter: Formatter for file output
    """
    for logger_name, level in config.loggers.items():
        named_logger = logging.getLogger(logger_name)
        named_logger.handlers.clear()
        named_logger.setLevel(level)
        named_logger.propagate = False  # Prevent duplicates

        # Add console handler
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(level)
        handler.setFormatter(console_formatter)
        named_logger.addHandler(handler)

        # Add file handler if configured
        if config.file_path:
            file_handler = RotatingFileHandler(
                config.file_path,
                maxBytes=config.max_bytes,
                backupCount=config.backup_count,
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(file_formatter)
            named_logger.addHandler(file_handler)


def setup_logging(config: LoggingConfig) -> logging.Logger:
    """
    Configure logging based on application configuration.

    Supports both legacy single-level configuration and new per-logger
    configuration with root and loggers sections.

    This function configures:
    1. Root logger with the effective root level
    2. Named loggers specified in config.loggers with their individual levels
    3. The javamcp application logger

    Args:
        config: LoggingConfig with level settings and format options

    Returns:
        Configured logger instance for javamcp
    """
    # Create colored formatter for console output
    console_formatter = ColoredFormatter(
        fmt=config.format,
        datefmt=config.date_format,
        use_colors=config.use_colors,
    )

    # Create plain formatter for file output (no colors)
    file_formatter = logging.Formatter(
        fmt=config.format,
        datefmt=config.date_format,
    )

    # Get effective root level (from root.level, legacy level, or default INFO)
    root_level = config.get_effective_root_level()

    # Configure root logger to affect all libraries including FastMCP
    root_logger = logging.getLogger()
    root_logger.setLevel(root_level)
    root_logger.handlers.clear()

    # Console handler for root logger (use stderr to avoid interfering with stdout)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(root_level)
    console_handler.setFormatter(console_formatter)
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
        file_handler.setLevel(root_level)
        file_handler.setFormatter(file_formatter)  # Use plain formatter for files
        root_logger.addHandler(file_handler)

    # Configure named loggers from config.loggers
    _configure_named_loggers(config, console_formatter, file_formatter)

    # Get application-specific logger
    logger = logging.getLogger("javamcp")

    # If javamcp is explicitly configured, it already has handlers from above
    # Otherwise, set level to root level (handlers come from root via propagation)
    if "javamcp" not in config.loggers:
        logger.setLevel(root_level)

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
