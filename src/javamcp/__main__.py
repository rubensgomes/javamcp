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
Entry point for running JavaMCP server using FastMCP.
"""

import argparse
import signal
import sys

from javamcp import __version__
from javamcp.config.loader import load_config
from javamcp.logging import (get_logger, log_server_shutdown,
                             log_server_startup, setup_logging)
from javamcp.server import (get_state, initialize_server,
                            register_tools_and_resources)
from javamcp.server_factory import get_mcp_server


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

        # Setup logging BEFORE creating FastMCP server instance
        # This ensures FastMCP library uses the same logging configuration
        logger = setup_logging(config.logging)
        log_server_startup(logger, args.config)

        # Register all MCP tools and resources (creates FastMCP instance)
        logger.info("Registering MCP tools and resources...")
        register_tools_and_resources()
        logger.info("MCP tools and resources registered successfully")

        # Setup signal handlers for graceful shutdown
        setup_signal_handlers(logger)

        # Initialize server state
        logger.info("Initializing JavaMCP server...")
        initialize_server(args.config)
        logger.info("Server initialized successfully")
        logger.info("Starting FastMCP server...")

        # Get MCP server instance and start it
        mcp = get_mcp_server()

        # Start FastMCP server - this handles stdio/http modes automatically
        if config.server.mode == "stdio":
            logger.info("Running FastMCP in stdio mode.")
            mcp.run(log_level=config.logging.level.upper())
        else:
            logger.info("Running FastMCP in normal HTTP mode.")
            mcp.run(
                transport="http",
                host=config.server.host,
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
