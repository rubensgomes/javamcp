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
Configuration file loader supporting YAML and JSON formats.
"""

import json
import logging
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from .schema import ApplicationConfig

# Module-level logger - use standard logging since this runs before logging setup
logger = logging.getLogger("javamcp.config")

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class ConfigurationError(Exception):
    """Raised when configuration loading or validation fails."""


def load_config(config_path: Optional[str] = None) -> ApplicationConfig:
    """
    Load application configuration from file or return default configuration.

    Args:
        config_path: Path to configuration file (YAML or JSON).
                    If None, returns default configuration.

    Returns:
        ApplicationConfig instance

    Raises:
        ConfigurationError: If configuration file cannot be loaded or is invalid
    """
    if config_path is None:
        logger.debug("No config path provided, using default configuration")
        return ApplicationConfig()

    logger.info("Loading configuration from: %s", config_path)
    path = Path(config_path)

    if not path.exists():
        logger.error("Configuration file not found: %s", config_path)
        raise ConfigurationError(f"Configuration file not found: {config_path}")

    if not path.is_file():
        raise ConfigurationError(f"Configuration path is not a file: {config_path}")

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        raise ConfigurationError(
            f"Failed to read configuration file {config_path}: {e}"
        ) from e

    suffix = path.suffix.lower()
    logger.debug("Detected configuration format: %s", suffix)

    if suffix in (".yaml", ".yml"):
        config = _load_yaml_config(content, config_path)
        logger.info("Configuration loaded successfully from %s", config_path)
        return config
    if suffix == ".json":
        config = _load_json_config(content, config_path)
        logger.info("Configuration loaded successfully from %s", config_path)
        return config

    logger.error("Unsupported configuration format: %s", suffix)
    raise ConfigurationError(
        f"Unsupported configuration file format: {suffix}. "
        "Supported formats: .yaml, .yml, .json"
    )


def _load_yaml_config(content: str, config_path: str) -> ApplicationConfig:
    """Load configuration from YAML content."""
    if not YAML_AVAILABLE:
        logger.error("YAML support not available")
        raise ConfigurationError(
            "YAML support not available. Install PyYAML: pip install pyyaml"
        )

    try:
        logger.debug("Parsing YAML configuration")
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        logger.error("Failed to parse YAML configuration: %s", e)
        raise ConfigurationError(
            f"Failed to parse YAML configuration {config_path}: {e}"
        ) from e

    if data is None:
        data = {}

    return _validate_config(data, config_path)


def _load_json_config(content: str, config_path: str) -> ApplicationConfig:
    """Load configuration from JSON content."""
    try:
        logger.debug("Parsing JSON configuration")
        data = json.loads(content)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse JSON configuration: %s", e)
        raise ConfigurationError(
            f"Failed to parse JSON configuration {config_path}: {e}"
        ) from e

    return _validate_config(data, config_path)


def _validate_config(data: dict, config_path: str) -> ApplicationConfig:
    """Validate configuration data using Pydantic."""
    logger.debug("Validating configuration")
    try:
        config = ApplicationConfig(**data)
        # Additional validation
        config.validate_logging_file_path()
        logger.debug(
            "Configuration validated: %d repositories, logging level=%s",
            len(config.repositories.urls),
            config.logging.level,
        )
        return config
    except ValidationError as e:
        logger.error("Configuration validation failed: %s", e)
        raise ConfigurationError(
            f"Configuration validation failed for {config_path}: {e}"
        ) from e
    except ValueError as e:
        logger.error("Configuration validation failed: %s", e)
        raise ConfigurationError(
            f"Configuration validation failed for {config_path}: {e}"
        ) from e
