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
Configuration management for the Java MCP server.
"""

from .loader import load_config
from .schema import (ApplicationConfig, LoggingConfig, RepositoryConfig,
                     ServerConfig, ServerMode)

__all__ = [
    "ServerMode",
    "ServerConfig",
    "RepositoryConfig",
    "LoggingConfig",
    "ApplicationConfig",
    "load_config",
]
