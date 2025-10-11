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
Data models for Java API entities, repositories, and MCP protocol.
"""

from .java_entities import (JavaAnnotation, JavaClass, JavaDoc, JavaField,
                            JavaMethod, JavaPackage, JavaParameter)
from .mcp_protocol import (AnalyzeClassRequest, AnalyzeClassResponse,
                           ErrorResponse, ExtractApisRequest,
                           ExtractApisResponse, GenerateGuideRequest,
                           GenerateGuideResponse, SearchMethodsRequest,
                           SearchMethodsResponse)
from .repository import RepositoryIndex, RepositoryMetadata

__all__ = [
    # Java entities
    "JavaAnnotation",
    "JavaClass",
    "JavaDoc",
    "JavaField",
    "JavaMethod",
    "JavaPackage",
    "JavaParameter",
    # Repository models
    "RepositoryMetadata",
    "RepositoryIndex",
    # MCP protocol models
    "SearchMethodsRequest",
    "SearchMethodsResponse",
    "AnalyzeClassRequest",
    "AnalyzeClassResponse",
    "ExtractApisRequest",
    "ExtractApisResponse",
    "GenerateGuideRequest",
    "GenerateGuideResponse",
    "ErrorResponse",
]
