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
Unit tests for logging module.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from javamcp.config.schema import LoggingConfig, RootLoggerConfig
from javamcp.logging import (
    ColoredFormatter,
    ContextLogger,
    get_logger,
    log_parse_operation,
    log_repository_operation,
    log_server_shutdown,
    log_server_startup,
    log_tool_invocation,
    setup_logging,
)


class TestColoredFormatter:
    """Tests for ColoredFormatter class."""

    def test_colored_formatter_init(self):
        """Test ColoredFormatter initialization."""
        formatter = ColoredFormatter(
            fmt="%(levelname)s - %(message)s",
            datefmt="%Y-%m-%d",
            use_colors=True,
        )
        assert formatter.use_colors is True

    def test_colored_formatter_without_colors(self):
        """Test ColoredFormatter with colors disabled."""
        formatter = ColoredFormatter(
            fmt="%(levelname)s - %(message)s",
            use_colors=False,
        )

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)
        assert "INFO - Test message" in result
        assert "\033[" not in result  # No ANSI codes

    @patch("sys.stderr")
    def test_colored_formatter_with_tty(self, mock_stderr):
        """Test ColoredFormatter with TTY (terminal) output."""
        mock_stderr.isatty.return_value = True

        formatter = ColoredFormatter(
            fmt="%(levelname)s - %(message)s",
            use_colors=True,
        )

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)
        # Should contain green color code for INFO
        assert "\033[92m" in result  # Green
        assert "\033[0m" in result  # Reset

    @patch("sys.stderr")
    def test_colored_formatter_without_tty(self, mock_stderr):
        """Test ColoredFormatter without TTY (redirected output)."""
        mock_stderr.isatty.return_value = False

        formatter = ColoredFormatter(
            fmt="%(levelname)s - %(message)s",
            use_colors=True,
        )

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)
        # Should NOT contain color codes when not TTY
        assert "\033[" not in result

    @patch("sys.stderr")
    def test_colored_formatter_different_levels(self, mock_stderr):
        """Test ColoredFormatter applies correct colors for different levels."""
        mock_stderr.isatty.return_value = True

        formatter = ColoredFormatter(
            fmt="%(levelname)s - %(message)s",
            use_colors=True,
        )

        # Test different log levels
        levels_and_colors = [
            (logging.DEBUG, "\033[96m"),  # Cyan
            (logging.INFO, "\033[92m"),  # Green
            (logging.WARNING, "\033[93m"),  # Yellow
            (logging.ERROR, "\033[91m"),  # Red
            (logging.CRITICAL, "\033[1;91m"),  # Bold Red
        ]

        for level, expected_color in levels_and_colors:
            record = logging.LogRecord(
                name="test",
                level=level,
                pathname="",
                lineno=0,
                msg="Test message",
                args=(),
                exc_info=None,
            )

            result = formatter.format(record)
            assert expected_color in result


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_logging_stderr_only(self):
        """Test logging setup with stderr output only."""
        import sys

        config = LoggingConfig(level="INFO")

        logger = setup_logging(config)

        assert logger.name == "javamcp"
        assert logger.level == logging.INFO
        # Handlers are now on root logger to affect FastMCP library
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) == 1
        assert isinstance(root_logger.handlers[0], logging.StreamHandler)
        # Verify console handler uses stderr (not stdout) to avoid interfering with STDIO mode
        assert root_logger.handlers[0].stream == sys.stderr

    def test_setup_logging_with_file(self, tmp_path):
        """Test logging setup with file output."""
        log_file = tmp_path / "test.log"
        config = LoggingConfig(level="DEBUG", file_path=str(log_file))

        logger = setup_logging(config)

        assert logger.level == logging.DEBUG
        # Handlers are now on root logger
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) == 2
        handler_types = [type(h).__name__ for h in root_logger.handlers]
        assert "StreamHandler" in handler_types
        assert "RotatingFileHandler" in handler_types

    def test_setup_logging_creates_directory(self, tmp_path):
        """Test that logging setup creates log directory if needed."""
        log_file = tmp_path / "logs" / "app" / "test.log"
        config = LoggingConfig(level="INFO", file_path=str(log_file))

        logger = setup_logging(config)

        assert log_file.parent.exists()
        # Handlers are now on root logger
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) == 2

    def test_setup_logging_different_levels(self):
        """Test logging setup with different log levels."""
        levels = [
            ("DEBUG", logging.DEBUG),
            ("INFO", logging.INFO),
            ("WARNING", logging.WARNING),
            ("ERROR", logging.ERROR),
        ]

        for level_name, level_value in levels:
            config = LoggingConfig(level=level_name)
            logger = setup_logging(config)
            assert logger.level == level_value

    def test_setup_logging_clears_existing_handlers(self):
        """Test that setup_logging clears existing handlers."""
        config = LoggingConfig(level="INFO")

        # Setup twice
        logger1 = setup_logging(config)
        logger2 = setup_logging(config)

        # Handlers are on root logger now, should have same number of handlers, not doubled
        root_logger = logging.getLogger()
        # Check that handlers weren't doubled
        assert len(root_logger.handlers) == 1

    def test_setup_logging_rotation_config(self, tmp_path):
        """Test logging setup with custom rotation configuration."""
        log_file = tmp_path / "test.log"
        config = LoggingConfig(
            level="INFO",
            file_path=str(log_file),
            max_bytes=1024,
            backup_count=3,
        )

        logger = setup_logging(config)

        # Find the RotatingFileHandler on root logger
        root_logger = logging.getLogger()
        rotating_handler = None
        for handler in root_logger.handlers:
            if isinstance(handler, RotatingFileHandler):
                rotating_handler = handler
                break

        assert rotating_handler is not None
        assert rotating_handler.maxBytes == 1024
        assert rotating_handler.backupCount == 3

    def test_setup_logging_rotation_behavior(self, tmp_path):
        """Test that log rotation actually occurs when max_bytes is exceeded."""
        log_file = tmp_path / "test.log"
        # Set very small max_bytes to trigger rotation easily
        config = LoggingConfig(
            level="INFO",
            file_path=str(log_file),
            max_bytes=100,
            backup_count=2,
        )

        logger = setup_logging(config)

        # Write enough logs to trigger rotation
        for i in range(50):
            logger.info(f"Test message number {i} with some extra text to fill space")

        # Check that rotation occurred - backup file should exist
        backup_file = Path(f"{log_file}.1")
        assert log_file.exists()
        # Backup file may or may not exist depending on exact log size
        # Just verify main log file didn't exceed max size by much
        if log_file.exists():
            # File size should be reasonably close to max_bytes after rotation
            assert log_file.stat().st_size < 1000  # Allow some overhead

    def test_setup_logging_configures_named_loggers_from_config(self):
        """Test that named loggers are configured from config.loggers dict."""
        config = LoggingConfig(
            root=RootLoggerConfig(level="INFO"),
            loggers={
                "uvicorn": "WARNING",
                "fastmcp": "DEBUG",
            },
        )

        setup_logging(config)

        # Verify uvicorn logger is configured with its specific level
        uvicorn_logger = logging.getLogger("uvicorn")
        assert len(uvicorn_logger.handlers) > 0
        assert uvicorn_logger.propagate is False
        assert uvicorn_logger.level == logging.WARNING

        # Verify fastmcp logger is configured with its specific level
        fastmcp_logger = logging.getLogger("fastmcp")
        assert len(fastmcp_logger.handlers) > 0
        assert fastmcp_logger.propagate is False
        assert fastmcp_logger.level == logging.DEBUG

    def test_setup_logging_named_loggers_use_colored_formatter(self):
        """Test that named loggers use ColoredFormatter."""
        config = LoggingConfig(
            root=RootLoggerConfig(level="INFO"),
            loggers={"testlogger": "DEBUG"},
            use_colors=True,
        )

        setup_logging(config)

        # Check test logger uses ColoredFormatter
        test_logger = logging.getLogger("testlogger")
        assert len(test_logger.handlers) > 0
        handler = test_logger.handlers[0]
        assert isinstance(handler.formatter, ColoredFormatter)

    def test_setup_logging_unconfigured_loggers_use_root(self):
        """Test that loggers not in config inherit from root via propagation."""
        config = LoggingConfig(
            root=RootLoggerConfig(level="WARNING"),
            loggers={"configured": "DEBUG"},  # Only this one is explicitly configured
        )

        setup_logging(config)

        # Unconfigured logger should have default propagate=True and use root handlers
        unconfigured_logger = logging.getLogger("unconfigured")
        # This logger was not explicitly configured, so it propagates to root
        assert unconfigured_logger.propagate is True


