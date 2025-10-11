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
MCP tool for searching Java methods by name.

NOTE: This tool is now implemented as a FastMCP decorated function in server.py.
This module is kept for backwards compatibility and testing purposes.
"""

from javamcp.context.context_builder import ContextBuilder
from javamcp.indexer.query_engine import QueryEngine
from javamcp.models.mcp_protocol import (SearchMethodsRequest,
                                         SearchMethodsResponse)


def search_methods_tool(
    request: SearchMethodsRequest, query_engine: QueryEngine
) -> SearchMethodsResponse:
    """
    Search for Java methods by name with optional class filter.

    Provides rich context including method signatures, javadocs, parameters,
    and containing class information.

    NOTE: For production use, the FastMCP tool in server.py should be used.
    This function is maintained for testing and backwards compatibility.

    Args:
        request: SearchMethodsRequest with method name and optional filters
        query_engine: QueryEngine instance for searching

    Returns:
        SearchMethodsResponse with matching methods and full context
    """
    context_builder = ContextBuilder()

    # Search for methods
    results = query_engine.search_methods(
        request.method_name,
        class_name=request.class_name,
        case_sensitive=request.case_sensitive,
    )

    # Build rich context for each method
    methods_with_context = []
    for java_class, method in results:
        # Add context to method
        context_builder.build_method_context(method, java_class)
        methods_with_context.append(method)

    return SearchMethodsResponse(
        methods=methods_with_context,
        total_found=len(methods_with_context),
        query=request,
    )
