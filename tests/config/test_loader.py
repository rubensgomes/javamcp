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
Unit tests for configuration loader.
"""

import json
import tempfile
from pathlib import Path

import pytest

from javamcp.config.loader import ConfigurationError, load_config
from javamcp.config.schema import ApplicationConfig, ServerMode


class TestLoadConfig:
    """Tests for configuration loading."""

    def test_load_config_no_path_returns_default(self):
        """Test that load_config with no path returns default config."""
        config = load_config()
        assert isinstance(config, ApplicationConfig)
        assert config.server.mode == ServerMode.STDIO

    def test_load_config_nonexistent_file_fails(self):
        """Test that loading nonexistent file raises error."""
        with pytest.raises(ConfigurationError, match="Configuration file not found"):
            load_config("/nonexistent/config.yaml")

    def test_load_config_directory_fails(self):
        """Test that loading directory raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ConfigurationError, match="not a file"):
                load_config(tmpdir)

    def test_load_config_unsupported_format_fails(self):
        """Test that unsupported file format raises error."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"some content")
            tmp_path = tmp.name

        try:
            with pytest.raises(
                ConfigurationError, match="Unsupported configuration file format"
            ):
                load_config(tmp_path)
        finally:
            Path(tmp_path).unlink()


class TestLoadJsonConfig:
    """Tests for JSON configuration loading."""

    def test_load_valid_json_config(self):
        """Test loading valid JSON configuration."""
        config_data = {
            "server": {"mode": "http", "port": 9000},
            "repositories": {
                "urls": ["https://github.com/example/repo.git"],
                "local_base_path": "/tmp/repos",
            },
            "logging": {"level": "DEBUG", "output": "console"},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            json.dump(config_data, tmp)
            tmp_path = tmp.name

        try:
            config = load_config(tmp_path)
            assert config.server.mode == ServerMode.HTTP
            assert config.server.port == 9000
            assert len(config.repositories.urls) == 1
            assert config.logging.level == "DEBUG"
        finally:
            Path(tmp_path).unlink()

    def test_load_invalid_json_fails(self):
        """Test loading invalid JSON raises error."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            tmp.write("{ invalid json }")
            tmp_path = tmp.name

        try:
            with pytest.raises(ConfigurationError, match="Failed to parse JSON"):
                load_config(tmp_path)
        finally:
            Path(tmp_path).unlink()

    def test_load_json_validation_fails(self):
        """Test loading JSON with invalid values fails validation."""
        config_data = {
            "server": {"port": 99999},  # Invalid port
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            json.dump(config_data, tmp)
            tmp_path = tmp.name

        try:
            with pytest.raises(
                ConfigurationError, match="Configuration validation failed"
            ):
                load_config(tmp_path)
        finally:
            Path(tmp_path).unlink()


class TestLoadYamlConfig:
    """Tests for YAML configuration loading."""

    def test_load_valid_yaml_config(self):
        """Test loading valid YAML configuration."""
        yaml_content = """
server:
  mode: http
  port: 8080
repositories:
  urls:
    - https://github.com/example/repo.git
  local_base_path: /tmp/repos
logging:
  level: INFO
  output: console
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write(yaml_content)
            tmp_path = tmp.name

        try:
            config = load_config(tmp_path)
            assert config.server.mode == ServerMode.HTTP
            assert config.server.port == 8080
            assert len(config.repositories.urls) == 1
        finally:
            Path(tmp_path).unlink()

    def test_load_yml_extension(self):
        """Test loading YAML file with .yml extension."""
        yaml_content = """
server:
  mode: stdio
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as tmp:
            tmp.write(yaml_content)
            tmp_path = tmp.name

        try:
            config = load_config(tmp_path)
            assert config.server.mode == ServerMode.STDIO
        finally:
            Path(tmp_path).unlink()

    def test_load_invalid_yaml_fails(self):
        """Test loading invalid YAML raises error."""
        invalid_yaml = """
server:
  mode: http
  invalid indentation
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write(invalid_yaml)
            tmp_path = tmp.name

        try:
            with pytest.raises(ConfigurationError, match="Failed to parse YAML"):
                load_config(tmp_path)
        finally:
            Path(tmp_path).unlink()

    def test_load_empty_yaml_returns_defaults(self):
        """Test loading empty YAML file returns default config."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write("")
            tmp_path = tmp.name

        try:
            config = load_config(tmp_path)
            assert isinstance(config, ApplicationConfig)
        finally:
            Path(tmp_path).unlink()
