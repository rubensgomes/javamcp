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
MCP tool for generating API usage guides.

NOTE: This tool is now implemented as a FastMCP decorated function in server.py.
This module is kept for backwards compatibility and testing purposes.
"""

from javamcp.context.context_builder import ContextBuilder
from javamcp.indexer.query_engine import QueryEngine
from javamcp.models.mcp_protocol import (GenerateGuideRequest,
                                         GenerateGuideResponse)


def generate_guide_tool(
    request: GenerateGuideRequest, query_engine: QueryEngine
) -> GenerateGuideResponse:
    """
    Generate an API usage guide based on a use case description.

    Searches for relevant APIs and creates a structured guide with
    javadoc-based examples, method descriptions, and usage patterns.

    NOTE: For production use, the FastMCP tool in server.py should be used.
    This function is maintained for testing and backwards compatibility.

    Args:
        request: GenerateGuideRequest with use case and optional filters
        query_engine: QueryEngine instance for searching APIs

    Returns:
        GenerateGuideResponse with formatted usage guide and relevant APIs
    """
    context_builder = ContextBuilder()

    # Simple keyword-based search in use case
    keywords = _extract_keywords(request.use_case)

    relevant_classes = []
    relevant_methods = []

    # Search for relevant classes and methods based on keywords
    for keyword in keywords[: request.max_results]:
        # Search methods by partial name
        methods = query_engine.search_methods_partial(keyword, case_sensitive=False)
        relevant_methods.extend([m for c, m in methods[: request.max_results]])

        # Search classes by name
        classes = query_engine.get_classes_by_name(keyword, case_sensitive=False)
        relevant_classes.extend(classes[: request.max_results])

    # Limit results
    relevant_classes = relevant_classes[: request.max_results]
    relevant_methods = relevant_methods[: request.max_results]

    # Build formatted guide
    guide_lines = []
    guide_lines.append(f"# API Usage Guide: {request.use_case}")
    guide_lines.append("")

    if relevant_classes:
        guide_lines.append("## Relevant Classes")
        guide_lines.append("")
        for java_class in relevant_classes[:5]:
            summary = context_builder.build_api_summary(java_class)
            guide_lines.append(summary)
            guide_lines.append("")

    if relevant_methods:
        guide_lines.append("## Relevant Methods")
        guide_lines.append("")
        # Group methods by class (simplified)
        guide_lines.append("Found relevant methods for the use case.")
        guide_lines.append("")

    guide = "\n".join(guide_lines)

    return GenerateGuideResponse(
        guide=guide,
        relevant_classes=relevant_classes,
        relevant_methods=relevant_methods,
        use_case=request.use_case,
    )


def _extract_keywords(use_case: str) -> list[str]:
    """Extract keywords from use case description."""
    # Simple implementation: split and filter common words
    words = use_case.lower().split()
    common_words = {
        "how",
        "to",
        "the",
        "a",
        "an",
        "is",
        "are",
        "for",
        "in",
        "on",
        "with",
    }
    keywords = [w for w in words if w not in common_words and len(w) > 2]
    return keywords
