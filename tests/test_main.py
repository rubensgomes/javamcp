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

import signal
from unittest.mock import MagicMock, patch

import pytest

from javamcp.__main__ import setup_signal_handlers


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
