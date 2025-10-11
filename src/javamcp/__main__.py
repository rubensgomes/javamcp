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
Entry point for running JavaMCP server using FastMCP.
"""

import argparse
import signal
import sys

from javamcp import __version__
from javamcp.config.loader import load_config
from javamcp.logging import (get_logger, log_server_shutdown,
                             log_server_startup, setup_logging)
from javamcp.server import get_state, initialize_server, mcp


def setup_signal_handlers(logger) -> None:
    """
    Setup signal handlers for graceful shutdown.

    Args:
        logger: Logger instance for logging shutdown events
    """

    def signal_handler(signum: int, frame) -> None:
        """
        Handle shutdown signals gracefully.

        Args:
            signum: Signal number
            frame: Current stack frame
        """
        signal_name = signal.Signals(signum).name
        logger.info(
            "Received signal %s (%d), initiating graceful shutdown...",
            signal_name,
            signum,
        )

        # Clear server state
        state = get_state()
        if state.indexer:
            logger.info("Clearing API indexer...")
            state.indexer.clear()

        state.initialized = False
        logger.info("Server state cleared")

        # Log shutdown and exit
        log_server_shutdown(logger)
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal

    logger.info("Signal handlers registered for graceful shutdown")


def main() -> int:
    """
    Main entry point for JavaMCP server.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="JavaMCP Server - MCP server for Java API documentation"
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"JavaMCP {__version__}",
    )
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default=None,
        help="Path to configuration file (YAML or JSON)",
    )

    args = parser.parse_args()

    try:
        # Load configuration
        config = load_config(args.config)

        # Setup logging
        logger = setup_logging(config.logging)
        log_server_startup(logger, args.config)

        # Setup signal handlers for graceful shutdown
        setup_signal_handlers(logger)

        # Initialize server state
        logger.info("Initializing JavaMCP server...")
        initialize_server(args.config)
        logger.info("Server initialized successfully")
        logger.info("Starting FastMCP server...")

        # Start FastMCP server - this handles stdio/http modes automatically
        if config.mode == "stdio":
            logger.info("Running FastMCP in stdio mode.")
            mcp.run(log_level=config.logging.level.upper())
        else:
            logger.info("Running FastMCP in normal HTTP mode.")
            mcp.run(
                transport="http",
                port=config.server.port,
                log_level=config.logging.level.upper(),
            )

        # Shutdown logging (only reached if server stops normally)
        log_server_shutdown(logger)
        return 0

    except KeyboardInterrupt:
        # This might not be reached due to signal handlers, but keep as fallback
        logger = get_logger()
        logger.info("Received keyboard interrupt")
        log_server_shutdown(logger)
        return 0

    except Exception as e:  # pylint: disable=broad-exception-caught
        logger = get_logger()
        logger.error("Server error: %s", e, exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
