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
Pydantic models for MCP (Model Context Protocol) request and response payloads.
"""

from typing import Optional

from pydantic import BaseModel, Field

from .java_entities import JavaClass, JavaMethod


class SearchMethodsRequest(BaseModel):
    """
    Request to search for Java methods by name.

    Attributes:
        method_name: Method name to search for (required)
        class_name: Optional filter by class name
        case_sensitive: Whether search is case-sensitive (default: False)
    """

    method_name: str = Field(..., description="Method name to search for")
    class_name: Optional[str] = Field(None, description="Filter by class name")
    case_sensitive: bool = Field(False, description="Case-sensitive search")


class SearchMethodsResponse(BaseModel):
    """
    Response containing matching Java methods with context.

    Attributes:
        methods: List of matching methods with full context
        total_found: Total number of methods found
        query: Original search query for reference
    """

    methods: list[JavaMethod] = Field(
        default_factory=list, description="Matching methods with context"
    )
    total_found: int = Field(0, description="Total methods found")
    query: SearchMethodsRequest = Field(..., description="Original query")


class AnalyzeClassRequest(BaseModel):
    """
    Request to analyze a specific Java class.

    Attributes:
        fully_qualified_name: Fully-qualified class name (e.g., "java.util.ArrayList")
        repository_name: Optional filter by repository name/URL
    """

    fully_qualified_name: str = Field(..., description="Fully-qualified class name")
    repository_name: Optional[str] = Field(
        None, description="Filter by repository name"
    )


class AnalyzeClassResponse(BaseModel):
    """
    Response containing complete class analysis with rich context.

    Attributes:
        java_class: Complete class information with methods, fields, javadocs
        found: Whether the class was found
        matches: Number of matching classes (may be > 1 if in multiple repositories)
    """

    java_class: Optional[JavaClass] = Field(
        None, description="Complete class information"
    )
    found: bool = Field(False, description="Whether class was found")
    matches: int = Field(0, description="Number of matching classes")


class ExtractApisRequest(BaseModel):
    """
    Request to extract APIs from a Git repository.

    Attributes:
        repository_url: Git repository URL (required)
        branch: Branch name (default: "main")
        package_filter: Optional package name filter
        class_filter: Optional class name filter
    """

    repository_url: str = Field(..., description="Git repository URL")
    branch: str = Field(default="main", description="Branch name")
    package_filter: Optional[str] = Field(None, description="Filter by package")
    class_filter: Optional[str] = Field(None, description="Filter by class name")


class ExtractApisResponse(BaseModel):
    """
    Response containing extracted API information with summaries.

    Attributes:
        classes: Extracted Java classes with full context
        total_classes: Total number of classes extracted
        total_methods: Total number of methods extracted
        repository_url: Repository URL for reference
        branch: Branch name for reference
    """

    classes: list[JavaClass] = Field(
        default_factory=list, description="Extracted classes with context"
    )
    total_classes: int = Field(0, description="Total classes extracted")
    total_methods: int = Field(0, description="Total methods extracted")
    repository_url: str = Field(..., description="Repository URL")
    branch: str = Field(..., description="Branch name")


class GenerateGuideRequest(BaseModel):
    """
    Request to generate API usage guide.

    Attributes:
        use_case: Description of use case or functionality (required)
        repository_filter: Optional filter to focus on specific repository
        max_results: Maximum number of relevant APIs to include (default: 10)
    """

    use_case: str = Field(..., description="Use case or functionality description")
    repository_filter: Optional[str] = Field(None, description="Filter by repository")
    max_results: int = Field(default=10, description="Maximum APIs to include in guide")


class GenerateGuideResponse(BaseModel):
    """
    Response containing generated usage guide with contextual API information.

    Attributes:
        guide: Formatted usage guide with examples and javadocs
        relevant_classes: List of relevant classes referenced in guide
        relevant_methods: List of relevant methods referenced in guide
        use_case: Original use case for reference
    """

    guide: str = Field(..., description="Generated usage guide")
    relevant_classes: list[JavaClass] = Field(
        default_factory=list, description="Relevant classes"
    )
    relevant_methods: list[JavaMethod] = Field(
        default_factory=list, description="Relevant methods"
    )
    use_case: str = Field(..., description="Original use case")


class ErrorResponse(BaseModel):
    """
    Error response for MCP protocol.

    Attributes:
        error: Error message
        error_code: Error code (e.g., "NOT_FOUND", "INVALID_REQUEST", "INTERNAL_ERROR")
        details: Additional error details
    """

    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    details: Optional[str] = Field(None, description="Additional error details")
