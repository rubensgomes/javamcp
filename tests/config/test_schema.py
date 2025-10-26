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
Unit tests for configuration schema models.
"""

import pytest
from pydantic import ValidationError

from javamcp.config.schema import (ApplicationConfig, LoggingConfig,
                                   RepositoryConfig, ServerConfig, ServerMode)


class TestServerMode:
    """Tests for ServerMode enum."""

    def test_server_mode_values(self):
        """Test ServerMode enum values."""
        assert ServerMode.STDIO == "stdio"
        assert ServerMode.HTTP == "http"


class TestServerConfig:
    """Tests for ServerConfig model."""

    def test_create_default_server_config(self):
        """Test creating server config with defaults."""
        config = ServerConfig()
        assert config.mode == ServerMode.STDIO
        assert config.port == 8000
        assert config.host == "localhost"

    def test_create_http_server_config(self):
        """Test creating HTTP server config."""
        config = ServerConfig(mode=ServerMode.HTTP, port=9000, host="0.0.0.0")
        assert config.mode == ServerMode.HTTP
        assert config.port == 9000
        assert config.host == "0.0.0.0"

    def test_invalid_port_too_low(self):
        """Test validation fails for port < 1."""
        with pytest.raises(ValidationError):
            ServerConfig(port=0)

    def test_invalid_port_too_high(self):
        """Test validation fails for port > 65535."""
        with pytest.raises(ValidationError):
            ServerConfig(port=70000)


class TestRepositoryConfig:
    """Tests for RepositoryConfig model."""

    def test_create_repository_config(self):
        """Test creating repository config."""
        config = RepositoryConfig(
            urls=["https://github.com/example/repo1.git"],
            local_base_path="/tmp/repos",
        )
        assert len(config.urls) == 1
        assert config.local_base_path == "/tmp/repos"
        assert config.auto_update

    def test_repository_config_no_urls_fails(self):
        """Test validation fails when no URLs provided."""
        with pytest.raises(ValidationError):
            RepositoryConfig(urls=[])

    def test_repository_config_empty_url_fails(self):
        """Test validation fails for empty URL."""
        with pytest.raises(ValidationError):
            RepositoryConfig(urls=[""])

    def test_repository_config_empty_path_fails(self):
        """Test validation fails for empty path."""
        with pytest.raises(ValidationError):
            RepositoryConfig(
                urls=["https://github.com/example/repo.git"], local_base_path=""
            )


class TestLoggingConfig:
    """Tests for LoggingConfig model."""

    def test_create_default_logging_config(self):
        """Test creating logging config with defaults."""
        config = LoggingConfig()
        assert config.level == "INFO"
        assert config.format == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        assert config.date_format == "%Y-%m-%d %H:%M:%S"
        assert config.use_colors is True
        assert config.output == "console"
        assert config.file_path is None

    def test_create_file_logging_config(self):
        """Test creating file logging config."""
        config = LoggingConfig(
            level="DEBUG", output="file", file_path="/var/log/app.log"
        )
        assert config.level == "DEBUG"
        assert config.output == "file"
        assert config.file_path == "/var/log/app.log"

    def test_logging_level_case_insensitive(self):
        """Test log level is converted to uppercase."""
        config = LoggingConfig(level="debug")
        assert config.level == "DEBUG"

    def test_invalid_log_level_fails(self):
        """Test validation fails for invalid log level."""
        with pytest.raises(ValidationError):
            LoggingConfig(level="INVALID")

    def test_invalid_log_output_fails(self):
        """Test validation fails for invalid output destination."""
        with pytest.raises(ValidationError):
            LoggingConfig(output="invalid")

    def test_custom_format_and_date_format(self):
        """Test custom log format and date format."""
        config = LoggingConfig(
            format="[%(levelname)s] %(name)s: %(message)s",
            date_format="%Y/%m/%d %H:%M",
        )
        assert config.format == "[%(levelname)s] %(name)s: %(message)s"
        assert config.date_format == "%Y/%m/%d %H:%M"

    def test_colors_can_be_disabled(self):
        """Test colors can be disabled via config."""
        config = LoggingConfig(use_colors=False)
        assert config.use_colors is False


class TestApplicationConfig:
    """Tests for ApplicationConfig model."""

    def test_create_default_application_config(self):
        """Test creating application config with defaults."""
        config = ApplicationConfig()
        assert config.server.mode == ServerMode.STDIO
        assert config.logging.level == "INFO"

    def test_create_complete_application_config(self):
        """Test creating complete application config."""
        config = ApplicationConfig(
            server=ServerConfig(mode=ServerMode.HTTP, port=9000),
            repositories=RepositoryConfig(
                urls=["https://github.com/example/repo.git"],
                local_base_path="/tmp/repos",
            ),
            logging=LoggingConfig(level="DEBUG", output="console"),
        )
        assert config.server.port == 9000
        assert len(config.repositories.urls) == 1
        assert config.logging.level == "DEBUG"

    def test_validate_logging_file_path_file_output(self):
        """Test validation fails when file output without file_path."""
        config = ApplicationConfig(logging=LoggingConfig(output="file"))
        with pytest.raises(ValueError, match="file_path must be specified"):
            config.validate_logging_file_path()

    def test_validate_logging_file_path_both_output(self):
        """Test validation fails when both output without file_path."""
        config = ApplicationConfig(logging=LoggingConfig(output="both"))
        with pytest.raises(ValueError, match="file_path must be specified"):
            config.validate_logging_file_path()

    def test_validate_logging_file_path_console_output(self):
        """Test validation passes when console output without file_path."""
        config = ApplicationConfig(logging=LoggingConfig(output="console"))
        # Should not raise
        config.validate_logging_file_path()
