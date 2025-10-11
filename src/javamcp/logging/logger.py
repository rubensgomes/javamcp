# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Rubens Gomes
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

    Args:
        config: LoggingConfig with level and file settings

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("javamcp")
    logger.setLevel(config.level.upper())

    # Remove existing handlers
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler (use stderr to avoid interfering with stdout in STDIO mode)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(config.level.upper())
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating file handler if file path specified
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
        logger.addHandler(file_handler)

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
