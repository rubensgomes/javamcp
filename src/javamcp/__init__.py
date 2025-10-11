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
JavaMCP - MCP server for exposing Java APIs with Javadoc context.

A Python-based MCP (Model Context Protocol) server that provides AI coding
assistants with rich contextual information about Java APIs, including
Javadocs, method signatures, class hierarchies, and usage examples.
"""

__version__ = "0.2.2"
__author__ = "JavaMCP Contributors"

from javamcp.server import get_state, initialize_server, mcp

__all__ = [
    "mcp",
    "initialize_server",
    "get_state",
    "__version__",
]
