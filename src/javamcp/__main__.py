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
from pathlib import Path

from javamcp import __version__
from javamcp.config.loader import load_config
from javamcp.logging import (
    get_logger,
    log_server_shutdown,
    log_server_startup,
    setup_logging,
)
from javamcp.server import get_state, initialize_server, register_tools_and_resources
from javamcp.server_factory import get_mcp_server

try:
    from importlib.resources import files
except ImportError:
    # Fallback for older Python versions (though we require 3.13+)
    from importlib_resources import files  # type: ignore


def get_help_epilog() -> str:
    """
    Generate detailed epilog text for CLI help.

    Returns:
        Formatted string with configuration file documentation
    """
    default_path = get_default_config_path()
    return f"""
CONFIGURATION FILE
==================

Default Location:
  {default_path}

You can also specify a custom config path with --config/-c.

Configuration Properties:
-------------------------

server:
  mode: str          Server mode: "stdio" (default) or "http"
  host: str          Host for HTTP mode (default: "localhost")
  port: int          Port for HTTP mode (default: 8000)

repositories:
  urls: list[str]    List of Git repository URLs to clone and parse
  local_base_path: str
                     Directory for cloned repositories (default: "./repositories")
  auto_update: bool  Auto-update repositories on startup (default: true)

logging:
  level: str         Log level: DEBUG, INFO (default), WARNING, ERROR, CRITICAL
  format: str        Python logging format string
  date_format: str   Date format (strftime format)
  use_colors: bool   Enable ANSI colors in console (default: true)
  output: str        Output destination: "stderr" (default), "file", or "both"
  file_path: str     Log file path (required if output is "file" or "both")
  max_bytes: int     Max log file size before rotation (default: 10MB)
  backup_count: int  Number of backup log files to keep (default: 5)

EXAMPLES
========

  # Run with default config (~/.config/javamcp/config.yml)
  python -m javamcp

  # Run with custom config file
  python -m javamcp --config /path/to/config.yml

  # Show version
  python -m javamcp --version

For more information, see: https://github.com/rubensgomes/javamcp
"""


def get_default_config_path() -> Path:
    """
    Get the default configuration file path.

    Returns:
        Path to default config file: ~/.config/javamcp/config.yml
    """
    return Path.home() / ".config" / "javamcp" / "config.yml"


def get_config_template() -> str:
    """
    Read the sample configuration template from package resources.

    Returns:
        Contents of config_template.yml as a string

    Raises:
        RuntimeError: If template file cannot be read
    """
    try:
        template_file = files("javamcp").joinpath("config_template.yml")
        return template_file.read_text(encoding="utf-8")
    except Exception as e:
        raise RuntimeError(f"Failed to read configuration template: {e}") from e


def display_config_error_and_exit() -> None:
    """
    Display error message when configuration file is not found.
    Shows the default config path and sample configuration template.
    Exits with code 1.
    """
    default_path = get_default_config_path()

    try:
        template_content = get_config_template()
        error_message = f"""Error: No configuration file found.

Please create a configuration file at: {default_path}

You can use the following sample configuration as a template:

{template_content}
"""
        print(error_message, file=sys.stderr)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)

    sys.exit(1)


def resolve_config_path(config_arg: str | None) -> str | None:
    """
    Resolve the configuration file path.

    If config_arg is provided, use it.
    If config_arg is None, check for default config at ~/.config/javamcp/config.yml.
    If default config doesn't exist, display error and exit.

    Args:
        config_arg: Config path from command line argument (or None)

    Returns:
        Resolved config path, or None if using defaults

    Side Effects:
        Exits with error message if default config doesn't exist
    """
    if config_arg is not None:
        return config_arg

    default_path = get_default_config_path()

    if default_path.exists():
        return str(default_path)

    # Default config doesn't exist - display error and exit
    display_config_error_and_exit()
    return None  # Never reached, but satisfies type checker


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
        prog="javamcp",
        description=f"""
JavaMCP {__version__} - MCP Server for Java API Documentation

JavaMCP is a Model Context Protocol (MCP) server that provides AI coding
assistants with rich contextual information about Java APIs. It clones
Java repositories, parses source code using ANTLR4, extracts Javadocs
and API information, and exposes this data through MCP tools and resources.

MCP Tools:
  - search_methods    Search for methods by name with optional class filter
  - analyze_class     Get complete class information by fully-qualified name
  - extract_apis      Clone/parse repository and extract APIs
  - generate_guide    Generate usage guide based on use case description

MCP Resources:
  - javamcp://project/{{repository_name}}/context
                      Get comprehensive project context
""",
        epilog=get_help_epilog(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
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
        help="Path to YAML configuration file (default: ~/.config/javamcp/config.yml)",
    )

    args = parser.parse_args()

    try:
        # Resolve configuration path (uses default if not specified)
        config_path = resolve_config_path(args.config)

        # Load configuration
        config = load_config(config_path)

        # Setup logging BEFORE creating FastMCP server instance
        # This ensures FastMCP library uses the same logging configuration
        logger = setup_logging(config.logging)
        log_server_startup(logger, config_path)

        # Register all MCP tools and resources (creates FastMCP instance)
        logger.info("Registering MCP tools and resources...")
        register_tools_and_resources()
        logger.info("MCP tools and resources registered successfully")

        # Setup signal handlers for graceful shutdown
        setup_signal_handlers(logger)

        # Initialize server state
        logger.info("Initializing JavaMCP server...")
        initialize_server(config_path)
        logger.info("Server initialized successfully")
        logger.info("Starting FastMCP server...")

        # Get MCP server instance and start it
        mcp = get_mcp_server()

        # Start FastMCP server - this handles stdio/http modes automatically
        # Note: We don't pass log_level to mcp.run() because logging is already
        # configured via setup_logging() which handles all loggers uniformly
        if config.server.mode == "stdio":
            logger.info("Running FastMCP in stdio mode.")
            mcp.run()
        else:
            logger.info("Running FastMCP in normal HTTP mode.")
            mcp.run(
                transport="http",
                host=config.server.host,
                port=config.server.port,
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
