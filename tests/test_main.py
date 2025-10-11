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