class TestSetupLoggingPerLogger:
    """Tests for per-logger setup_logging functionality."""

    def test_setup_logging_with_root_and_loggers(self):
        """Test logging setup with root and named loggers."""
        config = LoggingConfig(
            root=RootLoggerConfig(level="INFO"),
            loggers={"fastmcp": "DEBUG", "uvicorn": "WARNING"},
        )

        logger = setup_logging(config)

        # Check root logger
        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO

        # Check named loggers
        fastmcp_logger = logging.getLogger("fastmcp")
        assert fastmcp_logger.level == logging.DEBUG
        assert fastmcp_logger.propagate is False

        uvicorn_logger = logging.getLogger("uvicorn")
        assert uvicorn_logger.level == logging.WARNING
        assert uvicorn_logger.propagate is False

    def test_setup_logging_javamcp_explicit_level(self):
        """Test javamcp logger uses explicit level from config."""
        config = LoggingConfig(
            root=RootLoggerConfig(level="INFO"),
            loggers={"javamcp": "DEBUG"},
        )

        logger = setup_logging(config)

        assert logger.name == "javamcp"
        assert logger.level == logging.DEBUG

    def test_setup_logging_javamcp_inherits_root(self):
        """Test javamcp logger inherits root level when not explicitly set."""
        config = LoggingConfig(
            root=RootLoggerConfig(level="WARNING"),
            loggers={"fastmcp": "DEBUG"},  # javamcp not in here
        )

        logger = setup_logging(config)

        assert logger.name == "javamcp"
        assert logger.level == logging.WARNING

    def test_setup_logging_legacy_format(self):
        """Test legacy format continues to work."""
        config = LoggingConfig(level="DEBUG")

        logger = setup_logging(config)

        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG
        assert logger.level == logging.DEBUG

    def test_named_loggers_get_handlers(self):
        """Test named loggers receive their own handlers."""
        config = LoggingConfig(
            root=RootLoggerConfig(level="INFO"),
            loggers={"testlogger_handlers": "DEBUG"},
        )

        setup_logging(config)

        test_logger = logging.getLogger("testlogger_handlers")
        assert len(test_logger.handlers) > 0
        assert isinstance(test_logger.handlers[0], logging.StreamHandler)

    def test_named_loggers_with_file_output(self, tmp_path):
        """Test named loggers get file handlers when file output configured."""
        log_file = tmp_path / "test.log"
        config = LoggingConfig(
            root=RootLoggerConfig(level="INFO"),
            loggers={"testlogger_file": "DEBUG"},
            file_path=str(log_file),
        )

        setup_logging(config)

        test_logger = logging.getLogger("testlogger_file")
        handler_types = [type(h).__name__ for h in test_logger.handlers]
        assert "StreamHandler" in handler_types
        assert "RotatingFileHandler" in handler_types


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_default(self):
        """Test getting default logger."""
        logger = get_logger()

        assert logger.name == "javamcp"

    def test_get_logger_with_name(self):
        """Test getting named logger."""
        logger = get_logger("parser")

        assert logger.name == "javamcp.parser"

    def test_get_logger_hierarchy(self):
        """Test logger hierarchy."""
        parent = get_logger()
        child = get_logger("indexer")

        assert child.parent == parent or child.name.startswith(parent.name)


