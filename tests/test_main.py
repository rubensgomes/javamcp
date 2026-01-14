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
Unit tests for __main__ module.
"""

import re
import signal
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

from javamcp import __version__
from javamcp.__main__ import (
    display_config_error_and_exit,
    get_config_template,
    get_default_config_path,
    resolve_config_path,
    setup_signal_handlers,
)


class TestSignalHandlers:
    """Tests for signal handler setup."""

    @patch("javamcp.__main__.signal.signal")
    def test_setup_signal_handlers_registers_sigint(self, mock_signal):
        """Test that SIGINT signal handler is registered."""
        logger = MagicMock()

        setup_signal_handlers(logger)

        # Verify SIGINT handler was registered
        calls = mock_signal.call_args_list
        signal_numbers = [call[0][0] for call in calls]

        assert signal.SIGINT in signal_numbers
        logger.info.assert_called()

    @patch("javamcp.__main__.signal.signal")
    def test_setup_signal_handlers_registers_sigterm(self, mock_signal):
        """Test that SIGTERM signal handler is registered."""
        logger = MagicMock()

        setup_signal_handlers(logger)

        # Verify SIGTERM handler was registered
        calls = mock_signal.call_args_list
        signal_numbers = [call[0][0] for call in calls]

        assert signal.SIGTERM in signal_numbers
        logger.info.assert_called()

    @patch("javamcp.__main__.signal.signal")
    def test_setup_signal_handlers_logs_registration(self, mock_signal):
        """Test that signal handler registration is logged."""
        logger = MagicMock()

        setup_signal_handlers(logger)

        # Verify logging occurred
        assert logger.info.called
        log_calls = [str(call) for call in logger.info.call_args_list]
        assert any("Signal handlers registered" in str(call) for call in log_calls)

    @patch("javamcp.__main__.get_state")
    @patch("javamcp.__main__.log_server_shutdown")
    @patch("javamcp.__main__.sys.exit")
    def test_signal_handler_clears_indexer(
        self, mock_exit, mock_shutdown, mock_get_state
    ):
        """Test that signal handler clears the indexer."""
        logger = MagicMock()

        # Create mock state with indexer
        mock_state = MagicMock()
        mock_indexer = MagicMock()
        mock_state.indexer = mock_indexer
        mock_state.initialized = True
        mock_get_state.return_value = mock_state

        # Setup signal handlers
        setup_signal_handlers(logger)

        # Get the registered signal handler for SIGINT
        with patch("javamcp.__main__.signal.signal") as mock_signal:
            setup_signal_handlers(logger)
            # Get the handler function from the first call (SIGINT)
            handler = mock_signal.call_args_list[0][0][1]

            # Call the handler
            handler(signal.SIGINT, None)

            # Verify indexer was cleared
            mock_indexer.clear.assert_called_once()
            assert mock_state.initialized is False
            mock_shutdown.assert_called_once()
            mock_exit.assert_called_once_with(0)

    @patch("javamcp.__main__.get_state")
    @patch("javamcp.__main__.log_server_shutdown")
    @patch("javamcp.__main__.sys.exit")
    def test_signal_handler_handles_no_indexer(
        self, mock_exit, mock_shutdown, mock_get_state
    ):
        """Test that signal handler handles missing indexer gracefully."""
        logger = MagicMock()

        # Create mock state without indexer
        mock_state = MagicMock()
        mock_state.indexer = None
        mock_state.initialized = True
        mock_get_state.return_value = mock_state

        # Setup and trigger signal handler
        with patch("javamcp.__main__.signal.signal") as mock_signal:
            setup_signal_handlers(logger)
            handler = mock_signal.call_args_list[0][0][1]

            # Should not raise exception even without indexer
            handler(signal.SIGINT, None)

            assert mock_state.initialized is False
            mock_shutdown.assert_called_once()
            mock_exit.assert_called_once_with(0)


class TestConfigPathResolution:
    """Tests for configuration path resolution functions."""

    def test_get_default_config_path(self):
        """Test that default config path is constructed correctly."""
        expected_path = Path.home() / ".config" / "javamcp" / "config.yml"
        assert get_default_config_path() == expected_path

    @patch("javamcp.__main__.files")
    def test_get_config_template_success(self, mock_files):
        """Test successful reading of config template."""
        mock_template = MagicMock()
        mock_template.read_text.return_value = "sample: config\n"
        mock_files.return_value.joinpath.return_value = mock_template

        result = get_config_template()

        assert result == "sample: config\n"
        mock_files.assert_called_once_with("javamcp")
        mock_files.return_value.joinpath.assert_called_once_with("config_template.yml")

    @patch("javamcp.__main__.files")
    def test_get_config_template_failure(self, mock_files):
        """Test that RuntimeError is raised when template cannot be read."""
        mock_files.return_value.joinpath.side_effect = Exception("File not found")

        with pytest.raises(RuntimeError, match="Failed to read configuration template"):
            get_config_template()

    def test_resolve_config_path_with_explicit_path(self):
        """Test that explicit config path is returned unchanged."""
        config_path = "/custom/path/config.yml"
        result = resolve_config_path(config_path)
        assert result == config_path

    @patch("javamcp.__main__.get_default_config_path")
    def test_resolve_config_path_with_existing_default(self, mock_get_default):
        """Test that default config path is used when it exists."""
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        mock_path.__str__.return_value = "/home/user/.config/javamcp/config.yml"
        mock_get_default.return_value = mock_path

        result = resolve_config_path(None)

        assert result == "/home/user/.config/javamcp/config.yml"
        mock_path.exists.assert_called_once()

    @patch("javamcp.__main__.display_config_error_and_exit")
    @patch("javamcp.__main__.get_default_config_path")
    def test_resolve_config_path_without_default(
        self, mock_get_default, mock_display_error
    ):
        """Test that error is displayed when default config doesn't exist."""
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = False
        mock_get_default.return_value = mock_path

        # Mock the exit to prevent actual exit
        mock_display_error.side_effect = SystemExit(1)

        with pytest.raises(SystemExit):
            resolve_config_path(None)

        mock_display_error.assert_called_once()

    @patch("javamcp.__main__.sys.exit")
    @patch("javamcp.__main__.get_config_template")
    @patch("javamcp.__main__.get_default_config_path")
    def test_display_config_error_and_exit(
        self, mock_get_default, mock_get_template, mock_exit
    ):
        """Test that error message is displayed correctly."""
        mock_path = MagicMock(spec=Path)
        mock_path.__str__.return_value = "/home/user/.config/javamcp/config.yml"
        mock_get_default.return_value = mock_path
        mock_get_template.return_value = "sample: config\n"

        with patch("sys.stderr") as mock_stderr:
            display_config_error_and_exit()

            # Verify error message was printed
            printed_output = "".join(
                str(call[0][0]) for call in mock_stderr.write.call_args_list
            )
            assert "Error: No configuration file found" in printed_output
            assert "/home/user/.config/javamcp/config.yml" in printed_output
            assert "sample: config" in printed_output

            # Verify exit was called with code 1
            mock_exit.assert_called_once_with(1)

    @patch("javamcp.__main__.sys.exit")
    @patch("javamcp.__main__.get_config_template")
    @patch("javamcp.__main__.get_default_config_path")
    def test_display_config_error_when_template_fails(
        self, mock_get_default, mock_get_template, mock_exit
    ):
        """Test error handling when template cannot be read."""
        mock_path = MagicMock(spec=Path)
        mock_get_default.return_value = mock_path
        mock_get_template.side_effect = RuntimeError("Template error")

        with patch("sys.stderr"):
            display_config_error_and_exit()

            # Verify exit was called with code 1
            mock_exit.assert_called_once_with(1)


class TestVersion:
    """Tests for version information."""

    def test_version_is_accessible(self):
        """Test that __version__ is accessible and non-empty."""
        assert __version__ is not None
        assert __version__ != ""
        assert isinstance(__version__, str)

    def test_version_format(self):
        """Test that version follows semantic versioning format or is 'unknown'."""
        # Version should be either semantic version (X.Y.Z) or 'unknown'
        if __version__ != "unknown":
            # Semantic versioning pattern: major.minor.patch
            pattern = r"^\d+\.\d+\.\d+$"
            assert re.match(
                pattern, __version__
            ), f"Version '{__version__}' does not match semantic versioning format"
