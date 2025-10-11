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

"""Logging module for JavaMCP server."""

from .logger import (ContextLogger, get_logger, log_parse_operation,
                     log_repository_operation, log_server_shutdown,
                     log_server_startup, log_tool_invocation, setup_logging)

__all__ = [
    "setup_logging",
    "get_logger",
    "ContextLogger",
    "log_server_startup",
    "log_server_shutdown",
    "log_tool_invocation",
    "log_repository_operation",
    "log_parse_operation",
]