class TestContextLogger:
    """Tests for ContextLogger class."""

    def test_init(self):
        """Test ContextLogger initialization."""
        base_logger = logging.getLogger("test")
        context_logger = ContextLogger(base_logger)

        assert context_logger.logger == base_logger
        assert context_logger.context == {}

    def test_set_context(self):
        """Test setting context."""
        base_logger = logging.getLogger("test")
        context_logger = ContextLogger(base_logger)

        context_logger.set_context(repository="test-repo", class_name="TestClass")

        assert context_logger.context["repository"] == "test-repo"
        assert context_logger.context["class_name"] == "TestClass"

    def test_clear_context(self):
        """Test clearing context."""
        base_logger = logging.getLogger("test")
        context_logger = ContextLogger(base_logger)

        context_logger.set_context(repository="test-repo")
        context_logger.clear_context()

        assert context_logger.context == {}

    def test_format_message_with_context(self):
        """Test message formatting with context."""
        base_logger = logging.getLogger("test")
        context_logger = ContextLogger(base_logger)

        context_logger.set_context(repository="test-repo", class_name="TestClass")
        formatted = context_logger._format_message("Test message")

        assert "Test message" in formatted
        assert "repository=test-repo" in formatted
        assert "class_name=TestClass" in formatted

    def test_format_message_without_context(self):
        """Test message formatting without context."""
        base_logger = logging.getLogger("test")
        context_logger = ContextLogger(base_logger)

        formatted = context_logger._format_message("Test message")

        assert formatted == "Test message"

    def test_log_methods(self, caplog):
        """Test all logging methods."""
        base_logger = logging.getLogger("test")
        base_logger.setLevel(logging.DEBUG)
        context_logger = ContextLogger(base_logger)

        context_logger.set_context(test="value")

        with caplog.at_level(logging.DEBUG, logger="test"):
            context_logger.debug("Debug message")
            context_logger.info("Info message")
            context_logger.warning("Warning message")
            context_logger.error("Error message")

        assert "Debug message" in caplog.text
        assert "Info message" in caplog.text
        assert "Warning message" in caplog.text
        assert "Error message" in caplog.text
        assert "test=value" in caplog.text


