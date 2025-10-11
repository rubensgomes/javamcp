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
MCP tool for analyzing a specific Java class.

NOTE: This tool is now implemented as a FastMCP decorated function in server.py.
This module is kept for backwards compatibility and testing purposes.
"""

from javamcp.context.context_builder import ContextBuilder
from javamcp.indexer.query_engine import QueryEngine
from javamcp.models.mcp_protocol import (AnalyzeClassRequest,
                                         AnalyzeClassResponse)


def analyze_class_tool(
    request: AnalyzeClassRequest, query_engine: QueryEngine
) -> AnalyzeClassResponse:
    """
    Analyze a specific Java class by fully-qualified name.

    Provides complete class information including methods, fields, javadocs,
    inheritance hierarchy, and annotations.

    NOTE: For production use, the FastMCP tool in server.py should be used.
    This function is maintained for testing and backwards compatibility.

    Args:
        request: AnalyzeClassRequest with class name and optional repository filter
        query_engine: QueryEngine instance for searching

    Returns:
        AnalyzeClassResponse with complete class analysis and context
    """
    context_builder = ContextBuilder()

    # Search for the class
    java_class = query_engine.search_class(request.fully_qualified_name)

    if not java_class:
        return AnalyzeClassResponse(found=False, matches=0)

    # If repository filter specified, verify class is from that repository
    if request.repository_name:
        repo_classes = query_engine.filter_classes_by_repository(
            request.repository_name
        )
        if java_class not in repo_classes:
            return AnalyzeClassResponse(found=False, matches=0)

    # Build rich context
    context_builder.build_class_context(java_class, include_methods=True)

    return AnalyzeClassResponse(
        java_class=java_class,
        found=True,
        matches=1,
    )
