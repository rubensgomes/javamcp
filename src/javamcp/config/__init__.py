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
Configuration management for the JavaMCP server.

This module provides a comprehensive configuration system supporting YAML and JSON
formats with Pydantic-based validation. It handles all aspects of server, repository,
and logging configuration with sensible defaults and extensive validation.

Module Responsibilities
-----------------------
- Load and parse configuration files (YAML/JSON formats)
- Validate configuration data using Pydantic schemas
- Provide type-safe configuration models with defaults
- Export public configuration API for use throughout the application

Main Functionalities
--------------------
1. Configuration Loading:
   - Load from YAML or JSON configuration files
   - Support for default configuration when no file is provided
   - Automatic format detection based on file extension
   - Comprehensive error handling and validation

2. Configuration Schema:
   - ServerConfig: MCP server settings (mode, host, port)
   - RepositoryConfig: Git repository settings (URLs, paths, auto-update)
   - LoggingConfig: Logging settings (level, format, colors, output)
   - ApplicationConfig: Root configuration aggregating all sub-configs

3. Validation:
   - Type validation via Pydantic
   - Range validation (ports, file sizes)
   - Required field enforcement
   - Custom validation rules (file paths, URLs)

Usage Examples
--------------
Basic usage - loading a configuration file:

    >>> from javamcp.config import load_config
    >>> config = load_config("config.yml")
    >>> print(config.server.mode)
    ServerMode.STDIO
    >>> print(config.logging.level)
    INFO

Using default configuration:

    >>> from javamcp.config import load_config
    >>> config = load_config()  # No file path provided
    >>> print(config.server.port)
    8000

Accessing specific configuration sections:

    >>> from javamcp.config import load_config
    >>> config = load_config("config.yml")
    >>> print(config.repositories.local_base_path)
    ./repositories
    >>> print(config.repositories.urls)
    ['https://github.com/apache/commons-lang.git']

Creating configuration programmatically:

    >>> from javamcp.config import ApplicationConfig, ServerConfig, ServerMode
    >>> from javamcp.config import RepositoryConfig, LoggingConfig
    >>>
    >>> config = ApplicationConfig(
    ...     server=ServerConfig(mode=ServerMode.HTTP, port=9000),
    ...     repositories=RepositoryConfig(
    ...         urls=["https://github.com/user/repo.git"],
    ...         local_base_path="/tmp/repos"
    ...     ),
    ...     logging=LoggingConfig(level="DEBUG", use_colors=True)
    ... )

Error handling:

    >>> from javamcp.config import load_config
    >>> from javamcp.config.loader import ConfigurationError
    >>>
    >>> try:
    ...     config = load_config("missing.yml")
    ... except ConfigurationError as e:
    ...     print(f"Configuration error: {e}")

Configuration File Format
-------------------------
Example YAML configuration:

    server:
        mode: stdio  # or "http"
        host: localhost
        port: 8000

    repositories:
        urls:
            - https://github.com/apache/commons-lang.git
        local_base_path: ./repositories
        auto_update: true

    logging:
        level: INFO
        format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        date_format: "%Y-%m-%d %H:%M:%S"
        use_colors: true
        output: stderr  # "stderr", "file", or "both"
        file_path: null  # Required if output is "file" or "both"

Exported Classes and Functions
-------------------------------
- load_config: Function to load configuration from file or defaults
- ApplicationConfig: Root configuration model
- ServerConfig: Server-specific configuration
- RepositoryConfig: Repository management configuration
- LoggingConfig: Logging system configuration
- ServerMode: Enum for server operation modes (STDIO/HTTP)

See Also
--------
- config.loader: Configuration file loading implementation
- config.schema: Pydantic configuration models and validation
"""

from .loader import load_config
from .schema import (
    ApplicationConfig,
    LoggingConfig,
    RepositoryConfig,
    ServerConfig,
    ServerMode,
)

__all__ = [
    "ServerMode",
    "ServerConfig",
    "RepositoryConfig",
    "LoggingConfig",
    "ApplicationConfig",
    "load_config",
]