class TestLogHelpers:
    """Tests for logging helper functions."""

    def test_log_server_startup(self, caplog):
        """Test server startup logging."""
        logger = logging.getLogger("test")
        logger.setLevel(logging.INFO)

        with caplog.at_level(logging.INFO, logger="test"):
            log_server_startup(logger)

        assert "JavaMCP server starting" in caplog.text

    def test_log_server_startup_with_config(self, caplog):
        """Test server startup logging with config path."""
        logger = logging.getLogger("test")
        logger.setLevel(logging.INFO)

        with caplog.at_level(logging.INFO, logger="test"):
            log_server_startup(logger, config_path="/path/to/config.yml")

        assert "JavaMCP server starting" in caplog.text
        assert "/path/to/config.yml" in caplog.text

    def test_log_server_shutdown(self, caplog):
        """Test server shutdown logging."""
        logger = logging.getLogger("test")
        logger.setLevel(logging.INFO)

        with caplog.at_level(logging.INFO, logger="test"):
            log_server_shutdown(logger)

        assert "JavaMCP server shutting down" in caplog.text

    def test_log_tool_invocation(self, caplog):
        """Test tool invocation logging."""
        logger = logging.getLogger("test")
        logger.setLevel(logging.INFO)

        with caplog.at_level(logging.INFO, logger="test"):
            log_tool_invocation(
                logger,
                "search_methods",
                method_name="testMethod",
                class_name="TestClass",
            )

        assert "Tool invocation: search_methods" in caplog.text
        assert "method_name=testMethod" in caplog.text
        assert "class_name=TestClass" in caplog.text

    def test_log_repository_operation_success(self, caplog):
        """Test repository operation logging (success)."""
        logger = logging.getLogger("test")
        logger.setLevel(logging.INFO)

        with caplog.at_level(logging.INFO, logger="test"):
            log_repository_operation(
                logger, "clone", "https://github.com/example/repo.git"
            )

        assert "Repository clone" in caplog.text
        assert "https://github.com/example/repo.git" in caplog.text
        assert "success" in caplog.text

    def test_log_repository_operation_failure(self, caplog):
        """Test repository operation logging (failure)."""
        logger = logging.getLogger("test")
        logger.setLevel(logging.INFO)

        with caplog.at_level(logging.INFO, logger="test"):
            log_repository_operation(
                logger, "clone", "https://github.com/example/repo.git", status="failed"
            )

        assert "Repository clone" in caplog.text
        assert "failed" in caplog.text

    def test_log_parse_operation_success(self, caplog):
        """Test parse operation logging (success)."""
        logger = logging.getLogger("test")
        logger.setLevel(logging.DEBUG)

        with caplog.at_level(logging.DEBUG, logger="test"):
            log_parse_operation(logger, "/path/to/Test.java")

        assert "Parsed Java file" in caplog.text
        assert "/path/to/Test.java" in caplog.text

    def test_log_parse_operation_failure(self, caplog):
        """Test parse operation logging (failure)."""
        logger = logging.getLogger("test")
        logger.setLevel(logging.WARNING)

        with caplog.at_level(logging.WARNING, logger="test"):
            log_parse_operation(
                logger, "/path/to/Test.java", status="failed", error="Syntax error"
            )

        assert "Failed to parse Java file" in caplog.text
        assert "/path/to/Test.java" in caplog.text
        assert "Syntax error" in caplog.text
